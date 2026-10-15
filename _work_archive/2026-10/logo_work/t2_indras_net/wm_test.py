import os
import subprocess
from mark import build, place
from wordmark import *  # noqa: F401,F403

EM, IV, GO, GL = PALETTE['emerald'], PALETTE['ivory'], PALETTE['gold'], PALETTE['gold_lt']
OUT = os.path.join(HERE, 'wm_test')
os.makedirs(OUT, exist_ok=True)

files = []
r = build(gold=((-1, 0),))
for name in OPTIONS:
    wm = wordmark(name, cap=100)
    W, H = 1500, 500
    mh = 300
    (em, au), k = place([r['em'], r['au']], 0, mh, cx=0, cy=0)
    mb = bounds(union(em, au))
    mw = mb[2] - mb[0]
    gap = 110
    total = mw + gap + wm['width']
    x0 = (W - total) / 2
    em2 = transform(em, 1, 0, 0, 1, x0 - mb[0], H / 2)
    au2 = transform(au, 1, 0, 0, 1, x0 - mb[0], H / 2)
    # vertical: centre wordmark block (cap top .. sub bottom) on the mark centre
    blk_h = wm['bottom'] + 100  # from cap top (-cap) to sub baseline
    wy = H / 2 - (wm['bottom'] - wm['cap']) / 2
    wp = transform(wm['all'], 1, 0, 0, 1, x0 + mw + gap, wy)
    f = os.path.join(OUT, f'{name}.svg')
    write_svg(f, W, H, fill(em2, EM) + fill(au2, GO) + fill(wp, EM), IV)
    files.append(f)
subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sheet', os.path.join(HERE, 'wm_test.png'), *files], check=True)
