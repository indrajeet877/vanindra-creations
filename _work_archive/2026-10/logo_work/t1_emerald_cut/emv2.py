"""The Emerald Cut V, v2 - two step-cut stones forming a Didone V.

Grid: 9:16 box, W=90, H=160. The V's outer edges run from the box's top corners (inset ox) to the
culet on the axis. Broad stone tL, slender stone tR (perpendicular widths).
Each stone's outer top corner is cut at exactly 45 degrees (the emerald-cut girdle corner), the cut
sized in proportion to the stone (k * horizontal top width) so both stones share one cut ratio.
Optional inner-corner cut (ki), optional flat culet, hairline mitre seam between the stones.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from vgem2 import par_line, unit


def geom(W=90.0, H=160.0, ox=0.0, tL=30.0, tR=10.5, k=0.42, ki=0.0, culet=0.0, xv=None, clip=None):
    xv = W / 2 if xv is None else xv
    Vb = (xv, H)
    L0, R0 = (ox, 0.0), (W - ox, 0.0)
    Li = par_line(L0, Vb, tL, (xv, 0))
    Ri = par_line(R0, Vb, tR, (xv, 0))
    cr = isect(*Li, *Ri)
    TLi = isect(*Li, (0, 0), (1, 0))
    TRi = isect(*Ri, (0, 0), (1, 0))
    wl = TLi[0] - L0[0]
    wr = R0[0] - TRi[0]
    # 45-degree cuts: line x + y = L0x + a (left), x - y = R0x - a (right), a = k * top width
    aL, aR = (k * wl, k * wr) if clip is None else (clip, clip)
    cutL = ((L0[0] + aL, 0.0), (L0[0] + aL - 1.0, 1.0))
    cutR = ((R0[0] - aR, 0.0), (R0[0] - aR + 1.0, 1.0))
    pL = isect(*cutL, L0, Vb)
    pR = isect(*cutR, R0, Vb)
    left = [pL, (L0[0] + aL, 0.0), TLi, cr, Vb]
    right = [TRi, (R0[0] - aR, 0.0), pR, Vb, cr]
    if ki > 0:
        # inner top corner cut, also 45 deg (mirror sense)
        bl = ki * wl
        q1 = (TLi[0] - bl, 0.0)
        q2 = isect((TLi[0] - bl, 0.0), (TLi[0] - bl + 1, 1), *Li)
        left = [pL, (L0[0] + aL, 0.0), q1, q2, cr, Vb]
        br = ki * wr
        r1 = (TRi[0] + br, 0.0)
        r2 = isect((TRi[0] + br, 0.0), (TRi[0] + br - 1, 1), *Ri)
        right = [r2, r1, (R0[0] - aR, 0.0), pR, Vb, cr]
    V = union(poly(left), poly(right))
    if culet > 0:
        V = intersection(V, poly([(-50, -50), (W + 50, -50), (W + 50, H - culet), (-50, H - culet)]))
    return dict(W=W, H=H, V=V, left=left, right=right, cr=cr, Vb=Vb, TLi=TLi, TRi=TRi, pL=pL, pR=pR,
                L0=L0, R0=R0, aL=aL, aR=aR)


def build(seam=1.7, mitre=True, two_tone=False, gap_stones=None, seam_stop=0.0, seam_cap='butt', **kw):
    g = geom(**kw)
    if not mitre and not two_tone:
        return [(g['V'], 'A')], g
    stop = kw.get('seam_stop', 0.0) if False else seam_stop
    if stop > 0:
        t = (g['H'] - stop - g['cr'][1]) / (g['Vb'][1] - g['cr'][1])
        end = (g['cr'][0] + (g['Vb'][0] - g['cr'][0]) * t, g['H'] - stop)
        m = polyline([(g['cr'][0] - (g['Vb'][0] - g['cr'][0]) * 0.05, g['cr'][1] - (g['Vb'][1] - g['cr'][1]) * 0.05), end])
    else:
        # start the seam well inside the open counter so the counter flows into the hairline (no shelves)
        cx, cy = g['cr']; vx, vy = g['Vb']
        L = math.hypot(vx - cx, vy - cy)
        ux, uy = (vx - cx) / L, (vy - cy) / L
        m = polyline([(cx - ux * 20, cy - uy * 20), (vx + ux * 3, vy + uy * 3)])
    sw = gap_stones if gap_stones else seam
    L = intersection(g['V'], poly(g['left']))
    R = intersection(g['V'], poly(g['right']))
    if mitre:
        L = cut(L, [m], sw, seam_cap); R = cut(R, [m], sw, seam_cap)
    if two_tone:
        return [(L, 'A'), (R, 'B')], g
    return [(union(L, R), 'A')], g
