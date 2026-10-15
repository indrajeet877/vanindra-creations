"""Pythagoras: the 3-4-5 tick. Short stroke 3 (the hook) at slope 3/4, long stroke 4 at slope 4/3.
Squares on the strokes: 9 and 16. Vertex centred; tip heights 9:16."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell

u = (-0.8, -0.6)   # short arm direction (up-left)
v = (0.6, -0.8)    # long arm direction (up-right)
S = 100.0          # unit


def tick345(w=0.9, k=S, flat_tops=True, wl=None):
    """Uniform (or wl for long arm) right-angle tick, inner edges offset; terminals horizontal."""
    ws, wL = w * k, (wl if wl else w) * k
    O = V(0, 0)
    A = mul(u, 3 * k); B = mul(v, 4 * k)
    # outer edges through O along u and v; inner edges offset into the triangle interior
    ni_s = v  # interior normal for short arm
    ni_l = u
    inner = isect(mul(ni_s, ws), u, mul(ni_l, wL), v)
    if flat_tops:
        yA, yB = A[1], B[1]
        pA_out = isect(O, u, V(0, yA), (1, 0)); pA_in = isect(mul(ni_s, ws), u, V(0, yA), (1, 0))
        pB_out = isect(O, v, V(0, yB), (1, 0)); pB_in = isect(mul(ni_l, wL), v, V(0, yB), (1, 0))
        return poly([O, pB_out, pB_in, inner, pA_in, pA_out])
    return poly([O, B, add(B, mul(ni_l, wL)), inner, add(A, mul(ni_s, ws)), A])


def P1():
    return [(tick345(0.75), EM)]


def P2():  # Pythagoras squares (outward) -- the diagram itself
    O = V(0, 0); A = mul(u, 300); B = mul(v, 400)
    sq9 = poly([O, A, add(A, mul((-0.6, 0.8), 300)), mul((-0.6, 0.8), 300)])
    sq16 = poly([O, B, add(B, mul((0.8, 0.6), 400)), mul((0.8, 0.6), 400)])
    return [(sq9, GO), (sq16, EM)]


def lopsided(H=500.0, a=9, b=16, total=None, Tw=70, tw=70):
    total = total or H * 1.25
    k = total / (a + b)
    O = V(0, 0)
    L = V(-a * k, -H); R = V(b * k, -H)
    dl = norm(sub(L, O)); dr = norm(sub(R, O))
    # inner edges: horizontal offsets
    il = isect(V(Tw, 0), dl, V(-tw, 0), dr)
    pl_in = isect(V(Tw, 0), dl, V(0, -H), (1, 0)); pr_in = isect(V(-tw, 0), dr, V(0, -H), (1, 0))
    return poly([O, R, pr_in, il, pl_in, L])


def P3():
    return [(lopsided(Tw=78, tw=78), EM)]


def P4():
    return [(lopsided(Tw=110, tw=56), EM)]


def P5():  # two leaning 9:16 cards meeting at the vertex: hook card small, hold card large
    th = math.atan(9 / 16)
    def card(wd, ht, ang, side):
        # rectangle with bottom inner corner at origin, rotated by ang (side=-1 leans left, +1 right)
        if side < 0:
            pts = [(0, 0), (-wd, 0), (-wd, -ht), (0, -ht)]
        else:
            pts = [(0, 0), (wd, 0), (wd, -ht), (0, -ht)]
        c, s_ = math.cos(ang * side), math.sin(ang * side)
        return poly([(x * c - y * s_, x * s_ + y * c) for x, y in pts])
    a = card(9 * 16, 16 * 16, th, -1)
    b = card(9 * 28.4, 16 * 28.4, th, 1)
    return [(a, GO), (b, EM)]


def P6():  # 3-4-5 tick, stroke widths in 3:4 (the hold carries more), flat tops
    return [(tick345(0.6, wl=0.8), EM)]


V6 = [('P1_345_tick', P1), ('P2_pythagoras_squares', P2), ('P3_lopsided_V_916', P3), ('P4_lopsided_contrast', P4), ('P5_leaning_cards', P5), ('P6_345_widths_3to4', P6)]
if __name__ == '__main__':
    for n, f in V6:
        print(cell(n, f()))
