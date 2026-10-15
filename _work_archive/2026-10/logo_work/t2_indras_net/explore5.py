"""Exploration 5: 'one thread, many jewels'.

Thick stroke = band of stones (net cells). Thin stroke = a single positive thread of the SAME width as the light-lines
between the stones, laid exactly on a lattice line, so where it enters the band it continues as the light between stones
(figure/ground continuity).
"""
import os
import subprocess
from geo import *  # noqa: F401,F403
from explore import EM, IV, GO, GL
from explore3 import inset_par
from refine1 import place

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'explore5')
os.makedirs(OUT, exist_ok=True)


def thread_v(s=0.36, NL=2, K=6, g=3.0, h=60, ut=0, below=1, tw=None, gold=(), thread_top=None):
    """Left band: cells (i, j), j < NL, i in [-K, ut+below-1]. Thread: lattice line u = ut, from top to band's outer edge."""
    L = Lattice((0, 0), h, s)
    tw = 2 * g if tw is None else tw
    cells = [(i, j) for j in range(NL) for i in range(-K, ut + below)]
    stones = {c: inset_par(L, None, c[0], c[0] + 1, c[1], c[1] + 1, g) for c in cells}
    top_v = -K if thread_top is None else thread_top
    # thread from (ut, top_v) to (ut, 0) positive (outside the band)
    thread = seg(L.P(ut, top_v), L.P(ut, 0), tw)
    # square-off the thread end at the band's inner edge exactly (the light line continues inside)
    em = union(thread, *[p for c, p in stones.items() if c not in gold])
    au = union(*[p for c, p in stones.items() if c in gold]) if gold else None
    return em, au


CANDS = {
    'X1_thread_ut0_below1': dict(),
    'X2_thread_ut0_below1_gold': dict(gold=((0, 0), (0, 1))),
    'X3_thread_ut0_below2': dict(below=2, K=6),
    'X4_thread_3col': dict(NL=3, K=7, h=50, g=2.6),
    'X5_thread_thicker': dict(tw=12),
    'X6_thread_ut0_below0': dict(below=0, K=6),
}


def main():
    files = []
    for name, kw in CANDS.items():
        em, au = place(list(thread_v(**kw)))
        for bg, c1, c2, tag in ((IV, EM, GO, 'iv'), (EM, IV, GL, 'em')):
            body = fill(em, c1) + (fill(au, c2) if au is not None else '')
            f = os.path.join(OUT, f'{name}_{tag}.svg')
            write_svg(f, 1000, 1000, body, bg)
            files.append(f)
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sheet',
                    os.path.join(HERE, 'explore5.png'), *files], check=True)


if __name__ == '__main__':
    main()
