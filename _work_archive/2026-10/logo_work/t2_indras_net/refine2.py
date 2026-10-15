"""Refinement loop 2: slimmer stones, finer light-lines, heart stone; plus a fair fine-thread rival."""
import os
import subprocess
from geo import *  # noqa: F401,F403
from explore import EM, IV, GO, GL
from explore3 import inset_par
from explore4 import cells_v
from refine1 import mark, place

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'refine2')
os.makedirs(OUT, exist_ok=True)


def thread_mark(s=0.36, NL=3, K=6, h=50, w=2.6, r=11):
    """Thick stroke = NL hairline threads, thin stroke = 1 thread; jewels at the NL crossings."""
    L = Lattice((0, 0), h, s)
    parts = []
    # left threads: lines v = j + 0.5 (centre of columns), from top u to the thin thread at u = 0.5
    for j in range(NL):
        v = j + .5
        u_top = -K - .5 + (0 if j == 0 else 0)
        parts.append(seg(L.P(u_top - j * 0, v), L.P(.5, v), w))
    parts.append(seg(L.P(.5, -K - .5), L.P(.5, NL - .5), w))
    em = union(*parts)
    jw = union(*[L.jewel(.5, j + .5, r) for j in range(NL)])
    return em, jw


CANDS = {
    'S1_s34_K6_2v1_heart': dict(s=0.34, K=6, g=2.8, gold=((0, 0),)),
    'S2_s36_K6_2v1_heart': dict(s=0.36, K=6, g=2.8, gold=((0, 0),)),
    'S3_s34_K7_3v1_heart': dict(s=0.34, K=7, NL=3, h=48, g=2.4, gold=((0, 0),)),
    'S4_s34_K6_2v2_heart': dict(s=0.34, K=6, NR=2, g=2.8, gold=((0, 0),)),
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
    em, au = place(list(thread_mark()))
    for bg, c1, c2, tag in ((IV, EM, GO, 'iv'), (EM, IV, GL, 'em')):
        f = os.path.join(OUT, f'T1_threads_{tag}.svg')
        write_svg(f, 1000, 1000, fill(em, c1) + fill(au, c2), bg)
        files.append(f)
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sheet',
                    os.path.join(HERE, 'refine2.png'), *files], check=True)
    # small-size check of S1 on emerald
    em, au = place(list(mark(**CANDS['S1_s34_K6_2v1_heart'])), target=860)
    f = os.path.join(OUT, 'S1_small_test.svg')
    write_svg(f, 1000, 1000, fill(em, EM) + fill(au, GO))
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sizes',
                    os.path.join(HERE, 'refine2_sizes.png'), f], check=True)


if __name__ == '__main__':
    main()
