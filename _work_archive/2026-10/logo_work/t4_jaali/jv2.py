"""Jaali V v2: per-arm lattice in the arm's own frame (mirrored at the axis), whole cells only,
leftover spaces opened only where they lie BETWEEN stars (true jaali kites); ends closed by a lintel."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore8 import P_off_path, contours, area

TH = 22.5
S, C, TN = math.sin(TH * D2R), math.cos(TH * D2R), math.tan(TH * D2R)


def v_outline(H, t):
    dv = t / S
    return [(-H * TN, 0), (-(H - dv) * TN, 0), (0, H - dv), ((H - dv) * TN, 0), (H * TN, 0), (0, H)]


def to_world(O, u, n, a, b):
    return (O[0] + u[0] * a + n[0] * b, O[1] + u[1] * a + n[1] * b)


def build(H=124.0, t=26.0, rim=3.8, web=2.0, rows=1, lintel=5.0, vertex_scale=1.0, star_m=3, kites=True, min_area=1.0, half=False):
    region = P(v_outline(H, t))
    dv = t / S
    O = (0.0, H - dv / 2)
    band = t - 2 * rim                       # clear width between rails
    cell = band / rows                       # one cell per row across the arm
    R = cell / 2                             # star radius so side points touch the rails / neighbours (web shared)
    seeds = []
    inner = P_off_path(region, rim)
    inner = inter(inner, P([(-500, lintel), (500, lintel), (500, 500), (-500, 500)]))
    for side in (-1, 1):
        u = (side * S, -C)
        n = (C, side * S)
        ang = math.degrees(math.atan2(-u[1], u[0]))
        pitch = cell
        for r in range(rows):
            b = -band / 2 + cell * (r + 0.5)
            k = 1 if rows == 1 else 0
            while True:
                a = k * pitch + (cell / 2 if (rows > 1 and r % 2) else 0)
                c = to_world(O, u, n, a, b)
                pts = star_pts(c[0], c[1], R - web / 2, 8, star_m, a0=ang + 22.5)
                if min(p[1] for p in pts) < lintel + web:
                    break
                if area(diff(P(pts), inner)) < 1e-6:
                    seeds.append(pts)
                k += 1
                if k > 40:
                    break
    if rows == 1:
        Rv = (R - web / 2) * vertex_scale
        seeds.append(star_pts(O[0], O[1], Rv, 8, star_m, a0=90 + 22.5))
    holes = [P(s) for s in seeds]
    if kites:
        grown = merge([P(offset(s, -web)) for s in seeds])
        left = diff(inner, grown)
        keep = []
        for c in contours(left):
            if area(c) < min_area:
                continue
            # keep only spaces enclosed between stars: their bbox must not reach the lintel line
            b = vt.bounds(c)
            if b[1] <= lintel + 0.01 and not half:
                continue
            keep.append(c)
        holes += keep
    holes = inter(merge(holes), inner)
    return diff(region, holes)
