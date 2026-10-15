"""Refinement loop 1: Didone pavé V. Compare proportion, contrast, gold placement, on both grounds."""
import os
import subprocess
from geo import *  # noqa: F401,F403
from explore import EM, IV, GO, GL
from explore3 import inset_par
from explore4 import cells_v

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'refine1')
os.makedirs(OUT, exist_ok=True)


def mark(s=0.38, NL=2, NR=1, K=5, g=3.4, h=60, gold=()):
    L = Lattice((0, 0), h, s)
    cells = cells_v(NL, NR, K)
    em = union(*[inset_par(L, None, i, i + 1, j, j + 1, g) for (i, j) in cells if (i, j) not in gold])
    au = union(*[inset_par(L, None, i, i + 1, j, j + 1, g) for (i, j) in gold]) if gold else None
    return em, au


def place(paths, box=1000, target=640):
    allp = union(*[p for p in paths if p is not None])
    x0, y0, x1, y1 = bounds(allp)
    k = target / (y1 - y0)
    tx, ty = box / 2 - (x0 + x1) / 2 * k, box / 2 - (y0 + y1) / 2 * k
    return [transform(p, k, 0, 0, k, tx, ty) if p is not None else None for p in paths]


CANDS = {
    'R1_s38_K5_2v1': dict(),
    'R2_s38_K5_2v1_heart': dict(gold=((0, 0),)),
    'R3_s38_K5_2v1_knot': dict(gold=((0, 0), (0, 1))),
    'R4_s34_K6_2v1': dict(s=0.34, K=6),
    'R5_s38_K6_3v1_h50': dict(NL=3, K=6, h=50, g=3.0),
    'R6_s42_K4_2v1': dict(s=0.42, K=4),
}


def main():
    files = []
    for name, kw in CANDS.items():
        em, au = place(list(mark(**kw)))
        for bg, c1, c2, tag in ((IV, EM, GO, 'iv'), (EM, IV, GL, 'em')):
            body = fill(em, c1) + (fill(au, c2) if au is not None else '')
            f = os.path.join(OUT, f'{name}_{tag}.svg')
            write_svg(f, 1000, 1000, body, bg)
            files.append(f)
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sheet',
                    os.path.join(HERE, 'refine1.png'), *files], check=True)


if __name__ == '__main__':
    main()
