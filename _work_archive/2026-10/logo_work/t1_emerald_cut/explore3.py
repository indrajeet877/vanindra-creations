"""Exploration round 3."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell, v_outline
from explore2 import rot

W, H, C = 90.0, 160.0, 18.0


def hall_incision(nb=3, band=8.5, gap=3.0, ch=6.0):
    """Concentric step bands (hall of mirrors) + table; a V channel incised from the top corners to the culet."""
    O = octagon(W, H, C)
    rings = []
    d = 0
    for k in range(nb):
        outer = offset_poly(O, d); inner = offset_poly(O, d + band)
        rings.append(difference(poly(outer), poly(inner)))
        d += band + gap
    rings.append(poly(offset_poly(O, d)))
    B = (W / 2, H)
    tl = lerp((0, C), (C, 0), 0.5)
    tr = lerp((W, C), (W - C, 0), 0.5)
    seams = [seg(tl, B, 6), seg(tr, B, 6)]
    return [(cut(r, seams, ch), 'A') for r in rings]


def tunnel_big(C2=30.0, Py=150.0, scales=(1.0, 0.72, 0.47, 0.25), mode='two'):
    O = octagon(W, H, C2)
    Pc = (W / 2, Py)
    rings = [scale_about(O, Pc, s) for s in scales]
    out = []
    for k in range(len(rings) - 1):
        R0, R1 = rings[k], rings[k + 1]
        for i in range(8):
            j = (i + 1) % 8
            f = poly([R0[i], R0[j], R1[j], R1[i]])
            out.append((f, 'A' if i in (1, 7) else 'B'))
    out.append((poly(rings[-1]), 'A'))
    seams = [seg(rings[0][i], rings[-1][i], 2) for i in range(8)] + [polyline(R + [R[0]]) for R in rings[1:]]
    res = [(cut(p, seams, 2.0), r) for p, r in out]
    if mode == 'vonly':
        res = [(p, r) for p, r in res if r == 'A']
    return res


def opened_pendant(theta=11.0, Wd=88.0, Hd=160.0, c=16.0, cb=None, inset=11.0, seam=2.0):
    cb = Wd / 2 if cb is None else cb
    # pendant girdle: clipped top corners, bottom brought to a point
    G = [(c, 0), (Wd - c, 0), (Wd, c), (Wd, Hd - cb), (Wd / 2, Hd), (0, Hd - cb), (0, c)]
    T = offset_poly(G, inset)
    facets = []
    for i in range(len(G)):
        j = (i + 1) % len(G)
        facets.append(([G[i], G[j], T[j], T[i]], 'A'))
    facets.append((T, 'B'))
    seams = [seg(G[i], T[i], 0.01) for i in range(len(G))] + [polyline(T + [T[0]])]
    piv = (Wd / 2, Hd)
    out = []
    for pts, role in facets:
        p = cut(poly(pts), seams, seam)
        for sgn in (-1, 1):
            half = poly([(-50, -50), (Wd / 2, -50), (Wd / 2, Hd + 50), (-50, Hd + 50)]) if sgn < 0 else \
                poly([(Wd / 2, -50), (Wd + 50, -50), (Wd + 50, Hd + 50), (Wd / 2, Hd + 50)])
            q = intersection(p, half)
            a = math.radians(theta) * sgn
            q = transform(q, math.cos(a), math.sin(a), -math.sin(a), math.cos(a),
                          piv[0] - piv[0] * math.cos(a) + piv[1] * math.sin(a),
                          piv[1] - piv[0] * math.sin(a) - piv[1] * math.cos(a))
            out.append((q, role))
    return out


def crystal_v(Wd=96, Hd=160, c=14, t=30, f=7, steps=(7, 14), seam=1.6):
    """Single-colour V-stone with genuine step faceting (two steps + table) and corner seams."""
    Vp = v_outline(Wd, Hd, c, t, f)
    rings = [Vp] + [offset_poly(Vp, s) for s in steps]
    allv = poly(Vp)
    seams = [seg(rings[0][i], rings[-1][i], 0.01) for i in range(len(Vp))]
    seams += [polyline(R + [R[0]]) for R in rings[1:]]
    return [(cut(allv, seams, seam), 'A')]


def notched(depth=0.62, inset=10.0, seam=2.0):
    """Emerald girdle with a V cut down into it; the step ring follows the cut."""
    B = (W / 2, H * depth)
    G = [(C, 0), (W / 2 - 14, 0), B, (W / 2 + 14, 0), (W - C, 0), (W, C), (W, H - C), (W - C, H), (C, H), (0, H - C), (0, C)]
    T = offset_poly(G, inset)
    facets = []
    for i in range(len(G)):
        j = (i + 1) % len(G)
        facets.append(([G[i], G[j], T[j], T[i]], 'A'))
    facets.append((T, 'B'))
    seams = [seg(G[i], T[i], 0.01) for i in range(len(G))] + [polyline(T + [T[0]])]
    return [(cut(poly(p), seams, seam), r) for p, r in facets]


def channel(chw=7.0, inset=7.0, seam=1.6):
    """Girdle cut into three stones by a V channel; each stone keeps one step and its own table."""
    B = (W / 2, H)
    A0 = lerp((0, C), (C, 0), 0.0)
    pieces = [
        [(0, C), (C, 0), (C + 2, 0), B, (C, H), (0, H - C)],
        [(C + 2, 0), (W - C - 2, 0), B],
        [(W - C - 2, 0), (W - C, 0), (W, C), (W, H - C), (W - C, H), B],
    ]
    # the V channel: thick strokes from top chamfer region to culet
    tl = (C * 0.55, C * 0.45)
    tr = (W - C * 0.55, C * 0.45)
    ch = [seg((C + 6, -2), B, 0), seg((W - C - 6, -2), B, 0)]
    out = []
    O = octagon(W, H, C)
    body = poly(O)
    pieces_p = [difference(body, union(*[stroke_to_path(s, chw) for s in ch]))]
    # split remaining into its components with step lines (inset outline drawn as seam)
    inner = offset_poly(O, inset)
    steps = [polyline(inner + [inner[0]])] + [seg(O[i], inner[i], 0.01) for i in range(8)]
    return [(cut(pieces_p[0], steps, seam), 'A')]


VARIANTS3 = [
    ('16_hall_incision', hall_incision),
    ('17_tunnel_bigchamfer', tunnel_big),
    ('18_tunnel_vonly', lambda: tunnel_big(mode='vonly')),
    ('19_opened_pendant', opened_pendant),
    ('20_crystal_v', crystal_v),
    ('21_notched', notched),
    ('22_channel', channel),
]

if __name__ == '__main__':
    for n, f in VARIANTS3:
        print(cell(n, f()))
