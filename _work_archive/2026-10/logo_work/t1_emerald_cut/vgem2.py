"""Two-stone Didone V ('The Emerald Cut'), robust step-cut faceting.

Construction (all straight lines on a 9:16 grid, H=160, W=90):
  * outer edges of the V run from the top corners of the 9:16 box to the culet on the axis;
  * the broad stroke is a step-cut baguette (girdle, one step ring, table) - an elongated octagon;
  * the hairline stroke is a slender baguette, solid;
  * the two stones meet on a mitre seam running from the crotch to the culet;
  * insets are computed as exact half-plane intersections (Sutherland-Hodgman), and every corner
    seam runs along the vertex bisector to the table - exactly how a step cut is laid out.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *


def unit(dx, dy):
    L = math.hypot(dx, dy)
    return dx / L, dy / L


def par_line(p, q, d, toward):
    ux, uy = unit(q[0] - p[0], q[1] - p[1])
    nx, ny = -uy, ux
    if (toward[0] - p[0]) * nx + (toward[1] - p[1]) * ny < 0:
        nx, ny = -nx, -ny
    return (p[0] + nx * d, p[1] + ny * d), (q[0] + nx * d, q[1] + ny * d)


def clip_halfplane(pts, a, b, keep):
    """Keep the side of line ab that contains point `keep`."""
    def side(p):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    s_keep = side(keep)
    out = []
    n = len(pts)
    for i in range(n):
        P = pts[i]; Q = pts[(i + 1) % n]
        sp, sq = side(P) * s_keep, side(Q) * s_keep
        if sp >= 0:
            out.append(P)
        if sp * sq < 0:
            t = side(P) / (side(P) - side(Q))
            out.append((P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t))
    return out


def centroid(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def inset_convex(pts, d):
    """Exact inward offset of a convex polygon (edges that collapse simply vanish)."""
    c = centroid(pts)
    out = list(pts)
    n = len(pts)
    for i in range(n):
        a = pts[i]; b = pts[(i + 1) % n]
        a2, b2 = par_line(a, b, d, c)
        # a point strictly on the inward side of the shifted line (independent of the centroid)
        ux, uy = unit(b[0] - a[0], b[1] - a[1])
        nx, ny = a2[0] - a[0], a2[1] - a[1]
        L = math.hypot(nx, ny) or 1.0
        keep = (a2[0] + nx / L * 1000.0, a2[1] + ny / L * 1000.0)
        out = clip_halfplane(out, a2, b2, keep)
        if len(out) < 3:
            return []
    # dedupe
    res = []
    for p in out:
        if not res or math.hypot(p[0] - res[-1][0], p[1] - res[-1][1]) > 1e-6:
            res.append(p)
    if len(res) > 1 and math.hypot(res[0][0] - res[-1][0], res[0][1] - res[-1][1]) < 1e-6:
        res.pop()
    return res


def bisector(pts, i):
    n = len(pts)
    p = pts[i]; a = pts[i - 1]; b = pts[(i + 1) % n]
    ua = unit(a[0] - p[0], a[1] - p[1]); ub = unit(b[0] - p[0], b[1] - p[1])
    bx, by = ua[0] + ub[0], ua[1] + ub[1]
    return unit(bx, by)


def seams_to(girdle, table):
    out = []
    for i, v in enumerate(girdle):
        bx, by = bisector(girdle, i)
        best, bd = None, 1e9
        for t in table:
            dx, dy = t[0] - v[0], t[1] - v[1]
            proj = dx * bx + dy * by
            if proj <= 0:
                continue
            perp = abs(dx * by - dy * bx)
            if perp < bd:
                bd, best = perp, t
        if best is not None:
            out.append((v, best))
    return out


def clip_corner(pts, idx, d1, d2=None):
    d2 = d1 if d2 is None else d2
    n = len(pts)
    p = pts[idx]; a = pts[idx - 1]; b = pts[(idx + 1) % n]
    ua = unit(a[0] - p[0], a[1] - p[1]); ub = unit(b[0] - p[0], b[1] - p[1])
    return pts[:idx] + [(p[0] + ua[0] * d1, p[1] + ua[1] * d1), (p[0] + ub[0] * d2, p[1] + ub[1] * d2)] + pts[idx + 1:]


def stone(pts, insets, seam, step_role='A', table_role='A', seam_ends=0.0):
    """Facet a convex girdle polygon into step rings + table."""
    rings = [pts]
    for s in insets:
        t = inset_convex(pts, s)
        if len(t) >= 3:
            rings.append(t)
    if len(rings) == 1:
        return [(poly(pts), step_role)], []
    lines = []
    for k in range(len(rings) - 1):
        for a, b in seams_to(rings[k], rings[k + 1]):
            lines.append(seg(a, b, seam_ends))
    lines += [polyline(R + [R[0]]) for R in rings[1:]]
    parts = []
    for k in range(len(rings) - 1):
        parts.append((cut(difference(poly(rings[k]), poly(rings[k + 1])), lines, seam), step_role))
    parts.append((cut(poly(rings[-1]), lines, seam), table_role))
    return parts, rings


def build(H=160.0, W=90.0, xv=None, tL=33.0, tR=9.5, chO=11.0, chI=2.5, chT=6.0, culet=6.0,
          insets=(6.5,), seam=1.8, top='h', thin_role='A', table_role='A', step_role='A', mitre=True,
          thin_top='h', facets=True):
    xv = W / 2 if xv is None else xv
    Vb = (xv, H)
    TLo, TRo = (0.0, 0.0), (W, 0.0)
    Li = par_line(TLo, Vb, tL, (xv, 0))
    Ri = par_line(TRo, Vb, tR, (xv, 0))
    crotch = isect(*Li, *Ri)
    # top cut lines
    if top == 'h':
        tl_a, tl_b = (0, 0), (1, 0)
    else:  # perpendicular to the broad stroke, through the inner top point at y=0
        ux, uy = unit(Vb[0] - TLo[0], Vb[1] - TLo[1])
        pin = isect(*Li, (0, 0), (1, 0))
        tl_a, tl_b = pin, (pin[0] - uy, pin[1] + ux)
    TLo2 = isect(TLo, Vb, tl_a, tl_b)
    TLi = isect(*Li, tl_a, tl_b)
    if thin_top == 'h':
        tr_a, tr_b = (0, 0), (1, 0)
    else:
        ux, uy = unit(Vb[0] - TRo[0], Vb[1] - TRo[1])
        pin = isect(*Ri, (0, 0), (1, 0))
        tr_a, tr_b = pin, (pin[0] - uy, pin[1] + ux)
    TRo2 = isect(TRo, Vb, tr_a, tr_b)
    TRi = isect(*Ri, tr_a, tr_b)
    yc = H - culet
    Lo_c = isect(TLo, Vb, (0, yc), (1, yc))
    Ro_c = isect(TRo, Vb, (0, yc), (1, yc))
    M_c = isect(crotch, Vb, (0, yc), (1, yc))  # mitre meets culet
    left = [TLo2, TLi, crotch, M_c, Lo_c]
    right = [TRi, TRo2, Ro_c, M_c, crotch]
    left = clip_corner(left, 0, chO)
    if chI > 0:
        left = clip_corner(left, 2, chI)
    if chT > 0:
        right = clip_corner(right, 1, chT)
    parts = []
    rings = []
    if facets:
        pl, rings = stone(left, insets, seam, step_role, table_role)
    else:
        pl = [(poly(left), step_role)]
    parts += pl
    parts.append((poly(right), thin_role))
    if mitre:
        m = seg(crotch, M_c, 1.0)
        parts = [(cut(p, [m], seam), r) for p, r in parts]
    geo = dict(left=left, right=right, crotch=crotch, Vb=Vb, rings=rings)
    return parts, geo
