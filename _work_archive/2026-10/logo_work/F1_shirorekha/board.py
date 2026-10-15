"""board.png: 1600 x 2000 presentation board for the team vote (ivory, tiny labels, no paragraphs)."""
import subprocess, base64
from r5system import *
from build3 import stacked_parts, horizontal
from header3 import desktop_svg, phone_global, font_uri

B64 = lambda s: base64.b64encode(s.encode()).decode()
PNG = lambda p: 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
SVGF = lambda n: 'data:image/svg+xml;base64,' + B64(open(os.path.join(HERE, n)).read())
SVGS = lambda s: 'data:image/svg+xml;base64,' + B64(s)
LAB = '#8C7A55'
LINE = '#E3D9C6'
CARD = '#FBF8F2'


def fit_svg(path, w, h, ink, bg=None, fill=0.8, extra=None):
    x0, y0, x1, y1 = bbox(path)
    s = min(w * fill / (x1 - x0), h * fill / (y1 - y0))
    g = tr(path, s, w / 2 - (x0 + x1) / 2 * s, h / 2 - (y0 + y1) / 2 * s)
    layers = [(g, ink)]
    return svg(w, h, layers, bg=bg)


def main():
    W, H = 1600, 2000
    M = 80
    # pieces
    mk, _ = mark5('master')
    hero = fit_svg(mk, 680, 680, GL, bg=EM, fill=0.50)
    wm, tot, st = vanindra('master')
    wm_svg = fit_svg(wm, 736, 400, EM, fill=0.74)
    mk_pos, words, Wst, Hst = stacked_parts()
    stack = U(mk_pos, words)
    one = [fit_svg(stack, 291, 430, EM, bg=CARD, fill=0.72), fit_svg(stack, 291, 430, IV, bg=EM, fill=0.72),
           fit_svg(stack, 291, 430, GO, bg='#FFFFFF', fill=0.72)]
    d_in = desktop_svg(28.0, run_px=1440 - 128)
    p_in = open(os.path.join(HERE, 'wordmark_phone_17px.svg')).read()
    import re
    p_in_w = float(re.search(r'width="([\d.]+)"', p_in).group(1))
    p_gl, p_gl_w = phone_global()
    nav = ''.join(f'<span>{t}</span>' for t in ['Work', 'Services', 'Packages', 'About'])

    def lab(t, x, y, color=LAB, align='left', w=None):
        st_ = f'left:{x}px;top:{y}px;' + (f'width:{w}px;text-align:{align};' if w else '')
        return f'<div class="lab" style="{st_}color:{color}">{t}</div>'

    def tile(x, y, w, h, inner, bg=CARD, border=True, extra=''):
        b = f'box-shadow: inset 0 0 0 1px {LINE};' if border else ''
        return f'<div class="tile" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};{b}{extra}">{inner}</div>'

    def im(src, x, y, w, h, extra=''):
        return f'<img src="{src}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">'

    parts = []
    # masthead
    parts.append(lab('VanIndra Creations', M, 40, EM))
    parts.append(lab('Identity · Shirorekha · F1', 0, 40, LAB, 'right', W - M))
    parts.append(f'<div style="position:absolute;left:{M}px;top:62px;width:{W - 2 * M}px;height:1px;background:{EM}"></div>')
    # row 1
    y1 = 92
    parts.append(tile(M, y1, 680, 680, im(SVGS(hero), 0, 0, 680, 680) + lab('Primary mark · va', 22, 20, '#B9A26A'), bg=EM, border=False))
    parts.append(tile(784, y1, 736, 400, im(SVGS(wm_svg), 0, 0, 736, 400) + lab('Wordmark', 22, 20)))
    av_in = SVGF('mark_on_emerald.svg')
    av_gl = SVGF('mark_global_on_emerald.svg')
    ay = 74
    av = (im(av_in, 60, ay, 110, 110, 'border-radius:50%') + im(av_in, 190, ay + 70, 40, 40, 'border-radius:50%') +
          im(av_gl, 392, ay, 110, 110, 'border-radius:50%') + im(av_gl, 522, ay + 70, 40, 40, 'border-radius:50%') +
          lab('Instagram · 110 / 40 px', 22, 20) + lab('India', 60, ay + 132) + lab('Global · USD · South India', 392, ay + 132))
    parts.append(tile(784, y1 + 424, 736, 256, av, bg='#FFFFFF'))
    # row 2: website
    y2 = y1 + 680 + 40
    parts.append(lab('Website · desktop 1440 · real size', M, y2 - 22))
    desk = (im(SVGS(d_in), 64, 46, 1312, 40) +
            f'<div class="nav" style="right:{64 + 168}px;top:{46 + 11}px">{nav}</div>'
            f'<div class="cta" style="right:64px;top:46px">Book a call</div>')
    parts.append(tile(M, y2, 1440, 120, desk, bg=IV))
    y2b = y2 + 120 + 40
    parts.append(lab('Phone 390 · India / Global', M, y2b - 22))

    def phone(src, w):
        return im(src, 16, 23, w, 19) + '<div class="menu"><i></i><i></i></div>'
    parts.append(tile(M, y2b, 390, 64, phone(SVGS(p_in), p_in_w), bg=IV))
    parts.append(tile(M + 414, y2b, 390, 64, phone(SVGS(p_gl), p_gl_w), bg=IV))
    fav = (f'<div class="tab"><img src="{SVGF("mark_small.svg")}" width="16" height="16"><span>VanIndra Creations</span></div>')
    parts.append(lab('Favicon · 16 px', M + 828, y2b - 22))
    parts.append(tile(M + 828, y2b, 612, 64, fav, bg='#FFFFFF'))
    # row 3
    y3 = y2b + 64 + 48
    rh = 2000 - 92 - y3
    rw = round(rh * 540 / 960)
    parts.append(lab('Reel credit · Edit by', M, y3 - 22))
    parts.append(tile(M, y3, rw, rh, im(PNG(os.path.join(HERE, 'reel_tag.png')), 0, 0, rw, rh), border=False, extra='overflow:hidden'))
    xg = M + rw + 24
    wg = W - M - xg
    hg = round((rh - 24) * 0.46)
    parts.append(lab('Global · USD', xg, y3 - 22))
    gsvg = open(os.path.join(HERE, 'global.svg')).read()
    gw = float(re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', gsvg).group(1))
    gh = float(re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', gsvg).group(2))
    iw = wg * 0.80
    ih = iw * gh / gw
    parts.append(tile(xg, y3, wg, hg, im(SVGS(gsvg), (wg - iw) / 2, (hg - ih) / 2, iw, ih), bg=IV))
    yo = y3 + hg + 48
    ho = rh - hg - 48
    wo = (wg - 2 * 16) / 3
    parts.append(lab('One colour · emerald / ivory / gold', xg, yo - 22))
    for i, s in enumerate(one):
        bgc = [CARD, EM, '#FFFFFF'][i]
        parts.append(tile(xg + i * (wo + 16), yo, wo, ho, im(SVGS(s.replace('width="291"', f'width="{wo:.0f}"')), 0, (ho - wo * 430 / 291) / 2, wo, wo * 430 / 291), bg=bgc, border=(i != 1)))
    # footer
    parts.append(f'<div style="position:absolute;left:{M}px;top:{H - 56}px;width:{W - 2 * M}px;height:1px;background:{LINE}"></div>')
    parts.append(lab('Everything hangs from one line', M, H - 44, EM))
    parts.append(lab('Team vote · October 2026', 0, H - 44, LAB, 'right', W - M))

    html = f'''<!doctype html><html><head><style>
@font-face {{ font-family: Manrope; font-weight: 500; src: url({font_uri(500)}) format('woff2'); }}
@font-face {{ font-family: Manrope; font-weight: 600; src: url({font_uri(600)}) format('woff2'); }}
body {{ margin:0; background:{IV}; }}
#root {{ position:relative; width:{W}px; height:{H}px; background:{IV}; overflow:hidden; font-family: Manrope, sans-serif; }}
.lab {{ position:absolute; font: 600 10px/1 Manrope; letter-spacing:.14em; text-transform:uppercase; white-space:nowrap; }}
.tile {{ position:absolute; overflow:hidden; }}
.nav {{ position:absolute; display:flex; gap:34px; font: 500 15px/1 Manrope; color:{EM}; letter-spacing:.01em; }}
.cta {{ position:absolute; font: 600 14px/1 Manrope; color:{IV}; background:{EM}; padding: 13px 20px 12px; }}
.menu {{ position:absolute; right:16px; top:25px; width:22px; }}
.menu i {{ display:block; height:1px; background:{EM}; margin-bottom:7px; }}
.menu i:first-child {{ height:2px; }}
.tab {{ position:absolute; left:20px; top:16px; display:flex; align-items:center; gap:8px; background:#EEF0F2;
        padding:8px 14px; border-radius:8px 8px 0 0; font: 500 13px/1 Manrope; color:#222; height:16px; }}
</style></head><body><div id="root">{''.join(parts)}</div></body></html>'''
    hp = os.path.join(HERE, '_work', '_board.html')
    open(hp, 'w').write(html)
    subprocess.run(['node', os.path.join(HERE, '_r5', 'eshot.js'), hp, os.path.join(HERE, 'board.png'), str(W)], check=True)


if __name__ == '__main__':
    main()
