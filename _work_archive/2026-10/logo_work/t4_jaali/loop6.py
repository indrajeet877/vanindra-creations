"""Loop 6: the unit V with its two jaali joints -- radial mitre at the top, interlaced crossing at the base."""
import math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from unit import unit, K83
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop6'); os.makedirs(OUT, exist_ok=True)
TH = 22.5; S, C, TN = math.sin(TH*D2R), math.cos(TH*D2R), math.tan(TH*D2R)

def arm_band(side, R, t, ext, out_cut=None):
    """one arm of the bottom point as a straight band, extended `ext` past the tip along its own line."""
    # outer edge line passes through the star tip (0,R) and the notch; band goes inward by t
    tip = (0.0, R)
    notch = polar(0, 0, R * K83, 270 - side * 22.5)          # side=-1 -> left notch at 247.5
    ux, uy = notch[0] - tip[0], notch[1] - tip[1]
    L = math.hypot(ux, uy); ux, uy = ux / L, uy / L         # up the arm
    nx, ny = -uy, ux                                          # normal
    # make normal point inward (towards the axis)
    if nx * (-notch[0]) < 0:
        nx, ny = -nx, -ny
    a0, a1 = -ext, L + 40
    q = [(tip[0] + ux * a0, tip[1] + uy * a0), (tip[0] + ux * a1, tip[1] + uy * a1),
         (tip[0] + ux * a1 + nx * t, tip[1] + uy * a1 + ny * t), (tip[0] + ux * a0 + nx * t, tip[1] + uy * a0 + ny * t)]
    band = P(q)
    wedge = P([(0, 0), polar(0, 0, 900, 247.5), polar(0, 0, 900, 292.5), (0, 900)])
    # mitre at the top: keep inside the radial wedge (below the notch radii), plus everything below the centre
    return inter(band, union(wedge, P([(-900, R * 0.2), (900, R * 0.2), (900, 900), (-900, 900)])))

def crossed(R=100.0, t=10.0, ext=None, gap=2.2, cut=None, over='left'):
    ext = ext if ext is not None else t * 1.6
    Lb = arm_band(-1, R, t, ext); Rb = arm_band(1, R, t, ext)
    # horizontal tile-edge cut below the crossing
    cut = cut if cut is not None else R + t * 0.9
    keep = P([(-900, -900), (900, -900), (900, cut), (-900, cut)])
    Lb, Rb = inter(Lb, keep), inter(Rb, keep)
    top, und = (Lb, Rb) if over == 'left' else (Rb, Lb)
    gapP = vt.stroke_to_path(top, gap * 2, join='miter')
    return merge([top, diff(und, gapP)])

V = [('plain unit t10', lambda: unit(t=10)), ('crossed t10', lambda: crossed()), ('crossed t12 short', lambda: crossed(t=12, ext=14)),
     ('crossed t10 long', lambda: crossed(ext=22, cut=118)), ('crossed t11 tight', lambda: crossed(t=11, ext=16, gap=1.6)), ('crossed t9', lambda: crossed(t=9, ext=14, gap=2))]
files = []
for i, (name, fn) in enumerate(V):
    m, _ = fit(fn(), 240, 240, 200, 200)
    for bg, fg, tag in ((IVORY, EMERALD, 'i'), (EMERALD, GOLD_LT, 'e')):
        f = os.path.join(OUT, f'{i+1}{tag}.svg'); open(f, 'w').write(svg(400, 400, [(m, fg)], bg=bg, title=name)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loop6.png')] + files, check=True)
