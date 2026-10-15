"""Exploration round 5: bevel-free renderings."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import explore
import vgem2
from vgem2 import inset_convex, clip_corner, par_line, unit

W, H, C = 90.0, 160.0, 18.0


def solid_stones(tL=33, tR=9.5, chO=11, chI=4, chT=6, seam=2.2):
    parts, g = vgem2.build(tL=tL, tR=tR, chO=chO, chI=chI, chT=chT, facets=False, seam=seam)
    return parts


def banded(tL=34, tR=7.0, nb=3, band=None, gap=2.4, chO=11, chI=3, chT=5):
    """Thick stroke = concentric equal bands (steps) wrapping the stone; thin stroke = one band."""
    parts, g = vgem2.build(tL=tL, tR=tR, chO=chO, chI=chI, chT=chT, facets=False, seam=gap)
    left = g['left']
    band = band if band else tR
    out = []
    d = 0.0
    rings = [left]
    while True:
        d += band + gap
        r = inset_convex(left, d)
        if len(r) < 3:
            break
        rings.append(r)
    # draw ring k as region between offset (k*(band+gap)) and that + band
    for k in range(len(rings)):
        outer = left if k == 0 else inset_convex(left, k * (band + gap))
        inner = inset_convex(left, k * (band + gap) + band)
        pg = poly(outer)
        if len(inner) >= 3:
            pg = difference(pg, poly(inner))
        out.append((pg, 'A'))
    # thin stroke from the build (already mitre-cut)
    m = seg(g['crotch'], (g['Vb'][0], H + 5), 1.0)
    out = [(cut(p, [m], gap), r) for p, r in out]
    out.append(parts[-1])
    return out


def culet_fan(tL=34, tR=9.5, chO=11, chI=3, chT=6, seam=1.8, nf=3):
    """Thick stroke faceted by seams radiating from the culet to the top end (like pavilion mains)."""
    parts, g = vgem2.build(tL=tL, tR=tR, chO=chO, chI=chI, chT=chT, facets=False, seam=seam)
    left = g['left']
    # left = [o1(on outer edge), o2(top), i1(top), i2(inner edge), crotch, M_c, Lo_c]
    cul = lerp(left[-1], left[-2], 0.5)
    tops = left[0:4]
    lines = [seg(cul, p, 0.0) for p in tops]
    lines += [seg(cul, lerp(left[1], left[2], 0.5), 0)]
    thick = cut(parts[0][0], lines, seam)
    return [(thick, 'A'), parts[-1]]


def notch_only(seam=2.0):
    B = (W / 2, H * 0.97)
    G = [(C, 0), (C + 2, 0), B, (W - C - 2, 0), (W - C, 0), (W, C), (W, H - C), (W - C, H), (C, H), (0, H - C), (0, C)]
    return [(poly(G), 'A')]


def gem_seams(seam=2.4, step=None):
    O = octagon(W, H, C)
    B = (W / 2, H)
    a = lerp((0, C), (C, 0), 0.5)
    b = lerp((W, C), (W - C, 0), 0.5)
    lines = [seg(a, B, 3), seg(b, B, 3)]
    if step:
        T = offset_poly(O, step)
        lines += [polyline(T + [T[0]])] + [seg(O[i], T[i], 0) for i in range(8)]
    return [(cut(poly(O), lines, seam), 'A')]


def v_plus_i(seam=2.4):
    """V whose hairline stroke leans on an emerald-cut I (a 9:16-style baguette)."""
    Iw, c = 24.0, 7.0
    Ix = W - Iw
    I = octagon(Iw, H, c, Ix, 0)
    # V: thick stroke from top-left to culet, hairline from culet up to the I's top-left chamfer
    Vb = (Ix - 12, H)
    tL = 30.0
    TLo = (0, 0)
    Li = par_line(TLo, Vb, tL, (Vb[0], 0))
    tip = (Ix, c)  # start of the I's clipped top-left corner
    Ri = par_line(tip, Vb, 7.5, (0, 0))
    cr = isect(*Li, *Ri)
    TLi = isect(*Li, (0, 0), (1, 0))
    thick = clip_corner([TLo, TLi, cr, Vb], 0, 10)
    thin = [tip, Vb, Ri[1], Ri[0]]
    out = [(poly(thick), 'A'), (poly(thin), 'A'), (poly(I), 'B')]
    return out


R5 = [
    ('29_solid_stones', solid_stones),
    ('30_banded_3', banded),
    ('31_banded_wide', lambda: banded(tL=38, tR=8.0, gap=2.6)),
    ('32_culet_fan', culet_fan),
    ('33_notch_only', notch_only),
    ('34_gem_seams', gem_seams),
    ('35_gem_seams_step', lambda: gem_seams(step=11)),
    ('36_v_plus_i', v_plus_i),
]

if __name__ == '__main__':
    for n, f in R5:
        print(explore.cell(n, f()))
