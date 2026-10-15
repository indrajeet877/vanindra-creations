"""header.png: the recommended header lockups at real size.
Desktop 1440x120 on ivory: VANINDRA (sturdy cut, cap 28 px) hangs from the line; the line steps down to a 1 px rule
that runs on across the page; the navigation and the 'Book a call' button hang from that rule.
Phone 390x64: the pixel-fitted cut (wordmark_phone_17px.svg) at its native 17 px cap.
Third row: the full-name header lockup (lockup_horizontal_header.svg) for places the full name is required."""
import subprocess, base64, sys
from r4system import *
from build2 import phone_wordmark

MANROPE = os.path.join(SCRATCH, 'logo2', 'fonts', 'manrope')


def font_uri(weight):
    f = os.path.join(MANROPE, f'manrope-latin-{weight}-normal.woff2')
    return 'data:font/woff2;base64,' + base64.b64encode(open(f, 'rb').read()).decode()


def desktop_svg(cap=28.0, run_px=1312.0, rule_px=1.0):
    u = cap / 100.0
    wm, tot, st = vanindra('sturdy', bar=False)
    x0 = OVL * u
    bar = rect(0, 0, x0 + (tot + OVR) * u, st.b * u)
    rule = rect(x0 + (tot + OVR) * u - 0.5, 0, run_px, rule_px)
    g = U(tr(wm, u, x0, 0), bar, rule)
    return svg(run_px, 40, [(g, EM)])


def full_name_svg(cap=28.0):
    letters, line, end = full_name('sturdy')
    u = cap / 100.0
    g = tr(U(letters, line), u, OVL * u, 0)
    b = bbox(g)
    return svg(b[2] + 2, 40, [(g, EM)]), b[2] + 2


def make(out_png):
    W1, H1 = 1440, 120
    cap = 28.0
    top, left = 46, 64
    d_svg = desktop_svg(cap, run_px=W1 - 2 * left)
    pw, ptot = phone_wordmark(17.0)
    p_svg = open(os.path.join(HERE, 'wordmark_phone_17px.svg')).read()
    import re
    pw_px = float(re.search(r'width="([\d.]+)"', p_svg).group(1))
    f_svg, fw = full_name_svg(cap)
    b64 = lambda s: base64.b64encode(s.encode()).decode()
    nav = ''.join(f'<span>{t}</span>' for t in ['Work', 'Services', 'Packages', 'About'])
    html = f'''<!doctype html><html><head><style>
@font-face {{ font-family: Manrope; font-weight: 500; src: url({font_uri(500)}) format('woff2'); }}
@font-face {{ font-family: Manrope; font-weight: 600; src: url({font_uri(600)}) format('woff2'); }}
body {{ margin:0; background:#8f8f8f; font-family: Manrope, sans-serif; }}
.lab {{ font: 500 12px Manrope; color:#f6f1e7; padding: 14px 24px 6px; letter-spacing:.02em }}
.desk {{ position:relative; width:{W1}px; height:{H1}px; background:{IV}; }}
.desk img {{ position:absolute; left:{left}px; top:{top}px; }}
.nav {{ position:absolute; right:{left + 168}px; top:{top + 11}px; display:flex; gap:34px;
        font: 500 15px/1 Manrope; color:{EM}; letter-spacing:.01em; }}
.cta {{ position:absolute; right:{left}px; top:{top}px; font: 600 14px/1 Manrope; color:{IV};
        background:{EM}; padding: 13px 20px 12px; }}
.phone {{ position:relative; width:390px; height:64px; background:{IV}; margin-left:24px; }}
.phone img {{ position:absolute; left:16px; top:23px; }}
.menu {{ position:absolute; right:16px; top:25px; width:22px; }}
.menu i {{ display:block; height:1px; background:{EM}; margin-bottom:7px; }}
.menu i:first-child {{ height:2px; }}
.full {{ position:relative; width:{W1}px; height:{H1}px; background:{IV}; }}
.full img {{ position:absolute; left:{left}px; top:{top}px; }}
</style></head><body>
<div class="lab">Desktop header, 1440 x 120, real size (recommended): wordmark_header.svg (sturdy cut), VANINDRA cap {cap:.0f} px. The line steps down to a 1 px rule that runs on across the page; the navigation and "Book a call" hang from it.</div>
<div class="desk"><img src="data:image/svg+xml;base64,{b64(d_svg)}"><div class="nav">{nav}</div><div class="cta">Book a call</div></div>
<div class="lab">Phone header, 390 x 64, real size: wordmark_phone_17px.svg, pixel-fitted at a 17 px cap (every stem and the line on whole pixels; hairlines 1.7 px).</div>
<div style="padding-bottom:4px"><div class="phone"><img src="data:image/svg+xml;base64,{b64(p_svg)}" width="{pw_px:.0f}"><div class="menu"><i></i><i></i></div></div></div>
<div class="lab">Full name, when it must be complete (email signature, invoice, deck footer): lockup_horizontal_header.svg, cap {cap:.0f} px. CREATIONS stands on VANINDRA's baseline under the same line (no superscript).</div>
<div style="padding-bottom:20px"><div class="full"><img src="data:image/svg+xml;base64,{b64(f_svg)}"></div></div>
</body></html>'''
    os.makedirs(os.path.join(HERE, '_work'), exist_ok=True)
    hp = os.path.join(HERE, '_work', '_header2.html')
    open(hp, 'w').write(html)
    subprocess.run(['node', os.path.join(HERE, '_w2', 'shot.js'), hp, out_png, str(W1)], check=True)


if __name__ == '__main__':
    make(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'header.png'))
