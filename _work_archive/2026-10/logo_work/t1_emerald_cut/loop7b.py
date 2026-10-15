import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import explore, emv2
from vgem2 import par_line
explore.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop7')

def steplines(fracs, seam=1.6, along='outer', **kw):
    parts, g = emv2.build(**kw)
    L0, Vb = g['L0'], g['Vb']
    lines = []
    for f in fracs:
        d = f * kw.get('tL', 30.0)
        a, b = par_line(L0, Vb, d, (Vb[0], 0))
        lines.append(seg(a, b, 0))
    return [(cut(p, lines, seam), r) for p, r in parts]

base = dict(tL=30.0, tR=10.5, k=0.42, culet=0.0, seam=1.7, mitre=True)
V = [
    ('l7e_one_step', lambda: steplines([0.30], **base)),
    ('l7f_two_steps', lambda: steplines([0.22, 0.44], **base)),
    ('l7g_mid_step', lambda: steplines([0.5], **base)),
    ('l7h_plain', lambda: emv2.build(**base)[0]),
]
for n, f in V:
    print(explore.cell(n, f()))
