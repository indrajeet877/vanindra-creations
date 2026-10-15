"""Loop A: choose the wordmark voice next to the jaali-stroke V."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brand import *  # noqa
OUT = os.path.join(HERE, 'loopA'); os.makedirs(OUT, exist_ok=True)
files = []
for fam, wt, tr in (('marcellus', 400, 0.16), ('cormorant-garamond', 600, 0.16), ('bodoni-moda', 500, 0.14), ('tenor-sans', 400, 0.18)):
    for bg, cm, cw, cc, tag in ((IVORY, EMERALD, EMERALD, GOLD, 'i'), (EMERALD, GOLD_LT, IVORY, GOLD_LT, 'e')):
        cap = 60.0
        mk = place(norm_mark(10.0), 0, 0, 1.0)
        mh = cap * 1.95
        mk = place(norm_mark(10.0), 60 + mh * 0.33, 40, mh)
        wx = 60 + mh * 0.66 + 46
        w1 = word('VANINDRA', fam, wt, cap, tracking=tr, x=wx, baseline=40 + cap)
        w2 = word('CREATIONS', fam, wt, cap * 0.30, tracking=0.62, x=wx + 2, baseline=40 + cap + cap * 0.30 + cap * 0.42)
        W = max(vt.bounds(w1)[2], vt.bounds(w2)[2]) + 60
        f = os.path.join(OUT, f'{fam}_{tag}.svg')
        open(f, 'w').write(svg(W, 40 + mh + 40, [(mk, cm), (w1, cw), (w2, cc)], bg=bg)); files.append(f)
subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'loopA.png')] + files, check=True)
