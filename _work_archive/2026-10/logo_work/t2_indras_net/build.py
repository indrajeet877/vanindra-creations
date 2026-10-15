"""Build every deliverable for concept t2 'Indra's Net' — One Thread, Many Jewels.

Run:  logo_venv/bin/python build.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mark import *  # noqa: F401,F403,E402
from wordmark import setline  # noqa: E402
from vtype import glyph_paths  # noqa: E402

EM, IV, GO, GL, WH = PALETTE['emerald'], PALETTE['ivory'], PALETTE['gold'], PALETTE['gold_lt'], PALETTE['white']
RENDER = os.path.join(SCRATCH, 'logo2', 'toolkit', 'render.js')

# ---------------------------------------------------------------- the grid
# s = tan(half-angle of the V) = horizontal/vertical half-diagonal ratio of every cell; h = half cell height.
P = dict(s=0.40, h=60.0, K=5, NL=2, g=4.0, tw=12.0, gold=((-1, 0),))
# small-size master (<= 48 px): same lattice and construction; the strap's stones are merged into one solid
# lozenge-ended strap (4 rows), the thread is heavier, the junction light-line is kept; one colour.
SMALL = dict(s=0.40, h=60.0, K=4, NL=2, g=7.0, tw=20.0, gold=(), small=True, tw_small=20.0, split=0.0, fuse=False)

WM = dict(
    main=dict(text='VANINDRA', tracking=0.235, pairs={('V', 'A'): -0.085, ('R', 'A'): -0.05, ('A', 'N'): -0.025,
                                                      ('N', 'I'): 0.01, ('I', 'N'): 0.01, ('D', 'R'): 0.01},
              family='tenor-sans', weight=400),
    sub=dict(text='CREATIONS', tracking=0.50, pairs={('A', 'T'): -0.05, ('T', 'I'): -0.02, ('E', 'A'): -0.02},
             family='tenor-sans', weight=400),
)


def cap_height(fontkw):
    kw = {k: v for k, v in fontkw.items() if k not in ('text', 'tracking', 'pairs')}
    b = bounds(glyph_paths('H', size=100, **kw)[0].path)
    return (b[3] - b[1]) / 100.0


def make_wordmark(cap=100.0, sub_ratio=0.40, gap_ratio=0.62, justify=True):
    """Two-line wordmark; cap line of VANINDRA at y=0. CREATIONS is justified to VANINDRA's width."""
    m, s = dict(WM['main']), dict(WM['sub'])
    msz = cap / cap_height(m)
    mp, mw = setline(m.pop('text'), msz, m.pop('tracking'), m.pop('pairs'), **m)
    mp = transform(mp, 1, 0, 0, 1, 0, cap)
    scap = cap * sub_ratio
    ssz = scap / cap_height(s)
    st, strk, spairs = s.pop('text'), s.pop('tracking'), s.pop('pairs')
    sp, sw = setline(st, ssz, strk, spairs, **s)
    if justify:
        extra = (mw - sw) / (len(st) - 1) / ssz
        sp, sw = setline(st, ssz, strk + extra, spairs, **s)
    base2 = cap + cap * gap_ratio + scap
    sp = transform(sp, 1, 0, 0, 1, (mw - sw) / 2, base2)
    return dict(main=mp, sub=sp, w=max(mw, sw), top=0.0, bottom=base2)


def mark_paths(small=False):
    r = build2(**(SMALL if small else P))
    return r['em'], r['au']


def body_of(layers):
    return ''.join(fill(p, c) for p, c in layers if p is not None)


def save(name, w, h, layers, bg=None, extra=''):
    f = os.path.join(HERE, name)
    write_svg(f, w, h, body_of(layers) + extra, bg)
    return f


def colours(ground):
    return (IV, GL, IV) if ground == 'emerald' else (EM, GO, EM)


