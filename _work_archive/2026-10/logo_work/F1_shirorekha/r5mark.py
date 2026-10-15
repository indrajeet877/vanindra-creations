"""Round 3 finalist polish (F1): the va mark, loop redrawn as ONE stroke per contour.
Judges: the shoulder was a 15-unit knuckle (heavier than the 13-unit danda) and read as a Latin 'a' under a macron.
Now each contour of the loop is a single cubic: it leaves the danda horizontally, rounds through an open shoulder and
straightens into the arm that ends in the sharp point (G1 everywhere, no knuckle). The loop's weight is a leaf:
5.5 hairline where it leaves the danda, swelling to <= ~11 on the shoulder (always lighter than the 13 danda),
tapering into the point. The return stroke (the V's right arm) is unchanged. Units: line top y=0, baseline y=100."""
from r3geo import *

VL5 = dict(H=100, b=9.5, S=13.0, xs=58.0, ovl=3.0, ovr=3.0,
           jt=20.0, ht=5.5,
           P=(31.0, 95.0),
           arm=(-0.50, -1.0),        # direction the arm travels up from the point (normalised)
           o1=44.0, o2=58.0,         # outer handles: horizontal pull at the danda, pull along the arm at the point
           i1=38.0, i2=50.0,         # inner (counter) handles
           ioff=10.5,                # inner arm offset (perpendicular to the arm) at the point end of its handle
           yj=0.54, h=10.5)


def va5(**kw):
    p = dict(VL5); p.update(kw)
    H, b, S, xs, h = p['H'], p['b'], p['S'], p['xs'], p['h']
    P = p['P']
    ax, ay = p['arm']; L = math.hypot(ax, ay); ax, ay = ax / L, ay / L
    nx, ny = -ay, ax                       # normal pointing into the counter (right / up-right)
    T1 = (xs, p['jt'])
    o_c1 = (xs - p['o1'], T1[1])
    o_c2 = (P[0] + ax * p['o2'], P[1] + ay * p['o2'])
    Bj = (xs, p['jt'] + p['ht'])
    # inner contour: parallel arm, shifted into the counter by ioff, aimed at the point
    i_c1 = (xs - p['i1'], Bj[1])
    i_c2 = (P[0] + ax * p['i2'] + nx * p['ioff'], P[1] + ay * p['i2'] + ny * p['ioff'])
    J = (xs, p['yj'] * H)
    dx, dy = J[0] - P[0], J[1] - P[1]
    Lr = math.hypot(dx, dy)
    rnx, rny = dy / Lr, -dx / Lr
    Pi, Ji = (P[0] + rnx * h, P[1] + rny * h), (J[0] + rnx * h, J[1] + rny * h)
    J2 = (xs, line_y(Pi, Ji, xs))
    t = c_isect_line(Bj, i_c1, i_c2, P, Pi, Ji)
    (q0, q1, q2, Q), _ = csplit(Bj, i_c1, i_c2, P, t)
    shape = path_from([('M', *T1), ('C', *o_c1, *o_c2, *P), ('L', *J), ('L', xs + 1, J[1]), ('L', xs + 1, T1[1])])
    counter = path_from([('M', *Bj), ('C', *q1, *q2, *Q), ('L', *J2), ('L', xs + 1, J2[1]), ('L', xs + 1, Bj[1])])
    loop = D(shape, counter)
    xmin = c_extreme_x(T1, o_c1, o_c2, P)[0]
    xL = xmin - p['ovl']
    x1 = xs + S + p['ovr']
    g = U(loop, rect(xs, 0, xs + S, H), rect(xL, 0, x1, b))
    return g, dict(xL=xL, x1=x1, p=p, xmin=xmin, P=P, J=J, T1=T1, counter=counter,
                   outer=(T1, o_c1, o_c2, P), inner=(Bj, i_c1, i_c2, P), Q=Q)


def profile5(p):
    g, info = va5(**p)
    outer = [cpt(*info['outer'], i / 120) for i in range(121)]
    inner = [cpt(*info['inner'], i / 400) for i in range(401)]
    out = []
    for pt in outer[::8]:
        d = min(math.hypot(pt[0] - a[0], pt[1] - a[1]) for a in inner)
        out.append((round(pt[0]), round(pt[1]), round(d, 1)))
    return out
