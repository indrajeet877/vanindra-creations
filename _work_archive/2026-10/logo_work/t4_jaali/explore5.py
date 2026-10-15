"""Round 5: the V woven into a jaali {8/3} strapwork star; crossed-strap V; mitred V variants."""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER
from explore4 import point_v, rosette, star83

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')


def band_between(p, q, w, ext=0.0):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    p = (p[0] - ux * ext, p[1] - uy * ext)
    q = (q[0] + ux * ext, q[1] + uy * ext)
    h = w / 2
    return [(p[0] + nx * h, p[1] + ny * h), (q[0] + nx * h, q[1] + ny * h), (q[0] - nx * h, q[1] - ny * h), (p[0] - nx * h, p[1] - ny * h)]


def star_lines(R=100.0):
    verts = {a: polar(0, 0, R, a) for a in range(0, 360, 45)}
    lines = []
    for a in range(0, 360, 45):
        b = (a + 135) % 360
        key = tuple(sorted((a, b)))
        if key not in [tuple(sorted(l)) for l in lines]:
            lines.append((a, b))
    return verts, lines


def mitred_band(p_from, p_to, w, R):
    """band of width w whose ends are cut along the radial lines through the end vertices (star miters)."""
    pts = band_between(p_from, p_to, w, ext=w * 3)
    poly = P(pts)
    return poly


def woven_star(R=100.0, wv=14.0, wo=6.0, gap=2.4, v_only=False):
    verts, lines = star_lines(R)
    # the {8/3} star outline region -- bands are clipped to it so that the points are sharp
    outline = P(star83(0, 0, R + 0.0))
    outer_clip = P(offset(star83(0, 0, R), -0.0))
    shapes = []
    vlines = [l for l in lines if 270 in l]
    others = [l for l in lines if 270 not in l]
    # bands extended past vertices, then clipped by the star (outer contour) offset outward so points stay crisp
    big = P(offset(star83(0, 0, R), -max(wv, wo) * 1.31))
    def b(l, w):
        return inter(P(band_between(verts[l[0]], verts[l[1]], w, ext=w * 2)), outline_for(w))
    def outline_for(w):
        # star whose edges are offset outwards by w/2 so a band of width w running along a star edge fills to a sharp point
        return P(offset(star83(0, 0, R), -w / 2 / 1.0))
    V = union(*[b(l, wv) for l in vlines])
    if v_only:
        return V
    O = [b(l, wo) for l in others]
    # V passes over everything; others are cut where they pass under the V
    Vgap = vt.stroke_to_path(V, gap * 2)
    O = [diff(o, Vgap) for o in O]
    return union(V, *O)


def crossed(H=100.0, w=16.0, tail=18.0, gap=3.0):
    th = 22.5
    s, c = math.sin(th * D2R), math.cos(th * D2R)
    # two straps crossing below the vertex; ends mitred like star points
    apex = (0.0, H)
    def strap(side):
        top = (side * (H + tail) * math.tan(th * D2R) * 1.0, 0.0)
        bot = (-side * tail * math.tan(th * D2R), H + tail)
        return P(band_between(top, bot, w))
    L, Rr = strap(-1), strap(1)
    clip = P([(-300, 0), (300, 0), (300, H + tail * 0.9), (-300, H + tail * 0.9)])
    L, Rr = inter(L, clip), inter(Rr, clip)
    cut = vt.stroke_to_path(L, gap * 2)
    return union(L, diff(Rr, cut))


VARS = [('woven star', lambda: woven_star()), ('woven star bold V', lambda: woven_star(wv=18, wo=5)),
        ('woven V only (small)', lambda: woven_star(wv=18, v_only=True)), ('crossed straps', crossed),
        ('mitred V t=10', lambda: point_v(10.0)), ('rosette', lambda: rosette(10.0))]

if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m = fn()
        m, _ = fit(m, 250, 250, 200, 200)
        f = os.path.join(OUT, f'u{i+1}.svg')
        open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name))
        files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r4.png')] + files, check=True)
    print('ok')
