"""Third exploration: 'strands knot into jewels' family, built exactly on the lattice.

Every shape is a union of lattice cells (u,v) shrunk by a uniform gap, so all edges are parallel to e1/e2.
Strand = run of cells merged along its own direction; stones = individual cells where strands cross.
"""
import os
import subprocess
from geo import *  # noqa: F401,F403
from explore import keep, EM, IV, GO, GL

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'explore3')
os.makedirs(OUT, exist_ok=True)


def strand_left(L, j, i0, i1, g):
    """Left-arm strand: cells u in [i0, i1], fixed column j (v in [j, j+1]) merged, inset by g."""
    c = L.P
    p = poly([c(i0, j), c(i1, j), c(i1, j + 1), c(i0, j + 1)])
    return inset_par(L, p, i0, i1, j, j + 1, g)


def strand_right(L, i, j0, j1, g):
    c = L.P
    p = poly([c(i, j0), c(i + 1, j0), c(i + 1, j1), c(i, j1)])
    return inset_par(L, p, i, i + 1, j0, j1, g)


def inset_par(L, p, u0, u1, v0, v1, g):
    """Inset the lattice parallelogram u in [u0,u1], v in [v0,v1] by perpendicular distance g."""
    # perpendicular distance between adjacent v-lines (one cell) along the normal of e1:
    d1, d2 = norm(L.e1), norm(L.e2)
    cross = abs(L.e1[0] * L.e2[1] - L.e1[1] * L.e2[0])
    du = g / (cross / math.hypot(*L.e2))  # g expressed in u units (distance between u-lines = cross/|e2|)
    dv = g / (cross / math.hypot(*L.e1))
    a, b, c_, d = u0 + du, u1 - du, v0 + dv, v1 - dv
    return poly([L.P(a, c_), L.P(b, c_), L.P(b, d), L.P(a, d)])


def knot_v(s=0.42, N=2, K=4, g=3.2, top='lattice', gold=False, Nr=None, top_stone=False, h=60):
    Nr = N if Nr is None else Nr
    L = Lattice((0, 0), h, s)
    parts = []
    for j in range(N):           # left strands (columns j), above the knot
        i0 = -K
        if top == 'flat':
            i0 = -K - j          # extend outer strands so all top ends sit on the node row u+v = -K
        parts.append(strand_left(L, j, i0, 0, g))
    for i in range(Nr):
        j0 = -K
        if top == 'flat':
            j0 = -K - i
        parts.append(strand_right(L, i, j0, 0, g))
    stones = [inset_par(L, None, i, i + 1, j, j + 1, g) for i in range(Nr) for j in range(N)]
    strands = union(*parts)
    if top == 'flat':
        strands = intersection(strands, keep((0, -K * h), (1, 0), (0, 0)))
    if top_stone:
        pass
    if gold:
        return [(strands, EM), (union(*stones), GO)]
    return [(union(strands, *stones), EM)]


VARS = {
    'K1_lattice_top': lambda: knot_v(),
    'K2_flat_top': lambda: knot_v(top='flat', K=4),
    'K3_slim_s36': lambda: knot_v(s=0.36, K=5),
    'K4_three_strands': lambda: knot_v(N=3, K=5, g=3.0, h=44),
    'K5_didone_2plus1': lambda: knot_v(N=2, Nr=1, K=4),
    'K6_flat_gold': lambda: knot_v(top='flat', gold=True),
    'K7_flat_s38_K5': lambda: knot_v(top='flat', s=0.38, K=5),
    'K8_flat_three': lambda: knot_v(top='flat', N=3, K=5, g=3.0, h=44, s=0.40),
    'K9_flat_s46_K3': lambda: knot_v(top='flat', s=0.46, K=3),
}


def render(vars_, out_png, outdir=OUT):
    files = []
    for name, fn in vars_.items():
        layers = fn()
        allp = union(*[p for p, _ in layers])
        x0, y0, x1, y1 = bounds(allp)
        k = 700 / max(x1 - x0, y1 - y0)
        tx, ty = 500 - (x0 + x1) / 2 * k, 500 - (y0 + y1) / 2 * k
        body = ''.join(fill(transform(p, k, 0, 0, k, tx, ty), c) for p, c in layers)
        f = os.path.join(outdir, f'{name}.svg')
        write_svg(f, 1000, 1000, body, IV)
        files.append(f)
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sheet', out_png, *files], check=True)
    return files


if __name__ == '__main__':
    render(VARS, os.path.join(HERE, 'explore3.png'))
