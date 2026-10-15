"""Calligraphic va/V monogram: crescent left stroke (thin at the headline, swelling, pointed foot),
hairline return to the danda, headline bar. Exact quadratic/cubic geometry."""
import math
import pathops
from geo import *

def qpt(p0, c, p1, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])

def qsplit(p0, c, p1, t):
    """Return control & end of the sub-curve [0,t]."""
    a = (p0[0] + (c[0] - p0[0]) * t, p0[1] + (c[1] - p0[1]) * t)
    b = (c[0] + (p1[0] - c[0]) * t, c[1] + (p1[1] - c[1]) * t)
    e = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    return a, e

def perp_ctrl(p0, p1, bulge, frac=0.5):
    """Control point at chord fraction frac, pushed perpendicular by bulge (positive = left of travel when
    travelling p0->p1 in y-down coords, i.e. towards -x for a downward chord)."""
    mx, my = p0[0] + (p1[0] - p0[0]) * frac, p0[1] + (p1[1] - p0[1]) * frac
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    return (mx - nx * bulge, my - ny * bulge) if False else (mx + (-dy / L) * -bulge * -1, my + (dx / L) * -bulge * -1)

def ctrl_left(p0, p1, bulge, frac=0.5):
    # for a chord going down-right, push the control point towards lower-left (outward of a V's left arm)
    mx, my = p0[0] + (p1[0] - p0[0]) * frac, p0[1] + (p1[1] - p0[1]) * frac
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    # normal pointing to the left side of a downward chord: (dy, -dx)/L has +x for dy>0 ... we want -x: (-dy, dx)
    nx, ny = -dy / L, dx / L
    return (mx + nx * bulge, my + ny * bulge)

def line_isect_quad(p0, c, p1, a, b, n=400):
    """Find t where quadratic crosses the line a->b (first crossing from t=1 backwards)."""
    def side(pt):
        return (b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0])
    prev_t, prev_s = 1.0, side(qpt(p0, c, p1, 1.0))
    for i in range(n - 1, -1, -1):
        t = i / n
        s = side(qpt(p0, c, p1, t))
        if (s > 0) != (prev_s > 0):
            lo, hi = t, prev_t
            for _ in range(60):
                mid = (lo + hi) / 2
                if (side(qpt(p0, c, p1, mid)) > 0) == (s > 0):
                    lo = mid
                else:
                    hi = mid
            return (lo + hi) / 2
        prev_t, prev_s = t, s
    return None

def va2(H=100, b=9, S=15, h=3.6, t0=4.5, px=38, py=None, o=1.8, xs=64, yj=0.56,
        bo=11, bi=4, fo=0.45, fi=0.5, ovl=12, ovr=5, bindu=None, br=None, bgap=None, gap=None):
    py = H + o if py is None else py
    P = (px, py)
    J = (xs, yj * H)
    # right arm inner edge: parallel to P->J, offset towards upper-left by h
    dx, dy = J[0] - P[0], J[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L      # for P->J going up-right (dy<0): (dy,-dx) -> (-,-) upper-left
    Pi, Ji = (P[0] + nx * h, P[1] + ny * h), (J[0] + nx * h, J[1] + ny * h)
    Jy = line_x((Pi[1], Pi[0]), (Ji[1], Ji[0]), xs)  # y on inner line at x=xs (swap trick)
    J2 = (xs, Jy)
    # outer left edge
    O0 = (0.0, 0.0)
    co = ctrl_left(O0, P, bo, fo)
    # inner left edge: starts at bar bottom, thin t0
    I0 = (t0 + b * (px / py), float(b))
    ci = ctrl_left(I0, P, bi, fi)
    t = line_isect_quad(I0, ci, P, Pi, Ji)
    cq, Q = qsplit(I0, ci, P, t)
    p = pathops.Path()
    p.moveTo(*O0)
    p.quadTo(*co, *P)
    p.lineTo(*J)
    p.lineTo(xs + 0.5, J[1])
    p.lineTo(xs + 0.5, J2[1])
    p.lineTo(*J2)
    p.lineTo(*Q)
    p.quadTo(*cq, *I0)
    p.lineTo(I0[0], 0)
    p.close()
    bowl = U(p)
    stem = rect(xs, 0, xs + S, H)
    g = U(bowl, stem, rect(-ovl, 0, xs + S + ovr, b))
    g = I(g, rect(-ovl - 5, 0, xs + S + ovr + 5, H + o + 0.01))
    if gap:  # optional break in the headline above the counter
        g = D(g, rect(gap[0], -1, gap[1], b + 0.01))
    info = dict(P=P, J=J, Q=Q, xs=xs, S=S, x0=-ovl, x1=xs + S + ovr, co=co, ci=ci)
    if bindu:
        r = br or S * 0.55
        gp = bgap if bgap is not None else b * 1.0
        cx = xs + S / 2 if bindu == 'stem' else (-ovl + xs + S + ovr) / 2
        g = U(g, circle(cx, -gp - r, r))
    return g, info
