"""वनिंद्रा drawn in the Hinge system (TO BE VERIFIED BY THE TEAM / native readers before any use).

Same pen as the Latin:
  - dandas are stems; strokes falling to the right ( \\ ) are heavy, strokes rising to the right ( / ) and
    horizontals are light (the Latin V has the same logic: heavy left arm, hairline right arm);
  - the shirorekha is a light, level line; curves swell on their sides and thin at their tops;
  - every free stroke end is the same knife cut as the Latin a, r, s, C, t (no balls, no diamonds).
No font outlines are used. Tiro Devanagari Hindi was only measured for the anatomy (where each stroke
attaches); see loops/ref/tiro_grid.png.

Glyph order on the line:  व | ि (stem left of न, hook arching over न) | न | ं | द्र | ा
Coordinates: y-up, baseline 0, headline bottom = HB, headline top = HB + hl.
"""
import math
from glyphkit import B, rect, poly, ellipse, U, D, T, vt
from vitype import halfplane, expand


class DP:
    def __init__(s, **kw):
        s.HB = 560          # headline bottom (body height)
        s.hl = 40           # shirorekha thickness
        s.S = 80            # danda
        s.h = 30            # light strokes
        s.tw = 54           # knife-cut terminal thickness
        s.sh = 0.36         # knife-cut shear
        s.rise = 250        # i-matra rise above the headline top
        s.drop = 84         # how far द्र hangs below the baseline (was 150)
        s.__dict__.update(kw)


def danda(d, x, top=None, bottom=0.0):
    """vertical stem hanging from the headline; the foot is a knife cut rising to the right."""
    top = d.HB + 2 if top is None else top
    k = d.S * d.sh * 0.62
    return poly([(x, bottom - 6), (x + d.S, bottom - 6 + k), (x + d.S, top), (x, top)])


def g_va(d, x0):
    """व: a bowl hung on the left of the danda. Its upper stroke falls to the danda (heavy), its lower
    stroke rises to the danda (light); the counter is a teardrop pointing at the danda."""
    HB, S, h = d.HB, d.S, d.h
    w = 360
    xd = x0 + w; xL = x0
    yT = HB * 0.80                               # bowl top (outer)
    yB = HB * 0.22                               # bowl bottom (outer)
    thick = S * 1.02
    o = B().M(xd + 2, HB * 0.68)                 # upper stroke meets the danda (top edge)
    o.C(xd - w * 0.22, yT, xL + w * 0.66, yT, xL + w * 0.44, yT)
    o.C(xL + w * 0.16, yT, xL, HB * 0.66, xL, HB * 0.50)
    o.C(xL, HB * 0.32, xL + w * 0.20, yB, xL + w * 0.46, yB)
    o.C(xL + w * 0.70, yB, xd - w * 0.12, HB * 0.30, xd + 2, HB * 0.375)   # lower stroke meets the danda (bottom edge)
    o.Z()
    cy = HB * 0.47                               # counter point at the danda
    i = B().M(xd - 14, cy)
    i.C(xd - w * 0.22, HB * 0.62, xL + w * 0.62, yT - h, xL + w * 0.46, yT - h)
    i.C(xL + w * 0.30, yT - h, xL + thick, HB * 0.66, xL + thick, HB * 0.51)
    i.C(xL + thick, HB * 0.38, xL + thick + w * 0.08, yB + h, xL + w * 0.48, yB + h)
    i.C(xL + w * 0.66, yB + h, xd - w * 0.16, HB * 0.37, xd - 14, cy)
    i.Z()
    bowl = D(o.path(), i.path())
    return U(bowl, danda(d, xd)), xd + S