def main():
    out = {}
    em, au = mark_paths()
    S = 1000

    # ---------------------------------------------------------------- symbol files
    (e1, a1), _ = place([em, au], S, 720)
    out['mark'] = save('mark.svg', S, S, [(e1, EM), (a1, GO)])
    out['mark_on_ivory'] = save('mark_on_ivory.svg', S, S, [(e1, EM), (a1, GO)], IV)
    (e2, a2), _ = place([em, au], S, 620)
    out['mark_on_emerald'] = save('mark_on_emerald.svg', S, S, [(e2, IV), (a2, GL)], EM)
    out['mark_one_colour_gold'] = save('mark_one_colour_gold.svg', S, S, [(union(e1, a1), GO)])
    out['mark_one_colour_emerald'] = save('mark_one_colour_emerald.svg', S, S, [(union(e1, a1), EM)])
    out['mark_one_colour_ivory'] = save('mark_one_colour_ivory.svg', S, S, [(union(e2, a2), IV)], EM)

    sem, _ = mark_paths(small=True)
    (s1,), _ = place([sem], S, 960)
    out['mark_small'] = save('mark_small.svg', S, S, [(s1, EM)])
    (s2,), _ = place([sem], S, 640)
    out['mark_small_on_emerald'] = save('mark_small_on_emerald.svg', S, S, [(s2, IV)], EM)

    # ---------------------------------------------------------------- wordmark
    wm = make_wordmark(cap=100.0)
    pad = 36
    out['wordmark'] = save('wordmark.svg', wm['w'] + 2 * pad, wm['bottom'] + 2 * pad,
                           [(transform(union(wm['main'], wm['sub']), 1, 0, 0, 1, pad, pad), EM)])

    # ---------------------------------------------------------------- horizontal lockup
    def horizontal(ground):
        mc, ac, tc = colours(ground)
        M = 300.0
        wmh = make_wordmark(cap=M * 0.31, sub_ratio=0.44)
        (pe, pa), _ = place([em, au], 0, M, cx=0, cy=0, optical=0.0)
        mb = bounds(union(pe, pa))
        gap = M * 0.30
        blk = wmh['bottom']
        mx, my = M * 0.22, M * 0.20
        Wd = 2 * mx + (mb[2] - mb[0]) + gap + wmh['w']
        Hd = 2 * my + M
        pe = transform(pe, 1, 0, 0, 1, mx - mb[0], Hd / 2)
        pa = transform(pa, 1, 0, 0, 1, mx - mb[0], Hd / 2)
        t = transform(union(wmh['main'], wmh['sub']), 1, 0, 0, 1, mx + (mb[2] - mb[0]) + gap, Hd / 2 - blk / 2)
        return save(f'lockup_horizontal_on_{ground}.svg', Wd, Hd, [(pe, mc), (pa, ac), (t, tc)],
                    IV if ground == 'ivory' else EM)

    out['lockup_horizontal_on_ivory'] = horizontal('ivory')
    out['lockup_horizontal_on_emerald'] = horizontal('emerald')

    # ---------------------------------------------------------------- stacked lockup
    def stacked(ground):
        mc, ac, tc = colours(ground)
        Wd = Hd = 1000.0
        wmh = make_wordmark(cap=58.0)
        M = 400.0
        (pe, pa), _ = place([em, au], 0, M, cx=0, cy=0)
        gap = M * 0.26
        total = M + gap + wmh['bottom']
        top = (Hd - total) / 2
        pe = transform(pe, 1, 0, 0, 1, Wd / 2, top + M / 2)
        pa = transform(pa, 1, 0, 0, 1, Wd / 2, top + M / 2)
        t = transform(union(wmh['main'], wmh['sub']), 1, 0, 0, 1, (Wd - wmh['w']) / 2, top + M + gap)
        return save(f'lockup_stacked_on_{ground}.svg', Wd, Hd, [(pe, mc), (pa, ac), (t, tc)],
                    IV if ground == 'ivory' else EM)

    out['lockup_stacked_on_ivory'] = stacked('ivory')
    out['lockup_stacked_on_emerald'] = stacked('emerald')

    out['pattern_on_emerald'] = pattern('emerald')
    out['pattern_on_ivory'] = pattern('ivory')
    out['construction'] = construction()

    # ---------------------------------------------------------------- renders
    sheet_files = [out[k] for k in ('mark', 'mark_small', 'wordmark', 'mark_on_ivory', 'mark_on_emerald',
                                    'mark_one_colour_gold', 'lockup_horizontal_on_ivory',
                                    'lockup_horizontal_on_emerald', 'construction', 'lockup_stacked_on_ivory',
                                    'lockup_stacked_on_emerald', 'pattern_on_emerald')]
    subprocess.run(['node', RENDER, 'sheet', os.path.join(HERE, 'sheet.png'), *sheet_files], check=True)
    sem2, _ = mark_paths(small=True)
    (s3,), _ = place([sem2], 1000, 960)
    out['mark_small_ivory'] = save('mark_small_ivory.svg', 1000, 1000, [(s3, IV)])
    a = os.path.join(HERE, 'renders', 'sizes_mark_small.png')
    b = os.path.join(HERE, 'renders', 'sizes_mark_small_ivory.png')
    os.makedirs(os.path.dirname(a), exist_ok=True)
    subprocess.run(['node', RENDER, 'sizes', a, out['mark_small']], check=True)
    subprocess.run(['node', RENDER, 'sizes', b, out['mark_small_ivory']], check=True)
    subprocess.run(['node', os.path.join(HERE, 'sizes_combine.js'), os.path.join(HERE, 'sizes.png'), a, b], check=True)
    subprocess.run(['node', RENDER, 'context', os.path.join(HERE, 'context.png'), out['mark_on_emerald'],
                    out['lockup_horizontal_on_emerald']], check=True)
    for k, f in out.items():
        print(f'{k:32s} {os.path.getsize(f) / 1024:6.1f} KB')


