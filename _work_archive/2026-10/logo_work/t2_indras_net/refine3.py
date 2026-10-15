"""Refinement loop 3: thread-and-jewels V at large size; junction, top cut, proportion, gold placement."""
import os
import subprocess
from mark import *  # noqa: F401,F403

EM, IV, GO, GL = PALETTE['emerald'], PALETTE['ivory'], PALETTE['gold'], PALETTE['gold_lt']
OUT = os.path.join(HERE, 'refine3')
os.makedirs(OUT, exist_ok=True)

CANDS = {
    'M1_base_s38_K6': dict(),
    'M2_through_drop_inner': dict(below=1, drop=((0, 0),)),
    'M3_through_full': dict(below=1),
    'M4_s42_K5': dict(s=0.42, K=5),
    'M5_gold_knot_stone': dict(gold=((-1, 0),)),
    'M6_s36_K7': dict(s=0.36, K=7, g=3.0),
}


def main():
    files = []
    for name, kw in CANDS.items():
        r = build(**kw)
        (em, au), _ = place([r['em'], r['au']], 1000, 640)
        for bg, c1, c2, tag in ((IV, EM, GO, 'iv'), (EM, IV, GL, 'em')):
            f = os.path.join(OUT, f'{name}_{tag}.svg')
            write_svg(f, 1000, 1000, fill(em, c1) + (fill(au, c2) if au is not None else ''), bg)
            files.append(f)
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sheet',
                    os.path.join(HERE, 'refine3.png'), *files], check=True)


if __name__ == '__main__':
    main()
