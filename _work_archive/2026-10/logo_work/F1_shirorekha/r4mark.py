"""Round 3 final-final: the va mark with a V silhouette.
The loop hangs from the danda (as in type: व's bowl is closed by its own stroke, never by the line).
New in this pass: the outer contour is drawn as a V arm - a round shoulder under the line, then a near-straight
left arm down to a sharp point that drops below the bowl. The return stroke is the V's right arm. So the V is now
both the counter AND the silhouette. Units: line top y=0, baseline y=100."""
from r3geo import *

VLOOP = dict(H=100, b=9.5, S=13.0, xs=58.0, ovl=3.0, ovr=3.0,
             jt=20.0, ht=5.5,          # loop leaves the danda at y=jt; its top stroke is ht thick at the danda
             K=(4.0, 40.0),            # outer shoulder: leftmost point (vertical tangent)
             ks=(30.0, 12.0),          # shoulder handles: (horizontal pull from the danda, vertical pull above K)
             P=(31.0, 99.0),           # the V point
             karm=(10.0, 0.0),         # outer arm handles: (down from K, bow of the arm, + = outward/left)
             Ki=(16.0, 42.0),          # inner (counter) shoulder
             kis=(24.0, 9.0),
             kiarm=(8.0, 0.0),
             yj=0.55, h=10.0)          # return stroke (the V's right arm) meets the danda at yj*H, thickness h


def _arm(K, P, kdown, bow):
    """Cubic from K (vertical tangent) to P, near straight; bow pushes the middle outward (screen-left)."""
    dx, dy = P[0] - K[0], P[1] - K[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L                     # screen-left normal of a downward chord
    c1 = (K[0], K[1] + kdown)
    c2 = (K[0] + dx * 0.62 + nx * bow, K[1] + dy * 0.62 + ny * bow)
    return c1, c2


def va_vloop(**kw):
    p = dict(VLOOP); p.update(kw)
    H, b, S, xs, h = p['H'], p['b'], p['S'], p['xs'], p['h']
    T1 = (xs, p['jt'])
    K, P = p['K'], p['P']
    # outer: shoulder then arm
    s1 = (xs - p['ks'][0], T1[1])
    s2 = (K[0], K[1] - p['ks'][1])
    a1, a2 = _arm(K, P, p['karm'][0], p['karm'][1])
    Bj = (xs, p['jt'] + p['ht'])
    Ki = p['Ki']
    i1 = (xs - p['kis'][0], Bj[1])
    i2 = (Ki[0], Ki[1] - p['kis'][1])
    b1, b2 = _arm(Ki, P, p['kiarm'][0], p['kiarm'][1])
    J = (xs, p['yj'] * H)
    dx, dy = J[0] - P[0], J[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    Pi, Ji = (P[0] + nx * h, P[1] + ny * h), (J[0] + nx * h, J[1] + ny * h)
    J2 = (xs, line_y(Pi, Ji, xs))
    t = c_isect_line(Ki, b1, b2, P, Pi, Ji)
    (q0, q1, q2, Q), _ = csplit(Ki, b1, b2, P, t)
    shape = path_from([('M', *T1), ('C', *s1, *s2, *K), ('C', *a1, *a2, *P), ('L', *J), ('L', xs + 1, J[1]),
                       ('L', xs + 1, T1[1])])
    counter = path_from([('M', *Bj), ('C', *i1, *i2, *Ki), ('C', *q1, *q2, *Q), ('L', *J2), ('L', xs + 1, J2[1]),
                         ('L', xs + 1, Bj[1])])
    loop = D(shape, counter)
    xmin = min(K[0], c_extreme_x(T1, s1, s2, K)[0])
    xL = xmin - p['ovl']
    x1 = xs + S + p['ovr']
    g = U(loop, rect(xs, 0, xs + S, H), rect(xL, 0, x1, b))
    return g, dict(xL=xL, x1=x1, p=p, xmin=xmin, P=P, J=J, T1=T1, counter=counter)
