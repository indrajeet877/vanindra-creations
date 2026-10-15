import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import explore, emv2
explore.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop8')
os.makedirs(explore.OUT, exist_ok=True)
base = dict(tL=30.0, tR=10.5, k=0.42, culet=0.0, seam=1.7, mitre=True)
V = [
    ('l8a_through', dict(base)),
    ('l8b_stop12', dict(base, seam_stop=12.0)),
    ('l8c_culet3', dict(base, culet=3.0)),
    ('l8d_stop20_wider', dict(base, seam_stop=20.0, seam=2.0)),
]
for n, kw in V:
    parts, g = emv2.build(**kw)
    # big render of the base region
    print(explore.cell(n, parts))
    zoom = [(transform(p, 6, 0, 0, 6, -45*6 + 250, -160*6 + 450), r) for p, r in parts]
    body = ''.join(pth_c(p, EM) for p, r in zoom)
    open(os.path.join(explore.OUT, n + '_zoom.svg'), 'w').write(svg_doc(500, 500, body, IV))
