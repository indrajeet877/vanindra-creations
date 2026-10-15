import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop4'); os.makedirs(OUT, exist_ok=True)
fams = [('cormorant-garamond', 500), ('cormorant-garamond', 600), ('bodoni-moda', 500), ('marcellus', 400), ('forum', 400),
        ('tenor-sans', 400), ('jost', 400), ('cinzel', 500), ('libre-caslon-display', 400), ('italiana', 400), ('playfair-display', 500), ('gloock', 400)]
items = []
y = 70
for fam, wt in fams:
    try:
        tr = vt.text_path('VANINDRA', family=fam, weight=wt, size=56, x=30, y=y, tracking=0.12)
        tr2 = vt.text_path('CREATIONS', family=fam, weight=wt, size=18, x=32, y=y + 30, tracking=0.42)
        lab = vt.text_path(f'{fam} {wt}', family='jost', weight=400, size=12, x=520, y=y)
        items += [(tr.path, EMERALD), (tr2.path, GOLD), (lab.path, '#777')]
    except Exception as e:
        print(fam, e)
    y += 95
open(os.path.join(OUT, 'type.svg'), 'w').write(svg(760, y, items, bg=IVORY))
subprocess.run(['node', RENDER, 'png', os.path.join(OUT, 'type.svg'), os.path.join(OUT, 'type.png'), '760'], check=True)
