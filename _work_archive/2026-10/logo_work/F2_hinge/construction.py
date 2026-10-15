"""construction.png (F2): the staircase, the gold pin, the symbol crop, the d, the bilingual axis, the three cuts."""
import sys, base64, math
sys.path.insert(0, '.')
from build import *
from extras import compose, uri_svg

LINE = '#c9bfa9'; INK = '#0B2A20'; LAB = '#8a7f68'
ff = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
FONT = '../fonts/manrope/manrope-latin-500-normal.woff2'; FONT7 = '../fonts/manrope/manrope-latin-700-normal.woff2'


def svg(w, h, inner):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{inner}</svg>'


def P_(path, s, ox, base, col):
    return f'<path d="{rnd(to_svg_d(path, s, ox, base))}" fill="{col}"/>'


def guide(y, x0, x1, label, dash=True, right=False):
    tx = x1 - 4 if right else x0; anchor = 'end' if right else 'start'
    da = 'stroke-dasharray="5 5"' if dash else ''
    return (f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{LINE}" stroke-width="1" {da}/>'
            f'<text x="{tx}" y="{y-5:.1f}" text-anchor="{anchor}" font-family="M" font-size="11" fill="{LAB}">{label}</text>')


def note(x, y, tx, ty, text, anchor='start'):
    return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{INK}" stroke-width="0.8"/><circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{INK}"/>'
            f'<text x="{tx + (6 if anchor == "start" else -6):.1f}" y="{ty + 4:.1f}" text-anchor="{anchor}" font-family="M" font-size="13" fill="{INK}">{text}</text>')


def title(x, y, t):
    return f'<text x="{x}" y="{y}" font-family="M" font-weight="700" font-size="13" letter-spacing="0.6" fill="{INK}">{t}</text>'


# ---- A: the staircase and the pin
s = 0.215; ox = 60; b1 = 245
st = ST; L = st['L']; xl, xr = st['stem']; b2 = b1 + L * s
Y = lambda v, b=b1: b - v * s
Xx = lambda v: ox + v * s
a = title(24, 34, 'THE SIGNATURE · ONE STROKE, TWO WORDS')
a += guide(Y(pd.C), 40, 940, 'cap 700', right=True) + guide(Y(pd.X), 40, 940, 'x-height 490', right=True)
a += guide(Y(0), 40, 940, 'line 1 baseline', dash=False, right=True)
a += guide(Y(0, b2), 40, 940, 'line 2 baseline · L = 724 − 21 = 703', dash=False, right=True)
a += P_(st['van'], s, ox, b1, EM) + P_(st['I'], s, ox, b1, GD) + P_(st['indra'], s, ox, b1, EM)
cx = Xx((xl + xr) / 2)
a += note(Xx(xr), Y(pd.X * 0.50), 600, Y(pd.X * 0.95), 'colour break at ½ x-height, cut at the knife angle (20°)')
a += note(Xx(xr + pd.ie), Y(pd.it / 2), 600, Y(pd.X * 0.30), 'one slab: the n\'s foot and the I\'s head')
a += note(cx, Y(-L * 0.55), 330, Y(-L * 0.62), 'the gold pin: one stroke shared by Van and Indra', 'end')
a += note(Xx(xr + pd.ie + 18), Y(-L + 10), 330, Y(-L - 40), 'I-to-n gap 36 = the d-to-r gap', 'end')
A = svg(980, 470, a)

# ---- B: the symbol crop
h = SYMI; sz = 300
sym_svg = bleed(h, pi, IV, GL, EM, size=sz)
b = title(24, 34, 'THE SYMBOL · PROFILE PICTURE CROP')
b += f'<image href="{uri_svg(sym_svg)}" x="40" y="60" width="{sz}" height="{sz}" clip-path="url(#cc)"/>'
b += f'<defs><clipPath id="cc"><circle cx="{40+sz/2}" cy="{60+sz/2}" r="{sz/2}"/></clipPath></defs>'
b += f'<circle cx="{40+sz/2}" cy="{60+sz/2}" r="{sz/2}" fill="none" stroke="{LINE}" stroke-dasharray="4 4"/>'
xh_top = 60 + sz * 0.40 - sz * 0.20; xh_bot = 60 + sz * 0.40 + sz * 0.20
b += guide(xh_top, 30, 380, '') + guide(xh_bot, 30, 380, '')
b += f'<text x="352" y="{(xh_top+xh_bot)/2+4:.0f}" font-family="M" font-size="11" fill="{LAB}">x-height 40 %</text>'
b += f'<text x="40" y="392" font-family="M" font-size="13" fill="{INK}">Icon cut (stem 116, arch top 58). The pin runs off the</text>'
b += f'<text x="40" y="410" font-family="M" font-size="13" fill="{INK}">bottom edge: it continues into Indra.</text>'
B = svg(500, 430, b)

