"""VanIndra Creations - Shirorekha final-final. Generates every deliverable from r4system's parameters.
Run: <venv>/bin/python build2.py"""
import subprocess, sys
from r4system import *
import r4system as R
import r4deva
from r3latin import St, g_V

TOOL = os.path.join(SCRATCH, 'logo2', 'toolkit', 'render.js')
J = lambda n: os.path.join(HERE, n)


def place(path, x, y, s=1.0):
    return tr(path, s, x, y)


def optical_square(path, side, box_h, k=0.45):
    """Scale to height box_h and centre in a side x side square; the horizontal centre blends the bbox centre with
    the area centroid (k) because the danda and the line carry the weight on the right / top."""
    x0, y0, x1, y1 = bbox(path)
    s = box_h / (y1 - y0)
    p = tr(path, s, -x0 * s, -y0 * s)
    cx, cy = centroid(p)
    bw, bh = (x1 - x0) * s, (y1 - y0) * s
    tx = (1 - k) * (bw / 2) + k * cx
    ty = 0.75 * (bh / 2) + 0.25 * cy
    return tr(p, 1, side / 2 - tx, side / 2 - ty)


# ------------------------------------------------------------------ global avatar: the line, and a V hanging from it
GV = dict(b=11.0, h=13.0, W=70.0, t0=11.0, ko1=6.0, ko2=5.0, ki1=-3.0, ki2=-20.0, o=2.0)
GVS = dict(b=16.0, h=18.0, W=84.0, t0=16.0, ko1=6.0, ko2=5.0, ki1=-2.0, ki2=-24.0, o=2.0)


def v_global(p):
    st = St(H=100, b=p['b'], S=16, h=p['h'], ns=12, t0=p['t0'], Tf=20, o=p['o'],
            vleaf=dict(t0=p['t0'], ko1=p['ko1'], ko2=p['ko2'], ki1=p['ki1'], ki2=p['ki2']))
    g, w = g_V(st, W=p['W'])
    return g, w


def avatar_global(side, ink, bg, small=False):
    """Full-bleed line across the square (it runs off both edges of the circle crop) and the V hanging from it."""
    p = GVS if small else GV
    v, w = v_global(p)
    fill = 0.80 if small else 0.54
    s = side * fill / 101.0
    vh = 101.0 * s
    y0 = side / 2 - vh / 2 - (0.02 * side)
    g = tr(v, s, side / 2 - w * s / 2, y0)
    line = rect(0, y0, side, y0 + p['b'] * s)
    return svg(side, side, [(U(g, line), ink)], bg=bg)


# ------------------------------------------------------------------ pieces
def horizontal(cut='master'):
    letters, line, end = full_name(cut)
    return U(letters, line)


def stacked_parts(km=1.85, gap1=62.0, cre_k=0.44, gap2=40.0):
    mk, _ = mark('lockup')
    wm, tot, st = vanindra('master')
    cr, totc, _ = creations('master')
    mk_s = tr(mk, km)
    mb = bbox(mk_s)
    wb = bbox(wm)
    crs = tr(cr, cre_k)
    cb = bbox(crs)
    mS = 90.0
    tot_w = max(wb[2] - wb[0], mb[2], cb[2])
    Wst = tot_w + 2 * mS
    cxm, _ = centroid(mk_s)
    ox_m = 0.45 * cxm + 0.55 * (mb[2] / 2)
    y_w = mS + mb[3] + gap1
    y_c = y_w + 100.0 + gap2
    mk_pos = place(mk_s, Wst / 2 - ox_m, mS)
    wm_pos = place(wm, (Wst - (wb[2] - wb[0])) / 2 - wb[0], y_w)
    cr_pos = place(crs, (Wst - (cb[2] - cb[0])) / 2 - cb[0], y_c)
    Hst = y_c + cb[3] + mS
    return mk_pos, U(wm_pos, cr_pos), Wst, Hst


def bilingual(gap=46.0):
    wm, tot, st = vanindra('master', ovl=OVL, ovr=0.0)
    dv, (dx0, dx1) = r4deva.devanagari_word()
    dv = tr(dv, 1, tot + gap - dx0 - 4.0, 0)
    line = rect(-OVL, 0, bbox(dv)[2] + 0.5, st.b)
    return U(wm, dv, line)