def g_i_matra(d, x0, land_x):
    """ि (F2): the stem rises through the headline, swells gently to the left and turns over the next letter in
    ONE smooth pen stroke (no kink), then falls to the right and LANDS on the headline over न's danda, the way
    the written i-sign does. Rising stroke light, the turn thin, the falling stroke heavier (Latin pen logic)."""
    HB, S, h, hl = d.HB, d.S, d.h, d.hl
    top = HB + hl
    R = top + d.rise                                   # height of the turn
    xc = x0 + S / 2                                    # stem centre line
    span = land_x - xc
    bl = S * 0.16                                      # how far the stroke swells to the left of the stem
    end = (land_x, top - 4)                            # lands into the headline
    segs = [
        ((xc, top - 8), (xc, top + d.rise * 0.22), (xc - bl, top + d.rise * 0.36), (xc - bl, top + d.rise * 0.62)),
        ((xc - bl, top + d.rise * 0.62), (xc - bl, R - d.rise * 0.20), (xc + span * 0.06, R), (xc + span * 0.36, R)),
        ((xc + span * 0.36, R), (xc + span * 0.70, R), (end[0] - span * 0.10, top + d.rise * 0.42), end),
    ]
    wf = _wcurve([(0.0, S * 1.0), (0.12, S * 0.92), (0.26, S * 0.74), (0.40, h * 1.55), (0.54, h * 1.30),
                  (0.74, S * 0.70), (0.90, S * 0.80), (1.0, S * 0.78)])
    hook = expand(segs, wf, 70)
    return U(danda(d, x0, top), hook)


def g_na(d, x0):
    """न: a light level stroke leaves the danda to the left; at its end a heavy stroke falls ( \\ ) and ends
    in a knife cut (the anatomy of the font's hanging lobe, drawn with the Latin pen)."""
    HB, S, h = d.HB, d.S, d.h
    w = 300
    xd = x0 + w
    ybt = HB * 0.66; ybb = ybt - h * 1.15
    tw = d.tw * 1.55
    To = (x0 + 52, HB * 0.30)                          # outer (left) end of the cut, low
    Ti = (To[0] + tw, To[1] + tw * d.sh)
    o = B().M(xd + 2, ybt)
    o.L(x0 + 90, ybt)
    o.C(x0 + 30, ybt, x0, ybt - 40, x0, HB * 0.53)
    o.C(x0, HB * 0.43, To[0] - 30, HB * 0.36, To[0], To[1])
    o.L(*Ti)
    o.C(Ti[0] + 4, HB * 0.40, x0 + S * 1.05, HB * 0.48, x0 + S * 1.05 + 20, ybb)
    o.L(xd + 2, ybb)
    o.Z()
    return U(o.path(), danda(d, xd)), xd + S, xd


def _wcurve(keys):
    """smooth width profile through (u, w) keys (Catmull-Rom in u)."""
    def wf(u, tx, ty):
        ks = [keys[0]] + keys + [keys[-1]]
        for i in range(1, len(ks) - 2):
            (u0, w0), (u1, w1), (u2, w2), (u3, w3) = ks[i - 1], ks[i], ks[i + 1], ks[i + 2]
            if u <= u2:
                t = (u - u1) / (u2 - u1) if u2 > u1 else 0
                m1 = (w2 - w0) / 2; m2 = (w3 - w1) / 2
                h00 = 2 * t ** 3 - 3 * t * t + 1; h10 = t ** 3 - 2 * t * t + t; h01 = -2 * t ** 3 + 3 * t * t; h11 = t ** 3 - t * t
                return h00 * w1 + h10 * m1 + h01 * w2 + h11 * m2
        return keys[-1][1]
    return wf


