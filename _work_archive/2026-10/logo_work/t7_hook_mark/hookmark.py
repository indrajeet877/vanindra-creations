"""HOOK + TICK — parametric construction (all straight lines, exact intersections).

Grid: cap height H = 1000, baseline y = 0, SVG y-down (top of V at y = -H).
Outer edges of the V run on the diagonals of a 9:16 frame: x = +/- t*Y with t = tan(a) (default 9/16).
Both arms have the same perpendicular stroke p (Swiss, monoline). Horizontal width w = p / cos(a).
The vertex is a sharp point that overshoots the baseline by `over` (optical).
ONE horizontal cut crosses the LEFT arm only, centred at Y = cut*H, of height g:
  above the cut  -> the HOOK  (gold)   : the first thing the eye reads (top-left)
  below the cut  -> the TICK  (emerald): short stroke 9, long stroke 16
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *


def hook_tick(H=1000.0, t=9 / 16, p=135.0, cut=9 / 16, g=26.0, over=14.0, foot=0.0, hook_extra=0.0):
    a = math.atan(t)
    w = p / math.cos(a)                 # horizontal stroke width
    O = V(0, over)                      # sharp vertex, overshooting the baseline
    top = -H
    Ltop_out = V(-t * (H + over), top); Ltop_in = V(-t * (H + over) + w, top)
    Rtop_out = V(t * (H + over), top);  Rtop_in = V(t * (H + over) - w, top)
    # inner crotch = intersection of the two inner edges
    crotch = isect(Ltop_in, (t, 1), Rtop_in, (-t, 1))
    v = poly([O, Rtop_out, Rtop_in, crotch, Ltop_in, Ltop_out])
    if foot > 0:
        v = I(v, rect(-5000, -5000, 10000, 5000 + over - foot / (2 * t)))
    yc = -cut * H
    band = rect(-5000, yc - g / 2, 5000 - 0.0, g)  # x < 0 only (left arm lives at x<crotch.x there)
    # make sure the band only touches the left arm: limit its right edge to the crotch axis
    band = I(band, rect(-5000, -5000, 5000 + crotch[0] * 0 + 0.0, 10000))
    vv = D(v, band)
    hook = I(vv, rect(-5000, -5000, 5000, 5000 + yc - g / 2))
    hook = I(hook, rect(-5000, -5000, 5000, 10000))  # left half only
    hook = I(hook, rect(-5000, -5000, 5000 + 0.0, 10000))
    hook = I(hook, poly([V(-5000, -5000), V(0, -5000), V(0, 5000), V(-5000, 5000)]))
    tick = D(vv, hook)
    return tick, hook, dict(w=w, crotch=crotch, a=a)


def layers(on='ivory', mono=None, **kw):
    tk, hk, m = hook_tick(**kw)
    if mono:
        return [(tk, mono), (hk, mono)]
    if on == 'ivory':
        return [(tk, EM), (hk, GO)]
    return [(tk, IV), (hk, GL)]
