"""Round 4: the star-point V. One point of an 8-point (8/3) jaali star = a V; eight lock into the rosette."""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore import RENDER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
K = math.cos(math.pi * 3 / 8) / math.cos(math.pi * 2 / 8)


def star83(cx, cy, R, a0=90):
    return star_pts(cx, cy, R, 8, 3, a0=a0)


def point_v(t, R=100.0, slit=0.0, out=False, k=0):
    """one point (index k, k=0 => bottom) of an {8/3} star band of thickness t."""
    outer = star83(0, 0, R)
    if out:
        band = diff(P(offset(outer, -t)), P(outer))
    else:
        band = diff(P(outer), P(offset(outer, t)))
    a = 270 + 45 * k
    wedge = P([(0, 0), polar(0, 0, 900, a - 22.5), polar(0, 0, 900, a + 22.5)])
    v = inter(band, wedge)
    if slit:
        cuts = union(*[vt.stroke_to_path(P([(0, 0), polar(0, 0, 900, a + s * 22.5)]), slit) for s in (-1, 1)])
        v = diff(v, cuts)
    return v


def rosette(t, R=100.0, slit=3.0, out=False):
    return union(*[point_v(t, R, slit, out, k) for k in range(8)])


def inline(v, t, g):
    """carved groove along the middle of the band"""
    return v


def var(t, **kw):
    return lambda: point_v(t, **kw)


VARS = [
    ('P1 t=7', var(7.0)), ('P1 t=9', var(9.0)), ('P1 t=11', var(11.0)),
    ('P1 band outside, t=9', var(9.0, out=True)), ('rosette t=9', lambda: rosette(9.0)), ('rosette t=11 outside', lambda: rosette(11.0, out=True)),
]

if __name__ == '__main__':
    files = []
    for i, (name, fn) in enumerate(VARS):
        m = fn()
        m, _ = fit(m, 250, 250, 200, 200)
        f = os.path.join(OUT, f'w{i+1}.svg')
        open(f, 'w').write(svg(400, 400, [(m, EMERALD)], bg=IVORY, title=name))
        files.append(f)
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'explore_r3.png')] + files, check=True)
    print('ok')