def pattern(ground):
    """The net extended into a surface. The V is not placed ON the net: it is a few cells OF the net filled in.
    Every stone is a net cell and the net's fine threads run exactly through the light-lines between stones; the net
    line that would double the V's thread is interrupted for the thread's length. The tile is an exact period of both
    the net and the motif lattice (motif every n cells along both net directions), so it repeats seamlessly."""
    h, s = 22.0, P['s']
    n = 12                                  # even, so every motif sits identically on the net
    step = 2                                # the net is drawn on every 2nd lattice line
    tile_w, tile_h = 2 * n * s * h, 2 * n * h
    W, H = tile_w * 4, tile_h * 2
    L = Lattice((0.0, 0.0), h, s)
    mc, ac, _ = colours(ground)
    net_c = GL if ground == 'emerald' else GO
    lw = 1.0
    g = P['g'] * h / P['h']
    tw = P['tw'] * h / P['h']
    du, dv = lat_units(L, g)
    twu, _ = lat_units(L, tw)
    v_top = -P['K'] + 2 * du + dv + twu
    rng = 70
    motifs = []
    for a in range(-14, 14):
        for b in range(-14, 14):
            u0, v0 = a * n, b * n
            cx, cy = L.P(u0, v0)
            if -160 < cx < W + 160 and -60 < cy < H + 300:
                motifs.append((u0, v0))
    d_net = []
    for k in range(-rng, rng, step):
        # line u = k (direction e2): break it beside every thread lying on it
        gaps = sorted((v0 + v_top - 0.25, v0) for (u0, v0) in motifs if u0 == k)
        start_v = -rng
        for (g0, g1) in gaps:
            if g0 > start_v:
                d_net.append(to_d(seg(L.P(k, start_v), L.P(k, g0), lw)))
            start_v = max(start_v, g1)
        d_net.append(to_d(seg(L.P(k, start_v), L.P(k, rng), lw)))
        d_net.append(to_d(seg(L.P(-rng, k), L.P(rng, k), lw)))
    d_st, d_au = [], []
    for (u0, v0) in motifs:
        for j in range(2):
            for i in range(-P['K'], 0):
                p = stone(L, u0 + i, v0 + j, g)
                (d_au if (i, j) in P['gold'] else d_st).append(to_d(p))
        d_st.append(to_d(para(L, u0 - du - twu, u0 - du, v0 + v_top, v0 - dv)))
    body = (f'<clipPath id="c"><rect width="{W:g}" height="{H:g}"/></clipPath><g clip-path="url(#c)">'
            f'<path d="{"".join(d_net)}" fill="{net_c}"/>'
            f'<path d="{"".join(d_st)}" fill="{mc}"/><path d="{"".join(d_au)}" fill="{ac}"/></g>')
    f = os.path.join(HERE, f'pattern_on_{ground}.svg')
    write_svg(f, W, H, body, EM if ground == 'emerald' else IV)
    return f


def label(text, x, y, size=19, color='#5E5A50'):
    t = text_path(text, family='jost', weight=400, size=size, x=x, y=y, tracking=0.06)
    return f'<path d="{t.d}" fill="{color}"/>'


def construction():
    """Construction drawing on the lattice."""
    W = H = 1000.0
    r = build2(**P)
    L = r['L']
    em, au = r['em'], r['au']
    k = 600 / (bounds(union(em, au))[3] - bounds(union(em, au))[1])
    b0 = bounds(union(em, au))
    tx = W / 2 - (b0[0] + b0[2]) / 2 * k
    ty = 470 - (b0[1] + b0[3]) / 2 * k
    T = lambda p: transform(p, k, 0, 0, k, tx, ty)  # noqa: E731
    lw = 1.0 / k
    grid = []
    for q in range(-14, 10):
        grid.append(seg(L.P(q, -14), L.P(q, 10), lw))
        grid.append(seg(L.P(-14, q), L.P(10, q), lw))
    box = poly([(60, 60), (940, 60), (940, 880), (60, 880)])
    grid = intersection(T(union(*grid)), box)
    du, dv = lat_units(L, P['g'])
    # thread's outer edge, extended through the lower facets to the vertex
    guide = intersection(T(seg(L.P(-du, -9), L.P(-du, 4), 1.6 / k)), box)
    # cap line and vertex line
    top_y = (bounds(T(em))[1])
    bot_y = (bounds(T(union(em, au)))[3])
    hl = union(poly([(60, top_y - .8), (940, top_y - .8), (940, top_y + .8), (60, top_y + .8)]),
               poly([(60, bot_y - .8), (940, bot_y - .8), (940, bot_y + .8), (60, bot_y + .8)]))
    layers = [(grid, '#D8CDB4'), (hl, '#B9AE96'), (T(em), EM), (T(au), GO), (guide, '#B0412E')]
    txt = (label('LATTICE  s = tan(half-angle) = 0.40  ·  every stone is one cell', 60, 930) +
           label('LIGHT-LINE = 2g  ·  THREAD EDGE RUNS ON THE STONES\' LOWER FACETS TO THE VERTEX', 60, 958))
    return save('construction.svg', W, H, layers, IV, extra=txt)


if __name__ == '__main__':
    main()
