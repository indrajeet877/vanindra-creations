"""The Hook Mark: parametric construction.

Coordinates: SVG y-down. Baseline y=0, the hold rises to y=-H.
Both strokes run on the diagonals of a 9:16 frame: slope dx/dy = 9/16 (29.36 deg off vertical).
  HOLD  - one unbroken parallelogram band, horizontal foot and top, horizontal width tw.
          outer (right) edge: x = t*Y ;  inner edge: x = t*Y - tw      (Y = -y = height)
  HOOK  - the heavy short stroke, outer (left) edge x = -t*Y + s, inner edge x = -t*Y + s + Tw,
          top cut horizontal at Y = h, and cut on the right by a line parallel to the hold,
          a perpendicular gap g away from the hold's inner edge (the editor's cut).
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *

T = 9 / 16
COS = 16 / math.hypot(9, 16)   # cos of stroke angle from vertical; horizontal width * COS = perpendicular width


def hook_mark(H=560.0, Tw=124.0, tw=40.0, g=12.0, hr=9 / 16, s=0.0, foot_drop=0.0, hook_flat=False):
    """Return (hook, hold) pathops paths. g is the PERPENDICULAR gap. s shifts the hook's outer edge.
    foot_drop extends the hold below the baseline."""
    gh = g / COS                           # horizontal gap
    h = H * hr
    Y = lambda yy: -yy                     # height -> svg y
    # hold band
    hold = poly([V(-tw - T * foot_drop, foot_drop), V(-T * foot_drop, foot_drop), V(T * H, -H), V(T * H - tw, -H)])
    # hook: region between outer/inner edges, below h, left of cut line x = t*Y - tw - gh
    def xo(YY): return -T * YY + s
    def xi(YY): return -T * YY + s + Tw
    def xc(YY): return T * YY - tw - gh
    # tip: outer meets cut
    Yt = (tw + gh + s) / (2 * T)
    Yq = (tw + gh + s + Tw) / (2 * T)        # inner meets cut
    pts = [V(xo(h), -h), V(xi(h), -h)]
    if Yq < h:
        pts.append(V(xi(Yq), -Yq))
    else:
        pts[1] = V(xc(h), -h)
    pts.append(V(xc(Yt), -Yt))
    hook = poly(pts)
    if hook_flat and Yt > 0:
        pass
    return hook, hold, dict(h=h, Yt=Yt, Yq=Yq)


def layers(col_hook=EM, col_hold=EM, **kw):
    hk, hd, m = hook_mark(**kw)
    return [(hk, col_hook), (hd, col_hold)]
