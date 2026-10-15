"""Lace V (final family): symmetric per-arm frieze + designed junction + solid caps."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore8 import contours, area

TH = 22.5
S, C, TN = math.sin(TH * D2R), math.cos(TH * D2R), math.tan(TH * D2R)


def v_outline(H, t):
    dv = t / S
    return [(-H * TN, 0), (-(H - dv) * TN, 0), (0, H - dv), ((H - dv) * TN, 0), (H * TN, 0), (0, H)]


def inset(path, d):
    return diff(path, vt.stroke_to_path(path, 2 * d, join='miter'))


def build(H=124.0, t=26.0, rim=3.6, web=1.8, rot=22.5, m=3, k0=1.5, vstar=True, vscale=1.0, cap=6.0,
          gapf=1.0, kites=True, kite_min=1.0, last_full=True, ret=False):
    region = P(v_outline(H, t))
    dv = t / S
    O = (0.0, H - dv / 2)
    R = t / 2 - rim                             # star circumradius: side points one rim from each rail
    pitch = 2 * R * (math.cos(22.5 * D2R) if rot else 1.0) + web * gapf
    inner = inset(region, rim)
    inner = inter(inner, P([(-500, cap), (500, cap), (500, 500), (-500, 500)]))
    seeds = []
    for side in (-1, 1):
        u = (side * S, -C)
        ang = math.degrees(math.atan2(-u[1], u[0]))
        k = k0
        while True:
            c = (O[0] + u[0] * pitch * k, O[1] + u[1] * pitch * k)
            pts = star_pts(c[0], c[1], R, 8, m, a0=ang + rot)
            if min(p[1] for p in pts) < cap + web:
                break
            seeds.append(pts)
            k += 1
    if vstar:
        seeds.append(star_pts(O[0], O[1], R * vscale, 8, m, a0=90 + rot))
    holes = [P(offset(s, web / 2)) for s in seeds]
    if kites:
        grown = merge([P(offset(s, -web / 2)) for s in seeds])
        left = diff(inset(inner, web / 2), grown)
        for c in contours(left):
            if area(c) < kite_min:
                continue
            b = vt.bounds(c)
            if b[1] <= cap + web * 0.75:       # touches the cap: keep stone (closed lintel)
                continue
            holes.append(c)
    holes = inter(merge(holes), inner)
    mark = diff(region, holes)
    if ret:
        return mark, dict(seeds=seeds, R=R, pitch=pitch, O=O)
    return mark
