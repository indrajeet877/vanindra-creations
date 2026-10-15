"""Round 7: two stone piers (the V) holding a jaali screen in the counter."""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER, v_pts
from explore2 import BIG, TH, S, C
from explore4 import star83

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
TN = math.tan(TH * D2R)


def counter_pts(H, t):
    dv = t / S
    return [(-(H - dv) * TN, 0), ((H - dv) * TN, 0), (0, H - dv)]


def khatim_lattice(a, w, xr, yr, y0=0.0, kind='khatim'):
    """openings of a star-and-cross jaali on a square grid of pitch a (stars at nodes)."""
    holes = []
    for i in range(-xr, xr + 1):
        for j in range(-1, yr):
            cx, cy = i * a, y0 + j * a
            if kind == 'khatim':
                holes.append(P(offset(star_pts(cx, cy, a * 0.5 * 1.0, 8, 2, a0=90), w / 2)))
            elif kind == '83':
                holes.append(P(offset(star_pts(cx, cy, a * 0.5 / math.cos(22.5 * D2R) * 0.98, 8, 3, a0=90), w / 2)))
            elif kind == 'oct':
                holes.append(P(offset(ngon_pts(cx, cy, a * 0.5 / math.cos(22.5 * D2R), 8, a0=22.5), w / 2)))
                holes.append(P(offset(ngon_pts(cx + a / 2, cy + a / 2, (a - 2 * a * 0.5 * math.tan(22.5 * D2R)) / math.sqrt(2) * 0.5 * math.sqrt(2), 4, a0=0), w / 2)))
    return merge(holes)


def screen_V(H=100.0, t=24.0, a=8.0, w=1.6, kind='khatim', gap=0.0, top_rim=True):
    V = P(v_pts(H, TH, t))
    cpts = counter_pts(H, t)
    inner = P(offset(cpts, w if gap == 0 else gap + w))
    holes = khatim_lattice(a, w, 12, 16, y0=0.0, kind=kind)
    if top_rim:
        inner = inter(inner, P([(-300, w), (300, w), (300, 300), (-300, 300)]))
    holes = inter(holes, inner)
    solid = union(V, P(cpts))
    if gap:
        ring = diff(P(cpts), P(offset(cpts, gap)))
        solid = diff(solid, ring)
    return inter(diff(solid, holes), BIG)


def mitred_screen(R=100.0, t=12.0, a=6.0, w=1.3, kind='khatim'):
    s = star83(0, 0, R)
    band = diff(P(s), P(offset(s, t)))
    wedge = P([(0, 0), polar(0, 0, 900, 247.5), polar(0, 0, 900, 292.5)])
    v = inter(band, wedge)
    cnt = inter(P(offset(s, t)), wedge)              # counter region of the point
    inner = inter(P(offset(offset(s, t), w)), P([(0, w * 1.4), polar(0, w * 1.4, 900, 247.5), polar(0, w * 1.4, 900, 292.5)]))
    holes = khatim_lattice(a, w, 14, 30, y0=0.0, kind=kind)
    holes = inter(holes, inner)
    return diff(union(v, cnt), holes)


VARS = [('S1 piers + khatim screen', lambda: screen_V()), ('S2 piers + 8/3 screen', lambda: screen_V(kind='83', a=9.0)),
        ('S3 octagon-square screen', lambda: screen_V(kind='oct', a=9.0)), ('S4 mitred point + screen', mitred_screen),
        ('S5 inlaid screen (gap)', lambda: screen_V(gap=2.4)), ('S6 lighter V, larger cells', lambda: screen_V(t=18.0, a=11.0, w=1.8))]

if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m = fn()
        m, _ = fit(m, 250, 250, 200, 200)
        f = os.path.join(OUT, f's{i+1}.svg')
        open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name))
        files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r6.png')] + files, check=True)
    print('ok')