def global_parts(cut='master', hair=None):
    """Global: one uniform gold hairline over both words; VANINDRA's caps hang from it (overlap 55% of the hairline
    so they visibly touch, no anti-alias seam). CREATIONS stands on VANINDRA's baseline."""
    hair = (HAIR if cut == 'master' else HAIR_ST) if hair is None else hair
    wm, tot, st = vanindra(cut, bar=False, ovl=OVL, ovr=0.0)
    cr, totc, _ = creations(cut)
    dy = hair * 0.45
    gap = 36.0
    letters = U(tr(wm, 1, 0, dy), tr(cr, CRE_K, tot + gap, dy + 100.0 * (1 - CRE_K)))
    end = tot + gap + totc * CRE_K + OVR
    line = rect(-OVL, 0, end, hair)
    return letters, line


def phone_wordmark(cap=17.0):
    """Pixel-fitted cut for a 17 px cap: every letter origin, stem and the line land on whole pixels."""
    g = 100.0 / cap
    old = dict(R.STURDY)
    R.STURDY.update(S=3 * g, ns=2 * g, b=2 * g)
    _, tot0, _ = vanindra('sturdy', bar=False, grid=g, widths={'N': 12 * g})
    end_px = math.ceil(tot0 / g + 1.0)                     # the line ends on a whole pixel, >= 1 px past the A
    wm, tot, st = vanindra('sturdy', grid=g, widths={'N': 12 * g}, ovl=g, ovr=end_px * g - tot0)
    R.STURDY.clear(); R.STURDY.update(old)
    return wm, tot


