"""Parametric 'V cut from emeralds' generator.

The V is two step-cut stones (baguettes) mitred at the culet. Every edge is a straight line computed
from a few parameters; corners are clipped the way an emerald cut clips its girdle corners.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *


def unit(dx, dy):
    L = math.hypot(dx, dy)
    return dx / L, dy / L


def par_line(p, q, d, toward):
    """Line through p,q shifted by distance d toward point `toward`."""
    ux, uy = unit(q[0] - p[0], q[1] - p[1])
    nx, ny = -uy, ux
    if (toward[0] - p[0]) * nx + (toward[1] - p[1]) * ny < 0:
        nx, ny = -nx, -ny
    return (p[0] + nx * d, p[1] + ny * d), (q[0] + nx * d, q[1] + ny * d)


def clip_corner(pts, idx, d1, d2=None):
    """Replace vertex idx with two points at distances d1 (toward prev) and d2 (toward next)."""
    d2 = d1 if d2 is None else d2
    n = len(pts)
    p = pts[idx]; a = pts[idx - 1]; b = pts[(idx + 1) % n]
    ua = unit(a[0] - p[0], a[1] - p[1]); ub = unit(b[0] - p[0], b[1] - p[1])
    return pts[:idx] + [(p[0] + ua[0] * d1, p[1] + ua[1] * d1), (p[0] + ub[0] * d2, p[1] + ub[1] * d2)] + pts[idx + 1:]


def v_frame(H=160.0, xl=0.0, xr=90.0, xv=45.0, tL=26.0, tR=26.0, top='h'):
    """Return key points of a V: outer top-left, inner top-left, crotch, inner top-right, outer top-right, vertex."""
    Vb = (xv, H)
    TLo = (xl, 0.0)
    TRo = (xr, 0.0)
    Li = par_line(TLo, Vb, tL, (xv, 0))
    Ri = par_line(TRo, Vb, tR, (xv, 0))
    crotch = isect(*Li, *Ri)
    TLi = isect(*Li, (0, 0), (1, 0))
    TRi = isect(*Ri, (0, 0), (1, 0))
    return dict(TLo=TLo, TLi=TLi, crotch=crotch, TRi=TRi, TRo=TRo, Vb=Vb, Li=Li, Ri=Ri)


def build(H=160.0, W=90.0, xv=None, tL=26.0, tR=26.0, chO=10.0, chI=3.0, culet=7.0,
          inset=6.5, seam=1.8, mitre=True, table_role='B', step_role='A', thin_solid_below=0.0,
          steps=None, seam_cap='butt', top_cut=None):
    """Build the V gem. Returns list of (path, role)."""
    xv = W / 2 if xv is None else xv
    f = v_frame(H, 0.0, W, xv, tL, tR)
    # left stone polygon (clockwise in screen space): outer-top, inner-top, crotch, vertex
    left = [f['TLo'], f['TLi'], f['crotch'], f['Vb']]
    right = [f['TRi'], f['TRo'], f['Vb'], f['crotch']]
    # culet: cut the shared vertex with a horizontal line `culet` above the base
    yc = H - culet

    def cut_base(pts):
        out = []
        n = len(pts)
        for i in range(n):
            a = pts[i]; b = pts[(i + 1) % n]
            if a[1] <= yc:
                out.append(a)
            if (a[1] - yc) * (b[1] - yc) < 0:
                t = (yc - a[1]) / (b[1] - a[1])
                out.append((a[0] + (b[0] - a[0]) * t, yc))
        return out
    if culet > 0:
        left = cut_base(left); right = cut_base(right)
    # clip the outer top corners (emerald-cut girdle corners) and the inner top corners lightly
    left = clip_corner(left, 0, chO)            # outer top-left
    left = clip_corner(left, 2, chI) if chI > 0 else left  # inner top-left (index shifted by 1)
    ri = 1
    right = clip_corner(right, ri, chO)
    right = clip_corner(right, 0, chI) if chI > 0 else right
    stones = [(left, tL), (right, tR)]
    parts = []
    for pts, t in stones:
        if steps is None:
            ins = [inset] if t > 2.6 * inset else []
        else:
            ins = [s for s in steps if t > 2.4 * s]
        rings = [pts] + [offset_poly(pts, s) for s in ins]
        seams = []
        if len(rings) > 1:
            seams += [seg(rings[0][i], rings[-1][i], 0.01) for i in range(len(pts))]
            seams += [polyline(R + [R[0]]) for R in rings[1:]]
            for k in range(len(rings) - 1):
                parts.append((cut(difference(poly(rings[k]), poly(rings[k + 1])), seams, seam, seam_cap), step_role))
            parts.append((cut(poly(rings[-1]), seams, seam, seam_cap), table_role))
        else:
            parts.append((poly(pts), step_role))
    # open the mitre seam between the two stones
    if mitre:
        m = seg(f['crotch'], (f['Vb'][0], H + 5), 0.0)
        parts = [(cut(p, [m], seam), r) for p, r in parts]
    return parts, f


def silhouette(**kw):
    parts, f = build(**kw)
    return union(*[p for p, _ in parts])
