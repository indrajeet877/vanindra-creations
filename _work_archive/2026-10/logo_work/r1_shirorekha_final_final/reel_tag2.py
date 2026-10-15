"""reel_tag.png: a 540x960 Reel cover (real client photo, read-only) with the 'EDIT BY / VANINDRA' credit.
The credit is the system itself, in ivory, no box, no stamp: the line starts at the safe margin (never at the frame
edge), EDIT BY stands on its hairline, the line steps up to the heavy bar and VANINDRA (sturdy cut) hangs from it.
EDIT BY is drawn in the same alphabet (credit cut: every stroke >= 1.5 px at its real size)."""
import subprocess, base64, sys
from r4system import *
from r3latin import St
from r4latin import word, CRE_BUILD

PHOTO = '/home/user/vanindra-creations/assets/portfolio/reel_Ddl3VLbu4P5.jpg'
CREDIT = dict(H=100, b=4.5, S=21.0, h=15.0, ns=15.0, t0=14.0, Tf=22.0, lb=2.0, top=15.0, trap=0)
CREDIT_SP = {' ': 46.0, ('E', 'D'): 20, ('D', 'I'): 20, ('I', 'T'): 16, ('B', 'Y'): 10}


def tag_px(cap=21.0, eb_cap=10.5, style='stair', gap_px=8.0, rise_px=4.0, hair_px=1.5):
    """Returns (path in px, line top at y=0, x=0 at the line's left end)."""
    u = cap / 100.0
    ue = eb_cap / 100.0
    wm, tot, st = vanindra('sturdy', bar=False)
    stc = St(**CREDIT, bar=False)
    eb, tote, _ = word(stc, 'EDIT BY', CREDIT_SP, build=CRE_BUILD)
    ebw = tote * ue
    if style == 'stair':
        x_v = ebw + gap_px                         # VANINDRA starts after EDIT BY
        line = U(rect(0, 0, x_v + 0.5, hair_px), rect(x_v - OVL * u, 0, x_v + (tot + OVR) * u, st.b * u))
        ebp = tr(eb, ue, 0, -rise_px - 100 * ue)
    else:                                          # EDIT BY stands on the bar, left-aligned with the V
        x_v = OVL * u
        line = rect(0, 0, x_v + (tot + OVR) * u, st.b * u)
        ebp = tr(eb, ue, x_v, -rise_px - 100 * ue)
    g = U(line, tr(wm, u, x_v, 0), ebp)
    return g


def make(out_png, cap=21.0, left=30.0, top=152.0, photo=PHOTO, style='stair'):
    g = tag_px(cap, style=style)
    W, H = 540, 960
    tag = tr(g, 1, left, top)
    svg_overlay = svg(W, H, [(tag, IV)])
    img = base64.b64encode(open(photo, 'rb').read()).decode()
    ovb = base64.b64encode(svg_overlay.encode()).decode()
    html = f'''<!doctype html><html><body style="margin:0;background:#000">
<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden">
<img src="data:image/jpeg;base64,{img}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover">
<img src="data:image/svg+xml;base64,{ovb}" style="position:absolute;inset:0;width:{W}px;height:{H}px">
</div></body></html>'''
    os.makedirs(os.path.join(HERE, '_work'), exist_ok=True)
    hp = os.path.join(HERE, '_work', '_reel2.html')
    open(hp, 'w').write(html)
    subprocess.run(['node', os.path.join(HERE, '_w2', 'shot.js'), hp, out_png, str(W)], check=True)
    # the tag itself as assets (designed for a 1080 x 1920 cover at 2x these px values)
    b = bbox(g)
    tg = tr(g, 2, -b[0] * 2 + 2, -b[1] * 2 + 2)
    bw, bh = (b[2] - b[0]) * 2 + 4, (b[3] - b[1]) * 2 + 4
    write(os.path.join(HERE, 'reel_tag_ivory.svg'), svg(bw, bh, [(tg, IV)]))
    write(os.path.join(HERE, 'reel_tag_emerald.svg'), svg(bw, bh, [(tg, EM)]))


if __name__ == '__main__':
    make(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'reel_tag.png'),
         style=sys.argv[2] if len(sys.argv) > 2 else 'stair')
