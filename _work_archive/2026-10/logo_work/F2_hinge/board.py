"""board.png (F2): the team presentation board, 1600 x 2000 on ivory. Tiny labels, no paragraphs."""
import sys, base64
sys.path.insert(0, '.')
from build import *
from extras import compose, uri_svg, uri_file

F5 = '../fonts/manrope/manrope-latin-500-normal.woff2'; F6 = '../fonts/manrope/manrope-latin-600-normal.woff2'; F7 = '../fonts/manrope/manrope-latin-700-normal.woff2'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
rd = lambda f: open(f).read()
U_ = lambda f: uri_svg(rd(f))

PAGE = '#F6F1E7'; LAB = '#8C8575'; HAIR = '#DDD5C5'; CARD = '#FFFFFF'
W, H, M = 1600, 2000, 72


def symbol_panel(w, h, xh=0.30, cy=0.40):
    """the hinge set large on an emerald field; the gold pin runs off the bottom edge."""
    hh = SYMI; p = pi
    nb = vt.bounds(hh['n']); pb = vt.bounds(hh['pin'])
    s = w * xh / p.X
    x0 = nb[0]; x1 = max(nb[2], pb[2] - p.ie)
    dx = w / 2 - (x0 + x1) / 2 * s; dy = h * cy + p.X / 2 * s
    clip = D(hh['pin'], rect(-9000, -9000, 9000, (dy - h - 4) / s))
    inner = f'<rect width="{w}" height="{h}" fill="{EM}"/>' + body([(hh['n'], IV), (clip, GL)], s, dx, dy)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{inner}</svg>'


def lab(x, y, t, align='left', w=None):
    st = f'width:{w}px;text-align:{align};' if w else ''
    return f'<div class="lab" style="left:{x}px;top:{y}px;{st}">{t}</div>'


def box(x, y, w, h, inner='', bg=CARD, extra=''):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};overflow:hidden;{extra}">{inner}</div>'


def center_img(uri, w, extra=''):
    return f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><img src="{uri}" style="width:{w}px;display:block;{extra}"></div>'


html = []
# ---- top rule
html.append(lab(M, 50, 'VanIndra Creations'))
html.append(lab(W - M - 400, 50, 'Identity &nbsp;·&nbsp; The Hinge', 'right', 400))
html.append(f'<div style="position:absolute;left:{M}px;top:76px;width:{W-2*M}px;height:1px;background:{HAIR}"></div>')

# ---- hero: signature (left, on the page) + symbol (right, emerald field)
hy, hh_ = 108, 576
html.append(box(M, hy, 936, hh_, center_img(U_('staircase.svg'), 680), bg='transparent'))
html.append(lab(M, hy + hh_ + 14, 'Signature'))
html.append(box(M + 960, hy, 496, hh_, f'<img src="{uri_svg(symbol_panel(496, hh_, xh=0.30, cy=0.40))}" style="display:block">'))
html.append(lab(M + 960, hy + hh_ + 14, 'Symbol'))

# ---- row 2: wordmark / Instagram / global
ry = 734; rh = 214; cw = (W - 2 * M - 2 * 24) / 3
html.append(box(M, ry, cw, rh, center_img(U_('wordmark.svg'), 320)))
html.append(lab(M, ry + rh + 14, 'Wordmark · one line'))
av = U_('mark_on_emerald.svg')
ig = f'''<div style="position:absolute;left:32px;top:26px;display:flex;align-items:center;gap:22px">
  <img src="{av}" style="width:110px;height:110px;border-radius:50%;display:block">
  <div><div class="ui" style="font-weight:700;font-size:15px;color:#111">vanindracreations</div>
  <div class="ui" style="font-weight:500;font-size:12.5px;color:#737373;margin-top:3px">VanIndra Creations</div>
  <div style="display:flex;gap:6px;margin-top:12px"><div style="width:74px;height:26px;border-radius:7px;background:#EFEFEF"></div><div style="width:74px;height:26px;border-radius:7px;background:#EFEFEF"></div></div></div></div>
<div style="position:absolute;left:32px;top:158px;display:flex;align-items:center;gap:12px">
  <img src="{av}" style="width:40px;height:40px;border-radius:50%;display:block">
  <div><div class="ui" style="font-weight:700;font-size:12.5px;color:#111">vanindracreations</div>
  <div style="width:190px;height:7px;border-radius:4px;background:#EDEDED;margin-top:6px"></div></div></div>'''
