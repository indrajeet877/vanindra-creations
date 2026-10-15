"""The VanIndra jaali canvas: Hankin 4.8.8 pattern (contact 67.5 deg) where every star point is the brand's V-unit."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from hankin import oct_star, sq_star


def star_units(pts, cx, cy, t, slit, n):
    """band of thickness t inside a star outline (2n points), split into n V-units by radial slits through the notches."""
    band = diff(P(pts), P(offset(pts, t)))
    cuts = []
    for k in range(n):
        q = pts[2 * k + 1]                     # inner vertex (notch)
        a = math.degrees(math.atan2(-(q[1] - cy), q[0] - cx))
        cuts.append(vt.stroke_to_path(P([(cx, cy), polar(cx, cy, 1e3, a), polar(cx, cy, 1e3, a + 1e-4)]), slit))
    return diff(band, merge(cuts))


def canvas(a=100.0, t=None, slit=None, xr=3, yr=3, square=True):
    t = t if t is not None else a * 0.05
    slit = slit if slit is not None else t * 0.32
    parts = []
    for i in range(-xr, xr + 1):
        for j in range(-yr, yr + 1):
            cx, cy = i * a, j * a
            parts.append(star_units(oct_star(cx, cy, a), cx, cy, t, slit, 8))
            if square:
                sx, sy = cx + a / 2, cy + a / 2
                parts.append(star_units(sq_star(sx, sy, a), sx, sy, t * 0.8, slit * 0.8, 4))
    return merge(parts)