# ------------------------------------------------------------------ files
def make_all():
    f = {}
    mk, _ = mark('master')
    mks, _ = mark('small')
    mkl, _ = mark('lockup')
    # mark (transparent)
    x0, y0, x1, y1 = bbox(mk)
    pad = (y1 - y0) * 0.16
    f['mark.svg'] = write(J('mark.svg'), svg(x1 + 2 * pad, y1 + 2 * pad, [(place(mk, pad, pad), EM)]))
    f['mark_one_colour_gold.svg'] = write(J('mark_one_colour_gold.svg'), svg(x1 + 2 * pad, y1 + 2 * pad, [(place(mk, pad, pad), GO)]))
    lx0, ly0, lx1, ly1 = bbox(mkl)
    lpad = (ly1 - ly0) * 0.16
    f['mark_lockup.svg'] = write(J('mark_lockup.svg'), svg(lx1 + 2 * lpad, ly1 + 2 * lpad, [(place(mkl, lpad, lpad), EM)]))
    side = 100.0
    f['mark_small.svg'] = write(J('mark_small.svg'), svg(side, side, [(optical_square(mks, side, 92.0, k=0.40), EM)]))
    f['_mark_small_ivory.svg'] = write(J('_mark_small_ivory.svg'), svg(side, side, [(optical_square(mks, side, 92.0, k=0.40), IV)]))
    S = 512
    f['mark_on_ivory.svg'] = write(J('mark_on_ivory.svg'), svg(S, S, [(optical_square(mk, S, S * 0.54), EM)], bg=IV))
    f['mark_on_emerald.svg'] = write(J('mark_on_emerald.svg'), svg(S, S, [(optical_square(mk, S, S * 0.54), GL)], bg=EM))
    # global avatar (Latin-led): the line + V
    f['mark_global_on_emerald.svg'] = write(J('mark_global_on_emerald.svg'), avatar_global(S, GL, EM))
    f['mark_global_on_ivory.svg'] = write(J('mark_global_on_ivory.svg'), avatar_global(S, EM, IV))
    f['mark_global_small.svg'] = write(J('mark_global_small.svg'), avatar_global(100, EM, None, small=True))
    f['_mark_global_small_ivory.svg'] = write(J('_mark_global_small_ivory.svg'), avatar_global(100, IV, None, small=True))
    # wordmarks
    wpad = 34
    wm, tot, st = vanindra('master')
    wb = bbox(wm)
    f['wordmark.svg'] = write(J('wordmark.svg'), svg(wb[2] - wb[0] + 2 * wpad, wb[3] + 2 * wpad, [(place(wm, wpad - wb[0], wpad), EM)]))
    wh, toth, sth = vanindra('sturdy')
    hb = bbox(wh)
    f['wordmark_header.svg'] = write(J('wordmark_header.svg'), svg(hb[2] - hb[0] + 2 * wpad, hb[3] + 2 * wpad, [(place(wh, wpad - hb[0], wpad), EM)]))
    # phone cut, drawn at exactly 17 px cap: viewBox in px so 1 unit = 1 px when used at its natural size
    pw, ptot = phone_wordmark(17.0)
    u = 0.17
    pb = bbox(tr(pw, u))
    f['wordmark_phone_17px.svg'] = write(J('wordmark_phone_17px.svg'), svg(round(pb[2] - pb[0]) + 2, 19, [(place(tr(pw, u), 1 - round(pb[0]), 0), EM)]))
    # horizontal lockups (master and sturdy/header)
    m = 46
    hz = horizontal('master')
    lb = bbox(hz)
    W, H = lb[2] - lb[0] + 2 * m, lb[3] - lb[1] + 2 * m
    ox, oy = m - lb[0], m - lb[1]
    f['lockup_horizontal_on_ivory.svg'] = write(J('lockup_horizontal_on_ivory.svg'), svg(W, H, [(place(hz, ox, oy), EM)], bg=IV))
    f['lockup_horizontal_on_emerald.svg'] = write(J('lockup_horizontal_on_emerald.svg'), svg(W, H, [(place(hz, ox, oy), IV)], bg=EM))
    hh = horizontal('sturdy')
    hb2 = bbox(hh)
    Wh, Hh = hb2[2] - hb2[0] + 2 * m, hb2[3] - hb2[1] + 2 * m
    f['lockup_horizontal_header.svg'] = write(J('lockup_horizontal_header.svg'), svg(Wh, Hh, [(place(hh, m - hb2[0], m - hb2[1]), EM)]))
    f['_h_ivoryink.svg'] = write(J('_h_ivoryink.svg'), svg(Wh, Hh, [(place(hh, m - hb2[0], m - hb2[1]), IV)]))
    f['_h_emeraldink.svg'] = write(J('_h_emeraldink.svg'), svg(Wh, Hh, [(place(hh, m - hb2[0], m - hb2[1]), EM)]))
    # stacked: lockup cut of the mark (drawn at the wordmark's weights) over VANINDRA over CREATIONS
    mk_pos, words, Wst, Hst = stacked_parts()
    f['lockup_stacked_on_ivory.svg'] = write(J('lockup_stacked_on_ivory.svg'), svg(Wst, Hst, [(mk_pos, EM), (words, EM)], bg=IV))
    f['lockup_stacked_on_emerald.svg'] = write(J('lockup_stacked_on_emerald.svg'), svg(Wst, Hst, [(mk_pos, GL), (words, IV)], bg=EM))
    # bilingual + Devanagari
    bl = bilingual()
    bb = bbox(bl)
    m2 = 46
    Wb, Hb = bb[2] - bb[0] + 2 * m2, bb[3] - bb[1] + 2 * m2
    f['lockup_bilingual_on_ivory.svg'] = write(J('lockup_bilingual_on_ivory.svg'), svg(Wb, Hb, [(place(bl, m2 - bb[0], m2 - bb[1]), EM)], bg=IV))
    f['lockup_bilingual_on_emerald.svg'] = write(J('lockup_bilingual_on_emerald.svg'), svg(Wb, Hb, [(place(bl, m2 - bb[0], m2 - bb[1]), IV)], bg=EM))
    dv, _ = r4deva.devanagari_word()
    db = bbox(dv)
    f['wordmark_devanagari.svg'] = write(J('wordmark_devanagari.svg'), svg(db[2] - db[0] + 2 * m2, db[3] - db[1] + 2 * m2, [(place(dv, m2 - db[0], m2 - db[1]), EM)]))
    # global
    gl, gline = global_parts('master')
    gb = bbox(U(gl, gline))
    Wg, Hg = gb[2] - gb[0] + 2 * m, gb[3] - gb[1] + 2 * m
    gx, gy = m - gb[0], m - gb[1]
    f['global.svg'] = write(J('global.svg'), svg(Wg, Hg, [(place(gl, gx, gy), EM), (place(gline, gx, gy), GO)], bg=IV))
    f['global_on_emerald.svg'] = write(J('global_on_emerald.svg'), svg(Wg, Hg, [(place(gl, gx, gy), IV), (place(gline, gx, gy), GL)], bg=EM))
    f['global_one_colour.svg'] = write(J('global_one_colour.svg'), svg(Wg, Hg, [(place(U(gl, gline), gx, gy), EM)]))
    ghl, ghline = global_parts('sturdy')
    ghb = bbox(U(ghl, ghline))
    f['global_header.svg'] = write(J('global_header.svg'), svg(ghb[2] - ghb[0] + 2 * m, ghb[3] - ghb[1] + 2 * m,
                                   [(place(ghl, m - ghb[0], m - ghb[1]), EM), (place(ghline, m - ghb[0], m - ghb[1]), GO)]))
    gw, gtot, gst = vanindra('master', bar=False)
    gw_line = rect(-OVL, 0, gtot + OVR, HAIR)
    gw = tr(gw, 1, 0, HAIR * 0.45)
    gwb = bbox(U(gw, gw_line))
    f['global_wordmark.svg'] = write(J('global_wordmark.svg'), svg(gwb[2] - gwb[0] + 2 * wpad, gwb[3] + 2 * wpad,
                                     [(place(gw, wpad - gwb[0], wpad), EM), (place(gw_line, wpad - gwb[0], wpad), GO)]))
    return f


