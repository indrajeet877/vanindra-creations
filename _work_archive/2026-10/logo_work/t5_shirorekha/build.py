"""VanIndra Creations — Shirorekha identity. Generates every deliverable from one parameter set."""
import os, subprocess, json
from geo import *
import letters2
from letters2 import St, wordmark, g_V3, g_A, g_N, g_I, g_D, g_R
from mono2 import va2

HERE = os.path.dirname(os.path.abspath(__file__))
EM, IV, GO, GL, WH = PAL['emerald'], PAL['ivory'], PAL['gold'], PAL['gold_lt'], PAL['white']

# ------------------------------------------------------------------ parameters
P = dict(
    word=dict(H=100, b=8.8, S=14, h=4.0, t0=3.6),
    v_blade=dict(swell=-22, bo=7),
    spacing={('V', 'A'): -9.0, ('A', 'N'): 9.0, ('N', 'I'): 17.0, ('I', 'N'): 17.0, ('N', 'D'): 16.0,
             ('D', 'R'): 13.5, ('R', 'A'): 6.0},
    word_ov=(10, 5),
    mark=dict(bo=12, bi=-15, t0=4.5, py=90, yj=0.5, xs=62, px=37, b=9.6, S=14.5, h=5.0, ovl=11, ovr=7),
    mark_small=dict(bo=10, bi=-10, t0=7.0, py=90, yj=0.52, xs=63, px=36, b=13, S=18, h=8.5, ovl=7, ovr=5),
    desc=dict(family='jost', weight=500, tracking=0.44),
)

def build_word(p=P):
    st = St(**p['word'])
    letters2.BUILD['V'] = lambda st, W=72: g_V3(st, W=W, **p['v_blade'])
    letters2.BUILD['N'] = g_N_flat
    wm, total, spans = wordmark(st, space=p['spacing'], ovl=p['word_ov'][0], ovr=p['word_ov'][1])
    return wm, st

def g_N_flat(st, W=70):
    H, ns = st.H, st.ns
    left = rect(0, 0, ns, H)
    right = rect(W - ns, 0, W, H)
    diag = poly([(0, 0), (ns + st.t0, 0), (W, H), (W - st.Tf * 1.04, H)])
    return I(U(left, right, diag), rect(-2, 0, W + 2, H)), W

def build_mark(small=False, p=P):
    return va2(**(p['mark_small'] if small else p['mark']))[0]

def descriptor(cap_h, p=P):
    """CREATIONS, typeset, scaled so its cap height == cap_h. Returns path with top at y=0."""
    d_ = p['desc']
    t = V.text_path('CREATIONS', family=d_['family'], weight=d_['weight'], size=100, tracking=d_['tracking'])
    x0, y0, x1, y1 = bbox(t.path)
    s = cap_h / (y1 - y0)
    return tr(t.path, s, -x0 * s, -y0 * s)

def norm(path):
    x0, y0, x1, y1 = bbox(path)
    return tr(path, 1, -x0, -y0)

def place(path, x, y, s=1.0):
    return tr(path, s, x, y)

import re as _re
def rd(path):
    return _re.sub(r'-?\d+\.\d+', lambda m: ('%.2f' % float(m.group())).rstrip('0').rstrip('.'), d(path))

def svg(w, h, layers, bg=None, title='VanIndra Creations'):
    body = ''.join(f'<path fill="{c}" d="{rd(p)}"/>' for p, c in layers)
    return V.svg_doc(round(w, 2), round(h, 2), body, bg=bg, title=title)

def write(name, content):
    with open(os.path.join(HERE, name), 'w') as f:
        f.write(content)
    return os.path.join(HERE, name)

def fit_center(path, W, H, box_h=None, box_w=None, dy=0.0, dx=0.0):
    x0, y0, x1, y1 = bbox(path)
    s = min((box_w or 1e9) / (x1 - x0), (box_h or 1e9) / (y1 - y0))
    return tr(path, s, (W - (x1 - x0) * s) / 2 - x0 * s + dx, (H - (y1 - y0) * s) / 2 - y0 * s + dy)

def centroid(path):
    from fontTools.pens.statisticsPen import StatisticsPen
    pen = StatisticsPen()
    path.draw(pen)
    return pen.meanX, pen.meanY

