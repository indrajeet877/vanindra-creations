import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')
R2 = math.sqrt(0.5)
DL = (R2, -R2)    # long arm direction: up-right 45deg
DS = (-R2, -R2)   # short arm direction: up-left 45deg
T916 = 9 / 16     # tan of half-opening when arms are 9:16 frame diagonals


def corner_L(k=36.0, w=90.0, S=9, L=16):
    """A: the 9:16 frame corner (90deg L, arms 9:16) turned 45deg -> a tick."""
    O = V(0, 0)
    P1 = add(O, mul(DL, L * k)); P2 = add(P1, mul(DS, w))
    Ic = add(O, add(mul(DL, w), mul(DS, w)))
    P5 = add(O, mul(DS, S * k)); P4 = add(P5, mul(DL, w))
    return [(poly([O, P1, P2, Ic, P4, P5]), EM)]


def didone(H=560.0, Tw=118.0, tw=20.0):
    """B: broad-nib tick: arms on 9:16 diagonals, thick short hook, hairline long hold."""
    t = T916; h = H * 9 / 16
    O = V(0, 0)
    up = lambda x0, y: V(x0, -y)
    # thin (long, right) stroke
    thin_out_top = V(t * H, -H); thin_in_top = V(t * H - tw, -H)
    thick_out_top = V(-t * h, -h); thick_in_top = V(-t * h + Tw, -h)
    cy = (Tw + tw) / (2 * t)
    crotch = V(Tw - t * cy, -cy)
    return [(poly([O, thin_out_top, thin_in_top, crotch, thick_in_top, thick_out_top]), EM)]


def miter_cut(k=36.0, w=92.0, g=9.0):
    """C: the corner as a mitred frame joint -> one vertical hairline through the vertex (the edit cut)."""
    base = corner_L(k, w)[0][0]
    slit = rect(-g / 2, -2000, g, 4000)
    return [(D(base, slit), EM)]


def wedges(H=560.0, Tw=150.0, tw=150.0):
    """D: two straight wedges meeting at one point: hook tapers in, hold widens out."""
    t = T916; h = H * 9 / 16
    O = V(0, 0)
    a = poly([O, V(-t * h, -h), V(-t * h + Tw, -h)])
    b = poly([O, V(t * H - tw * 0.02, -H), V(t * H - tw, -H)])
    b = poly([O, V(t * H + tw * 0.5, -H), V(t * H - tw * 0.5, -H)])
    return [(a, EM), (b, EM)]


def slab(k=40.0, gw=34.0):
    """E: a 9:16 slab split by a tick-shaped channel (the frame becomes the tick)."""
    W, Hh = 9 * k, 16 * k
    s = rect(0, 0, W, Hh)
    vx = V(W * 3 / 9, Hh * 13 / 16)
    left = V(-50, vx[1] - (vx[0] + 50))
    right_top = add(vx, mul(DL, 2000))
    chan = vt.stroke_to_path(poly([left, vx, right_top, (right_top[0] + 1, right_top[1])]), gw)
    # build channel as two slabs
    c1 = vt.stroke_to_path(_line(left, vx), gw, cap='square')
    c2 = vt.stroke_to_path(_line(vx, right_top), gw, cap='square')
    return [(D(s, U(c1, c2)), EM)]


def _line(a, b):
    p = pathops.Path(); p.moveTo(*a); p.lineTo(*b); return p


def fold(k=36.0, w=96.0):
    """F: a band folded once: short arm under, long arm over; fold triangle in gold."""
    O = V(0, 0)
    L, S = 16 * k, 9 * k
    long_r = poly([O, add(O, mul(DL, L)), add(add(O, mul(DL, L)), mul(DS, w)), add(O, mul(DS, w))])
    short_r = poly([O, add(O, mul(DS, S)), add(add(O, mul(DS, S)), mul(DL, w)), add(O, mul(DL, w))])
    sq = I(long_r, short_r)
    tri = poly([O, add(O, mul(DL, w)), add(O, mul(DS, w))])
    return [(D(U(long_r, short_r), tri), EM), (tri, GO)]


def three_beats(k=36.0, w=92.0, g=10.0):
    """G: the hook arm counted in three beats (1-2-3 s), then one unbroken hold."""
    base = corner_L(k, w)[0][0]
    # cuts perpendicular to the short arm at 1/3, 2/3 of its free length
    O = V(0, 0)
    out = base
    S = 9 * k
    for f in (0.45, 0.72):
        c = add(O, mul(DS, S * f + w * 0.0))
        cut = poly([add(c, mul(DL, -50)), add(c, mul(DL, 300)), add(add(c, mul(DL, 300)), mul(DS, g)), add(add(c, mul(DL, -50)), mul(DS, g))])
        out = D(out, cut)
    return [(out, EM)]


def leadin(H=520.0, sw=34.0):
    """I: the retention line: level start, one sharp hook, a long rising hold."""
    t = 0.62
    p0 = V(-360, -H * 0.62); p1 = V(-200, -H * 0.62); p2 = V(-30, 0); p3 = V(300, -H)
    p = pathops.Path(); p.moveTo(*p0); p.lineTo(*p1); p.lineTo(*p2); p.lineTo(*p3)
    return [(vt.stroke_to_path(p, sw, cap='butt', join='miter'), EM)]


VARIANTS = [
    ('A_corner_9x16', corner_L),
    ('B_broadnib_tick', didone),
    ('C_miter_cut', miter_cut),
    ('D_wedges', wedges),
    ('E_slab_channel', slab),
    ('F_fold', fold),
    ('G_three_beats', three_beats),
    ('I_retention_line', leadin),
]


def cell(name, layers):
    allp = U(*[p for p, _ in layers])
    x0, y0, x1, y1 = bbox(allp)
    body = ''
    _, s, tx, ty = fit(allp, (170, 170, 660, 660))
    for p, c in layers:
        body += pathel(tf(p, s, tx, ty), c)
    # mini previews (approx 16px and 32px when sheet cell renders ~490px wide)
    for size, ox in ((33, 760), (66, 840)):
        _, s2, tx2, ty2 = fit(allp, (ox, 920 - size, size, size))
        for p, c in layers:
            body += pathel(tf(p, s2, tx2, ty2), c)
    return write(os.path.join(OUT, name + '.svg'), 1000, 1000, body, bg=IV)


if __name__ == '__main__':
    files = [cell(n, f()) for n, f in VARIANTS]
    print('\n'.join(files))