# ---- C: the d
pz = P(**DISPLAY); sd = 0.27
n_, nw_ = g_n(pz); d_, dw_ = g_d(pz)
c = title(24, 34, 'THE d · AS WIDE AS THE n, ONE OVAL COUNTER')
c += P_(n_, sd, 40, 270, EM) + P_(d_, sd, 40 + (nw_ + 30) * sd, 270, EM)
c += guide(270, 30, 420, '') + guide(270 - pz.X * sd, 30, 420, '')
nb = vt.bounds(n_); db = vt.bounds(d_)
c += f'<line x1="{40+53*sd:.1f}" x2="{40+481*sd:.1f}" y1="292" y2="292" stroke="{GD}" stroke-width="1.5"/><text x="{40+60*sd:.0f}" y="308" font-family="M" font-size="11" fill="{LAB}">n 428</text>'
dx0 = 40 + (nw_ + 30) * sd
c += f'<line x1="{dx0+26*sd:.1f}" x2="{dx0+446*sd:.1f}" y1="292" y2="292" stroke="{GD}" stroke-width="1.5"/><text x="{dx0+30*sd:.0f}" y="308" font-family="M" font-size="11" fill="{LAB}">d 420 (was 356)</text>'
c += f'<text x="40" y="340" font-family="M" font-size="13" fill="{INK}">Outer and inner contours are ellipses meeting the stem at</text>'
c += f'<text x="40" y="358" font-family="M" font-size="13" fill="{INK}">0.86 / 0.78 x-height: no flat wall, no corner, thin joins.</text>'
C = svg(450, 380, c)

# ---- D: the bilingual axis
dk, di, dbd = deva_placed()
parts = [(WM['ink'], EM), (WM['I'], GD), (dk, EM), (di, GD), (dbd, EM)]
bb = bbox(*[p for p, q in parts]); sb = 0.105
ib = vt.bounds(WM['I']); ax = (ib[0] + ib[2]) / 2
oxd = 40 - bb[0] * sb; byd = 80 + bb[3] * sb
d = title(24, 34, 'BILINGUAL · ONE GOLD AXIS (DEVANAGARI TO BE VERIFIED)')
d += ''.join(P_(p, sb, oxd, byd, q) for p, q in parts)
d += f'<line x1="{oxd+ax*sb:.1f}" x2="{oxd+ax*sb:.1f}" y1="56" y2="{byd-bb[1]*sb+14:.0f}" stroke="#a14b2a" stroke-width="0.8" stroke-dasharray="3 3"/>'
d += f'<text x="40" y="{byd-bb[1]*sb+40:.0f}" font-family="M" font-size="13" fill="{INK}">Gold I and gold i-sign on one vertical; danda = Latin stem; headline height = cap height.</text>'
D_ = svg(540, int(byd - bb[1] * sb + 60), d)

# ---- E: the three cuts
e = title(24, 34, 'THREE OPTICAL CUTS')
yy = 90
for p_, lab in [(pd, 'display · 64 px tall and up, print: stem 82, hairline 24'), (ps, 'small · headers, Reel credit, email: stem 90, hairline 34'),
                (pi, 'icon · avatar, favicon, app icon: stem 116, arch top 58')]:
    hs = hinge_symbol(p_, L=p_.X * 0.9)
    e += P_(hs['n'], 0.085, 40, yy + 30, EM) + P_(hs['pin'], 0.085, 40, yy + 30, GD)
    e += f'<text x="104" y="{yy+12}" font-family="M" font-size="12" fill="{INK}">{lab}</text>'
    yy += 95
E = svg(470, 390, e)

html = f'''<!doctype html><html><head><style>@font-face{{font-family:M;src:url(data:font/woff2;base64,{ff(FONT)}) format("woff2");font-weight:500}}
@font-face{{font-family:M;src:url(data:font/woff2;base64,{ff(FONT7)}) format("woff2");font-weight:700}}
.c{{background:#fff;border-radius:6px;padding:6px}}</style></head><body style="margin:0;background:{IV};width:1600px">
<div style="padding:28px 36px 6px;font:700 24px M;color:{EM}">The Hinge: construction</div>
<div style="padding:0 36px 16px;font:500 14px M;color:#3a3a35">The n that ends Van and the I that begins Indra share one stroke. Gold marks that shared stroke, in both scripts.</div>
<div style="display:flex;gap:18px;padding:0 36px"><div class="c">{A}</div><div class="c">{B}</div></div>
<div style="display:flex;gap:18px;padding:18px 36px 30px"><div class="c">{C}</div><div class="c">{D_}</div><div class="c">{E}</div></div>
</body></html>'''
compose(html, 'construction.png', 1600, 1100)
print('construction ok')
