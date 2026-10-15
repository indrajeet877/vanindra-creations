import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell

T = 9 / 16


def vee(H=560.0, Tw=118.0, tw=28.0, foot=0.0, hl=None, hr=None):
    """Contrast V: outer edges on the 9:16 diagonals meeting at the origin; left thick, right thin."""
    hl = H if hl is None else hl
    hr = H if hr is None else hr
    O = V(0, 0)
    cy = (Tw + tw) / (2 * T)
    crotch = V(Tw - T * cy, -cy)
    p = poly([O, V(T * hr, -hr), V(T * hr - tw, -hr), crotch, V(-T * hl + Tw, -hl), V(-T * hl, -hl)])
    if foot:
        p = I(p, rect(-5000, -5000, 10000, 5000 - foot / (2 * T)))
    return p


def cut_left(p, yc, gap):
    """Horizontal cut through the left arm only (x < 0 side) centred at height yc."""
    return D(p, rect(-5000, -yc - gap / 2, 5000 - 0.0 + 0, gap)) if False else D(p, rect(-5000, -yc - gap / 2, 5000 - 60, gap))


def X1():  # didone V, hairline cut at 9/16
    H = 560; p = vee(H, 118, 28, foot=20)
    return [(cut_left(p, H * 9 / 16, 12), EM)]


def X2():  # didone V, bolder gap, gold off-cut
    H = 560; p = vee(H, 118, 28, foot=20)
    below = I(p, rect(-5000, -H * 9 / 16 + 9, 10000, 5000))
    above = I(p, rect(-5000, -5000, 10000, 5000 - H * 9 / 16 - 9))
    left_above = I(above, rect(-5000, -5000, 5000 - 60, 10000))
    rest = U(below, D(above, left_above))
    return [(rest, EM), (left_above, GO)]


def X3():  # uniform Swiss V, cut
    H = 560; p = vee(H, 92, 92, foot=40)
    return [(cut_left(p, H * 9 / 16, 14), EM)]


def X4():  # tick proportion (right arm higher), off-cut floats above to complete the V height
    H = 560; p = vee(H, 118, 30, foot=20)
    return [(cut_left(p, H * 0.5, 22), EM)]


def X5():  # moderate contrast, cut at the 1/3 (the 3-second third), measured from top
    H = 560; p = vee(H, 126, 40, foot=26)
    return [(cut_left(p, H * 2 / 3, 12), EM)]


def X6():  # cut is a sliver that is perpendicular to the arm
    H = 560; p = vee(H, 118, 30, foot=20)
    import math
    yc = H * 9 / 16
    xc = -T * yc + 59
    ang = math.atan(T)
    d_ = (math.sin(ang) * -1, -math.cos(ang))  # along left arm going up-left
    n_ = (math.cos(ang), -math.sin(ang) * -1)
    band = poly([add(V(xc, -yc), mul(n_, -300)), add(V(xc, -yc), mul(n_, 300)), add(add(V(xc, -yc), mul(n_, 300)), mul(d_, 12)), add(add(V(xc, -yc), mul(n_, -300)), mul(d_, 12))])
    band = I(band, rect(-5000, -5000, 5000 - 60, 10000))
    return [(D(p, band), EM)]


V3 = [('X1_V_cut_didone', X1), ('X2_V_cut_gold_offcut', X2), ('X3_V_cut_uniform', X3), ('X4_V_cut_wide', X4), ('X5_V_cut_third', X5), ('X6_V_cut_perpendicular', X6)]
if __name__ == '__main__':
    for n, f in V3:
        print(cell(n, f()))