def optical(path, W, H, box_h, k=0.5, lift=0.0):
    """Scale to box_h and centre: horizontal position blends bbox centre and area centroid (k)."""
    x0, y0, x1, y1 = bbox(path)
    s = box_h / (y1 - y0)
    p = tr(path, s, -x0 * s, -y0 * s)
    cx, cy = centroid(p)
    bw, bh = (x1 - x0) * s, (y1 - y0) * s
    tx = (1 - k) * (bw / 2) + k * cx
    return tr(p, 1, W / 2 - tx, (H - bh) / 2 - lift * H)

def make_all(p=P, out_prefix=''):
    wm, st = build_word(p)
    wm = norm(wm)
    mk = norm(build_mark(False, p))
    mks = norm(build_mark(True, p))
    files = {}
    mx0, my0, mx1, my1 = bbox(mk)
    mw, mh = mx1, my1
    pad = mh * 0.18
    files['mark.svg'] = write(out_prefix + 'mark.svg', svg(mw + 2 * pad, mh + 2 * pad, [(place(mk, pad, pad), EM)]))
    sx0, sy0, sx1, sy1 = bbox(mks)
    side = max(sx1, sy1) * 1.05
    files['mark_small.svg'] = write(out_prefix + 'mark_small.svg', svg(side, side, [(optical(mks, side, side, sy1 * 0.985 * min(1, side / 1.05 / sy1), k=0.5), EM)]))
    files['_mark_small_ivory.svg'] = write(out_prefix + '_mark_small_ivory.svg', svg(side, side, [(optical(mks, side, side, sy1 * 0.985 * min(1, side / 1.05 / sy1), k=0.5), IV)]))
    S = 512
    box = S * 0.54
    files['mark_on_ivory.svg'] = write(out_prefix + 'mark_on_ivory.svg', svg(S, S, [(optical(mk, S, S, box, k=0.6, lift=-0.008), EM)], bg=IV))
    files['mark_on_emerald.svg'] = write(out_prefix + 'mark_on_emerald.svg', svg(S, S, [(optical(mk, S, S, box, k=0.6, lift=-0.008), GL)], bg=EM))
    files['mark_one_colour_gold.svg'] = write(out_prefix + 'mark_one_colour_gold.svg', svg(mw + 2 * pad, mh + 2 * pad, [(place(mk, pad, pad), GO)]))
    # wordmark: VANINDRA over CREATIONS
    wx0, wy0, wx1, wy1 = bbox(wm)
    Hw = st.H
    cap = Hw * 0.20
    ds = descriptor(cap, p)
    dx0, dy0, dx1, dy1 = bbox(ds)
    gap = Hw * 0.36
    ds_c = place(ds, (wx1 - dx1) / 2, wy1 + gap)
    wpad = Hw * 0.35
    WW, WH_ = wx1 + 2 * wpad, wy1 + gap + cap + 2 * wpad
    files['wordmark.svg'] = write(out_prefix + 'wordmark.svg', svg(WW, WH_, [(place(wm, wpad, wpad), EM), (place(ds_c, wpad, wpad), GO)]))
    # horizontal lockup: everything hangs from one top line; descriptor sits on the danda's baseline
    Hm = mh
    k = p.get('h_k', 0.58)
    sw = (Hm * k) / Hw
    capH = Hm * p.get('h_cap', 0.155)
    dsH = descriptor(capH, p)
    gx = Hm * p.get('h_gap', 0.36)
    wm_s = place(wm, mw + gx, 0, sw)
    w_right = mw + gx + wx1 * sw
    # descriptor left-aligned with the V's top-left (the wordmark bar starts 10u earlier)
    ds_h = place(dsH, mw + gx + 10 * sw, Hm - capH)
    lw, lh = w_right, Hm
    m = Hm * p.get('h_margin', 0.25)
    def horiz(bg, c_mark, c_word, c_desc):
        return svg(lw + 2 * m, lh + 2 * m, [(place(mk, m, m), c_mark), (place(wm_s, m, m), c_word), (place(ds_h, m, m), c_desc)], bg=bg)
    files['lockup_horizontal_on_ivory.svg'] = write(out_prefix + 'lockup_horizontal_on_ivory.svg', horiz(IV, EM, EM, GO))
    files['lockup_horizontal_on_emerald.svg'] = write(out_prefix + 'lockup_horizontal_on_emerald.svg', horiz(EM, GL, IV, GL))
    files['_h_ivoryink.svg'] = write(out_prefix + '_h_ivoryink.svg', horiz(None, GL, IV, GL))
    files['_h_emeraldink.svg'] = write(out_prefix + '_h_emeraldink.svg', horiz(None, EM, EM, GO))
    # stacked lockup
    km = p.get('s_km', 2.0)
    msc = (Hw * km) / Hm
    mk_st = tr(mk, msc)
    mbx = bbox(mk_st)
    g1 = Hw * 0.62
    g2 = Hw * 0.40
    capS = Hw * 0.19
    dsS = descriptor(capS, p)
    sdx1 = bbox(dsS)[2]
    total_w = max(wx1, mbx[2])
    tot_h = mbx[3] + g1 + wy1 + g2 + capS
    mS = Hw * 0.9
    Wst, Hst = total_w + 2 * mS, tot_h + 2 * mS
    cxm, _ = centroid(mk_st)
    ox = 0.6 * cxm + 0.4 * (mbx[2] / 2)
    mk_pos = place(mk_st, Wst / 2 - ox, mS)
    wm_pos = place(wm, (Wst - wx1) / 2, mS + mbx[3] + g1)
    ds_pos = place(dsS, (Wst - sdx1) / 2, mS + mbx[3] + g1 + wy1 + g2)
    def stacked(bg, c_mark, c_word, c_desc):
        return svg(Wst, Hst, [(mk_pos, c_mark), (wm_pos, c_word), (ds_pos, c_desc)], bg=bg)
    files['lockup_stacked_on_ivory.svg'] = write(out_prefix + 'lockup_stacked_on_ivory.svg', stacked(IV, EM, EM, GO))
    files['lockup_stacked_on_emerald.svg'] = write(out_prefix + 'lockup_stacked_on_emerald.svg', stacked(EM, GL, IV, GL))
    return files

