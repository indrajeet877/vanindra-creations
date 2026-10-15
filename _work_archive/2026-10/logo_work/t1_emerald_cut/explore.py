"""Round of >= 6 exploratory variations for The Emerald Cut. Writes explore/*.svg"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
os.makedirs(OUT, exist_ok=True)

W, H, C = 90.0, 160.0, 18.0
G = 2.6  # seam gap


def v1_wedge():
    """Five facets: V arms are the long corner facets from the top chamfers to the culet."""
    O = octagon(W, H, C)
    B = (W / 2, H)
    arms = [poly([(0, C), (C, 0), B]), poly([(W - C, 0), (W, C), B])]
    rest = [poly([(C, 0), (W - C, 0), B]), poly([(0, C), B, (C, H), (0, H - C)]),
            poly([(W, C), (W, H - C), (W - C, H), B])]
    seams = [seg((C, 0), B, 4), seg((0, C), B, 4), seg((W - C, 0), B, 4), seg((W, C), B, 4)]
    return [(cut(p, seams, G), 'A') for p in arms] + [(cut(p, seams, G), 'B') for p in rest]


def v2_split():
    """Three facets: the girdle split by two seams; V is the outer mass, table is the counter."""
    B = (W / 2, H)
    l = poly([(0, C), (C, 0), B, (C, H), (0, H - C)])
    r = poly([(W - C, 0), (W, C), (W, H - C), (W - C, H), B])
    t = poly([(C, 0), (W - C, 0), B])
    seams = [seg((C, 0), B, 4), seg((W - C, 0), B, 4)]
    return [(cut(l, seams, G), 'A'), (cut(r, seams, G), 'A'), (cut(t, seams, G), 'B')]


def v3_tunnel():
    """Step rings shrink toward a low centre; the top corner facets chain into a V."""
    O = octagon(W, H, C)
    Pc = (W / 2, 136)
    scales = [1.0, 0.76, 0.54, 0.34]
    rings = [scale_about(O, Pc, s) for s in scales]
    out = []
    seams = []
    for k in range(len(rings) - 1):
        R0, R1 = rings[k], rings[k + 1]
        for i in range(8):
            j = (i + 1) % 8
            f = poly([R0[i], R0[j], R1[j], R1[i]])
            role = 'A' if i in (1, 7) else 'B'
            out.append((f, role))
    for i in range(8):
        seams.append(seg(rings[0][i], rings[-1][i], 2))
    for R in rings[1:]:
        seams.append(polyline(R + [R[0]]))
    out.append((poly(rings[-1]), 'A'))
    return [(cut(p, seams, G * 0.8), r) for p, r in out]


def v4_didone():
    """Thick/thin V (Didone stress) cut from the girdle; table and side facets in gold."""
    xa, xb = 39.0, 51.0
    t1, t2 = 17.0, 5.5
    Lo = ((0, C), (xa, H))
    Ro = ((W, C), (xb, H))

    def par(line, d, side):
        (x1, y1), (x2, y2) = line
        L = math.hypot(x2 - x1, y2 - y1)
        nx, ny = (y2 - y1) / L * side, -(x2 - x1) / L * side
        return ((x1 + nx * d, y1 + ny * d), (x2 + nx * d, y2 + ny * d))
    Li = par(Lo, t1, -1)
    Ri = par(Ro, t2, 1)
    # make sure inner offsets point into the counter
    cr = isect(*Li, *Ri)
    xiL = isect(*Li, (0, 0), (1, 0))
    xiR = isect(*Ri, (0, 0), (1, 0))
    if xiL[0] < C:
        Li = par(Lo, t1, 1); cr = isect(*Li, *Ri); xiL = isect(*Li, (0, 0), (1, 0))
    if xiR[0] > W - C:
        Ri = par(Ro, t2, -1); cr = isect(*Li, *Ri); xiR = isect(*Ri, (0, 0), (1, 0))
    V = poly([(0, C), (C, 0), xiL, cr, xiR, (W - C, 0), (W, C), (xb, H), (xa, H)])
    tab = poly([xiL, xiR, cr])
    ls = poly([(0, C), (xa, H), (C, H), (0, H - C)])
    rs = poly([(W, C), (W, H - C), (W - C, H), (xb, H)])
    seams = [seg((0, C), (xa, H), 3), seg(xiL, cr, 3), seg(xiR, cr, 3), seg((W, C), (xb, H), 3)]
    return [(cut(V, seams, G), 'A'), (cut(tab, seams, G), 'B'), (cut(ls, seams, G), 'B'), (cut(rs, seams, G), 'B')]


def baguette(w, h, c, inset):
    O = octagon(w, h, c, -w / 2, -h)
    T = offset_poly(O, inset)
    return O, T


def v5_baguettes():
    """Two step-cut baguettes set as a V (jeweller's channel setting)."""
    w, h, c, ins = 24.0, 158.0, 6.0, 6.5
    O, T = baguette(w, h, c, ins)
    ang = math.radians(14.5)
    out = []
    for side in (-1, 1):
        a = -ang * side
        ca, sa = math.cos(a), math.sin(a)

        def tf(p):
            x, y = p
            return (W / 2 + side * 0 + x * ca - y * sa, H + x * sa + y * ca)
        Ot = [tf(p) for p in O]
        Tt = [tf(p) for p in T]
        ring = difference(poly(Ot), poly(Tt))
        seams = [seg(Ot[i], Tt[i], 0.5) for i in range(8)]
        ring = cut(ring, seams, 1.6)
        tab = poly(Tt)
        clip = poly([(-50, -50), (W / 2, -50), (W / 2, H + 50), (-50, H + 50)]) if side < 0 else \
            poly([(W / 2, -50), (W + 50, -50), (W + 50, H + 50), (W / 2, H + 50)])
        ring = intersection(ring, clip)
        tab = intersection(tab, clip)
        out += [(ring, 'A'), (cut(tab, [seg((W / 2, -50), (W / 2, H + 50))], 1.6), 'B')]
    return out


def v_outline(Wd, Hd, c, t, f):
    """V silhouette with emerald-cut clipped terminals. t = perpendicular arm width, f = half flat at base."""
    Lo = ((0, c), (Wd / 2 - f, Hd))
    (x1, y1), (x2, y2) = Lo
    L = math.hypot(x2 - x1, y2 - y1)
    nx, ny = (y2 - y1) / L, -(x2 - x1) / L  # points right/up of the downward line
    if nx < 0:
        nx, ny = -nx, -ny
    Li = ((x1 + nx * t, y1 + ny * t), (x2 + nx * t, y2 + ny * t))
    xi = isect(*Li, (0, 0), (1, 0))
    cr = isect(*Li, (Wd - Li[0][0], Li[0][1]), (Wd - Li[1][0], Li[1][1]))
    return [(0, c), (c, 0), xi, cr, (Wd - xi[0], 0), (Wd - c, 0), (Wd, c), (Wd / 2 + f, Hd), (Wd / 2 - f, Hd)]


def v7_stepped_v():
    """The V itself is the gemstone: a step-cut applied to a V girdle (rings + V-shaped table)."""
    Vp = v_outline(100, 150, 14, 30, 9)
    rings = [Vp, offset_poly(Vp, 6.5), offset_poly(Vp, 13)]
    out = []
    for k in range(2):
        out.append((difference(poly(rings[k]), poly(rings[k + 1])), 'A'))
    out.append((poly(rings[-1]), 'B'))
    seams = [seg(rings[0][i], rings[-1][i], 0.3) for i in range(len(Vp))]
    seams += [polyline(rings[1] + [rings[1][0]])]
    return [(cut(p, seams, 1.8), r) for p, r in out]


def v8_chevron_steps():
    """Pendant-cut girdle: concentric steps become nested V chevrons at the base."""
    Op = [(C, 0), (W - C, 0), (W, C), (W, H - 50), (W / 2, H), (0, H - 50), (0, C)]
    rings = [Op, offset_poly(Op, 9), offset_poly(Op, 18), offset_poly(Op, 27)]
    out = []
    for k in range(3):
        band = difference(poly(rings[k]), poly(rings[k + 1]))
        out.append((band, 'A' if k % 2 == 0 else 'B'))
    out.append((poly(rings[-1]), 'B'))
    seams = [seg(rings[0][i], rings[-1][i], 0.3) for i in range(len(Op))]
    return [(cut(p, seams, G), r) for p, r in out]


def v9_girdle_stepped_v():
    """Octagon girdle; V arms are stepped bands (two steps each) running from the top chamfers to the culet."""
    B = (W / 2, H)
    # arm defined by the chamfer endpoints converging on B, subdivided into 3 parallel-ish steps
    Ltop = [(0, C), (C, 0)]
    Rtop = [(W, C), (W - C, 0)]
    out = []
    seams = []
    for top, sgn in ((Ltop, -1), (Rtop, 1)):
        pts = [lerp(top[0], top[1], t) for t in (0, 1 / 3, 2 / 3, 1)]
        for k in range(3):
            out.append((poly([pts[k], pts[k + 1], B]), 'A' if k != 1 else 'A'))
        for p in pts:
            seams.append(seg(p, B, 4))
    out.append((poly([(C, 0), (W - C, 0), B]), 'B'))
    out.append((poly([(0, C), B, (C, H), (0, H - C)]), 'B'))
    out.append((poly([(W, C), (W, H - C), (W - C, H), B]), 'B'))
    return [(cut(p, seams, 1.7), r) for p, r in out]


def v10_corner_v():
    """Classic centred emerald cut (girdle, one step ring, table); the V is the ring's two upper corner
    facets run long + the two lower side facets, i.e. light path through the stone."""
    O = octagon(W, H, C)
    Tb = offset_poly(O, 14)
    out = []
    seams = []
    for i in range(8):
        j = (i + 1) % 8
        f = poly([O[i], O[j], Tb[j], Tb[i]])
        out.append((f, 'B'))
        seams.append(seg(O[i], Tb[i], 2))
    seams.append(polyline(Tb + [Tb[0]]))
    # table divided by the V
    B = (W / 2, Tb[4][1])
    tl, tr = Tb[0], Tb[1]
    out.append((poly([Tb[7], Tb[0], B]), 'A'))
    out.append((poly([Tb[1], Tb[2], B]), 'A'))
    out.append((poly([Tb[0], Tb[1], B]), 'B'))
    out.append((poly([Tb[7], B, Tb[5], Tb[6]]), 'B'))
    out.append((poly([Tb[2], Tb[3], Tb[4], B]), 'B'))
    for p in (Tb[7], Tb[0], Tb[1], Tb[2]):
        seams.append(seg(p, B, 2))
    return [(cut(p, seams, 2.0), r) for p, r in out]


VARIANTS = [
    ('01_wedge', v1_wedge), ('02_split', v2_split), ('03_tunnel', v3_tunnel), ('04_didone', v4_didone),
    ('05_baguettes', v5_baguettes), ('06_stepped_v', v7_stepped_v), ('07_chevron_steps', v8_chevron_steps),
    ('08_stepped_arms', v9_girdle_stepped_v), ('09_table_v', v10_corner_v),
]


def cell(name, parts):
    S = 500
    allp = union(*[p for p, _ in parts])
    s, tx, ty = fit(allp, (40, 40, 300, 420))
    body = ''
    for p, r in parts:
        body += pth_c(place(p, s, tx, ty), EM if r == 'A' else GO)
    # one-colour versions
    s2, tx2, ty2 = fit(allp, (350, 40, 130, 130))
    body += f'<rect x="350" y="190" width="130" height="130" fill="{EM}"/>'
    s3, tx3, ty3 = fit(allp, (350, 190, 130, 130), pad=12)
    for p, r in parts:
        body += pth_c(place(p, s2, tx2, ty2), EM)
        body += pth_c(place(p, s3, tx3, ty3), IV)
    # small sizes: 32 and 16 px (height) on ivory and emerald
    body += f'<rect x="350" y="340" width="130" height="140" fill="{EM}"/>'
    for (bx, by, sz, onem) in [(356, 345, 32, False), (400, 345, 16, False), (356, 400, 32, True), (400, 400, 16, True)]:
        sx, txx, tyy = fit(allp, (bx, by, sz, sz))
        if not onem:
            body += f'<rect x="{bx-2}" y="{by-2}" width="{sz+4}" height="{sz+4}" fill="{IV}"/>'
        for p, r in parts:
            col = (EM if r == 'A' else GO) if not onem else (IV if r == 'A' else GL)
            body += pth_c(place(p, sx, txx, tyy), col)
    svg = svg_doc(S, S, body, IV)
    fn = os.path.join(OUT, f'{name}.svg')
    open(fn, 'w').write(svg)
    return fn


if __name__ == '__main__':
    files = [cell(n, f()) for n, f in VARIANTS]
    print('\n'.join(files))
