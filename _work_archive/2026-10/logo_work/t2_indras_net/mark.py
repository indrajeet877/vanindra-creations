"""The 'One Thread, Many Jewels' mark — exact construction on a rhombic lattice.

GRID
  P(u, v) = O + u*e1 + v*e2 ;  e1 = (s*h, h), e2 = (-s*h, h)      (SVG y-down)
  A cell is the rhombus u in [i, i+1], v in [j, j+1]: vertical diagonal 2h, horizontal diagonal 2sh.
  The two lattice directions are the two strokes of the V.

PARTS
  stones : the thick (down-right) stroke is a band of NL cell-columns (j = 0..NL-1), rows i = -K..-1.
           every cell becomes a stone by insetting it by g on every side, so a light-line of width 2g
           (the net's thread, drawn in negative) separates neighbouring stones.
  thread : the thin (down-left) stroke is ONE positive thread on the lattice line u = 0, with the SAME
           width 2g as the light-lines.  All light-lines that cross the band run parallel to it, so the
           thread visibly repeats through the jewels as light.  Its upper end is cut on the lattice
           (parallel to e1) so every top terminal of the mark is a lattice point.
  through: optional — the thread continues through the band as a light-line; stones below it form the
           tip (variant of the base construction).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from geo import *  # noqa: F401,F403,E402
from fontTools.pens.statisticsPen import StatisticsPen  # noqa: E402


def lat_units(L, g):
    cross = abs(L.e1[0] * L.e2[1] - L.e1[1] * L.e2[0])
    du = g / (cross / math.hypot(*L.e2))   # a perpendicular distance g expressed in u units
    dv = g / (cross / math.hypot(*L.e1))
    return du, dv


def para(L, u0, u1, v0, v1):
    return poly([L.P(u0, v0), L.P(u1, v0), L.P(u1, v1), L.P(u0, v1)])


def stone(L, i, j, g):
    du, dv = lat_units(L, g)
    return para(L, i + du, i + 1 - du, j + dv, j + 1 - dv)


def build(s=0.38, h=60.0, K=6, NL=2, g=3.2, tw=None, thread_top=None, top='lattice',
          below=0, drop=(), gold=(), solid=False, thread_join=0.0):
    """Return dict(em=Path, au=Path|None, L=Lattice, meta=...)."""
    L = Lattice((0.0, 0.0), h, s)
    du, dv = lat_units(L, g)
    tw = 2 * g if tw is None else tw
    tdu, _ = lat_units(L, tw / 2)
    cells = [(i, j) for j in range(NL) for i in range(-K, below) if (i, j) not in drop]
    if solid:
        band = union(*[para(L, i, i + 1, j, j + 1) for (i, j) in cells])
        stones = {('solid',): band}
    else:
        stones = {c: stone(L, c[0], c[1], g) for c in cells}
    vt = -K if thread_top is None else thread_top
    v_end = 0.0 + thread_join
    if top == 'lattice':
        thread = para(L, -tdu, tdu, vt, v_end)
    else:  # flat (horizontal) top at the cap line y = -K*h
        thread = intersection(para(L, -tdu, tdu, vt - 2, v_end), halfplane_below(-K * h))
    em = union(thread, *[p for c, p in stones.items() if c not in gold])
    au = union(*[p for c, p in stones.items() if c in gold]) if gold else None
    return dict(em=em, au=au, L=L, cells=cells)


def halfplane_below(y, big=1e5):
    return poly([(-big, y), (big, y), (big, big), (-big, big)])


def centroid(path):
    pen = StatisticsPen()
    path.draw(pen)
    return pen.meanX, pen.meanY, abs(pen.area)


def place(paths, box, height, cx=None, cy=None, optical=0.35):
    """Scale so the union's height == height, centre: horizontally by a blend of bbox-centre and area-centroid."""
    allp = union(*[p for p in paths if p is not None])
    x0, y0, x1, y1 = bounds(allp)
    k = height / (y1 - y0)
    mx, my, _ = centroid(allp)
    bx = (x0 + x1) / 2
    ox = bx * (1 - optical) + mx * optical
    cx = box / 2 if cx is None else cx
    cy = box / 2 if cy is None else cy
    tx, ty = cx - ox * k, cy - (y0 + y1) / 2 * k
    return [transform(p, k, 0, 0, k, tx, ty) if p is not None else None for p in paths], k


def build2(s=0.40, h=60.0, K=5, NL=2, g=4.0, tw=12.0, gold=((-1, 0),), small=False,
           split=0.0, fuse=False, tw_small=None):
    """Final construction.

    The thread's OUTER edge lies on the line u = -du, i.e. exactly on the lower facets of the bottom stones, so the
    V's right-hand contour is one straight line from the thread's top to the vertex.  The thread stops one
    light-line (2g) short of the stone it meets.  Its top is cut on the lattice and lifted so its peak sits exactly at
    the cap line defined by the band's top stone.
    small=True: stones merge into a solid band (optionally split once along its length by `split`), the thread is
    thickened to tw_small and fused to the band.
    """
    L = Lattice((0.0, 0.0), h, s)
    du, dv = lat_units(L, g)
    tww = tw_small if (small and tw_small) else tw
    twu, _ = lat_units(L, tww)
    a, b = -du - twu, -du                 # thread spans u in [a, b]
    v_top = -K + 2 * du + dv + twu        # peak of thread == peak of band's top stone
    v_end = dv if fuse else -dv
    thread = para(L, a, b, v_top, v_end)
    stones = {}
    if small:
        if split > 0:
            _, sv = lat_units(L, split / 2)
            parts = [para(L, -K + du, -du, dv, 1 - sv), para(L, -K + du, -du, 1 + sv, NL - dv)]
        else:
            parts = [para(L, -K + du, -du, dv, NL - dv)]
        em = union(thread, *parts)
        return dict(em=em, au=None, L=L)
    for j in range(NL):
        for i in range(-K, 0):
            stones[(i, j)] = stone(L, i, j, g)
    em = union(thread, *[p for c, p in stones.items() if c not in gold])
    au = union(*[p for c, p in stones.items() if c in gold]) if gold else None
    return dict(em=em, au=au, L=L, stones=stones, thread=thread)


def build_small_knot(s=0.40, h=60.0, K=4, NL=2, g=7.0, tw=20.0, knot=((-1, 0),), rows_cut=()):
    """Small master: solid strap (cells merged) with the knot stone(s) set apart by light-lines, plus the thread.
    rows_cut: extra cross light-lines (u values) to cut the strap into segments."""
    L = Lattice((0.0, 0.0), h, s)
    du, dv = lat_units(L, g)
    twu, _ = lat_units(L, tw)
    strap = para(L, -K + du, -du, dv, NL - dv)
    cut = []
    for (i, j) in knot:
        cut.append(para(L, i - du, i + 1 + du, j - dv, j + 1 + dv))
    for u in rows_cut:
        cut.append(para(L, u - du, u + du, -1, NL + 1))
    if cut:
        strap = difference(strap, union(*cut))
    stones = [stone(L, i, j, g) for (i, j) in knot]
    v_top = -K + 2 * du + dv + twu
    thread = para(L, -du - twu, -du, v_top, -dv)
    return dict(em=union(strap, thread, *stones), au=None, L=L)
