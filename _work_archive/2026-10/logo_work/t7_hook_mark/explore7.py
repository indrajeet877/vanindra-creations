import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell
from explore4 import baton, dauphine, circle, HOUR, MIN

T = 9 / 16


def uvee(H=560.0, w=90.0, foot=None):
    """Uniform-weight V on the 9:16 diagonals. w = horizontal stroke width. Flat foot = w (optically)."""
    foot = w * 0.9 if foot is None else foot
    O = V(0, 0)
    cy = (w + w) / (2 * T)
    crotch = V(w - T * cy, -cy)
    p = poly([O, V(T * H, -H), V(T * H - w, -H), crotch, V(-T * H + w, -H), V(-T * H, -H)])
    # outer edges meet at O; flat foot
    return I(p, rect(-5000, -5000, 10000, 5000 - foot / (2 * T)))


def split_left(p, yc, gap, xmax=-1.0):
    below = I(p, rect(-5000, -yc + gap / 2, 10000, 10000))
    above = I(p, rect(-5000, -5000, 10000, 5000 - yc - gap / 2))
    off = I(above, rect(-5000, -5000, 5000 + xmax, 10000))
    rest = U(below, D(above, off))
    return rest, off


def C1():
    H = 560; p = uvee(H, 92); r, o = split_left(p, H * 9 / 16, 16)
    return [(r, EM), (o, EM)]

def C2():
    H = 560; p = uvee(H, 92); r, o = split_left(p, H * 9 / 16, 16)
    return [(r, EM), (o, GO)]

def C3():  # off-cut slid along the cut (jump cut)
    H = 560; p = uvee(H, 92); r, o = split_left(p, H * 9 / 16, 16)
    return [(r, EM), (vt.transform(o, 1, 0, 0, 1, -26, 0), EM)]

def C4():  # medium weight, gold off-cut
    H = 560; p = uvee(H, 70); r, o = split_left(p, H * 9 / 16, 14)
    return [(r, EM), (o, GO)]

def C5():  # heavier, cut at 1/2
    H = 560; p = uvee(H, 112); r, o = split_left(p, H * 0.5, 18)
    return [(r, EM), (o, GO)]

def C6():  # off-cut lifted (gap grows upward), mono
    H = 560; p = uvee(H, 92); r, o = split_left(p, H * 9 / 16, 16)
    return [(r, EM), (vt.transform(o, 1, 0, 0, 1, 0, -22), EM)]

def W1():  # compact 10:10 hands: dauphine hour + baton minute, hub knocked out
    L = 420
    hands = U(dauphine(HOUR, L * 9 / 16, 92, tail=0), dauphine(MIN, L, 70, tail=0), circle(0, 0, 44))
    return [(D(hands, circle(0, 0, 16)), EM)]

V7 = [('C1_swiss_cutV_mono', C1), ('C2_swiss_cutV_gold', C2), ('C3_swiss_cutV_jumpcut', C3), ('C4_swiss_cutV_medium', C4), ('C5_swiss_cutV_heavy_half', C5), ('C6_swiss_cutV_lifted', C6), ('W1_1010_compact', W1)]
if __name__ == '__main__':
    for n, f in V7:
        print(cell(n, f()))
