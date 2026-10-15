"""Exploration round 4: V cut from emeralds, symmetric vs Didone stress."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from explore import cell
from explore3 import opened_pendant
import vgem

V4 = [
    ('23_bagV_sym_2tone', lambda: vgem.build(tL=24, tR=24)[0]),
    ('24_bagV_didone_2tone', lambda: vgem.build(tL=33, tR=9.5, chO=11)[0]),
    ('25_bagV_didone_mono', lambda: vgem.build(tL=33, tR=9.5, chO=11, table_role='A')[0]),
    ('26_bagV_didone_thin_gold', lambda: [(p, 'B' if i == len(vgem.build(tL=33, tR=9.5, chO=11, table_role='A')[0]) - 1 else 'A')
                                          for i, (p, r) in enumerate(vgem.build(tL=33, tR=9.5, chO=11, table_role='A')[0])]),
    ('27_bagV_didone_2steps', lambda: vgem.build(tL=36, tR=10, chO=12, steps=(5.5, 11), table_role='B', seam=1.6)[0]),
    ('28_opened_mono', lambda: opened_pendant(theta=11)),
]

if __name__ == '__main__':
    for n, f in V4:
        print(cell(n, f()))
