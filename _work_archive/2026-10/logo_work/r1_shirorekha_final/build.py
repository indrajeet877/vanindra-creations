"""VanIndra Creations - Round 3 Shirorekha (final). Generates every deliverable from r3system's parameters.
Run: <venv>/bin/python build.py"""
import subprocess, sys
from r3system import *

TOOL = os.path.join(SCRATCH, 'logo2', 'toolkit', 'render.js')
J = lambda n: os.path.join(HERE, n)


def place(path, x, y, s=1.0):
    return tr(path, s, x, y)


def optical_square(path, side, box_h, k=0.45, lift=0.0):
    """Scale path to height box_h and centre it in a side x side square. Horizontal centre blends the bbox centre
    with the area centroid (k), because the danda and the line carry the weight on the right/top."""
    x0, y0, x1, y1 = bbox(path)
    s = box_h / (y1 - y0)
    p = tr(path, s, -x0 * s, -y0 * s)
    cx, cy = centroid(p)
    bw, bh = (x1 - x0) * s, (y1 - y0) * s
    tx = (1 - k) * (bw / 2) + k * cx
    ty = 0.75 * (bh / 2) + 0.25 * cy
    return tr(p, 1, side / 2 - tx, side / 2 - ty - lift * side)


# ------------------------------------------------------------------ pieces
def pieces():
    mk, mki = mark()
    mks, _ = mark(small=True)
    wm, tot, st = vanindra(ovl=OVL, ovr=OVR)
    wmh, toth, sth = vanindra('header', ovl=OVL, ovr=OVR)
    return dict(mk=mk, mks=mks, wm=wm, tot=tot, st=st, wmh=wmh, toth=toth, sth=sth)


def full_name(cut='master', k=0.50, gap=32.0, hair=None, bar=True):
    """VANINDRA hangs from the heavy line; the same line steps down to a hairline and CREATIONS hangs from it.
    bar=False -> global: one uniform hairline, both words hang just under it (letters keep their own tops)."""
    hair = HAIR if hair is None else hair
    wm, tot, st = vanindra(cut, bar=bar, ovl=OVL, ovr=0.0)
    cr, totc, stc = creations(bar=False, ovl=0.0, ovr=0.0)
    dy = 0.0 if bar else hair
    crs = tr(cr, k, tot + gap, dy)
    end = tot + gap + totc * k + OVR
    if bar:
        line = U(rect(-OVL, 0, tot, st.b), rect(tot - 1, 0, end, hair))
        letters = U(wm, crs)
    else:
        line = rect(-OVL, 0, end, hair)
        letters = U(tr(wm, 1, 0, dy), crs)
    return letters, line, end


def bilingual(gap=46.0):
    wm, tot, st = vanindra(ovl=OVL, ovr=0.0)
    dv, (dx0, dx1) = devanagari()
    dv = tr(dv, 1, tot + gap - dx0 - 4.0, 0)
    line = rect(-OVL, 0, bbox(dv)[2] + 0.5, st.b)
    return U(wm, dv, line)


