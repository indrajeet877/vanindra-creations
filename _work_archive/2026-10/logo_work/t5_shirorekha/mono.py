"""Monogram constructions: Latin V + Devanagari va under one shirorekha."""
import math
import pathops
from geo import *

def va_mark(H=100, b=13, S=17, Td=18, h=5.0, vx=40, yb=1.0, yj=0.55, o=1.6, ovl=None, ovr=None,
            bindu=None, bindu_r=None, bindu_gap=None, curve=0.0, bar_cut=None):
    """V-bowl + danda under a headline = va.
    Outer left edge of the V runs from (0,0) to the point P=(vx, yb*H+o).
    The right (thin) arm rises from P symmetric to the left edge until it meets the danda at height yj*H.
    curve > 0 bows the left arm outward (both edges), giving the va-bowl feel."""
    Py = yb * H + (o if yb >= 0.999 else 0)
    P = (vx, Py)
    theta = math.atan2(vx, Py)
    xs = vx + (Py - yj * H) * math.tan(theta)
    L0, L1 = (0, 0), P
    R0, R1 = (2 * vx, 0), P
    Li = offset(L0, L1, Td); Li = Li if line_x(*Li, 0) > 0 else offset(L0, L1, -Td)
    Ri = offset(R0, R1, h); Ri = Ri if line_x(*Ri, 0) < 2 * vx else offset(R0, R1, -h)
    iv = isect(*Li, *Ri)
    top = 0
    p = pathops.Path()
    p.moveTo(0, top)
    if curve <= 0:
        p.lineTo(line_x(*Li, top), top)
        p.lineTo(*iv)
    else:
        p.lineTo(line_x(*Li, top), top)
        a = (line_x(*Li, top), top)
        n = (-(iv[1] - a[1]), iv[0] - a[0]); L = math.hypot(*n); n = (n[0] / L, n[1] / L)
        c = ((a[0] + iv[0]) / 2 + n[0] * curve * 0.8, (a[1] + iv[1]) / 2 + n[1] * curve * 0.8)
        p.quadTo(*c, *iv)
    p.lineTo(line_x(*Ri, top), top)
    p.lineTo(2 * vx, top)
    p.lineTo(*P)
    if curve <= 0:
        p.lineTo(0, top)
    else:
        n = (-(0 - P[1]), 0 - P[0]); L = math.hypot(*n); n = (n[0] / L, n[1] / L)
        c = ((P[0]) / 2 + n[0] * curve, (P[1]) / 2 + n[1] * curve)
        p.quadTo(*c, 0, top)
    p.close()
    v = U(p)
    stem = rect(xs, 0, xs + S, H)
    g = I(U(v, stem), rect(-50, 0, xs + S, H + o))
    ovl = b * 0.9 if ovl is None else ovl
    ovr = b * 0.5 if ovr is None else ovr
    x0, x1 = -ovl, xs + S + ovr
    if bar_cut:
        bar = poly([(x0, 0), (x1, 0), (x1, b), (x0 + bar_cut, b)])
    else:
        bar = rect(x0, 0, x1, b)
    g = U(g, bar)
    if bindu:
        r = bindu_r or S * 0.56
        gp = bindu_gap if bindu_gap is not None else b * 0.85
        cx = xs + S / 2 if bindu == 'stem' else (x0 + x1) / 2
        g = U(g, circle(cx, -gp - r, r))
    return g, dict(xs=xs, S=S, x0=x0, x1=x1, P=P)
