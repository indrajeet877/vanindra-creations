"""Hankin 'polygons in contact' jaali on the 4.8.8 (octagon-square) tiling, contact angle 67.5 deg.
Every star in this pattern is made of 45-degree V's whose tips sit on the tile-edge midpoints."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa

R83 = math.cos(math.pi * 3 / 8) / math.cos(math.pi * 2 / 8)   # 0.5412


def oct_star(cx, cy, a):
    """{8/3} star inscribed in the octagon of the 4.8.8 tiling (apothem a/2): points at edge midpoints."""
    A = a / 2
    pts = []
    for k in range(8):
        pts.append(polar(cx, cy, A, k * 45.0))
        pts.append(polar(cx, cy, A * R83, k * 45.0 + 22.5))
    return pts


def sq_star(cx, cy, a):
    """4-point star in the 45-degree square of the tiling; points at its edge midpoints."""
    s = a * math.tan(22.5 * D2R)             # tiling edge length
    A = s / 2                                # square apothem
    rin = A * 0.41421356                     # Hankin 67.5deg in a square
    pts = []
    for k in range(4):
        pts.append(polar(cx, cy, A, 45.0 + k * 90.0))
        pts.append(polar(cx, cy, rin, 90.0 + k * 90.0))
    return pts


def hankin_cells(a, xr, yr, ox=0.0, oy=0.0):
    """list of star outlines (point lists) covering i in [-xr, xr], j in [-yr, yr]."""
    stars = []
    for i in range(-xr, xr + 1):
        for j in range(-yr, yr + 1):
            stars.append(('o', oct_star(ox + i * a, oy + j * a, a)))
            stars.append(('s', sq_star(ox + (i + 0.5) * a, oy + (j + 0.5) * a, a)))
    return stars


def hankin_webs(a, w, xr, yr, ox=0.0, oy=0.0):
    """stone webs of width w along every star outline (strapwork)."""
    paths = []
    for kind, pts in hankin_cells(a, xr, yr, ox, oy):
        paths.append(vt.stroke_to_path(P(pts), w, join='miter'))
    return merge(paths)