html.append(box(M + cw + 24, ry, cw, rh, ig))
html.append(lab(M + cw + 24, ry + rh + 14, 'Instagram · 110 px &nbsp;/&nbsp; 40 px'))
html.append(box(M + 2 * (cw + 24), ry, cw, rh, center_img(U_('global.svg'), 350)))
html.append(lab(M + 2 * (cw + 24), ry + rh + 14, 'Global · USD'))

# ---- row 3: the website header at 1:1, full width
r3 = 1000; dw = W - 2 * M
nav = ''.join(f'<span class="ui" style="font-size:15px;font-weight:500;color:{EM}">{t}</span>' for t in ['Work', 'Services', 'Pricing', 'About'])
desk = f'''<div style="position:absolute;left:0;top:0;width:{dw}px;height:24px;background:#ECE7DD;display:flex;align-items:center;gap:6px;padding-left:12px;box-sizing:border-box">
<i style="width:8px;height:8px;border-radius:50%;background:#D6CDBC;display:block"></i><i style="width:8px;height:8px;border-radius:50%;background:#D6CDBC;display:block"></i><i style="width:8px;height:8px;border-radius:50%;background:#D6CDBC;display:block"></i>
<div style="margin-left:14px;height:14px;width:260px;border-radius:7px;background:#F7F4EE"></div></div>
<div style="position:absolute;left:{(dw-1440)/2:.0f}px;top:24px;width:1440px;height:120px;background:{IV};display:flex;align-items:center;justify-content:space-between;padding:0 64px;box-sizing:border-box;border-bottom:1px solid #E6DECF">
  <img src="{U_('header_staircase_emerald.svg')}" style="height:64px;display:block">
  <div style="display:flex;align-items:center;gap:40px">{nav}<div class="ui" style="background:{EM};color:{IV};border-radius:999px;padding:13px 22px;font-size:15px;font-weight:600">Book a free call</div></div></div>
<div style="position:absolute;left:{(dw-1440)/2+64:.0f}px;top:{24+120+30}px;width:520px;height:18px;border-radius:3px;background:#E7E0D2"></div>'''
desk_h = 190
html.append(box(M, r3, dw, desk_h, desk, bg=IV, extra='box-shadow:0 0 0 1px #E2DACA;border-radius:6px'))
html.append(lab(M, r3 + desk_h + 14, 'Website · desktop 1440 · 1:1'))

# ---- row 4: two Reel covers / two phones / favicon strip
r4 = 1248; rw_, rh4 = 252, 448
html.append(box(M, r4, rw_, rh4, f'<img src="{uri_file("reel_tag.png", "image/png")}" style="width:{rw_}px;height:{rh4}px;display:block">', extra='border-radius:4px'))
html.append(box(M + rw_ + 24, r4, rw_, rh4, f'<img src="{uri_file("reel_tag_light.png", "image/png")}" style="width:{rw_}px;height:{rh4}px;display:block">', extra='border-radius:4px'))
html.append(lab(M, r4 + rh4 + 14, 'Reel credit · ivory on dark footage, emerald on light'))
burger = lambda c: f'<svg width="22" height="14" viewBox="0 0 22 14"><rect y="1" width="22" height="1.6" fill="{c}"/><rect y="11" width="14" height="1.6" fill="{c}" x="8"/></svg>'
px0 = M + 2 * (rw_ + 24); ph = 290
def phone(x, bg, ink_svg, bc):
    inner = f'''<div style="position:absolute;left:0;top:0;width:390px;height:22px;background:{bg}"></div>
<div style="position:absolute;left:0;top:22px;width:390px;height:64px;background:{bg};display:flex;align-items:center;justify-content:space-between;padding:0 18px;box-sizing:border-box">
<img src="{U_(ink_svg)}" style="height:44px;display:block">{burger(bc)}</div>
<div style="position:absolute;left:18px;top:{22+64+28}px;width:250px;height:16px;border-radius:3px;background:#ECE6DA"></div>
<div style="position:absolute;left:18px;top:{22+64+54}px;width:180px;height:16px;border-radius:3px;background:#ECE6DA"></div>'''
    return box(x, r4, 390, ph, inner, bg='#FBF9F5', extra='border-radius:22px 22px 0 0;box-shadow:0 0 0 1px #E2DACA')
