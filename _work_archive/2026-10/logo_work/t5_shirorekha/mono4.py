"""Two-stroke va: headline + danda + one sweeping blade from the headline's left into the danda.
The blade and the danda converge like the two arms of a V."""
import math
import pathops
from geo import *
from mono2 import qpt, qsplit, ctrl_left

def cubic_pt(p0, c1, c2, p1, t):
    mt = 1 - t
    return (mt**3*p0[0] + 3*mt*mt*t*c1[0] + 3*mt*t*t*c2[0] + t**3*p1[0],
            mt**3*p0[1] + 3*mt*mt*t*c1[1] + 3*mt*t*t*c2[1] + t**3*p1[1])

def va4(H=100, b=10, S=15, xs=60, yj=0.86, t0=4.0, wj=None, ovl=12, ovr=7,
        oc1=(0.10, 0.45), oc2=(0.55, 0.92), ic1=(0.30, 0.40), ic2=(0.75, 0.70), bindu=None, br=None, bgap=None,
        straight=False):
    """Blade outer edge: cubic from (0,0) to J=(xs, yj*H) with controls given as fractions of (xs, H).
    Inner edge: cubic from (t0', b) to Ji=(xs, yj*H - wj) (wj = blade thickness where it meets the danda)."""
    wj = wj if wj is not None else S * 1.6
    J = (xs, yj * H)
    Ji = (xs, yj * H - wj)
    O0 = (0.0, 0.0)
    I0 = (t0 + b * 0.25, b)
    p = pathops.Path()
    p.moveTo(*O0)
    if straight:
        p.lineTo(*J)
        p.lineTo(xs + 0.5, J[1])
        p.lineTo(xs + 0.5, Ji[1])
        p.lineTo(*Ji)
        p.lineTo(*I0)
    else:
        c1 = (oc1[0] * xs, oc1[1] * H); c2 = (oc2[0] * xs, oc2[1] * H)
        p.cubicTo(*c1, *c2, *J)
        p.lineTo(xs + 0.5, J[1])
        p.lineTo(xs + 0.5, Ji[1])
        p.lineTo(*Ji)
        d1 = (ic2[0] * xs, ic2[1] * H); d2 = (ic1[0] * xs, ic1[1] * H)
        p.cubicTo(*d1, *d2, *I0)
    p.lineTo(I0[0], 0)
    p.close()
    blade = U(p)
    g = U(blade, rect(xs, 0, xs + S, H), rect(-ovl, 0, xs + S + ovr, b))
    g = I(g, rect(-ovl - 1, 0, xs + S + ovr + 1, H))
    if bindu:
        r = br or S * 0.56
        gp = bgap if bgap is not None else b
        cx = xs + S / 2 if bindu == 'stem' else (-ovl + xs + S + ovr) / 2
        g = U(g, circle(cx, -gp - r, r))
    return g, dict(xs=xs, S=S, x0=-ovl, x1=xs + S + ovr, J=J)
