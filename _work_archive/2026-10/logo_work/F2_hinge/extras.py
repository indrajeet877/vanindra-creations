"""reel_tag.png, reel_tag_light.png, header.png, global.png (HTML -> Playwright)."""
import sys, base64, subprocess, os
sys.path.insert(0, '.')
from build import *

PORT = '/home/user/vanindra-creations/assets/portfolio'


def uri_svg(svgtext): return 'data:image/svg+xml;base64,' + base64.b64encode(svgtext.encode()).decode()
def uri_file(path, mime): return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def compose(html, out, w, h):
    os.makedirs('work', exist_ok=True)
    open('work/_tmp.html', 'w').write(html)
    subprocess.run(['node', 'compose.js', 'work/_tmp.html', out, str(w), str(h)], check=True)


def ui_label(text, size, color, weight=500):
    """UI text for the mock pages only (nav links, captions) — not part of the identity."""
    t = vt.text_path(text, family='manrope', weight=weight, size=size)
    b = t.bounds; w = b[2] - b[0]
    y0 = -size * 0.74; h = size * 1.0
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w+2:.1f}" height="{h:.1f}" viewBox="{b[0]-1:.1f} {y0:.1f} {w+2:.1f} {h:.1f}" overflow="visible"><path d="{t.d}" fill="{color}"/></svg>'


# ---------------- REEL CREDIT: 'edit by' (drawn in the same system) over the small-cut staircase
EB = edit_by(ps)


def reel_tag_svg(ink, icol, unit=0.1):
    """'edit by' set at the staircase's x-height ratio 0.42, left-aligned with the V, one x-height above."""
    stp = stair_parts(STS, ink, icol)
    sb = bbox(*[p for p, c in stp])
    s = 0.42
    eb = vt.bounds(EB['ink'])
    lab = T(T(EB['ink'], -eb[0], 0, s, s), sb[0] + 10, sb[3] + ps.X * 0.62)
    return fit(stp + [(lab, ink)], unit=unit)


def reel_html(photo, svg, pos):
    return f'''<!doctype html><html><body style="margin:0;width:540px;height:960px;overflow:hidden;background:#000">
<img src="{uri_file(photo, 'image/jpeg')}" style="position:absolute;left:0;top:0;width:540px;height:960px;object-fit:cover">
<img src="{uri_svg(svg)}" style="position:absolute;{pos};height:64px;display:block">
</body></html>'''


if __name__ == '__main__':
    # F2 contrast rule: on photographs the credit is ALWAYS one colour (gold is only used on flat brand grounds)
    tag_em = reel_tag_svg(EM, EM)        # light footage: all emerald
    tag_iv = reel_tag_svg(IV, IV)        # dark footage: all ivory
    write('reel_tag_emerald.svg', tag_em)
    write('reel_tag_ivory.svg', tag_iv)
    # inside both the 9:16 playback-safe area and the 3:4 profile-grid crop (y 120..840)
    compose(reel_html(f'{PORT}/reel_Ddl3VLbu4P5.jpg', tag_iv, 'left:30px;top:150px'), 'reel_tag.png', 540, 960)
    compose(reel_html(f'{PORT}/reel_Da0liqXAemF.jpg', tag_em, 'left:30px;top:150px'), 'reel_tag_light.png', 540, 960)

    # ---------------- HEADER (recommended: the small-cut staircase)
    nav = [ui_label(t, 30, EM, 500) for t in ['Work', 'Services', 'Pricing', 'About']]
    cta = ui_label('Book a free call', 30, IV, 600)
    navhtml = ''.join(f'<img src="{uri_svg(n)}" style="height:13.5px">' for n in nav)
    burger = '<svg width="22" height="14" viewBox="0 0 22 14"><rect y="1" width="22" height="1.6" fill="#0B2A20"/><rect y="11" width="14" height="1.6" fill="#0B2A20" x="8"/></svg>'
    burger_iv = burger.replace('#0B2A20', '#F6F1E7')
    cap1 = ui_label('Desktop header 1440 × 120 · staircase (small cut) 64 px tall · cap height 31 px', 26, '#5b5b55', 500)
    cap2 = ui_label('Phone header 390 × 64 · staircase 44 px tall · cap 21 px', 26, '#5b5b55', 500)
    cap3 = ui_label('Same, on emerald (ivory + soft-gold shared stroke)', 26, '#5b5b55', 500)
    hs_em = open('header_staircase_emerald.svg').read(); hs_iv = open('header_staircase_ivory.svg').read()
    hdr = f'''<!doctype html><html><body style="margin:0;width:1440px;height:340px;background:#E7E4DC;font-family:sans-serif">
<div style="position:absolute;left:0;top:0;width:1440px;height:120px;background:{IV};display:flex;align-items:center;justify-content:space-between;padding:0 64px;box-sizing:border-box;border-bottom:1px solid #e3dccd">
  <img src="{uri_svg(hs_em)}" style="height:64px;display:block">
  <div style="display:flex;align-items:center;gap:40px">{navhtml}
    <div style="background:{EM};border-radius:999px;padding:13px 22px;display:flex"><img src="{uri_svg(cta)}" style="height:13.5px"></div></div>
</div>
<img src="{uri_svg(cap1)}" style="position:absolute;left:64px;top:136px;height:12px">
<div style="position:absolute;left:64px;top:170px;width:390px;height:64px;background:{IV};display:flex;align-items:center;justify-content:space-between;padding:0 18px;box-sizing:border-box;border-radius:10px 10px 0 0;box-shadow:0 0 0 1px #d8d1c2">
  <img src="{uri_svg(hs_em)}" style="height:44px;display:block">{burger}
</div>
<div style="position:absolute;left:64px;top:234px;width:390px;height:76px;background:#fff;box-shadow:0 0 0 1px #d8d1c2;border-radius:0 0 10px 10px"></div>
<img src="{uri_svg(cap2)}" style="position:absolute;left:480px;top:196px;height:12px">
<div style="position:absolute;left:880px;top:170px;width:390px;height:64px;background:{EM};display:flex;align-items:center;justify-content:space-between;padding:0 18px;box-sizing:border-box;border-radius:10px">
  <img src="{uri_svg(hs_iv)}" style="height:44px;display:block">{burger_iv}</div>
<img src="{uri_svg(cap3)}" style="position:absolute;left:880px;top:246px;height:12px">
</body></html>'''
    compose(hdr, 'header.png', 1440, 340)

    # ---------------- GLOBAL
    subprocess.run(['node', '../toolkit/render.js', 'png', 'global.svg', 'global.png', '1600'], check=True)
    print('extras done')
