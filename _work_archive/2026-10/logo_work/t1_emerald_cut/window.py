"""'The Emerald Cut' - the V is a window cut from a true 9:16 emerald-cut facet diagram.

Grid: girdle 90 x 160 (9:16), clipped corners C. Step rings at insets s_k. Corner seams on bisectors.
The V: outer edges are pavilion lines from the girdle corners (0,C) and (W,C) to the culet (W/2,H);
broad stroke tL, hairline stroke tR (Didone stress); mitre from crotch to culet.
Everything drawn = (V silhouette) minus (facet lines of the gem that fall inside it).
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from vgem2 import par_line, unit, inset_convex, seams_to


def emerald_lines(W, H, C, steps, culet_seam=True):
    G = octagon(W, H, C)
    rings = [G] + [inset_convex(G, s) for s in steps]
    lines = []
    for k in range(len(rings) - 1):
        for a, b in seams_to(rings[k], rings[k + 1]):
            lines.append((a, b))
    for R in rings[1:]:
        for i in range(len(R)):
            lines.append((R[i], R[(i + 1) % len(R)]))
    return G, rings, lines


def v_shape(W, H, C, tL, tR, culet=0.0, xv=None, outer_from='corner'):
    xv = W / 2 if xv is None else xv
    Vb = (xv, H)
    if outer_from == 'corner':
        L0, R0 = (0.0, C), (W, C)
    elif isinstance(outer_from, tuple):  # ('ring', s): pass through the step ring's upper corner vertex
        s = outer_from[1]
        yr = C + s * (math.sqrt(2) - 1)
        L0, R0 = (s, yr), (W - s, yr)
    else:
        L0, R0 = (0.0, 0.0), (W, 0.0)
    Li = par_line(L0, Vb, tL, (xv, 0))
    Ri = par_line(R0, Vb, tR, (xv, 0))
    cr = isect(*Li, *Ri)
    top = ((0, 0), (1, 0))
    TLo = isect(L0, Vb, *top)  # extended outer edge meets y=0 (left of 0 -> clipped by girdle chamfer)
    TLi = isect(*Li, *top)
    TRi = isect(*Ri, *top)
    TRo = isect(R0, Vb, *top)
    # polygon of the V (before chamfer): we intersect with the girdle to get the clipped corners
    pts = [TLo, TLi, cr, TRi, TRo, Vb]
    return pts, dict(cr=cr, Vb=Vb, TLi=TLi, TRi=TRi, Li=Li, Ri=Ri, L0=L0, R0=R0)


def build(W=90.0, H=160.0, C=15.0, steps=(10.0,), tL=31.0, tR=9.0, seam=1.6, culet=0.0,
          mitre=True, outer_from='corner', show_lines=True, extra=None):
    G, rings, lines = emerald_lines(W, H, C, steps)
    vpts, k = v_shape(W, H, C, tL, tR, culet, outer_from=outer_from)
    V = intersection(poly(vpts), poly(G))
    if culet > 0:
        V = intersection(V, poly([(-10, -10), (W + 10, -10), (W + 10, H - culet), (-10, H - culet)]))
    cuts = []
    if show_lines:
        cuts += [seg(a, b, 0.0) for a, b in lines]
    if mitre:
        cuts.append(seg(k['cr'], k['Vb'], 2.0))
    if extra:
        cuts += extra(k)
    Vc = cut(V, cuts, seam)
    return [(Vc, 'A')], dict(G=G, rings=rings, lines=lines, k=k, V=V)


def construction_svg(fn, **kw):
    """Ghosted full gem diagram + the V window, for the presentation."""
    parts, g = build(**kw)
    s, tx, ty = fit(poly(g['G']), (60, 40, 380, 520))
    body = ''
    Gp = place(poly(g['G']), s, tx, ty)
    body += f'<path d="{fmt(to_d(Gp))}" fill="none" stroke="{GO}" stroke-width="1"/>'
    for a, b in g['lines']:
        A = (a[0] * s + tx, a[1] * s + ty); B = (b[0] * s + tx, b[1] * s + ty)
        body += f'<line x1="{A[0]:.2f}" y1="{A[1]:.2f}" x2="{B[0]:.2f}" y2="{B[1]:.2f}" stroke="{GO}" stroke-width="1"/>'
    for p, r in parts:
        body += pth_c(place(p, s, tx, ty), EM)
    open(fn, 'w').write(svg_doc(500, 600, body, IV))
