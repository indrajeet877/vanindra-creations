"""Small-size candidates rendered at true pixel sizes (1:1)."""
import os
import subprocess
from mark import *  # noqa: F401,F403

EM, IV, GO, GL = PALETTE['emerald'], PALETTE['ivory'], PALETTE['gold'], PALETTE['gold_lt']
OUT = os.path.join(HERE, 'small_test')
os.makedirs(OUT, exist_ok=True)
BASE = dict(s=0.40, h=60.0, K=5, NL=2, g=4.0, tw=12.0, gold=((-1, 0),))
C = {
    'full_mark': dict(),
    'E_solid_tw20_gap': dict(small=True, tw_small=20, split=0, fuse=False),
    'H_K3_g7_tw20': dict(K=3, g=7.0, tw=20.0, gold=()),
    'I_K4_g6_tw18': dict(K=4, g=6.0, tw=18.0, gold=()),
    'J_K3_g8_tw22_gold': dict(K=3, g=8.0, tw=22.0),
}
sizes = (16, 20, 24, 32, 48, 64)
rows = []
for name, kw in C.items():
    r = build2(**{**BASE, **kw})
    for bg, c1, c2 in ((IV, EM, GO), (EM, IV, GL)):
        x = 10
        body = ''
        for sz in sizes:
            (pe, pa), _ = place([r['em'], r['au']], sz, sz * 0.92)
            body += fill(transform(pe, 1, 0, 0, 1, x, 6), c1)
            if pa is not None:
                body += fill(transform(pa, 1, 0, 0, 1, x, 6), c2)
            x += sz + 14
        rows.append((name, bg, body))
H = 76
W = 360
body = ''
for k, (name, bg, b) in enumerate(rows):
    y = k * H
    body += f'<rect x="0" y="{y}" width="{W}" height="{H}" fill="{bg}"/><g transform="translate(0,{y})">{b}</g>'
f = os.path.join(OUT, 'small.svg')
open(f, 'w').write(svg_doc(W, H * len(rows), body))
subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'png', f, os.path.join(HERE, 'small_test.png'), str(W)], check=True)
print([r[0] for r in rows[::2]])