ORDER = ['mark.svg', 'mark_small.svg', 'wordmark.svg', 'mark_on_ivory.svg', 'mark_on_emerald.svg', 'mark_one_colour_gold.svg',
         'lockup_horizontal_on_ivory.svg', 'lockup_horizontal_on_emerald.svg', 'lockup_stacked_on_ivory.svg',
         'lockup_stacked_on_emerald.svg', 'lockup_bilingual_on_ivory.svg', 'global.svg',
         'mark_global_on_emerald.svg', 'wordmark_header.svg', 'mark_lockup.svg']


def render(f, tag=''):
    Rn = ['node', TOOL]
    C = ['node', J('compose.js')]
    subprocess.run(Rn + ['sheet', J(f'sheet{tag}.png')] + [f[k] for k in ORDER], check=True)
    subprocess.run(Rn + ['sizes', J('_sizes_a.png'), f['mark_small.svg']], check=True)
    subprocess.run(Rn + ['sizes', J('_sizes_b.png'), f['_mark_small_ivory.svg']], check=True)
    subprocess.run(C + [J('_sizes_a.png'), J('_sizes_b.png'), '168', J(f'sizes{tag}.png')], check=True)
    subprocess.run(Rn + ['sizes', J('_sizes_a.png'), f['mark_global_small.svg']], check=True)
    subprocess.run(Rn + ['sizes', J('_sizes_b.png'), f['_mark_global_small_ivory.svg']], check=True)
    subprocess.run(C + [J('_sizes_a.png'), J('_sizes_b.png'), '168', J(f'sizes_global{tag}.png')], check=True)
    subprocess.run(Rn + ['context', J('_ctx_a.png'), f['mark_on_emerald.svg'], f['_h_ivoryink.svg']], check=True)
    subprocess.run(Rn + ['context', J('_ctx_b.png'), f['mark_on_emerald.svg'], f['_h_emeraldink.svg']], check=True)
    subprocess.run(C + [J('_ctx_a.png'), J('_ctx_b.png'), '312', J(f'context{tag}.png')], check=True)
    subprocess.run(Rn + ['context', J('_ctx_a.png'), f['mark_global_on_emerald.svg'], f['_h_ivoryink.svg']], check=True)
    subprocess.run(Rn + ['context', J('_ctx_b.png'), f['mark_global_on_emerald.svg'], f['_h_emeraldink.svg']], check=True)
    subprocess.run(C + [J('_ctx_a.png'), J('_ctx_b.png'), '312', J(f'context_global{tag}.png')], check=True)
    subprocess.run(Rn + ['png', f['global.svg'], J(f'global{tag}.png'), '1400'], check=True)
    for n in ('_sizes_a.png', '_sizes_b.png', '_ctx_a.png', '_ctx_b.png'):
        os.remove(J(n))


if __name__ == '__main__':
    f = make_all()
    tag = sys.argv[1] if len(sys.argv) > 1 else ''
    render(f, tag)
    for k in sorted(f):
        print(k, os.path.getsize(f[k]))
