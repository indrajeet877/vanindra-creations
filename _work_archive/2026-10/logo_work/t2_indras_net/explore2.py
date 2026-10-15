"""Second exploration: pavé (stones = net cells, threads = negative gaps) vs. woven strips (intrecciato)."""
import os
import subprocess
from geo import *  # noqa: F401,F403
from explore import keep, v_clip, pave_cells, EM, IV, GO, GL

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'explore2')
os.makedirs(OUT, exist_ok=True)


def pave(s=0.42, N=2, K=4, g=3.2, flat=None, gold=()):
    L = Lattice((0, 0), 60, s)
    cells = pave_cells(N, K)
    em = union(*[L.cell(i, j, inset=g) for (i, j) in cells if (i, j) not in gold])
    layers = [(em, EM)]
    if gold:
        layers.append((union(*[L.cell(i, j, inset=g) for (i, j) in gold]), GO))
    if flat is not None:
        clipr = keep((0, flat * 60), (1, 0), (0, 1e3))
        layers = [(intersection(p, clipr), c) for p, c in layers]
    return layers


def woven(s=0.42, N=2, K=4, W=40, g=6, h=60, gold_knots=False, stones_in_block=False):
    L = Lattice((0, 0), h, s)
    left = {i: L.thread_v(i, -K - 8, N + 3, W) for i in range(N)}
    right = {j: L.thread_u(j, -K - 8, N + 3, W) for j in range(N)}
    if stones_in_block:
        for i in range(N):
            for j in range(N):
                right[j] = difference(right[j], L.thread_v(i, j - 1, j + 1, W + 2 * g)) if False else right[j]
    else:
        for i in range(N):
            for j in range(N):
                if (i + j) % 2 == 0:
                    right[j] = difference(right[j], L.thread_v(i, j - .9, j + .9, W + 2 * g))
                else:
                    left[i] = difference(left[i], L.thread_u(j, i - .9, i + .9, W + 2 * g))
    t = union(*left.values(), *right.values())
    clip = v_clip(L, N, W, -K * h)
    return [(intersection(t, clip), EM)]


def strands_and_stones(s=0.42, N=2, K=4, g=3.2, gold=False):
    """Arms are continuous strands (gap only between strands); the crossing block is cut into stones."""
    L = Lattice((0, 0), 60, s)
    parts = []
    # left strands: column j, cells i from -K..N-1 merged except inside block
    for j in range(N):
        # strand above the block: from u=-K to u=0
        a = poly([L.P(-K, j), L.P(0, j), L.P(0, j + 1), L.P(-K, j + 1)])
        parts.append(a)
    for i in range(N):
        a = poly([L.P(i, -K), L.P(i, 0), L.P(i + 1, 0), L.P(i + 1, -K)])
        parts.append(a)
    # inset strands by g (shrink): use difference with gap lines
    strands = union(*parts)
    gaps = []
    for k in range(0, N + 1):
        gaps.append(seg(L.P(-K - 2, k), L.P(N + 2, k), 2 * g))
        gaps.append(seg(L.P(k, -K - 2), L.P(k, N + 2), 2 * g))
    strands = difference(strands, union(*gaps))
    stones = union(*[L.cell(i, j, inset=g) for i in range(N) for j in range(N)])
    # restore outer edges: strands were shrunk on their outer side too; acceptable for exploration
    if gold:
        return [(strands, EM), (stones, GO)]
    return [(union(strands, stones), EM)]


VARS = {
    'P1_pave_s42_N2K4': lambda: pave(),
    'P2_pave_s50_N2K3': lambda: pave(s=0.5, K=3),
    'P3_pave_flattop': lambda: pave(K=5, flat=-4),
    'P4_pave_gold_knot': lambda: pave(gold=((0, 0), (0, 1), (1, 0), (1, 1))),
    'P5_pave_N3K4': lambda: pave(N=3, K=4, g=3.6),
    'P6_pave_s36_N2K5': lambda: pave(s=0.36, K=5),
    'W1_woven_N2': lambda: woven(N=2, K=4, W=44, g=7, h=60),
    'W2_woven_N3': lambda: woven(N=3, K=5, W=30, g=6, h=40),
    'S1_strands_stones': lambda: strands_and_stones(),
    'S2_strands_gold': lambda: strands_and_stones(gold=True),
    'P7_pave_N1K6': lambda: pave(N=1, K=6, s=0.42, g=3.5),
    'P8_pave_N2K4_wide_gap': lambda: pave(g=6),
}


def render(vars_, out_png, mini=False):
    files = []
    for name, fn in vars_.items():
        layers = fn()
        allp = union(*[p for p, _ in layers])
        x0, y0, x1, y1 = bounds(allp)
        k = 700 / max(x1 - x0, y1 - y0)
        tx, ty = 500 - (x0 + x1) / 2 * k, 500 - (y0 + y1) / 2 * k
        body = ''.join(fill(transform(p, k, 0, 0, k, tx, ty), c) for p, c in layers)
        f = os.path.join(OUT, f'{name}.svg')
        write_svg(f, 1000, 1000, body, IV)
        files.append(f)
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sheet', out_png, *files], check=True)
    return files


if __name__ == '__main__':
    render(VARS, os.path.join(HERE, 'explore2.png'))
