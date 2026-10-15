"""Round 6: star-hearted V, large-scale jaali cut, leaf-lens jaali, nested points."""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
from explore2 import Arm, BIG, TH, S, C
from explore4 import point_v, rosette, star83, K

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
TN = math.tan(TH * D2R)


def star_heart(H=100.0, t=30.0, R=None, shell=None):
    """V whose counter flows down into an {8/3} star; star's lower point concentric with the V tip."""
    V = P(v_pts(H, TH, t))
    dv = t / S
    shell = shell or t * 0.55
    tip_y = H - shell / S              # star bottom tip, leaving constant shell under it
    R = R or 24.0
    cy = tip_y - R
    star = P(star83(0, cy, R))
    # counter: original counter (apex H-dv) ; star top point merges with it
    return inter(diff(V, star), BIG)


def khatim_cut(H=100.0, t=34.0, a=24.0, w=3.0):
    V = P(v_pts(H, TH, t))
    holes = []
    for i in range(-6, 7):
        for j in range(-2, 7):
            holes.append(P(offset(star_pts(i * a, H - 14 - j * a, a * 0.62, 8, 2, a0=90), w / 2)))
    return inter(diff(V, union(*holes)), BIG)


def arc_pts(cx, cy, r, a0, a1, n=48):
    return [polar(cx, cy, r, a0 + (a1 - a0) * k / n) for k in range(n + 1)]


def lens_local(L, Wd, n=40):
    """vesica along x from -L/2..L/2 with max half-width Wd/2 (two circular arcs)."""
    h = Wd / 2
    c = L / 2
    r = (c * c + h * h) / (2 * h)
    yc = r - h
    a = math.degrees(math.atan2(c, yc))
    top = [(r * math.sin(math.radians(-a + 2 * a * k / n)), -(r * math.cos(math.radians(-a + 2 * a * k / n)) - yc)) for k in range(n + 1)]
    bot = [(x, -y) for (x, y) in reversed(top)]
    return top[:-1] + bot[:-1]


def leaf_jaali(H=100.0, t=24.0, w=2.8):
    V = P(v_pts(H, TH, t))
    holes = []
    for side in (-1, 1):
        arm = Arm(H, t, side)
        L = 26.0
        a = t * 0.9
        while a < arm.L + 10:
            pts = lens_local(L - w, t - 2 * w - 4)
            holes.append(arm.poly([(a + x, y) for (x, y) in pts]))
            a += L
    A0 = Arm(H, t, 1)
    return inter(diff(V, union(*holes)), BIG)


def nested_points(R=100.0, t=8.0, g=3.0):
    outer = point_v(t, R)
    s2 = star83(0, 0, R)
    inner_ring = diff(P(offset(s2, t + g)), P(offset(s2, 2 * t + g)))
    wedge = P([(0, 0), polar(0, 0, 900, 247.5), polar(0, 0, 900, 292.5)])
    return union(outer, inter(inner_ring, wedge))


def jaali_rosette(R=100.0, t=9.0, g=2.6):
    """two concentric star bands, split into Vs by radial slits -- a true jaali rosette made of Vs"""
    s = star83(0, 0, R)
    ring1 = diff(P(s), P(offset(s, t)))
    ring2 = diff(P(offset(s, t + g)), P(offset(s, 2 * t + g)))
    rings = union(ring1, ring2)
    slits = union(*[vt.stroke_to_path(P([(0, 0), polar(0, 0, 300, 247.5 + 45 * k)]), g) for k in range(8)])
    core = P(star_pts(0, 0, R * 0.22, 8, 3, a0=90))
    return diff(rings, slits)


VARS = [('star heart t30 R24', lambda: star_heart()), ('star heart t34 R28', lambda: star_heart(t=34, R=28)),
        ('khatim cut large', khatim_cut), ('leaf-lens jaali', leaf_jaali), ('nested points', nested_points),
        ('jaali rosette of Vs', jaali_rosette)]

if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m = fn()
        m, _ = fit(m, 250, 250, 200, 200)
        f = os.path.join(OUT, f'v{i+1}.svg')
        open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name))
        files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r5.png')] + files, check=True)
    print('ok')
