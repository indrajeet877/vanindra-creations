"""reel_tag.png: a 540x960 Reel cover (real client photo, read-only) with the 'EDIT BY VANINDRA' tag.
The tag is the system itself: a hairline enters from the frame edge, EDIT BY hangs from it, the line thickens
into the headline and VANINDRA hangs from that. Ivory, one colour, no box, no stamp."""
import subprocess, base64, sys
from r3system import *
from r3latin import St, wordmark

PHOTO = '/home/user/vanindra-creations/assets/portfolio/reel_Ddl3VLbu4P5.jpg'


def tag_paths(cap_px, k=0.46, lead=22.0, lift=7.0):
    """Compact tag. A hairline enters from the frame edge (x=0) and becomes the headline over VANINDRA; VANINDRA hangs
    below it; EDIT BY stands on top of it (as a matra sits above the shirorekha), left-aligned with the V.
    Returns (path in px with the line top at y=0, width_px, (ymin, ymax))."""
    wm, tot, st = vanindra('header', ovl=0.0, ovr=OVR)
    stc = St(**CRE, bar=False)
    eb, tote, _ = wordmark(stc, 'EDIT BY', space={' ': 42.0, ('E', 'D'): 15, ('D', 'I'): 15, ('I', 'T'): 13, ('B', 'Y'): 8},
                           ovl=0, ovr=0, bar=False)
    u = cap_px / 100.0
    x_wm = lead / u
    hair = HAIR * 1.25
    line = U(rect(-2, 0, x_wm, hair), rect(x_wm - 0.5, 0, x_wm + tot + OVR, st.b))
    ebb = bbox(eb)
    eb_s = tr(eb, k, x_wm + 2.0, -ebb[3] * k - lift)       # stands on the line with a small gap
    g = tr(U(line, tr(wm, 1, x_wm, 0), eb_s), u, 0, 0)
    x0, y0, x1, y1 = bbox(g)
    return g, x1, (y0, y1)


def make(out_png, cap_px=20.0, top=148.0, photo=PHOTO):
    g, w, (ya, yb) = tag_paths(cap_px)
    h = yb - ya
    W, H = 540, 960
    tag = tr(g, 1, 0, top)
    svg_overlay = svg(W, H, [(tag, IV)])
    ov = os.path.join(HERE, '_work', '_reel_overlay.svg')
    write(ov, svg_overlay)
    img = base64.b64encode(open(photo, 'rb').read()).decode()
    ovb = base64.b64encode(svg_overlay.encode()).decode()
    html = f'''<!doctype html><html><body style="margin:0;background:#000">
<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden">
<img src="data:image/jpeg;base64,{img}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover">
<img src="data:image/svg+xml;base64,{ovb}" style="position:absolute;inset:0;width:{W}px;height:{H}px">
</div></body></html>'''
    hp = os.path.join(HERE, '_work', '_reel.html')
    open(hp, 'w').write(html)
    js = f'''const {{ chromium }} = require('/opt/node22/lib/node_modules/playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: {W}, height: {H} }} }});
await p.goto('file://{hp}'); await p.screenshot({{ path: '{out_png}' }}); await b.close(); }})();'''
    jp = os.path.join(HERE, '_work', '_reel.js')
    open(jp, 'w').write(js)
    subprocess.run(['node', jp], check=True)
    # also save the tag itself as an asset (ivory on transparent, and emerald)
    tg = tr(g, 1, 0, -ya + 1)
    write(os.path.join(HERE, 'reel_tag_ivory.svg'), svg(w + 2, h + 2, [(tg, IV)]))
    write(os.path.join(HERE, 'reel_tag_emerald.svg'), svg(w + 2, h + 2, [(tg, EM)]))


if __name__ == '__main__':
    make(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'reel_tag.png'))
