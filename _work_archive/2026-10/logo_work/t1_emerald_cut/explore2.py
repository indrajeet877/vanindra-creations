"""Exploration round 2: the opened emerald, baguette V, refined V-stone."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell, v_outline, OUT

W, H, C = 90.0, 160.0, 18.0


def rot(pts, c, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def emerald_facets(W, H, C, steps, seam):
    """Full step-cut: returns list of (polygon_pts, kind) with kind in 'step', 'table'.
    steps = list of cumulative insets."""
    rings = [octagon(W, H, C)] + [offset_poly(octagon(W, H, C), s) for s in steps]
    facets = []
    for k in range(len(rings) - 1):
        R0, R1 = rings[k], rings[k + 1]
        for i in range(8):
            j = (i + 1) % 8
            facets.append(([R0[i], R0[j], R1[j], R1[i]], f'step{k}', i))
    facets.append((rings[-1], 'table', -1))
    return facets, rings


def opened(theta_deg, steps=(13,), table_role='B', step_roles=('A', 'A', 'A'), seam=2.2, Wd=W, Hd=H, Cd=C, gapc=0.0):
    facets, rings = emerald_facets(Wd, Hd, Cd, steps, seam)
    seams = []
    for i in range(8):
        seams.append(seg(rings[0][i], rings[-1][i], 0.01))
    for R in rings[1:]:
        seams.append(polyline(R + [R[0]]))
    piv = (Wd / 2, Hd)
    half_l = poly([(-10, -10), (Wd / 2 - gapc, -10), (Wd / 2 - gapc, Hd + 10), (-10, Hd + 10)])
    half_r = poly([(Wd / 2 + gapc, -10), (Wd + 10, -10), (Wd + 10, Hd + 10), (Wd / 2 + gapc, Hd + 10)])
    out = []
    for pts, kind, i in facets:
        role = table_role if kind == 'table' else step_roles[int(kind[4:])]
        p = cut(poly(pts), seams, seam)
        for half, sgn in ((half_l, -1), (half_r, 1)):
            q = intersection(p, half)
            a = math.radians(theta_deg) * sgn
            q = transform(q, math.cos(a), math.sin(a), -math.sin(a), math.cos(a),
                          piv[0] - piv[0] * math.cos(a) + piv[1] * math.sin(a),
                          piv[1] - piv[0] * math.sin(a) - piv[1] * math.cos(a))
            out.append((q, role))
    return out


def baguette_v(w=26.0, c=6.5, ins=7.0, ang=13.0, seam=1.8):
    """Two step-cut baguettes, mitred on the axis like a jeweller's channel-set V."""
    Hd = 175.0
    O = octagon(w, Hd, c, -w / 2, -Hd)
    T = offset_poly(O, ins)
    out = []
    for sgn in (-1, 1):
        a = math.radians(ang) * sgn
        # rotate about bottom-centre so the bottom outer corner lands on the axis
        Ot = rot(O, (0, 0), a)
        Tt = rot(T, (0, 0), a)
        # shift so that the inner bottom corner sits on the axis x=0
        dx = -sgn * (w / 2) * math.cos(a) * 0.0
        Ot = [(x + W / 2 + dx, y + H) for x, y in Ot]
        Tt = [(x + W / 2 + dx, y + H) for x, y in Tt]
        seams = [seg(Ot[i], Tt[i], 0.01) for i in range(8)] + [polyline(Tt + [Tt[0]])]
        clip = poly([(-100, -100), (W / 2, -100), (W / 2, H + 100), (-100, H + 100)]) if sgn < 0 else \
            poly([(W / 2, -100), (W + 100, -100), (W + 100, H + 100), (W / 2, H + 100)])
        ring = intersection(cut(difference(poly(Ot), poly(Tt)), seams, seam), clip)
        tab = intersection(cut(poly(Tt), seams, seam), clip)
        out += [(ring, 'A'), (tab, 'B')]
    # mitre seam on the axis
    ax = [seg((W / 2, -100), (W / 2, H + 100))]
    return [(cut(p, ax, seam), r) for p, r in out]


def vstone(Wd=90, Hd=160, c=13, t=27, f=8, steps=(8,), seam=1.8, table_role='B'):
    Vp = v_outline(Wd, Hd, c, t, f)
    rings = [Vp] + [offset_poly(Vp, s) for s in steps]
    out = []
    for k in range(len(rings) - 1):
        out.append((difference(poly(rings[k]), poly(rings[k + 1])), 'A'))
    out.append((poly(rings[-1]), table_role))
    seams = [seg(rings[0][i], rings[-1][i], 0.01) for i in range(len(Vp))]
    seams += [polyline(R + [R[0]]) for R in rings[1:]]
    return [(cut(p, seams, seam), r) for p, r in out]


VARIANTS2 = [
    ('10_opened_9deg', lambda: opened(9)),
    ('11_opened_14deg', lambda: opened(14)),
    ('12_opened_20deg_2steps', lambda: opened(19, steps=(9, 18), step_roles=('A', 'A'))),
    ('13_opened_14_tableA_stepB', lambda: opened(14, steps=(12,), table_role='A', step_roles=('B',))),
    ('14_baguette_v', baguette_v),
    ('15_vstone_1step', vstone),
]

if __name__ == '__main__':
    for n, f in VARIANTS2:
        print(cell(n, f()))
