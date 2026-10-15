"""header.png: the recommended header lockups at real size, India (.in) beside global (.com), as the judges asked.
Desktop 1440x120: VANINDRA (sturdy cut, cap 28 px) hangs from the line; the line runs on as a 1 px page rule and the
navigation and 'Book a call' hang from it. India: emerald heavy line. Global: one gold hairline.
Phone 390x64: the pixel-fitted 17 px cut (India) and its gold-hairline twin (global).
Last row: the full name (lockup_horizontal_header.svg) for places the full name is required."""
import subprocess, base64, sys, re
from r5system import *
import r5system as R5
from build3 import phone_wordmark
import r4system as R4

MANROPE = os.path.join(SCRATCH, 'logo2', 'fonts', 'manrope')


def font_uri(weight):
    f = os.path.join(MANROPE, f'manrope-latin-{weight}-normal.woff2')
    return 'data:font/woff2;base64,' + base64.b64encode(open(f, 'rb').read()).decode()


def desktop_svg(cap=28.0, run_px=1312.0, rule_px=1.0, mode='india'):
    u = cap / 100.0
    if mode == 'india':
        wm, tot, st = vanindra('sturdy', bar=False)
        x0 = round(OVL * u)
        bar = rect(0, 0, x0 + (tot + OVR) * u, round(st.b * u))
        rule = rect(x0 + (tot + OVR) * u - 0.5, 0, run_px, rule_px)
        g = U(tr(wm, u, x0, 0), bar, rule)
        return svg(run_px, 40, [(g, EM)])
    # global: the caps hang from one gold hairline (>= 1.5 px at this size) that runs on as the page rule
    hair = max(HAIR_ST * u, 1.5)
    wm, tot, st = vanindra('sturdy', bar=False)
    x0 = OVL * u
    g = tr(wm, u, x0, hair * 0.55)
    line = U(rect(0, 0, x0 + (tot + OVR) * u, hair), rect(0, 0, run_px, rule_px))
    return svg(run_px, 40, [(g, EM), (line, GO)])


def phone_global(cap=17.0):
    """pixel-fitted letters (same snapping as the India phone cut) hanging from a 1 px gold line."""
    g = 100.0 / cap
    old = dict(R4.STURDY)
    R4.STURDY.update(S=3 * g, ns=2 * g, b=2 * g)
    wm, tot, st = vanindra('sturdy', bar=False, grid=g, widths={'N': 12 * g})
    R4.STURDY.clear(); R4.STURDY.update(old)
    u = cap / 100.0
    end_px = math.ceil(tot * u + 1.0)
    letters = tr(wm, u, 1, 0.0)                     # the caps' top pixel row sits under the 1 px gold line
    line = rect(0, 0, end_px + 2, 1)
    return svg(end_px + 2, 19, [(letters, EM), (line, GO)]), end_px + 2


def full_name_svg(cap=28.0):
    g, k = full_name_px(cap)
    b = bbox(g)
    return svg(math.ceil(b[2]) + 2, 40, [(g, EM)]), math.ceil(b[2]) + 2


def make(out_png):
    W1, H1 = 1440, 120
    cap = 28.0
    top, left = 46, 64
    d_in = desktop_svg(cap, run_px=W1 - 2 * left)
    d_com = desktop_svg(cap, run_px=W1 - 2 * left, mode='global')
    p_svg = open(os.path.join(HERE, 'wordmark_phone_17px.svg')).read()
    pw_px = float(re.search(r'width="([\d.]+)"', p_svg).group(1))
    pg_svg, pg_w = phone_global()
    f_svg, fw = full_name_svg(cap)
    b64 = lambda s: base64.b64encode(s.encode()).decode()
    nav = ''.join(f'<span>{t}</span>' for t in ['Work', 'Services', 'Packages', 'About'])

    def desk(svgs, cta_bg):
        return (f'<div class="desk"><img src="data:image/svg+xml;base64,{b64(svgs)}"><div class="nav">{nav}</div>'
                f'<div class="cta" style="background:{cta_bg}">Book a call</div></div>')

    def phone(svgs, w):
        return (f'<div class="phone"><img src="data:image/svg+xml;base64,{b64(svgs)}" width="{w:.0f}">'
                f'<div class="menu"><i></i><i></i></div></div>')
    html = f'''<!doctype html><html><head><style>
@font-face {{ font-family: Manrope; font-weight: 500; src: url({font_uri(500)}) format('woff2'); }}
@font-face {{ font-family: Manrope; font-weight: 600; src: url({font_uri(600)}) format('woff2'); }}
body {{ margin:0; background:#E9E2D3; font-family: Manrope, sans-serif; }}
#root {{ width:{W1}px; padding-bottom:24px; }}
.lab {{ font: 500 11px Manrope; color:#7a6a4a; padding: 18px 64px 8px; letter-spacing:.08em; text-transform:uppercase }}
.desk {{ position:relative; width:{W1}px; height:{H1}px; background:{IV}; }}
.desk img {{ position:absolute; left:{left}px; top:{top}px; }}
.nav {{ position:absolute; right:{left + 168}px; top:{top + 11}px; display:flex; gap:34px;
        font: 500 15px/1 Manrope; color:{EM}; letter-spacing:.01em; }}
.cta {{ position:absolute; right:{left}px; top:{top}px; font: 600 14px/1 Manrope; color:{IV}; padding: 13px 20px 12px; }}
.prow {{ display:flex; gap:40px; padding-left:64px; }}
.phone {{ position:relative; width:390px; height:64px; background:{IV}; }}
.phone img {{ position:absolute; left:16px; top:23px; }}
.menu {{ position:absolute; right:16px; top:25px; width:22px; }}
.menu i {{ display:block; height:1px; background:{EM}; margin-bottom:7px; }}
.menu i:first-child {{ height:2px; }}
.full {{ position:relative; width:{W1}px; height:{H1}px; background:{IV}; }}
.full img {{ position:absolute; left:{left}px; top:{top}px; }}
</style></head><body><div id="root">
<div class="lab">Desktop · India (.in) · wordmark_header.svg · cap 28 px</div>
{desk(d_in, EM)}
<div class="lab">Desktop · Global (.com) · global_header.svg · cap 28 px</div>
{desk(d_com, EM)}
<div class="lab">Phone 390 · India · wordmark_phone_17px.svg &nbsp;&nbsp;|&nbsp;&nbsp; Global · global_phone_17px.svg</div>
<div class="prow">{phone(p_svg, pw_px)}{phone(pg_svg, pg_w)}</div>
<div class="lab">Full name · lockup_horizontal_header.svg · cap 28 px</div>
<div class="full"><img src="data:image/svg+xml;base64,{b64(f_svg)}"></div>
</div></body></html>'''
    write(os.path.join(HERE, 'global_phone_17px.svg'), pg_svg)
    os.makedirs(os.path.join(HERE, '_work'), exist_ok=True)
    hp = os.path.join(HERE, '_work', '_header3.html')
    open(hp, 'w').write(html)
    subprocess.run(['node', os.path.join(HERE, '_r5', 'eshot.js'), hp, out_png, str(W1)], check=True)


if __name__ == '__main__':
    make(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'header.png'))
