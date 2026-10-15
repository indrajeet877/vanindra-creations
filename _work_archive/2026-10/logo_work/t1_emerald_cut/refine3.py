import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import explore
import window

explore.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refine')
R = [
    ('r3a_window_1ring', dict(steps=(10.0,))),
    ('r3b_window_2rings', dict(steps=(7.0, 14.0), seam=1.4)),
    ('r3c_window_bigC', dict(C=20.0, steps=(11.0,), tL=33)),
    ('r3d_window_3rings', dict(C=18.0, steps=(6.0, 12.0, 18.0), seam=1.3, tL=34, tR=10)),
]
if __name__ == '__main__':
    for n, kw in R:
        parts, g = window.build(**kw)
        print(explore.cell(n, parts))
        window.construction_svg(os.path.join(explore.OUT, n + '_construction.svg'), **kw)
