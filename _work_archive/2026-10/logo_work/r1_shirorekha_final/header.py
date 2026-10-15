"""header.png: the recommended header lockups at real size.
Desktop 1440x120 on ivory: header-cut VANINDRA hanging from the line, which steps to a hairline for CREATIONS and then
runs on as the page's top rule; the navigation hangs from the same rule. Phone 390x64: VANINDRA alone (header cut)."""
import subprocess, base64, sys
from r3system import *

MANROPE = os.path.join(SCRATCH, 'logo2', 'fonts', 'manrope')


def font_uri(weight):
    f = os.path.join(MANROPE, f'manrope-latin-{weight}-normal.woff2')
    return 'data:font/woff2;base64,' + base64.b64encode(open(f, 'rb').read()).decode()


def lockup_px(cap_px, with_creations=True, run_to=None, k=0.52, gap=34.0):
    """Header-cut lockup in px; line top at y=0, x=0 at the line's left end. run_to (px): extend the hairline."""
    u = cap_px / 100.0
    wm, tot, st = vanindra('header', ovl=OVL, ovr=0.0 if with_creations else OVR)
    parts = [wm]
    hair = HAIR * 1.35
    if with_creations:
        cr, totc, _ = creations(bar=False, ovl=0.0, ovr=0.0)
        parts.append(tr(cr, k, tot + gap, 0))
        end = tot + gap + totc * k + OVR
        line = U(rect(-OVL, 0, tot, st.b), rect(tot - 1, 0, end, hair))
    else:
        end = tot + OVR
        line = rect(-OVL, 0, end, st.b)
    if run_to is not None:
        line = U(line, rect(end - 1, 0, run_to / u + OVL, hair))
    g = tr(U(*parts, line), u, OVL * u, 0)
    return g, (end + OVL) * u


def make(out_png):
    # desktop
    W1, H1 = 1440, 120
    cap = 28.0
    top = 44.0
    left = 64.0
    g, wpx = lockup_px(cap, True, run_to=W1 - 2 * left)
    d_svg = svg(W1 - 2 * left + 4, 60, [(tr(g, 1, 0, 0), EM)])
    # phone
    W2, H2 = 390, 64
    cap2 = 17.0
    g2, w2 = lockup_px(cap2, False)
    p_svg = svg(w2 + 4, 30, [(g2, EM)])
    b64 = lambda s: base64.b64encode(s.encode()).decode()
    nav_items = ['Work', 'Services', 'Packages', 'About']
    nav = ''.join(f'<span>{t}</span>' for t in nav_items)
    html = f'''<!doctype html><html><head><style>
@font-face {{ font-family: Manrope; font-weight: 500; src: url({font_uri(500)}) format('woff2'); }}
@font-face {{ font-family: Manrope; font-weight: 600; src: url({font_uri(600)}) format('woff2'); }}
body {{ margin:0; background:#8f8f8f; font-family: Manrope, sans-serif; }}
.lab {{ font: 500 12px Manrope; color:#f6f1e7; padding: 14px 24px 6px; letter-spacing:.02em }}
.desk {{ position:relative; width:{W1}px; height:{H1}px; background:{IV}; }}
.desk img {{ position:absolute; left:{left}px; top:{top}px; }}
.nav {{ position:absolute; right:{left + 172}px; top:{top + 6 + HAIR * 1.35 * cap / 100}px; display:flex; gap:34px;
        font: 500 15px/1 Manrope; color:{EM}; letter-spacing:.01em; }}
.cta {{ position:absolute; right:{left}px; top:{top}px; font: 600 14px/1 Manrope; color:{IV};
        background:{EM}; padding: 13px 20px 12px; }}
.phone {{ position:relative; width:{W2}px; height:{H2}px; background:{IV}; margin-left:24px; }}
.phone img {{ position:absolute; left:16px; top:22px; }}
.menu {{ position:absolute; right:16px; top:24px; width:22px; }}
.menu i {{ display:block; height:1.6px; background:{EM}; margin-bottom:7px; }}
.menu i:first-child {{ height:2.6px; }}
</style></head><body>
<div class="lab">Desktop header, 1440 x 120, real size: header cut, VANINDRA cap height {cap:.0f} px, CREATIONS {cap*0.52:.1f} px; the line runs on as the page rule and the navigation hangs from it.</div>
<div class="desk"><img src="data:image/svg+xml;base64,{b64(d_svg)}"><div class="nav">{nav}</div><div class="cta">Book a call</div></div>
<div class="lab">Phone header, 390 x 64, real size: VANINDRA only (cap {cap2:.0f} px). Menu icon = the line, twice.</div>
<div style="padding-bottom:20px"><div class="phone"><img src="data:image/svg+xml;base64,{b64(p_svg)}"><div class="menu"><i></i><i></i></div></div></div>
</body></html>'''
    hp = os.path.join(HERE, '_work', '_header.html')
    open(hp, 'w').write(html)
    js = f'''const {{ chromium }} = require('/opt/node22/lib/node_modules/playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: {W1}, height: 300 }}, deviceScaleFactor: 1 }});
await p.goto('file://{hp}'); await p.waitForTimeout(200); await p.screenshot({{ path: '{out_png}', fullPage: true }}); await b.close(); }})();'''
    jp = os.path.join(HERE, '_work', '_header.js')
    open(jp, 'w').write(js)
    subprocess.run(['node', jp], check=True)


if __name__ == '__main__':
    make(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'header.png'))
