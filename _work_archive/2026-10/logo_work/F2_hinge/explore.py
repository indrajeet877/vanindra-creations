"""explore.png (F2): the polish studies - each judge's must-fix as a row of variations, chosen one marked."""
import sys, os, base64
sys.path.insert(0, '.')
from build import *
from extras import compose, uri_svg, uri_file

R3 = '../r3_hinge_final'
FONT = '../fonts/manrope/manrope-latin-500-normal.woff2'
FONT6 = '../fonts/manrope/manrope-latin-700-normal.woff2'
ff = lambda f: base64.b64encode(open(f, 'rb').read()).decode()


def cell(img_uri, label, chosen=False, h=200, bg='#F6F1E7', w=None, fit='contain'):
    mark = '<span style="color:#A8843A">&#9679; chosen</span>' if chosen else ''
    st = f'width:{w}px;' if w else ''
    return (f'<div style="{st}flex:{0 if w else 1};min-width:0"><div style="height:{h}px;background:{bg};display:flex;align-items:center;justify-content:center;overflow:hidden;'
            f'{"outline:2px solid #A8843A;outline-offset:-2px;" if chosen else ""}"><img src="{img_uri}" style="max-width:92%;max-height:88%;object-fit:{fit}"></div>'
            f'<div style="font:500 12px/1.35 M;color:#3b3a36;margin-top:6px">{label} {mark}</div></div>')


def row(title, cells):
    return (f'<div style="margin:0 0 26px"><div style="font:700 15px M;color:#0B2A20;margin:0 0 10px">{title}</div>'
            f'<div style="display:flex;gap:14px;align-items:flex-start">{"".join(cells)}</div></div>')


S = lambda svg: uri_svg(svg)
F = lambda f: uri_file(f, 'image/svg+xml' if f.endswith('.svg') else 'image/png')

# 1 - the join: where does the colour break?
st_split = staircase(pd, pin=False)
def st_crop(st, ink, gc, brk=None):
    parts = stair_parts(st, ink, gc)
    return fit(parts, unit=0.2, padx=40, pady=40, bg=IV)
p_flat = staircase(pd); 
from vitype import g_hinge_down
def stair_custom(p, brk, shear):
    # same staircase, different break of the gold
    L = p.A - p.it
    V_, vw = g_V(p); a, aw = g_a(p); n, nw = g_n(p); d, dw = g_d(p); r, rw = g_r(p)
    hn, hI, hw, _ = g_hinge_down(p, L, pin=True, brk=brk, shear=shear)
    x = vw + KERN['Va'] + aw + KERN['an']
    van = U(V_, T(a, vw + KERN['Va'], 0), T(hn, x, 0)); I = T(hI, x, 0); x += hw + KERN['In']
    ind = []
    for g, adv, k in [(n, nw, KERN['nd']), (d, dw, KERN['dr']), (r, rw, KERN['ra']), (a, aw, 0)]:
        ind.append(T(g, x, -L)); x += adv + k
    return dict(van=van, I=I, indra=U(*ind))
r1 = row('1 · The join: one stroke, or an emerald post in a gold collar?', [
    cell(F(R3 + '/staircase.svg'), 'R3: colour breaks on top of the slab, gold brackets flare round the n (collar)'),
    cell(S(st_crop(st_split, EM, GD)), 'break under the shared slab: the n is whole, the I hangs below (two strokes)'),
    cell(S(st_crop(stair_custom(pd, 0.50, False), EM, GD)), 'gold pin from mid-leg, level cut'),
    cell(S(st_crop(staircase(pd), EM, GD)), 'gold pin from mid-leg, knife-angle cut: the shared stroke is one gold piece', True),
])

# 2 - the symbol / avatar
HE = dict(S=104, Sc=110, H=42, Ht=50, Hb=48, ft=36, fe=31, fb=13, he=38, hd=42, ie=34, it=38, cw=248, tw=60)
pm = P(**HE)
hm = hinge_symbol(pm)
av_centre = square([(hm['n'], IV), (hm['pin'], GL)], bg=EM, fill=0.62, circle=0.8)
av_nopin = square([(hinge_symbol(pm, pin=False)['n'], IV), (hinge_symbol(pm, pin=False)['pin'], GL)], bg=EM, fill=0.62, circle=0.8)
av_small = bleed(SYMI, pi, IV, GL, EM, xh=0.30, cyk=0.44)
av_pick = open('mark_on_emerald.svg').read()
def avs(svg):
    u = S(svg)
    return (f'data:image/svg+xml;base64,' + base64.b64encode((
        f'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="160"><defs><clipPath id="a"><circle cx="70" cy="80" r="65"/></clipPath>'
        f'<clipPath id="b"><circle cx="190" cy="80" r="24"/></clipPath><clipPath id="c"><circle cx="252" cy="80" r="16"/></clipPath></defs>'
        f'<image href="{u}" x="5" y="15" width="130" height="130" clip-path="url(#a)"/><image href="{u}" x="166" y="56" width="48" height="48" clip-path="url(#b)"/>'
        f'<image href="{u}" x="236" y="64" width="32" height="32" clip-path="url(#c)"/></svg>').encode()).decode())
