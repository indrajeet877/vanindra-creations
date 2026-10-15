"""Fourth exploration: refine the pavé direction (stones = cells of the net, threads = light between stones)."""
import os
import subprocess
from geo import *  # noqa: F401,F403
from explore import keep, EM, IV, GO, GL
from explore3 import inset_par, render

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'explore4')
os.makedirs(OUT, exist_ok=True)


def cells_v(NL=2, NR=2, KL=4, KR=None, step_outer=True):
    KR = KL if KR is None else KR
    cells = set()
    for j in range(NL):
        for i in range(-KL, NR):
            cells.add((i, j))
    for i in range(NR):
        for j in range(-KR, NL):
            cells.add((i, j))
    return cells


def pave(s=0.40, NL=2, NR=2, K=5, g=3.2, gold=(), h=60, drop=()):
    L = Lattice((0, 0), h, s)
    cells = cells_v(NL, NR, K) - set(drop)
    em = [inset_par(L, None, i, i + 1, j, j + 1, g) for (i, j) in cells if (i, j) not in gold]
    layers = [(union(*em), EM)]
    if gold:
        layers.append((union(*[inset_par(L, None, i, i + 1, j, j + 1, g) for (i, j) in gold]), GO))
    return layers


VARS = {
    'Q1_s40_K5': lambda: pave(),
    'Q2_s40_K5_heart': lambda: pave(gold=((0, 0),)),
    'Q3_didone_2_1': lambda: pave(NL=2, NR=1, K=5),
    'Q4_didone_3_1': lambda: pave(NL=3, NR=1, K=6, h=50, s=0.38),
    'Q5_didone_2_1_heart': lambda: pave(NL=2, NR=1, K=5, gold=((0, 0),)),
    'Q6_s36_K6_thin_gap': lambda: pave(s=0.36, K=6, g=2.4),
    'Q7_s40_K5_knot_gold': lambda: pave(gold=((0, 0), (0, 1), (1, 0), (1, 1))),
    'Q8_didone_3_1_heart': lambda: pave(NL=3, NR=1, K=6, h=50, s=0.38, gold=((0, 0),)),
    'Q9_s44_K4': lambda: pave(s=0.44, K=4),
}

if __name__ == '__main__':
    render(VARS, os.path.join(HERE, 'explore4.png'), OUT)