def g_dra(d, x0):
    """द्र: a danda-stub hangs from the headline; from its foot ONE pen stroke runs left (light), falls down
    the left side (heavy), turns along the bottom (light) and curls up under the stub into a solid drop
    (the font's lobe) whose point is the knife cut. From the drop's foot two strokes fall below the baseline:
    the द's own tail to the right ( \\ heavy) and the rakaar ्र to the left ( / light).
    -> (glyph, right edge of the stub, right edge of the tail)"""
    HB, S, h = d.HB, d.S, d.h
    xs0 = x0 + 214; xs1 = xs0 + S * 0.92
    ys = HB * 0.70
    L = x0 + S * 0.52                                # centre line of the bowl's left side
    yb = HB * 0.13                                   # centre line of the bowl's bottom
    segs = [
        ((xs0 + 30, ys + h * 0.7), (x0 + 150, ys + h * 0.7 + 4), (L, HB * 0.66), (L, HB * 0.45)),
        ((L, HB * 0.45), (L, HB * 0.24), (x0 + 100, yb), (x0 + 190, yb)),
        ((x0 + 190, yb), (x0 + 250, yb), (x0 + 286, HB * 0.17), (x0 + 300, HB * 0.24)),
    ]
    wf = _wcurve([(0.0, h * 1.5), (0.20, h * 1.9), (0.36, S * 1.0), (0.52, S * 0.7), (0.70, h * 1.15),
                  (0.86, h * 1.6), (1.0, h * 2.4)])
    bowl = expand(segs, wf, 70)
    # the drop: an egg under the stub, its long axis aimed up-left; the narrow end is knife-cut
    cx, cy = x0 + 300, HB * 0.31
    th = math.radians(132)
    ca, sa = math.cos(th), math.sin(th)
    egg = B()
    ra, rb_, rc = 96, 62, 56                      # half-length toward the point, toward the body, half-width
    pts = []
    for k in range(73):
        t = 2 * math.pi * k / 72
        u = math.cos(t); v = math.sin(t)
        along = (ra if u > 0 else rb_) * u
        across = rc * v * (1 - 0.22 * max(u, 0) ** 2)
        pts.append((cx + along * ca - across * sa, cy + along * sa + across * ca))
    knot = poly(pts)
    cut_c = (cx + (ra - 22) * ca, cy + (ra - 22) * sa)
    knot = D(knot, halfplane((cut_c[0] - 100, cut_c[1] - 100 * d.sh), (cut_c[0] + 100, cut_c[1] + 100 * d.sh), side=1))
    bowl = U(bowl, knot)
    stub = rect(xs0, ys, xs1, HB + 2)
    depth = d.drop
    cx, cy = x0 + 320, HB * 0.20
    # tail: heavy, falls to the right from the drop's foot
    wt = S * 0.74
    t0 = (cx + 14, cy + 20); t1 = (cx + 78, -depth)
    tail = poly([(t0[0] - wt * 0.5, t0[1]), (t0[0] + wt * 0.5, t0[1]), (t1[0] + wt * 0.5, t1[1]), (t1[0] - wt * 0.5, t1[1])])
    tail = D(tail, halfplane((t1[0] - 300, t1[1] - 300 * d.sh + 30), (t1[0] + 300, t1[1] + 300 * d.sh + 30), side=-1))
    # rakaar: light, falls to the left from the drop's foot
    wr = h * 1.3
    r0 = (cx - 6, cy + 10); r1 = (cx - 168, -depth + 16)
    rak = poly([(r0[0] - wr * 0.6, r0[1] + 30), (r0[0] + wr * 0.6, r0[1] + 30), (r1[0] + wr * 0.6, r1[1]), (r1[0] - wr * 0.6, r1[1])])
    rak = D(rak, halfplane((r1[0] - 300, r1[1] - 300 * d.sh + 20), (r1[0] + 300, r1[1] + 300 * d.sh + 20), side=-1))
    return U(stub, bowl, tail, rak), xs1, t1[0] + wt * 0.5


def headline(d, x0, x1):
    """the shirorekha; both ends are cut square (the Latin slabs end square too)."""
    return rect(x0, d.HB, x1, d.HB + d.hl)


def vanindra_deva(d=None):
    """-> dict(ink=<all but the i-matra and bindu>, i=<the i-matra>, bindu=<dot>, width)"""
    d = d or DP()
    x = 0
    va, x = g_va(d, x)
    x += 150
    xi = x; x += d.S + 120                     # i-matra stem, then न's left element
    na, na_end, xd_na = g_na(d, x)
    x = na_end
    land = xd_na - 6                            # the hook lands over न's danda
    im = g_i_matra(d, xi, land)
    bindu = ellipse(land + 104, d.HB + d.hl + d.rise * 0.58, d.S * 0.52, d.S * 0.52)
    x += 190
    dra, x, tail_r = g_dra(d, x)
    x = max(x + 220, tail_r + 70)
    aa = danda(d, x)
    x += d.S
    hl = headline(d, -30, x + 30)
    ink = U(va, na, dra, aa, hl)
    return dict(ink=ink, i=im, bindu=bindu, width=x, istem=xi + d.S / 2)