r2 = row('2 · Profile picture: drawn from the hinge, not the name set small (130 / 48 / 32 px)', [
    cell(avs(open(R3 + '/mark_on_emerald.svg').read()), 'R3: the staircase in a circle, a grey texture below 56 px', h=170, bg='#fff'),
    cell(avs(av_centre), 'the whole symbol centred: honest, but small and thin at 32 px', h=170, bg='#fff'),
    cell(avs(av_nopin), 'n whole, gold I below: reads as two stacked letters', h=170, bg='#fff'),
    cell(avs(av_pick), 'icon cut, n at 40 %, gold pin runs off the edge into Indra', True, h=170, bg='#fff'),
])

# 3 - favicon
def fav(svg, label, chosen=False):
    u = S(svg)
    strip = ''.join(f'<img src="{u}" style="width:{s}px;height:{s}px;margin:0 6px;vertical-align:bottom">' for s in [48, 32, 24, 16])
    html_img = ('data:image/svg+xml;base64,' + base64.b64encode((f'<svg xmlns="http://www.w3.org/2000/svg" width="190" height="60">'
               + ''.join(f'<image href="{u}" x="{x}" y="{54 - s}" width="{s}" height="{s}"/>' for x, s in [(4, 48), (66, 32), (112, 24), (150, 16)]) + '</svg>').encode()).decode())
    return cell(html_img, label, chosen, h=110, bg='#F6F1E7')
r3 = row('3 · 48 px and below: from a stock-looking V to the hinge', [
    fav(open(R3 + '/mark_small.svg').read(), 'R3: Didone V, no trace of the idea'),
    fav(open('mark_small.svg').read(), 'icon cut, short pin with its foot (transparent files)', True),
    fav(open('mark_small_tile.svg').read(), 'icon cut on an emerald tile, pin bleeding (browser tab, app icon)', True),
])

# 4 - d, one line, Creations, bilingual
n_, nw_ = g_n(pd); d_, dw_ = g_d(pd); r_, rw_ = g_r(pd); a_, aw_ = g_a(pd)
ndra = U(n_, T(d_, nw_ - 6, 0), T(r_, nw_ - 6 + dw_ - 6, 0), T(a_, nw_ - 6 + dw_ - 6 + rw_ - 46, 0))
r4 = row('4 · Letters: the d, the one-line I, the weight of Creations', [
    cell(F('../round3/judge_tmp/ed/r3_d.png'), 'R3 d: 80 % of the n, slot counter, corner at the bottom left', h=180, bg='#fff'),
    cell(S(fit([(ndra, EM)], unit=0.2, padx=40, pady=40, bg=IV)), 'F2 d: as wide as the n, one oval counter, thin joins', True, h=180),
    cell(F(R3 + '/wordmark.svg'), 'R3 one line: I above the V\'s cap line', h=180, bg='#fff'),
    cell(S(fit([(wordmark_text(pd, join='slab')['ink'], EM), (wordmark_text(pd, join='slab')['I'], GD)], unit=0.2, padx=40, pady=40, bg=IV)), 'shared foot slab: reads "VanLndra", rejected', h=180),
    cell(F('wordmark.svg'), 'F2 one line: I at cap height, level with the V', True, h=180, bg='#fff'),
])
r5 = row('5 · Creations at 58 %, and the bilingual axis', [
    cell(F(R3 + '/global.svg'), 'R3: Creations ~40 % heavier per unit than Indra', h=200, bg='#fff'),
    cell(F('global.svg'), 'F2: ~10 % optical compensation, open e, lighter s spine', True, h=200, bg='#fff'),
    cell(F(R3 + '/lockup_bilingual_on_ivory.svg'), 'R3: gold I and gold i-sign 90 px apart, Hindi line darker', h=200),
    cell(F('lockup_bilingual_on_ivory.svg'), 'F2: one gold axis through both scripts, danda = Latin stem, headline = cap height', True, h=200),
])
html = f'''<!doctype html><html><head><style>@font-face{{font-family:M;src:url(data:font/woff2;base64,{ff(FONT)}) format("woff2");font-weight:500}}
@font-face{{font-family:M;src:url(data:font/woff2;base64,{ff(FONT6)}) format("woff2");font-weight:700}}</style></head>
<body style="margin:0;background:#ECE6D9"><div style="padding:30px 34px;width:1600px;box-sizing:border-box">
<div style="font:700 24px M;color:#0B2A20;margin:0 0 4px">F2 · The Hinge — final polish studies</div>
<div style="font:500 14px M;color:#5b5850;margin:0 0 24px">Each row answers one of the final judges' must-fix items. Gold outline = chosen.</div>
{r1}{r2}{r3}{r4}{r5}</div></body></html>'''
compose(html, 'explore.png', 1600, 1500)
print('explore ok')
