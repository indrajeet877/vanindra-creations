import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import explore, window
explore.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refine')
R = [
    ('r4a_ring1', dict(C=16.0, steps=(10.0,), outer_from=('ring', 10.0), tL=30, tR=9.5)),
    ('r4b_ring2_outer', dict(C=18.0, steps=(7.0, 14.0), outer_from=('ring', 7.0), tL=31, tR=10, seam=1.4)),
    ('r4c_ring2_inner', dict(C=18.0, steps=(7.0, 14.0), outer_from=('ring', 14.0), tL=29, tR=9.5, seam=1.4)),
    ('r4d_ring1_bigC', dict(C=22.0, steps=(11.0,), outer_from=('ring', 11.0), tL=30, tR=10)),
]
if __name__ == '__main__':
    for n, kw in R:
        parts, g = window.build(**kw)
        print(explore.cell(n, parts))
        window.construction_svg(os.path.join(explore.OUT, n + '_construction.svg'), **kw)
