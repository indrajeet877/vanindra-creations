import math, os, subprocess
from geo import *
from letters import *

OUT = 'explore'
os.makedirs(OUT, exist_ok=True)
EM, IV, GO = PAL['emerald'], PAL['ivory'], PAL['gold']

def place(path, box, align='center'):
    """Scale path to fit box (x,y,w,h)."""
    x0, y0, x1, y1 = bbox(path)
    bx, by, bw, bh = box
    s = min(bw / (x1 - x0), bh / (y1 - y0))
    dx = bx + (bw - (x1 - x0) * s) / 2 - x0 * s if align == 'center' else bx - x0 * s
    dy = by + (bh - (y1 - y0) * s) / 2 - y0 * s
    return tr(path, s, dx, dy)

def label(s, x, y, size=16, fill='#7a6a4a'):
    t = text(s, family='jost', weight=400, size=size, x=x, y=y)
    return f'<path d="{t.d}" fill="{fill}"/>'

def card(name, mono, wm, note, bg=IV, fg=EM, accent=None, extra=None):
    W, H = 1000, 600
    m = place(mono, (60, 50, 300, 300))
    w = place(wm, (60, 400, 880, 110), align='left')
    body = f'<path d="{d(m)}" fill="{fg}"/><path d="{d(w)}" fill="{fg}"/>'
    if extra is not None:
        body += f'<path d="{d(place(extra, (420, 80, 520, 240)))}" fill="{fg}"/>'
    body += label(name + ' — ' + note, 60, 575)
    svg = V.svg_doc(W, H, body, bg=bg)
    p = f'{OUT}/{name}.svg'
    open(p, 'w').write(svg)
    return p

# ---------- monogram constructions ----------
def mono_vi(st, vx=40, yj=0.5, ov=None, bindu=False, bar_b=None, rounded=False):
    """V + I fused under one headline = व. vx: vertex x; yj: fraction of height where V's right arm meets the stem."""
    H, o = st.H, st.o
    bb = bar_b or st.b
    theta = math.atan2(vx, H + o)
    # outer right edge of V arm: from vertex up-right symmetric
    xs = vx + (H + o - yj * H) * math.tan(theta)   # stem left edge where arm outer edge meets at height yj*H
    S = st.S
    top = 0
    L0, L1 = (0, 0), (vx, H + o)
    R0, R1 = (2 * vx, 0), (vx, H + o)
    a = offset(L0, L1, st.Td); b2 = offset(L0, L1, -st.Td)
    Li = a if line_x(*a, 0) > 0 else b2
    a = offset(R0, R1, st.h); b2 = offset(R0, R1, -st.h)
    Ri = a if line_x(*a, 0) < 2 * vx else b2
    iv = isect(*Li, *Ri)
    v = poly([(0, top), (line_x(*Li, top), top), iv, (line_x(*Ri, top), top), (2 * vx, top), (vx, H + o)])
    stem = rect(xs, 0, xs + S, H)
    p = U(v, stem)
    # clip anything of V right arm beyond stem right edge
    p = I(p, rect(-5, 0, xs + S, H + o))
    ovh = ov if ov is not None else st.b * 0.6
    bar = rect(-ovh, 0, xs + S + ovh, bb)
    p = U(p, bar)
    if bindu:
        r = st.S * 0.55
        p = U(p, circle(xs + S / 2, -r - st.b * 0.9, r))
    return p

def mono_vi_sep(st, vx=38, gap=10, bar_b=None):
    H, o = st.H, st.o
    v, w = glyph_V(st, W=2 * vx)
    v = I(v, rect(-5, 0, w + 5, H + o))
    xs = w + gap
    stem = rect(xs, 0, xs + st.S, H)
    ovh = st.b * 0.6
    return U(v, stem, rect(-ovh, 0, xs + st.S + ovh, bar_b or st.b))

def mono_mirror(st):
    """Latin V stands on the line; Devanagari-style va hangs below it."""
    H = st.H
    v, w = glyph_V(st, W=78)
    v = tr(I(v, rect(-5, 0, 100, H + 5)), 1, 0, 0)
    # flip: V standing ON the line => V above line, vertex at line. Use V as is with vertex at bottom touching line
    up = tr(v, 0.6, 0, -H * 0.6 - st.o * 0.6)
    lower = mono_vi(st, vx=30, yj=0.55)
    lb = bbox(lower)
    upb = bbox(up)
    up = tr(up, 1, (lb[0] + lb[2]) / 2 - (upb[0] + upb[2]) / 2 - 8, 0)
    return U(up, lower)

