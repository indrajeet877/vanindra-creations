import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell
from explore7 import uvee

T = 9 / 16


def left_only_cut(p, yc, gap, xsplit=0.0):
    """Cut only the LEFT arm: remove a horizontal band of height gap centred at height yc, x < xsplit."""
    band = rect(-5000, -yc - gap / 2, 5000 + xsplit, gap)
    q = D(p, band)
    off = I(q, rect(-5000, -5000, 5000 + xsplit, 5000 - yc - gap / 2))
    rest = D(q, off)
    return rest, off


def K1():
    H = 560; p = uvee(H, 92)
    r, o = left_only_cut(p, H * 9 / 16, 16)
    return [(r, EM), (o, GO)]

def K2():
    H = 560; p = uvee(H, 92)
    r, o = left_only_cut(p, H * 9 / 16, 16)
    return [(r, EM), (o, EM)]

def K3():  # medium weight
    H = 560; p = uvee(H, 72)
    r, o = left_only_cut(p, H * 9 / 16, 14)
    return [(r, EM), (o, GO)]


def cropped_tick(Wf=9 * 40.0, Hf=16 * 40.0, w=110.0, vx=0.40, hy=0.45, ang_long=None):
    """A heavy tick cropped by an invisible 9:16 frame (0,0)-(Wf,Hf): touches all four edges."""
    frame = rect(0, 0, Wf, Hf)
    V0 = V(Wf * vx, Hf + w * 0.35)            # vertex below the frame bottom (cropped flat)
    tr = V(Wf + w * 0.2, -w * 0.2)            # long arm aims at (beyond) top-right corner
    tl = V(-w, Hf * hy)                        # short arm exits through the left edge
    def bar(a, b):
        pth = pathops.Path(); pth.moveTo(*a); pth.lineTo(*b)
        return vt.stroke_to_path(pth, w, cap='square')
    # build tick as union of two bars meeting with a miter at V0
    path = pathops.Path(); path.moveTo(*tl); path.lineTo(*V0); path.lineTo(*tr)
    t = vt.stroke_to_path(path, w, cap='square', join='miter')
    return I(t, frame)

def F1(): return [(cropped_tick(), EM)]
def F2(): return [(cropped_tick(w=86, vx=0.36, hy=0.40), EM)]
def F3(): return [(cropped_tick(w=130, vx=0.42, hy=0.52), EM)]

V8 = [('K1_leftcut_gold', K1), ('K2_leftcut_mono', K2), ('K3_leftcut_medium', K3), ('F1_crop916', F1), ('F2_crop916_light', F2), ('F3_crop916_heavy', F3)]
if __name__ == '__main__':
    for n, f in V8:
        print(cell(n, f()))