html.append(phone(px0, IV, 'header_staircase_emerald.svg', EM))
html.append(phone(W - M - 390, EM, 'header_staircase_ivory.svg', IV))
html.append(lab(px0, r4 + ph + 12, 'Phone 390 · 1:1'))
html.append(lab(W - M - 390, r4 + ph + 12, 'Phone · on emerald'))
fy = r4 + ph + 40; fh = rh4 - ph - 40; fw = W - M - px0
tile = U_('mark_small_tile.svg'); msm = U_('mark_small.svg')
fav = f'''<div style="position:absolute;left:28px;top:0;bottom:0;display:flex;align-items:center;gap:16px">
<img src="{tile}" style="width:48px;height:48px;border-radius:9px"><img src="{tile}" style="width:32px;height:32px;border-radius:6px"><img src="{tile}" style="width:16px;height:16px;border-radius:3px">
<span style="width:18px"></span><img src="{msm}" style="width:48px;height:48px"><img src="{msm}" style="width:32px;height:32px"><img src="{msm}" style="width:16px;height:16px"></div>
<div style="position:absolute;right:28px;top:{fh/2-15:.0f}px;width:220px;height:30px;border-radius:8px 8px 0 0;background:#fff;display:flex;align-items:center;gap:8px;padding:0 10px;box-sizing:border-box">
<img src="{tile}" style="width:16px;height:16px;border-radius:3px"><span class="ui" style="font-size:12px;color:#333">VanIndra Creations</span></div>'''
html.append(box(px0, fy, fw, fh, fav, bg='#ECE7DD', extra='border-radius:6px'))
html.append(lab(px0, fy + fh + 14, 'Favicon & app icon · 48 / 32 / 16'))

# ---- row 5: one colour
r5 = 1754; oh = 140; ow = (W - 2 * M - 5 * 24) / 6
items = [('staircase_one_colour_emerald.svg', CARD, 150), ('staircase_one_colour_gold.svg', CARD, 150), ('staircase_one_colour_ivory.svg', EM, 178),
         ('mark_one_colour_emerald.svg', CARD, 104), ('mark_one_colour_gold.svg', CARD, 104), ('mark_one_colour_ivory.svg', EM, 104)]
for i, (f, bg, wimg) in enumerate(items):
    html.append(box(M + i * (ow + 24), r5, ow, oh, center_img(U_(f), wimg), bg=bg))
html.append(lab(M, r5 + oh + 14, 'One colour · emerald, antique gold, ivory'))

# ---- palette chips (bottom right)
chips = [(EM, '#0B2A20'), (IV, '#F6F1E7'), (GD, '#A8843A'), (GL, '#D2B26A')]
cx = W - M - 4 * 104 + 20
for i, (c, t) in enumerate(chips):
    html.append(f'<div style="position:absolute;left:{cx + i*104}px;top:{r5+oh+12}px;display:flex;align-items:center;gap:7px"><i style="display:block;width:11px;height:11px;border-radius:50%;background:{c};box-shadow:0 0 0 1px #D6CDBC"></i><span class="lab" style="position:static">{t}</span></div>')

page = f'''<!doctype html><html><head><style>
@font-face{{font-family:M;src:url(data:font/woff2;base64,{b64(F5)}) format("woff2");font-weight:500}}
@font-face{{font-family:M;src:url(data:font/woff2;base64,{b64(F6)}) format("woff2");font-weight:600}}
@font-face{{font-family:M;src:url(data:font/woff2;base64,{b64(F7)}) format("woff2");font-weight:700}}
.lab{{position:absolute;font:600 10.5px/1 M;letter-spacing:0.14em;text-transform:uppercase;color:{LAB};white-space:nowrap}}
.ui{{font-family:M}}
</style></head><body style="margin:0;width:{W}px;height:{H}px;background:{PAGE};position:relative;overflow:hidden">{"".join(html)}</body></html>'''
compose(page, 'board.png', W, H)
print('board ok')
