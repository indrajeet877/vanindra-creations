"""reel_tag.png: a 540x960 Reel cover (real client photo, read-only) with the 'EDIT BY / VANINDRA' credit.
F1 polish (judges): the step from the hairline to the heavy line is now 2.4x (it was ~1 px, read as an uneven rule);
EDIT BY is drawn with 1.4 px stems (it was 2.2 px and looked darker than the name it credits); VANINDRA is the sturdy
cut (every hairline >= 2.2 px here); the credit sits on a calm wall, not on hair texture. Emerald on light footage,
ivory on dark footage (reel_tag_dark.png)."""
import subprocess, base64, sys
from r5system import *
from r3latin import St
from r4latin import word, CRE_BUILD

PHOTO_LIGHT = '/home/user/vanindra-creations/assets/portfolio/reel_DSo0ikHkVkb.jpg'
PHOTO_DARK = '/home/user/vanindra-creations/assets/portfolio/reel_Ddl3VLbu4P5.jpg'
# credit cut of EDIT BY: drawn for a 10 px cap at 540 (20 px at 1080): stems 1.4 px, hairlines 1.0 px
CREDIT = dict(H=100, b=4.5, S=14.0, h=10.0, ns=11.0, t0=10.0, Tf=15.0, lb=1.6, top=10.0, trap=0)
CREDIT_SP = {' ': 52.0, ('E', 'D'): 22, ('D', 'I'): 22, ('I', 'T'): 18, ('B', 'Y'): 12}


def tag_px(cap=22.0, eb_cap=10.0, gap_px=9.0, rise_px=4.0, hair_px=1.25, bar_px=3.0):
    """Returns the credit as a path in px (line top at y=0, x=0 at the line's left end)."""
    u = cap / 100.0
    ue = eb_cap / 100.0
    wm, tot, st = vanindra('sturdy', bar=False)
    stc = St(**CREDIT, bar=False)
    eb, tote, _ = word(stc, 'EDIT BY', CREDIT_SP, build=CRE_BUILD)
    ebw = tote * ue
    x_v = ebw + gap_px
    line = U(rect(0, 0, x_v + 0.5, hair_px), rect(x_v - OVL * u, 0, x_v + (tot + OVR) * u, bar_px))
    ebp = tr(eb, ue, 0, -rise_px - 100 * ue)
    return U(line, tr(wm, u, x_v, bar_px * 0.45), ebp)


def make(out_png, photo, ink, left=30.0, top=176.0, W=540, H=960):
    g = tag_px()
    tag = tr(g, 1, left, top)
    svg_overlay = svg(W, H, [(tag, ink)])
    img = base64.b64encode(open(photo, 'rb').read()).decode()
    ovb = base64.b64encode(svg_overlay.encode()).decode()
    html = f'''<!doctype html><html><body style="margin:0;background:#000"><div id="root">
<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden">
<img src="data:image/jpeg;base64,{img}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover">
<img src="data:image/svg+xml;base64,{ovb}" style="position:absolute;inset:0;width:{W}px;height:{H}px">
</div></div></body></html>'''
    os.makedirs(os.path.join(HERE, '_work'), exist_ok=True)
    hp = os.path.join(HERE, '_work', '_reel3.html')
    open(hp, 'w').write(html)
    subprocess.run(['node', os.path.join(HERE, '_r5', 'eshot.js'), hp, out_png, str(W)], check=True)
    return g


def assets(g):
    """the credit as files, drawn for a 1080 x 1920 cover (2x the 540 px values)."""
    b = bbox(g)
    tg = tr(g, 2, -b[0] * 2 + 2, -b[1] * 2 + 2)
    bw, bh = (b[2] - b[0]) * 2 + 4, (b[3] - b[1]) * 2 + 4
    write(os.path.join(HERE, 'reel_tag_ivory.svg'), svg(bw, bh, [(tg, IV)]))
    write(os.path.join(HERE, 'reel_tag_emerald.svg'), svg(bw, bh, [(tg, EM)]))


if __name__ == '__main__':
    g = make(os.path.join(HERE, 'reel_tag.png'), PHOTO_LIGHT, EM)
    make(os.path.join(HERE, 'reel_tag_dark.png'), PHOTO_DARK, IV, top=152.0)
    assets(g)
