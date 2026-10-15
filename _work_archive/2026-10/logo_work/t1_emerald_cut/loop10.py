import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import explore, emv2
explore.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop10')
os.makedirs(explore.OUT, exist_ok=True)
base = dict(tL=30.0, tR=11.0, culet=0.0, seam=1.7, mitre=True)
V = [
    ('l10a_clip6', dict(base, clip=6.0)),
    ('l10b_clip8', dict(base, clip=8.0)),
    ('l10c_clip9_tR12', dict(base, clip=9.0, tR=12.0)),
    ('l10d_prop_ref', dict(base, k=0.42)),
]
for n, kw in V:
    parts, g = emv2.build(**kw)
    print(n, round(g['aL'],2), round(g['TRi'][0],2), explore.cell(n, parts))
