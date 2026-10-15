"""Refinement loop 1 for the two-stone Didone V."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell
import vgem2

R = [
    ('r1a_top_h_1step', dict()),
    ('r1b_top_perp', dict(top='p', thin_top='p')),
    ('r1c_2steps', dict(insets=(5.0, 10.0), seam=1.5)),
    ('r1d_table_gold', dict(table_role='B')),
    ('r1e_thin_gold', dict(thin_role='B')),
    ('r1f_heavier', dict(tL=38, tR=8.5, chO=12, insets=(7.0,))),
]

if __name__ == '__main__':
    os.makedirs('refine', exist_ok=True)
    import explore
    explore.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refine')
    for n, kw in R:
        parts, g = vgem2.build(**kw)
        print(explore.cell(n, parts))
