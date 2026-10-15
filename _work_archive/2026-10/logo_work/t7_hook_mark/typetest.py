import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from hookmark import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'typetest'); os.makedirs(OUT, exist_ok=True)
tk, hk, m = hook_tick(p=125, g=24)
mark = U(tk, hk)

opts = [
    ('jost500_caps', dict(text='VANINDRA', family='jost', weight=500, tracking=0.16), dict(text='CREATIONS', family='jost', weight=400, tracking=0.5)),
    ('jost400_caps', dict(text='VANINDRA', family='jost', weight=400, tracking=0.2), dict(text='CREATIONS', family='jost', weight=400, tracking=0.5)),
    ('manrope500_caps', dict(text='VANINDRA', family='manrope', weight=500, tracking=0.14), dict(text='CREATIONS', family='manrope', weight=500, tracking=0.5)),
    ('tenor_caps', dict(text='VANINDRA', family='tenor-sans', weight=400, tracking=0.16), dict(text='CREATIONS', family='tenor-sans', weight=400, tracking=0.5)),
    ('jost500_mixed', dict(text='VanIndra', family='jost', weight=500, tracking=0.0), dict(text='CREATIONS', family='jost', weight=400, tracking=0.42)),
    ('outfit400_caps', dict(text='VANINDRA', family='outfit', weight=400, tracking=0.18), dict(text='CREATIONS', family='outfit', weight=400, tracking=0.5)),
]
files = []
for name, a, b in opts:
    A = vt.text_path(size=200, y=0, **a)
    x0, y0, x1, y1 = A.bounds
    capH = -y0
    B = vt.text_path(size=200 * 0.3, y=0, **b)
    bx0, by0, bx1, by1 = B.bounds
    # layout: mark height = 1.5 * capH, wordmark left
    mk, s, tx, ty = fit(mark, (0, 0, 10000, capH * 1.9))
    mb = bbox(mk)
    gap = capH * 0.55
    wx = mb[2] + gap
    Ap = tf(A.path, 1, wx - x0, 0)
    Bp = tf(B.path, 1, wx - bx0, 0)
    # vertical: cap of A centred to mark, B below
    total_h = capH + capH * 0.42 + (by1 - by0)
    mk_cy = (mb[1] + mb[3]) / 2
    Ay = mk_cy - total_h / 2 + capH
    Ap = tf(A.path, 1, wx - x0, Ay)
    By = Ay + capH * 0.42 + (by1 - by0) - by1 * 0
    Bp = tf(B.path, 1, wx - bx0, Ay + capH * 0.42 + (-by0))
    tk2 = tf(tk, s, tx, ty); hk2 = tf(hk, s, tx, ty)
    allb = bbox(U(tk2, hk2, Ap, Bp))
    W = allb[2] - allb[0] + 160; Hh = allb[3] - allb[1] + 160
    ox, oy = 80 - allb[0], 80 - allb[1]
    body = ''.join(pathel(tf(q, 1, ox, oy), c) for q, c in [(tk2, EM), (hk2, GO), (Ap, EM), (Bp, GO)])
    files.append(write(os.path.join(OUT, name + '.svg'), W, Hh, body, bg=IV))
print('\n'.join(files))
