"""Round of >= 6 variations inside the Indra's Net territory -> explore/*.svg + explore.png"""
import os
import subprocess
from geo import *  # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'explore')
os.makedirs(OUT, exist_ok=True)
EM, IV, GO, GL = PALETTE['emerald'], PALETTE['ivory'], PALETTE['gold'], PALETTE['gold_lt']


def keep(p, d, inside):
    a = halfplane(p, d)
    b = halfplane(p, mul(d, -1))
    probe = poly([inside, add(inside, (0.01, 0)), add(inside, (0, 0.01))])
    return a if len(list(intersection(a, probe).segments)) else b


def v_clip(L, N, w, ytop):
    """Wedge bounded by outer edges of the outermost threads + flat top."""
    d1, d2 = norm(L.e1), norm(L.e2)
    pl = add(L.P(0, N - 1), mul(perp(d1), w / 2))           # outer-left edge line point
    pr = add(L.P(N - 1, 0), mul(perp(d2), -w / 2))          # outer-right edge line point
    centre = L.P((N - 1) / 2, (N - 1) / 2)
    c = intersection(keep(pl, d1, centre), keep(pr, d2, centre))
    c = intersection(c, keep((0, ytop), (1, 0), (centre[0], ytop + 10)))
    return c


def threads(L, N_left, N_right, K, w, gap=None, weave=True, ext=0.0):
    """Return union path of left (fixed v) and right (fixed u) threads with optional over/under."""
    left = {i: L.thread_v(i, -K - 6, N_right - 1 + 3, w) for i in range(N_left)}
    right = {j: L.thread_u(j, -K - 6, N_left - 1 + 3, w) for j in range(N_right)}
    if weave and gap:
        for i in range(N_left):
            for j in range(N_right):
                over_left = (i + j) % 2 == 0
                if over_left:
                    right[j] = difference(right[j], L.thread_v(i, j - 1, j + 1, w + 2 * gap))
                else:
                    left[i] = difference(left[i], L.thread_u(j, i - 1, i + 1, w + 2 * gap))
    return union(*left.values(), *right.values())


def A_woven():
    L = Lattice((0, 0), 60, 0.42)
    N, K, w = 3, 5, 9
    t = threads(L, N, N, K, w, gap=7)
    clip = v_clip(L, N, w, -K * 60)
    return [(intersection(t, clip), EM)]


def B_jewelled():
    L = Lattice((0, 0), 60, 0.42)
    N, K, w = 3, 5, 3.2
    t = threads(L, N, N, K, w, weave=False)
    clip = v_clip(L, N, w, -K * 60)
    t = intersection(t, clip)
    js = union(*[L.jewel(u, v, 17) for u in range(N) for v in range(N)])
    return [(union(t, js), EM)]


def C_jaal():
    L = Lattice((0, 0), 60, 0.42)
    K, w = 4, 3.2
    nodes = set()
    for v in (0, 1):
        for u in range(-K, 2):
            nodes.add((u, v))
    for u in (0, 1):
        for v in range(-K, 2):
            nodes.add((u, v))
    parts = []
    for (u, v) in nodes:
        if (u + 1, v) in nodes:
            parts.append(seg(L.P(u, v), L.P(u + 1, v), w))
        if (u, v + 1) in nodes:
            parts.append(seg(L.P(u, v), L.P(u, v + 1), w))
        parts.append(L.jewel(u, v, 14))
    return [(union(*parts), EM)]


def D_didone():
    L = Lattice((0, 0), 46, 0.42)
    N, K = 3, 7
    wl, wr, gap = 10, 4, 6
    left = {i: L.thread_v(i, -K - 6, 3, wl) for i in range(N)}
    right = L.thread_u(0, -K - 6, N + 3, wr)
    for i in range(N):
        if i % 2 == 0:
            right = difference(right, L.thread_v(i, -1, 1, wl + 2 * gap))
        else:
            left[i] = difference(left[i], L.thread_u(0, i - 1, i + 1, wr + 2 * gap))
    t = union(*left.values(), right)
    d1, d2 = norm(L.e1), norm(L.e2)
    pl = add(L.P(0, N - 1), mul(perp(d1), wl / 2))
    pr = add(L.P(0, 0), mul(perp(d2), -wr / 2))
    centre = L.P(0, 1)
    c = intersection(keep(pl, d1, centre), keep(pr, d2, centre))
    ytop = -K * 46
    c = intersection(c, keep((0, ytop), (1, 0), (centre[0], ytop + 10)))
    return [(intersection(t, c), EM)]


