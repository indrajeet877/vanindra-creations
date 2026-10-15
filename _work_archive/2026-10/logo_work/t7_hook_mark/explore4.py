"""Hands: the tick as two watch hands (no dial)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell

def circle(cx, cy, r, n=0):
    k = 0.5522847498 * r
    p = pathops.Path()
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close()
    return p

def dirc(deg_cw_from_12):
    a = math.radians(deg_cw_from_12)
    return (math.sin(a), -math.cos(a))

def baton(angle, length, width, tail=0.0, point=False):
    d_ = dirc(angle); n_ = (-d_[1], d_[0])
    a = mul(d_, -tail); b = mul(d_, length)
    if point:
        tip = mul(d_, length + width * 0.9)
        return poly([add(a, mul(n_, -width / 2)), add(b, mul(n_, -width / 2)), tip, add(b, mul(n_, width / 2)), add(a, mul(n_, width / 2))])
    return poly([add(a, mul(n_, -width / 2)), add(b, mul(n_, -width / 2)), add(b, mul(n_, width / 2)), add(a, mul(n_, width / 2))])

def dauphine(angle, length, width, tail=0.0):
    d_ = dirc(angle); n_ = (-d_[1], d_[0])
    a = mul(d_, -tail); m = mul(d_, length * 0.18); b = mul(d_, length)
    return poly([a, add(m, mul(n_, -width / 2)), b, add(m, mul(n_, width / 2))])

HOUR = 300 + 10 / 2   # 10:10 -> 305 deg
MIN = 60.0

def H1():
    L = 520
    return [(U(baton(HOUR, L * 9 / 16, 64, tail=30), baton(MIN, L, 40, tail=60), circle(0, 0, 46)), EM)]

def H2():
    L = 520
    return [(U(baton(HOUR, L * 9 / 16, 70), baton(MIN, L, 70)), EM)]

def H3():
    L = 520
    return [(U(dauphine(HOUR, L * 9 / 16, 70, tail=40), dauphine(MIN, L, 56, tail=60), circle(0, 0, 30)), EM)]

def H4():  # 9:16 V angles, hub
    L = 560; a = math.degrees(math.atan(9 / 16))
    return [(U(baton(360 - a, L * 9 / 16, 62, tail=0), baton(a, L, 40, tail=0), circle(0, 0, 40)), EM)]

def H5():  # hands around an empty pivot (negative hub)
    L = 520
    hands = U(baton(HOUR, L * 9 / 16, 64, tail=0), baton(MIN, L, 44, tail=0), circle(0, 0, 70))
    return [(D(hands, circle(0, 0, 34)), EM)]

def H6():  # Max Bill thin batons, gold hub, tails
    L = 540
    return [(U(baton(HOUR, L * 9 / 16, 46, tail=40), baton(MIN, L, 26, tail=70)), EM), (circle(0, 0, 30), GO)]

V4 = [('H1_1010_baton_hub', H1), ('H2_1010_pure', H2), ('H3_1010_dauphine', H3), ('H4_916_hub', H4), ('H5_open_pivot', H5), ('H6_maxbill_goldhub', H6)]
if __name__ == '__main__':
    for n, f in V4:
        print(cell(n, f()))