# ------------------------------------------------------------------ files
def make_all():
    P = pieces()
    mk, mks, wm, st = P['mk'], P['mks'], P['wm'], P['st']
    f = {}
    # mark (transparent)
    x0, y0, x1, y1 = bbox(mk)
    pad = (y1 - y0) * 0.16
    f['mark.svg'] = write(J('mark.svg'), svg(x1 + 2 * pad, y1 + 2 * pad, [(place(mk, pad, pad), EM)]))
    f['mark_one_colour_gold.svg'] = write(J('mark_one_colour_gold.svg'), svg(x1 + 2 * pad, y1 + 2 * pad, [(place(mk, pad, pad), GO)]))
    # small cut: square, fills ~92%
    side = 100.0
    f['mark_small.svg'] = write(J('mark_small.svg'), svg(side, side, [(optical_square(mks, side, 92.0, k=0.40), EM)]))
    f['_mark_small_ivory.svg'] = write(J('_mark_small_ivory.svg'), svg(side, side, [(optical_square(mks, side, 92.0, k=0.40), IV)]))
    # avatar squares
    S = 512
    f['mark_on_ivory.svg'] = write(J('mark_on_ivory.svg'), svg(S, S, [(optical_square(mk, S, S * 0.54), EM)], bg=IV))
    f['mark_on_emerald.svg'] = write(J('mark_on_emerald.svg'), svg(S, S, [(optical_square(mk, S, S * 0.54), GL)], bg=EM))
    # wordmark (master) and header cut
    wb = bbox(wm)
    wpad = 34
    f['wordmark.svg'] = write(J('wordmark.svg'), svg(wb[2] - wb[0] + 2 * wpad, wb[3] + 2 * wpad, [(place(wm, wpad - wb[0], wpad), EM)]))
    hb = bbox(P['wmh'])
    f['wordmark_header.svg'] = write(J('wordmark_header.svg'), svg(hb[2] - hb[0] + 2 * wpad, hb[3] + 2 * wpad, [(place(P['wmh'], wpad - hb[0], wpad), EM)]))
    # horizontal lockup: one line, VANINDRA + CREATIONS (no mark -> no repeated initial)
    letters, line, end = full_name()
    lb = bbox(U(letters, line))
    m = 46
    W, H = lb[2] - lb[0] + 2 * m, lb[3] - lb[1] + 2 * m
    ox, oy = m - lb[0], m - lb[1]
    def horiz(bg, c_word, c_line):
        return svg(W, H, [(place(line, ox, oy), c_line), (place(letters, ox, oy), c_word)], bg=bg)
    f['lockup_horizontal_on_ivory.svg'] = write(J('lockup_horizontal_on_ivory.svg'), horiz(IV, EM, EM))
    f['lockup_horizontal_on_emerald.svg'] = write(J('lockup_horizontal_on_emerald.svg'), horiz(EM, IV, IV))
    f['_h_ivoryink.svg'] = write(J('_h_ivoryink.svg'), horiz(None, IV, IV))
    f['_h_emeraldink.svg'] = write(J('_h_emeraldink.svg'), horiz(None, EM, EM))
    hl, hline, _ = full_name('header', k=0.52, gap=34.0, hair=HAIR * 1.25)
    hb2 = bbox(U(hl, hline))
    Wh, Hh = hb2[2] - hb2[0] + 2 * m, hb2[3] - hb2[1] + 2 * m
    f['lockup_horizontal_header.svg'] = write(J('lockup_horizontal_header.svg'), svg(Wh, Hh, [(place(U(hl, hline), m - hb2[0], m - hb2[1]), EM)]))
    # stacked lockup: mark over VANINDRA (vertical repetition only)
    km = 1.85
    mk_s = tr(mk, km)
    mb = bbox(mk_s)
    gap1 = 64
    tot_w = max(wb[2] - wb[0], mb[2])
    mS = 90
    Wst = tot_w + 2 * mS
    Hst = mb[3] + gap1 + wb[3] + 2 * mS
    cxm, _ = centroid(mk_s)
    ox_m = 0.45 * cxm + 0.55 * (mb[2] / 2)
    mk_pos = place(mk_s, Wst / 2 - ox_m, mS)
    wm_pos = place(wm, (Wst - (wb[2] - wb[0])) / 2 - wb[0], mS + mb[3] + gap1)
    def stacked(bg, c_mark, c_word):
        return svg(Wst, Hst, [(mk_pos, c_mark), (wm_pos, c_word)], bg=bg)
    f['lockup_stacked_on_ivory.svg'] = write(J('lockup_stacked_on_ivory.svg'), stacked(IV, EM, EM))
    f['lockup_stacked_on_emerald.svg'] = write(J('lockup_stacked_on_emerald.svg'), stacked(EM, GL, IV))
    # bilingual (optional line; Devanagari to be verified by the team)
    bl = bilingual()
    bb = bbox(bl)
    m2 = 46
    Wb, Hb = bb[2] - bb[0] + 2 * m2, bb[3] - bb[1] + 2 * m2
    f['lockup_bilingual_on_ivory.svg'] = write(J('lockup_bilingual_on_ivory.svg'), svg(Wb, Hb, [(place(bl, m2 - bb[0], m2 - bb[1]), EM)], bg=IV))
    f['lockup_bilingual_on_emerald.svg'] = write(J('lockup_bilingual_on_emerald.svg'), svg(Wb, Hb, [(place(bl, m2 - bb[0], m2 - bb[1]), IV)], bg=EM))
    dv, _ = devanagari()
    db = bbox(dv)
    f['wordmark_devanagari.svg'] = write(J('wordmark_devanagari.svg'), svg(db[2] - db[0] + 2 * m2, db[3] - db[1] + 2 * m2, [(place(dv, m2 - db[0], m2 - db[1]), EM)]))
    # global (USD workspace): same capitals, no headline bar; both words hang from one gold hairline
    gl_letters, gl_line, gl_end = full_name(bar=False)
    gb = bbox(U(gl_letters, gl_line))
    Wg, Hg = gb[2] - gb[0] + 2 * m, gb[3] - gb[1] + 2 * m
    gx, gy = m - gb[0], m - gb[1]
    f['global.svg'] = write(J('global.svg'), svg(Wg, Hg, [(place(gl_letters, gx, gy), EM), (place(gl_line, gx, gy), GO)], bg=IV))
    f['global_on_emerald.svg'] = write(J('global_on_emerald.svg'), svg(Wg, Hg, [(place(gl_letters, gx, gy), IV), (place(gl_line, gx, gy), GL)], bg=EM))
    f['global_one_colour.svg'] = write(J('global_one_colour.svg'), svg(Wg, Hg, [(place(gl_letters, gx, gy), EM), (place(gl_line, gx, gy), EM)]))
    gh_letters, gh_line, _ = full_name('header', k=0.52, gap=34.0, hair=HAIR * 1.4, bar=False)
    ghb = bbox(U(gh_letters, gh_line))
    f['global_header.svg'] = write(J('global_header.svg'), svg(ghb[2] - ghb[0] + 2 * m, ghb[3] - ghb[1] + 2 * m,
                                   [(place(gh_letters, m - ghb[0], m - ghb[1]), EM), (place(gh_line, m - ghb[0], m - ghb[1]), GO)]))
    gw, gtot, gst = vanindra(bar=False, ovl=OVL, ovr=OVR)
    gw_line = rect(-OVL, 0, gtot + OVR, HAIR)
    gw = tr(gw, 1, 0, HAIR)
    gwb = bbox(U(gw, gw_line))
    f['global_wordmark.svg'] = write(J('global_wordmark.svg'), svg(gwb[2] - gwb[0] + 2 * wpad, gwb[3] + 2 * wpad,
                                     [(place(gw, wpad - gwb[0], wpad), EM), (place(gw_line, wpad - gwb[0], wpad), GO)]))
    return f


