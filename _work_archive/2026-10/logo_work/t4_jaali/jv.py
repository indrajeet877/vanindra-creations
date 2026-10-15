"""The Jaali V -- parametric builder (all geometry from one 22.5-degree grid).

V: arms at +-22.5 deg from vertical (the point angle of the Mughal {8/3} star), thickness t, height H, flat top.
Lace: {8/3} star openings along each arm's centre line, edges parallel to the rails; every leftover
space between stars and rails is opened too, so the stone is only constant-width webs (true jaali).
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from explore8 import P_off_path, contours, area

TH = 22.5
S, C, TN = math.sin(TH * D2R), math.cos(TH * D2R), math.tan(TH * D2R)


def v_outline(H, t, tip_cut=0.0):
    dv = t / S
    Wo, Wi = H * TN, (H - dv) * TN
    pts = [(-Wo, 0), (-Wi, 0), (0, H - dv), (Wi, 0), (Wo, 0)]
    if tip_cut > 0:
        pts += [(tip_cut * TN, H - tip_cut), (-tip_cut * TN, H - tip_cut)]
    else:
        pts += [(0, H)]
    return pts


def arms():
    out = []
    for side in (-1, 1):
        u = (side * S, -C)
        out.append((u, math.degrees(math.atan2(-u[1], u[0]))))
    return out


def build(H=124.0, t=24.0, rim=3.6, web=1.9, lintel=None, n=None, R=None, min_area=1.2, star_m=3, vertex=True, keep_left=True, ret_parts=False):
    region = P(v_outline(H, t))
    dv = t / S
    O = (0.0, H - dv / 2)                      # where the two arm centre lines meet
    R = R if R else t / 2 - rim                # star radius: side points sit exactly one rim from each rail
    L = (H - dv / 2) / C                       # centre-line length up to the top edge
    lintel = lintel if lintel is not None else rim
    # number of stars per arm and an exact pitch so the last star clears the lintel by one web
    ext = R                                    # conservative along-axis extent
    seeds = []
    pitch0 = 2 * R * math.cos(22.5 * D2R) + web
    # top limit along the axis: the star must stay below y = lintel (+web)
    for u, ang in arms():
        k = 1
        while True:
            c = (O[0] + u[0] * pitch0 * k, O[1] + u[1] * pitch0 * k)
            pts = star_pts(c[0], c[1], R, 8, star_m, a0=ang + 22.5)
            if min(p[1] for p in pts) < lintel + web * 0.999:
                break
            seeds.append(pts)
            k += 1
            if n and k > n:
                break
    if vertex:
        seeds.append(star_pts(O[0], O[1], R, 8, star_m, a0=90 + 22.5))
    inner = P_off_path(region, rim)
    inner = inter(inner, P([(-500, lintel), (500, lintel), (500, 500), (-500, 500)]))
    stars = [P(offset(s, web / 2)) for s in seeds]
    grown = merge([P(offset(s, -web / 2)) for s in seeds])
    left = [c for c in contours(diff(inner, grown)) if area(c) > min_area] if keep_left else []
    holes = inter(merge(stars + left), inner)
    mark = diff(region, holes)
    if ret_parts:
        return mark, dict(region=region, seeds=seeds, O=O, R=R, pitch=pitch0, inner=inner)
    return mark
