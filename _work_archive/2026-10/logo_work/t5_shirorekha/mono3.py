"""Final-logic monogram: straight wedge V (hairline at the headline, widening downward, pointed foot),
hairline return stroke into the danda, headline bar."""
import math
from geo import *

def va3(H=100, b=10, S=15, h=4.4, t0=4.5, px=37, py=101.6, yj=0.5, xs=62, qh=0.66, ovl=12, ovr=7,
        bindu=None, br=None, bgap=None, danda_top=0):
    P = (px, py)
    J = (xs, yj * H)
    dx, dy = J[0] - P[0], J[1] - P[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    if nx > 0: nx, ny = -nx, -ny
    Pi, Ji = (P[0] + nx * h, P[1] + ny * h), (J[0] + nx * h, J[1] + ny * h)
    J2 = (xs, line_x((Pi[1], Pi[0]), (Ji[1], Ji[0]), xs))
    yq = H * qh
    Q = (line_x(Pi, Ji, yq), yq)
    I0 = (t0 + b * px / py, b)
    x_top = line_x(I0, Q, 0)
    bowl = poly([(0, 0), (x_top, 0), Q, J2, (xs + 0.5, J2[1]), (xs + 0.5, J[1]), J, P])
    g = U(bowl, rect(xs, danda_top, xs + S, H), rect(-ovl, 0, xs + S + ovr, b))
    g = I(g, rect(-ovl - 1, min(0, danda_top), xs + S + ovr + 1, max(H, py)))
    info = dict(P=P, J=J, J2=J2, Q=Q, I0=I0, x_top=x_top, xs=xs, S=S, x0=-ovl, x1=xs + S + ovr, b=b, H=H)
    if bindu:
        r = br or S * 0.56
        gp = bgap if bgap is not None else b
        cx = xs + S / 2 if bindu == 'stem' else (-ovl + xs + S + ovr) / 2
        g = U(g, circle(cx, -gp - r, r))
    return g, info
