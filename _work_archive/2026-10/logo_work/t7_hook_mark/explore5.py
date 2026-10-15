"""Loop tick: two straight arms on the 9:16 diagonals, joined below their crossing by an exact circular loop."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell

KAPPA = 0.5522847498


def arc_path(p, cx, cy, r, a0, a1, first=False):
    """Append circular arc (angles in radians, standard math orientation in y-down space: x=cx+r cos a, y=cy+r sin a)."""
    n = max(1, int(math.ceil(abs(a1 - a0) / (math.pi / 2))))
    da = (a1 - a0) / n
    for i in range(n):
        s, e = a0 + i * da, a0 + (i + 1) * da
        k = 4 / 3 * math.tan((e - s) / 4)
        x0, y0 = cx + r * math.cos(s), cy + r * math.sin(s)
        x3, y3 = cx + r * math.cos(e), cy + r * math.sin(e)
        x1, y1 = x0 - k * r * math.sin(s), y0 + k * r * math.cos(s)
        x2, y2 = x3 + k * r * math.sin(e), y3 - k * r * math.cos(e)
        if first and i == 0:
            p.moveTo(x0, y0)
        p.cubicTo(x1, y1, x2, y2, x3, y3)


def loop_centerline(H=560.0, half=math.atan(9 / 16), r=70.0, hr=9 / 16):
    """Centreline: short arm (top-left) down, around a circle, up the long arm (top-right).
    Arms are tangent to the circle; they cross above it (on the axis)."""
    # circle centre at (0, 0); arms are lines tangent to circle, symmetric about vertical axis, crossing at (0, -yc)
    # A line through (0,-yc) at angle `half` from vertical is at distance yc*sin(half) from the centre -> = r
    yc = r / math.sin(half)
    # tangent points: for the arm going up-right from the crossing (direction (sin, -cos)), continuing down-left below crossing
    # Left-going-down line (the long arm extended below the crossing) touches the circle on the left side.
    dLong = (math.sin(half), -math.cos(half))   # up-right
    dShort = (-math.sin(half), -math.cos(half))  # up-left
    X = (0.0, -yc)
    # tangent point of long-arm line: foot of perpendicular from centre
    def foot(d_):
        t = -(X[0] * d_[0] + X[1] * d_[1])
        return (X[0] + t * d_[0], X[1] + t * d_[1])
    tL = foot(dLong)     # lies on left-lower side
    tS = foot(dShort)    # lies on right-lower side
    top_y = -yc - H * 0.0
    long_top = isect(X, dLong, (0, -yc - H), (1, 0))
    short_top = isect(X, dShort, (0, -yc - H * hr), (1, 0))
    return X, tL, tS, long_top, short_top, yc


def loop_tick(H=560.0, r=70.0, w=40.0, gap=14.0, half=math.atan(9 / 16), hr=9 / 16, cap='butt'):
    X, tL, tS, long_top, short_top, yc = loop_centerline(H, half, r, hr)
    aS = math.atan2(tS[1], tS[0]); aL = math.atan2(tL[1], tL[0])
    # path: short_top -> tS (down the short arm), around the bottom of circle to tL, -> long_top
    # going from tS (right side) clockwise in screen?  tS is at lower right, tL lower left; go through the bottom (angle pi/2)
    short_line = pathops.Path(); short_line.moveTo(*short_top); short_line.lineTo(*tS)
    loop = pathops.Path()
    a0 = aS
    a1 = aL
    # ensure we pass through bottom (pi/2 in y-down) going increasing angle
    if a1 < a0:
        a1 += 2 * math.pi
    arc_path(loop, 0, 0, r, a0, a1, first=True)
    long_line = pathops.Path(); long_line.moveTo(*tL); long_line.lineTo(*long_top)
    sS = vt.stroke_to_path(short_line, w, cap='butt')
    sLoop = vt.stroke_to_path(loop, w, cap='butt')
    sLong = vt.stroke_to_path(long_line, w, cap='butt')
    under = U(sS, sLoop)
    # over/under at the crossing: long arm passes over; cut the short arm with dilated long arm near the crossing
    dil = vt.stroke_to_path(long_line, w + 2 * gap, cap='butt')
    near = rect(X[0] - 3 * w, X[1] - 3 * w, 6 * w, 6 * w)
    under = D(under, I(dil, near))
    # horizontal terminals: clip tops
    res = U(under, sLong)
    clipL = rect(-5000, long_top[1], 10000, 10000)
    res = I(res, U(rect(0, long_top[1], 5000, 10000), rect(-5000, short_top[1], 5000, 10000)))
    return [(res, EM)]


def L1(): return loop_tick(r=62, w=40, gap=13)
def L2(): return loop_tick(r=90, w=46, gap=15)
def L3(): return loop_tick(r=52, w=56, gap=16)
def L4(): return loop_tick(r=70, w=40, gap=13, half=math.radians(45), hr=0.5)
def L5(): return loop_tick(r=74, w=34, gap=12, hr=0.75)
def L6(): return loop_tick(r=60, w=48, gap=0)

V5 = [('L1_loop_916', L1), ('L2_loop_big', L2), ('L3_loop_heavy', L3), ('L4_loop_90deg', L4), ('L5_loop_tall_hook', L5), ('L6_loop_no_gap', L6)]
if __name__ == '__main__':
    for n, f in V5:
        print(cell(n, f()))
