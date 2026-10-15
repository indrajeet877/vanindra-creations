"""Loop B: optically spaced wordmark in two voices + horizontal & stacked lockups."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brand import *  # noqa
OUT = os.path.join(HERE, 'loopB'); os.makedirs(OUT, exist_ok=True)
files = []
for fam, wt in (('marcellus', 400), ('tenor-sans', 400), ('cormorant-garamond', 600)):
    cap = 60.0
    w1 = optical_word('VANINDRA', fam, wt, cap, gap=0.42, x=0, baseline=cap)
    w2 = optical_word('CREATIONS', fam, wt, cap * 0.28, gap=0.95, x=0, baseline=0)
    b1, b2 = vt.bounds(w1), vt.bounds(w2)
    # centre CREATIONS under VANINDRA
    w2 = vt.transform(w2, 1, 0, 0, 1, (b1[0] + b1[2]) / 2 - (b2[0] + b2[2]) / 2, cap + cap * 0.62 + cap * 0.28)
    for bg, cm, cw, cc, tag in ((IVORY, EMERALD, EMERALD, GOLD, 'i'), (EMERALD, GOLD_LT, IVORY, GOLD_LT, 'e')):
        mh = (vt.bounds(w2)[3] - vt.bounds(w1)[1]) * 1.18
        mk = norm_mark(10.0)
        mk = place(mk, 0, 0, mh)
        mb = vt.bounds(mk)
        top = vt.bounds(w1)[1] - mh * 0.06
        mk = vt.transform(mk, 1, 0, 0, 1, -mb[2] - cap * 0.62, top - mb[1])
        allb = vt.bounds(merge([mk, w1, w2]))
        pad = 50
        tr = lambda p: vt.transform(p, 1, 0, 0, 1, pad - allb[0], pad - allb[1])
        W, H = allb[2] - allb[0] + 2 * pad, allb[3] - allb[1] + 2 * pad
        f = os.path.join(OUT, f'h_{fam}_{tag}.svg'); open(f, 'w').write(svg(W, H, [(tr(mk), cm), (tr(w1), cw), (tr(w2), cc)], bg=bg)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loopB.png')] + files, check=True)
