import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import explore, emv
explore.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refine')
R = [
    ('r5a_corner_only', dict()),
    ('r5b_corner_ringtop', dict(ring_top=True)),
    ('r5c_gold_facets', dict(gold_facets=True)),
    ('r5d_heavier_hair', dict(tL=31, tR=12.5)),
    ('r5e_C26', dict(C=26, s=12, tL=31, tR=11)),
    ('r5f_solid', dict(solid=True, tR=11)),
]
if __name__ == '__main__':
    for n, kw in R:
        parts, g = emv.build(**kw)
        print(explore.cell(n, parts))
    emv.construction(os.path.join(explore.OUT, 'r5_construction.svg'))
