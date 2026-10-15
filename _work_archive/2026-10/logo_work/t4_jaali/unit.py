"""The jaali unit: one point of the Mughal {8/3} star, drawn the way masons draw it (Hankin, contact 67.5 deg).
Eight units lock into the star; a field of stars is the jaali."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa

K83 = math.cos(math.pi * 3 / 8) / math.cos(math.pi * 2 / 8)   # inner/outer radius of {8/3} = 0.5412


def unit(R=100.0, t=10.0, k=0, slit=0.0, cx=0.0, cy=0.0, outside=False):
    """k=0 -> the bottom point (a V). Band of thickness t inside (or outside) the star outline,
    cut on the two radii through the notches; slit = optional gap on those radii (for the rosette)."""
    s = star_pts(cx, cy, R, 8, 3, a0=90)
    band = diff(P(offset(s, -t)), P(s)) if outside else diff(P(s), P(offset(s, t)))
    a = 270 + 45 * k
    wedge = P([(cx, cy), polar(cx, cy, 4 * R, a - 22.5), polar(cx, cy, 4 * R, a + 22.5)])
    u = inter(band, wedge)
    if slit:
        cuts = merge([vt.stroke_to_path(P([(cx, cy), polar(cx, cy, 4 * R, a + sg * 22.5), polar(cx, cy, 4 * R, a + sg * 22.5 + 0.001)]), slit) for sg in (-1, 1)])
        u = diff(u, cuts)
    return u


def rosette(R=100.0, t=10.0, slit=2.0, cx=0.0, cy=0.0, outside=False):
    return merge([unit(R, t, k, slit, cx, cy, outside) for k in range(8)])