ORDER = ['mark.svg', 'mark_small.svg', 'wordmark.svg', 'mark_on_ivory.svg', 'mark_on_emerald.svg', 'mark_one_colour_gold.svg',
         'lockup_horizontal_on_ivory.svg', 'lockup_horizontal_on_emerald.svg', 'lockup_stacked_on_ivory.svg',
         'lockup_stacked_on_emerald.svg', 'lockup_bilingual_on_ivory.svg', 'global.svg']


def render(f, tag=''):
    R = ['node', TOOL]
    C = ['node', J('compose.js')]
    subprocess.run(R + ['sheet', J(f'sheet{tag}.png')] + [f[k] for k in ORDER], check=True)
    subprocess.run(R + ['sizes', J('_sizes_a.png'), f['mark_small.svg']], check=True)
    subprocess.run(R + ['sizes', J('_sizes_b.png'), f['_mark_small_ivory.svg']], check=True)
    subprocess.run(C + [J('_sizes_a.png'), J('_sizes_b.png'), '168', J(f'sizes{tag}.png')], check=True)
    subprocess.run(R + ['context', J('_ctx_a.png'), f['mark_on_emerald.svg'], f['_h_ivoryink.svg']], check=True)
    subprocess.run(R + ['context', J('_ctx_b.png'), f['mark_on_emerald.svg'], f['_h_emeraldink.svg']], check=True)
    subprocess.run(C + [J('_ctx_a.png'), J('_ctx_b.png'), '312', J(f'context{tag}.png')], check=True)
    subprocess.run(R + ['png', f['global.svg'], J('global.png'), '1400'], check=True)
    for n in ('_sizes_a.png', '_sizes_b.png', '_ctx_a.png', '_ctx_b.png'):
        os.remove(J(n))


if __name__ == '__main__':
    f = make_all()
    tag = sys.argv[1] if len(sys.argv) > 1 else ''
    render(f, tag)
    for k in sorted(f):
        print(k, os.path.getsize(f[k]))