# ---------- lowercase from font skeleton + bar ----------
def lower_wm(fam, weight, size=100, bar_rel=0.11, tracking=0.02, bindu_lift=0.0):
    gs = V.glyph_paths('vanindra', family=fam, weight=weight, size=size, tracking=tracking)
    xg = V.glyph_paths('x', family=fam, weight=weight, size=size)[0]
    xh = -xg.bounds[1]
    parts = []
    i_idx = 3
    for i, g in enumerate(gs):
        p = g.path
        if i == i_idx:
            # separate dot from stem: components above x-height
            stem = I(p, rect(-1e4, -xh - 1, 1e4, 1e4))
            dot = I(p, rect(-1e4, -1e4, 1e4, -xh - size * 0.05))
            p = U(stem, tr(dot, 1, 0, -bindu_lift * size))
        parts.append(p)
    body = U(*parts)
    x0, y0, x1, y1 = bbox(body)
    bb = size * bar_rel
    bar = rect(x0 - bb * 0.5, -xh - bb * 0.55, x1 + bb * 0.5, -xh + bb * 0.45)
    return U(body, bar)

def deva(txt, fam='rozha-one', w=400, size=100):
    return V.text_path(txt, family=fam, weight=w, subset='devanagari', size=size).path

cards = []
# E1 didone caps, continuous bar; व-ligature monogram
st = Style(H=100, b=11, S=15, h=3.4)
wm, tot, spans = wordmark(st, track=9)
wm = I(wm, rect(-50, 0, 2000, 200))
stm = Style(H=100, b=14, S=18, h=5, Td=19)
cards.append(card('E1', mono_vi(stm, vx=40, yj=0.5), wm, 'didone hanging caps, continuous shirorekha; VI = va ligature'))

# E2 didone caps, bar broken over V counter; separate VI under one bar
vs = spans[0]
gap = [(vs[1] + st.Td * 1.25, vs[2] - st.h * 2.2)]
wm2, _, _ = wordmark(st, track=9, gaps=gap)
wm2 = I(wm2, rect(-50, 0, 2000, 200))
cards.append(card('E2', mono_vi_sep(stm), wm2, 'headline broken over the V (as in Devanagari), VI under one bar'))

# E3 monoline caps
stmono = Style(H=100, b=12, S=12, mono=True, k=0.62)
wm3, _, _ = wordmark(stmono, track=11)
wm3 = I(wm3, rect(-50, 0, 2000, 200))
cards.append(card('E3', mono_vi(Style(H=100, b=15, S=15, mono=True), vx=40, yj=0.5), wm3, 'monoline geometric, everything one weight'))

# E4 lowercase bodoni + bindu
wm4 = lower_wm('bodoni-moda', 600, bar_rel=0.10, tracking=0.03, bindu_lift=0.06)
cards.append(card('E4', mono_vi(stm, vx=40, yj=0.5, bindu=True), wm4, 'lowercase, i-dot becomes the bindu above the headline; mark = vam'))

# E5 lowercase jost
wm5 = lower_wm('jost', 400, bar_rel=0.09, tracking=0.04, bindu_lift=0.05)
cards.append(card('E5', mono_vi(Style(H=100, b=12, S=13, mono=True), vx=38, yj=0.62, bindu=True), wm5, 'geometric lowercase hanging from x-height line'))

# E6 hairline rail, spaced caps
st6 = Style(H=100, b=3.4, S=13, h=3.0)
wm6, _, _ = wordmark(st6, track=34, overhang=60)
wm6 = I(wm6, rect(-100, 0, 3000, 200))
cards.append(card('E6', mono_vi(Style(H=100, b=4, S=15, h=3.4, Td=16), vx=40, yj=0.45, ov=30), wm6, 'hairline rail, wide-set caps hang like jewellery'))

# E7 bilingual shared line: Latin stands on it, Devanagari hangs from it
st7 = Style(H=100, b=11, S=15, h=3.4)
lat, _, _ = wordmark(st7, track=9, bar=False)
lat = I(lat, rect(-50, 0, 2000, 200))
lb = bbox(lat)
dv = deva('वनिंद्रा', size=150)
db = bbox(dv)
# find headline top of devanagari: approx y where the bar is (take top of the glyph body excluding matra) -> use 'व' top
vtop = bbox(deva('व', size=150))[1]
dv = tr(dv, 1, (lb[0] + lb[2]) / 2 - (db[0] + db[2]) / 2, 100 + 6 - vtop)
line = rect(lb[0] - 30, 100, lb[2] + 30, 106)
wm7 = U(lat, dv, line)
cards.append(card('E7', mono_mirror(stm), wm7, 'one line: English stands on it, Hindi hangs from it (deva to verify)'))

# E8 kalam-cut caps
st8 = Style(H=100, b=12, S=16, h=4.2, foot=9)
wm8, _, _ = wordmark(st8, track=9)
wm8 = I(wm8, rect(-50, 0, 2000, 200))
cards.append(card('E8', mono_vi(Style(H=100, b=14, S=18, h=5.5, Td=19, foot=0), vx=42, yj=0.62), wm8, 'kalam (reed-pen) chisel cut at the stem feet'))

# E9 on emerald: E1 inverted with gold for color test
cards.append(card('E9', mono_vi(stm, vx=40, yj=0.5), wm, 'E1 reversed (colour check)', bg=EM, fg=PAL['gold_lt']))

subprocess.run(['node', '../toolkit/render.js', 'sheet', 'explore.png'] + cards, check=True)
print('done')
