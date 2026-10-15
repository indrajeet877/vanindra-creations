"""Round 8: true lace -- the stone is ONLY constant-width webs around seed openings (all leftovers open too)."""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
from explore4 import star83, rosette

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
TH = 22.5
S, C = math.sin(TH * D2R), math.cos(TH * D2R)


def contours(path):
    """split a pathops path into separate closed contours (as Paths)."""
    out = []
    for c in path.contours:
        q = pathops.Path()
        c.draw(q.getPen())
        out.append(q)
    return out


def area(path):
    try:
        return abs(path.area)
    except Exception:
        x0, y0, x1, y1 = vt.bounds(path)
        return (x1 - x0) * (y1 - y0)


def lace(region, seeds, w, min_area=0.0):
    """region: solid outline. seeds: list of opening polygons (point lists). returns region minus openings
    where openings = seeds (inset w/2) + every leftover space (inset w/2, rim w)."""
    inner = P_off_path(region, w)
    grown = merge([P(offset(s, -w / 2)) for s in seeds])
    holes = [P(offset(s, w / 2)) for s in seeds]
    left = diff(inner, grown)
    keep = [c for c in contours(left) if area(c) >= min_area]
    allholes = merge(holes + keep)
    allholes = inter(allholes, inner)
    return diff(region, allholes)


def P_off_path(region, w):
    """inset an arbitrary path by w (via stroke)."""
    st = vt.stroke_to_path(region, 2 * w, join='miter')
    return diff(region, st)


def v_point_region(R, t):
    s = star83(0, 0, R)
    band = diff(P(s), P(offset(s, t)))
    wedge = P([(0, 0), polar(0, 0, 900, 247.5), polar(0, 0, 900, 292.5)])
    return inter(band, wedge)


def arm_frame(R, t, side):
    """centre line of one arm of the bottom point of an {8/3} star band: from the tip-centre up to the miter."""
    s = star83(0, 0, R)
    tip_out = (0.0, R)
    dv = t / S
    tip_mid = (0.0, R - dv / 2)
    u = (side * S, -C)
    n = (C, side * S)
    return tip_mid, u, n


def seeds_star_frieze(R, t, w, scale=1.0, rot=0.0, first=0.0, n_max=12, centre=True, kind=(8, 3)):
    seeds = []
    rr = (t / 2 - w) * scale
    for side in (-1, 1):
        O, u, n = arm_frame(R, t, side)
        ang = math.degrees(math.atan2(-u[1], u[0]))          # math angle of u
        pitch = 2 * rr * math.cos(0 * D2R) + w
        k = 1
        while k < n_max:
            a = first + pitch * k
            c = (O[0] + u[0] * a, O[1] + u[1] * a)
            seeds.append(star_pts(c[0], c[1], rr, kind[0], kind[1], a0=ang + rot))
            k += 1
    if centre:
        O, u, n = arm_frame(R, t, 1)
        seeds.append(star_pts(O[0], O[1] + 0.0, rr, kind[0], kind[1], a0=90 + rot))
    return seeds


def mk(R=100.0, t=16.0, w=1.6, **kw):
    def f():
        region = v_point_region(R, t)
        seeds = seeds_star_frieze(R, t, w, **kw)
        return lace(region, seeds, w, min_area=w * w * 0.8)
    return f


def straight_v(H=100.0, t=24.0, w=2.0, scale=1.0, rot=0.0):
    def f():
        region = P(v_pts(H, TH, t))
        dv = t / S
        seeds = []
        rr = (t / 2 - w) * scale
        for side in (-1, 1):
            O = (0.0, H - dv / 2)
            u = (side * S, -C)
            ang = math.degrees(math.atan2(-u[1], u[0]))
            pitch = 2 * rr + w
            for k in range(1, 12):
                c = (O[0] + u[0] * pitch * k, O[1] + u[1] * pitch * k)
                seeds.append(star_pts(c[0], c[1], rr, 8, 3, a0=ang + rot))
        seeds.append(star_pts(0, H - dv / 2, rr, 8, 3, a0=90 + rot))
        top = P([(-300, 0), (300, 0), (300, 300), (-300, 300)])
        return inter(lace(region, seeds, w, min_area=w * w), top)
    return f


VARS = [('lace point t16 8/3 axis', mk(t=16.0, w=1.5)), ('lace point t16 rot22.5', mk(t=16.0, w=1.5, rot=22.5)),
        ('lace point t18 khatim', mk(t=18.0, w=1.6, kind=(8, 2), rot=22.5)), ('straight lace t24', straight_v()),
        ('straight lace rot', straight_v(rot=22.5)), ('lace point smaller stars', mk(t=16.0, w=1.4, scale=0.8))]

if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m = fn()
        m, _ = fit(m, 250, 250, 200, 200)
        f = os.path.join(OUT, f'l{i+1}.svg')
        open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name))
        files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r7.png')] + files, check=True)
    print('ok')