def render(f, tag=''):
    R = ['node', os.path.join(HERE, '..', 'toolkit', 'render.js')]
    C = ['node', os.path.join(HERE, 'compose.js')]
    order = ['mark.svg', 'mark_small.svg', 'wordmark.svg', 'mark_on_ivory.svg', 'mark_on_emerald.svg', 'mark_one_colour_gold.svg',
             'lockup_horizontal_on_ivory.svg', 'lockup_horizontal_on_emerald.svg', 'lockup_stacked_on_ivory.svg', 'lockup_stacked_on_emerald.svg']
    J = lambda n: os.path.join(HERE, n)
    extra = [J(n) for n in ('lockup_bilingual_on_ivory.svg', 'lockup_bilingual_on_emerald.svg') if os.path.exists(J(n))]
    subprocess.run(R + ['sheet', J(f'sheet{tag}.png')] + [f[k] for k in order] + extra, check=True)
    subprocess.run(R + ['sizes', J('_sizes_a.png'), f['mark_small.svg']], check=True)
    subprocess.run(R + ['sizes', J('_sizes_b.png'), f['_mark_small_ivory.svg']], check=True)
    subprocess.run(C + [J('_sizes_a.png'), J('_sizes_b.png'), '168', J(f'sizes{tag}.png')], check=True)
    subprocess.run(R + ['context', J('_ctx_a.png'), f['mark_on_emerald.svg'], f['_h_ivoryink.svg']], check=True)
    subprocess.run(R + ['context', J('_ctx_b.png'), f['mark_on_emerald.svg'], f['_h_emeraldink.svg']], check=True)
    subprocess.run(C + [J('_ctx_a.png'), J('_ctx_b.png'), '312', J(f'context{tag}.png')], check=True)
    for n in ('_sizes_a.png', '_sizes_b.png', '_ctx_a.png', '_ctx_b.png'):
        os.remove(J(n))
    return order

if __name__ == '__main__':
    f = make_all()
    import bilingual
    bilingual.make_bilingual()
    order = render(f)
    for k in order:
        print(k, os.path.getsize(f[k]))