def E_knot():
    L = Lattice((0, 0), 90, 0.42)
    N, K, w = 2, 4, 13
    t = threads(L, N, N, K, w, gap=9)
    clip = v_clip(L, N, w, -K * 90)
    t = intersection(t, clip)
    jewel = L.cell(0, 0, inset=w / 2 + 9)
    return [(t, EM), (jewel, GO)]


def pave_cells(N, K):
    cells = set()
    for j in range(N):
        for i in range(-K, N):
            cells.add((i, j))
    for i in range(N):
        for j in range(-K, N):
            cells.add((i, j))
    return cells


def F_pave():
    L = Lattice((0, 0), 60, 0.42)
    cells = pave_cells(2, 4)
    return [(union(*[L.cell(i, j, inset=3.2) for (i, j) in cells]), EM)]


def G_pave_flat():
    L = Lattice((0, 0), 60, 0.42)
    cells = pave_cells(2, 6)
    p = union(*[L.cell(i, j, inset=3.2) for (i, j) in cells])
    ytop = -4.6 * 60
    p = intersection(p, keep((0, ytop), (1, 0), (0, 0)))
    return [(p, EM)]


def H_pave_gold_tip():
    L = Lattice((0, 0), 60, 0.42)
    cells = pave_cells(2, 4)
    tip = (1, 1)
    em = union(*[L.cell(i, j, inset=3.2) for (i, j) in cells if (i, j) != tip])
    return [(em, EM), (L.cell(*tip, inset=3.2), GO)]


def I_field():
    """V emerging from a hairline net: V cells are stones, the rest is the net."""
    L = Lattice((0, 0), 60, 0.42)
    cells = pave_cells(2, 3)
    us = range(-3, 3)
    parts = []
    # net hairlines over the diamond field u,v in [-3,2]
    for k in range(-3, 3):
        parts.append(seg(L.P(k, -3), L.P(k, 2), 2.0))
        parts.append(seg(L.P(-3, k), L.P(2, k), 2.0))
    parts.append(seg(L.P(-3, 2), L.P(2, 2), 2.0))
    parts.append(seg(L.P(2, -3), L.P(2, 2), 2.0))
    net = union(*parts)
    stones = union(*[L.cell(i, j, inset=4.5) for (i, j) in cells])
    return [(union(net, stones), EM)]


def J_vi():
    """V of two jewelled threads + an I: a vertical column of jewels through the crotch."""
    L = Lattice((0, 0), 60, 0.42)
    N, K, w = 2, 5, 3.2
    t = threads(L, N, N, K, w, weave=False)
    clip = v_clip(L, N, w, -K * 60)
    t = intersection(t, clip)
    js = [L.jewel(u, v, 16) for u in range(N) for v in range(N)]
    # I: jewels stacked on the axis above the crotch
    col = [L.jewel(-k, -k, 16) for k in range(1, 5)]
    return [(union(t, *js), EM), (union(*col), GO)]


VARS = [A_woven, B_jewelled, C_jaal, D_didone, E_knot, F_pave, G_pave_flat, H_pave_gold_tip, I_field, J_vi]


def render_all():
    files = []
    for fn in VARS:
        layers = fn()
        allp = union(*[p for p, _ in layers])
        x0, y0, x1, y1 = bounds(allp)
        k = 700 / max(x1 - x0, y1 - y0)
        tx, ty = 500 - (x0 + x1) / 2 * k, 500 - (y0 + y1) / 2 * k
        body = ''.join(fill(transform(p, k, 0, 0, k, tx, ty), c) for p, c in layers)
        f = os.path.join(OUT, f'{fn.__name__}.svg')
        write_svg(f, 1000, 1000, body, IV)
        files.append(f)
    subprocess.run(['node', os.path.join(SCRATCH, 'logo2/toolkit/render.js'), 'sheet',
                    os.path.join(HERE, 'explore.png'), *files], check=True)


if __name__ == '__main__':
    render_all()
