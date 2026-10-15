"""Refinement loop 4: light-line width, stone count, thread weight — judged at large AND at real pixel sizes."""
import os
import subprocess
from mark import *  # noqa: F401,F403

EM, IV, GO, GL = PALETTE['emerald'], PALETTE['ivory'], PALETTE['gold'], PALETTE['gold_lt']
OUT = os.path.join(HERE, 'refine4')
os.makedirs(OUT, exist_ok=True)

CANDS = {
    'N1_s38_K6_g32': dict(s=0.38, K=6, g=3.2, gold=((-1, 0),)),
    'N2_s40_K5_g40': dict(s=0.40, K=5, g=4.0, gold=((-1, 0),)),
    'N3_s40_K5_g40_tw12': dict(s=0.40, K=5, g=4.0, tw=12, gold=((-1, 0),)),
    'N4_s42_K5_g45': dict(s=0.42, K=5, g=4.5, gold=((-1, 0),)),
    'N5_s40_K6_g40': dict(s=0.40, K=6, g=4.0, gold=((-1, 0),)),
}


def strip(paths_colors, bg, sizes=(16, 24, 32, 48, 64, 110), W=520, H=150):
    body = ''
    x = 16
    for sz in sizes:
        layers = []
        ps = [p for p, _ in paths_colors]
        placed, _ = place(ps, sz, sz * 0.86)
        for p, (_, c) in zip(placed, paths_colors):
            layers.append(fill(transform(p, 1, 0, 0, 1, x, H - sz - 20), c))
        body += ''.join(layers)
        x += sz + 18
    return svg_doc(W, H, body, bg)


def main():
    files = []
    for name, kw in CANDS.items():
        r = build(**kw)
        (em, au), _ = place([r['em'], r['au']], 1000, 640)
        f = os.path.join(OUT, f'{name}_em.svg')
        write_svg(f, 1000, 1000, fill(em, IV) + fill(au, GL), EM)
        files.append(f)
        for bg, c1, c2, tag in ((IV, EM, GO, 'iv'), (EM, IV, GL, 'em')):
            f = os.path.join(OUT, f'{name}_strip_{tag}.svg')
            open(f, 'w').write(strip([(r['em'], c1), (r['au'], c2)], bg))
            files.append(f)
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sheet',
                    os.path.join(HERE, 'refine4.png'), *files], check=True)
    # true pixel strips (1:1)
    for name in CANDS:
        for tag in ('iv', 'em'):
            subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'png',
                            os.path.join(OUT, f'{name}_strip_{tag}.svg'), os.path.join(OUT, f'{name}_strip_{tag}.png'), '520'], check=True)


if __name__ == '__main__':
    main()
