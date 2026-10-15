import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell, _line

T = 9 / 16  # arms run on the diagonals of a 9:16 frame


def nib(H=560.0, Tw=118.0, tw=30.0, foot=0.0, hratio=9 / 16):
    """Broad-nib tick. Vertex (outer edges meet) at origin, y up = negative."""
    h = H * hratio
    O = V(0, 0)
    thin_out_top = V(T * H, -H); thin_in_top = V(T * H - tw, -H)
    thick_out_top = V(-T * h, -h); thick_in_top = V(-T * h + Tw, -h)
    cy = (Tw + tw) / (2 * T)
    crotch = V(Tw - T * cy, -cy)
    p = poly([O, thin_out_top, thin_in_top, crotch, thick_in_top, thick_out_top])
    if foot > 0:
        fy = foot / (2 * T)
        p = I(p, rect(-5000, -5000, 10000, 5000 - fy))
    return p, dict(h=h, H=H, Tw=Tw, tw=tw, crotch=crotch)


def B1():
    p, _ = nib(Tw=120, tw=38, foot=26)
    return [(p, EM)]


def B2():
    p, _ = nib(Tw=132, tw=16, foot=14)
    return [(p, EM)]


def M1(g=12):
    """Stencil: one vertical cut from the foot to the crotch (the edit point)."""
    p, m = nib(Tw=124, tw=34, foot=24)
    return [(D(p, rect(-g / 2, -2000, g, 4000)), EM)]


def M2(g=12):
    """Lean cut: the hold line runs unbroken; the heavy hook leans on it across a hairline."""
    H, Tw, tw = 560.0, 124.0, 34.0
    p, m = nib(H=H, Tw=Tw, tw=tw, foot=0)
    # thin stroke band (parallelogram), full length
    thin = poly([V(0, 0), V(T * H, -H), V(T * H - tw, -H), V(-tw, 0)])
    thin = I(thin, rect(-5000, -5000, 10000, 5000))
    # hook = everything left of the thin stroke's inner edge minus gap
    a = V(-tw - g, 0); b = V(T * H - tw - g, -H)
    left_half = poly([a, add(a, mul(sub(b, a), 4)), V(-3000, -3000), V(-3000, 1000), add(a, mul(sub(a, b), 4))])
    hook = I(p, left_half)
    return [(hook, EM), (thin, EM)]


def M3(g=12):
    """Two-tone stencil: gold hook, emerald hold."""
    p, m = nib(Tw=124, tw=34, foot=24)
    L = I(p, rect(-3000, -3000, 3000 - g / 2, 6000))
    R = I(p, rect(g / 2, -3000, 3000, 6000))
    return [(L, GO), (R, EM)]


def K(u=40.0, w=78.0):
    """Natural tick: short arm on the 16:9 diagonal, long arm on the 9:16 diagonal (perpendicular)."""
    n = math.hypot(9, 16)
    dL = (9 / n, -16 / n); dS = (-16 / n, -9 / n)
    O = V(0, 0)
    nL = (16 / n, 9 / n)    # normal pointing inward-left of long arm? compute inner offset directions
    # inner offset of long arm: towards upper-left = perpendicular to dL rotated toward dS
    offL = (-dL[1] * -1, dL[0] * -1)
    offL = (-16 / n, -9 / n)  # = dS
    offS = (9 / n, -16 / n)   # = dL
    Hl = 16 * u * 16 / n; Hs = 9 * u * 9 / n
    # outer edges
    pL = isect(O, dL, V(0, -Hl), (1, 0))
    pS = isect(O, dS, V(0, -Hs), (1, 0))
    iL0 = add(O, mul(offL, w)); iS0 = add(O, mul(offS, w))
    inner = isect(iL0, dL, iS0, dS)
    qL = isect(iL0, dL, V(0, -Hl), (1, 0))
    qS = isect(iS0, dS, V(0, -Hs), (1, 0))
    return [(poly([O, pL, qL, inner, qS, pS]), EM)]


def N(H=560.0, w=70.0, tail=70.0, g=14.0):
    """Crossed tick: the two strokes overrun the turn; the hold passes over the hook."""
    def band(p0, p1, w):
        dd = norm(sub(p1, p0)); n_ = perp(dd)
        return poly([add(p0, mul(n_, -w / 2)), add(p1, mul(n_, -w / 2)), add(p1, mul(n_, w / 2)), add(p0, mul(n_, w / 2))])
    vx = V(0, 0)
    h = H * 9 / 16
    dl = norm((T, -1)); ds = norm((-T, -1))
    long_ = band(add(vx, mul(dl, -tail)), add(vx, mul(dl, H / math.cos(math.atan(T)))), w)
    short = band(add(vx, mul(ds, -tail)), add(vx, mul(ds, h / math.cos(math.atan(T)))), w)
    gapband = band(add(vx, mul(dl, -tail - 50)), add(vx, mul(dl, H)), w + 2 * g)
    clip = rect(-5000, -5000, 10000, 5000 + 0)
    short = D(short, gapband)
    return [(short, EM), (long_, EM)]


def P():
    """Inverse contrast: a hairline hook, a heavy hold (the retention carries the weight)."""
    H, Tw, tw = 560.0, 132.0, 22.0
    h = H * 9 / 16
    O = V(0, 0)
    # thick = long right arm, thin = short left arm
    long_out = V(T * H, -H); long_in = V(T * H - Tw, -H)
    short_out = V(-T * h, -h); short_in = V(-T * h + tw, -h)
    cy = (Tw + tw) / (2 * T)
    crotch = V(tw - T * cy, -cy)
    p = poly([O, long_out, long_in, crotch, short_in, short_out])
    return [(p, EM)]


VARIANTS2 = [('J_nib_moderate', B1), ('J_nib_high', B2), ('M1_nib_stencil_cut', M1), ('M2_nib_lean_cut', M2),
             ('M3_nib_two_tone', M3), ('K_landscape_portrait', K), ('N_crossed_overunder', N), ('P_inverse_contrast', P)]

if __name__ == '__main__':
    for n, f in VARIANTS2:
        print(cell(n, f()))
