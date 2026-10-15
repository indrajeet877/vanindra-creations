"""The Emerald Cut V - explicit facet construction.

Grid (units): girdle W x H = 90 x 160 (9:16), corner chamfer C (45 deg), one step ring at inset s.
Ring upper corner vertices: P = (s, C + s(sqrt2 - 1))   [ring side meets ring chamfer]
                            Q = (C + s(sqrt2 - 1), s)   [ring chamfer meets ring top]
Culet: Vb = (W/2, H).
V outer edges: Vb -> P_L and Vb -> P_R, extended until they meet the girdle chamfers (A_L, A_R),
so each terminal's outer corner is the girdle's own clipped corner.
Stroke widths: broad tL, hairline tR (Didone stress, thick stroke on the left).
Facet seams that fall inside the V: corner seam (C,0)->Q, ring chamfer Q->P, optional ring top line,
ring bottom line (culet facet), and the mitre between the two stones (crotch -> culet facet).
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from vgem2 import par_line, unit

R2 = math.sqrt(2) - 1


def geom(W=90.0, H=160.0, C=22.0, s=11.0, tL=30.0, tR=10.0, xv=None):
    xv = W / 2 if xv is None else xv
    Vb = (xv, H)
    PL, PR = (s, C + s * R2), (W - s, C + s * R2)
    QL, QR = (C + s * R2, s), (W - C - s * R2, s)
    G = octagon(W, H, C)
    Li = par_line(PL, Vb, tL, (xv, 0))
    Ri = par_line(PR, Vb, tR, (xv, 0))
    cr = isect(*Li, *Ri)
    TLi = isect(*Li, (0, 0), (1, 0))
    TRi = isect(*Ri, (0, 0), (1, 0))
    TLo = isect(PL, Vb, (0, 0), (1, 0))
    TRo = isect(PR, Vb, (0, 0), (1, 0))
    AL = isect(PL, Vb, (0, C), (C, 0))
    AR = isect(PR, Vb, (W, C), (W - C, 0))
    raw = [TLo, TLi, cr, TRi, TRo, Vb]
    V = intersection(poly(raw), poly(G))
    yb = H - s
    culL = isect(PL, Vb, (0, yb), (1, yb))
    culR = isect(PR, Vb, (0, yb), (1, yb))
    mitre_end = isect(cr, Vb, (0, yb), (1, yb))
    return dict(W=W, H=H, C=C, s=s, Vb=Vb, PL=PL, PR=PR, QL=QL, QR=QR, G=G, cr=cr, TLi=TLi, TRi=TRi,
                AL=AL, AR=AR, V=V, yb=yb, culL=culL, culR=culR, mitre_end=mitre_end, xv=xv, tL=tL, tR=tR)


def build(seam=1.8, ring_top=False, culet=True, mitre=True, gold_facets=False, solid=False, **kw):
    g = geom(**kw)
    W, H, C = g['W'], g['H'], g['C']
    if solid:
        return [(g['V'], 'A')], g
    lines = [seg((C, 0), g['QL'], 0.0), seg(g['QL'], g['PL'], 0.0),
             seg((W - C, 0), g['QR'], 0.0), seg(g['QR'], g['PR'], 0.0)]
    if ring_top:
        lines.append(seg(g['QL'], g['QR'], 0.0))
    if culet:
        lines.append(seg((g['culL'][0] - 2, g['yb']), (g['culR'][0] + 2, g['yb']), 0.0))
    if mitre:
        end = g['mitre_end'] if culet else g['Vb']
        lines.append(seg(g['cr'], end, 0.0))
    body = cut(g['V'], lines, seam)
    if not gold_facets:
        return [(body, 'A')], g
    # separate the corner facets and culet facet into the second colour
    cfL = poly([g['AL'], (C, 0), g['QL'], g['PL']])
    cfR = poly([g['AR'], g['PR'], g['QR'], (W - C, 0)])
    cul = poly([(g['culL'][0] - 5, g['yb']), (g['culR'][0] + 5, g['yb']), g['Vb']])
    facets = union(cfL, cfR, cul)
    return [(difference(body, facets), 'A'), (intersection(body, facets), 'B')], g


def construction(fn, scale=3.0, **kw):
    g = geom(**kw)
    parts, _ = build(**kw)
    W, H, C, s = g['W'], g['H'], g['C'], g['s']
    from vgem2 import inset_convex
    ring = inset_convex(g['G'], s)
    pad = 30
    tx, ty = pad, pad
    body = ''

    def L(a, b, col=GO, w=1.0, dash=None):
        A = (a[0] * scale + tx, a[1] * scale + ty); B = (b[0] * scale + tx, b[1] * scale + ty)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return f'<line x1="{A[0]:.2f}" y1="{A[1]:.2f}" x2="{B[0]:.2f}" y2="{B[1]:.2f}" stroke="{col}" stroke-width="{w}"{d}/>'
    # 9-unit grid
    for i in range(10):
        body += L((i * 10, -6), (i * 10, H + 6), '#d9cfb8', 0.6)
    for j in range(17):
        body += L((-6, j * 10), (W + 6, j * 10), '#d9cfb8', 0.6)
    Gp = transform(poly(g['G']), scale, 0, 0, scale, tx, ty)
    body += f'<path d="{fmt(to_d(Gp))}" fill="none" stroke="{GO}" stroke-width="1.2"/>'
    Rp = transform(poly(ring), scale, 0, 0, scale, tx, ty)
    body += f'<path d="{fmt(to_d(Rp))}" fill="none" stroke="{GO}" stroke-width="1"/>'
    # corner seams on all eight girdle vertices
    from vgem2 import seams_to
    for a, b in seams_to(g['G'], ring):
        body += L(a, b, GO, 1.0)
    # pavilion lines (V outer edges) extended to the culet, dashed
    body += L(g['AL'], g['Vb'], GO, 1.0, '4 3') + L(g['AR'], g['Vb'], GO, 1.0, '4 3')
    for p, r in parts:
        body += pth_c(transform(p, scale, 0, 0, scale, tx, ty), EM if r == 'A' else GO)
    w = W * scale + 2 * pad; h = H * scale + 2 * pad
    open(fn, 'w').write(svg_doc(w, h, body, IV))
