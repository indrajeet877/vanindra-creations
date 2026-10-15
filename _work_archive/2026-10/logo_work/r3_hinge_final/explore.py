"""explore.png: the final-round studies (what was tried, what each taught)."""
import sys, os, subprocess
sys.path.insert(0, '.')
from build import *
from extras import compose, uri_svg, uri_file

os.makedirs('work/explore', exist_ok=True)
W = 'work/explore'


def svg_of(parts, unit=0.1, pad=0):
    return fit(parts, unit=unit, padx=pad, pady=pad)


# ---- study 1: the name at header size, four ways (same cap height, 2x pixel zoom of a real 1x render)
old = open('../r3_hinge/_header_emeraldink.svg').read() if os.path.exists('../r3_hinge/_header_emeraldink.svg') else None
p784 = P(**dict(SMALL, Itop=812))
wm_old_small = wordmark(p784)
wm724 = wordmark(ps)
cells = [
    ('A · Round-3 hinge (I rises behind the n)', svg_of([(wm_old_small['ink'], EM), (wm_old_small['I'], EM)]), 36),
    ('B · same, I lowered to the ascender', svg_of([(wm724['ink'], EM), (wm724['I'], GD)]), 32),
    ('C · ligature released (text cut)', svg_of([(WT['ink'], EM), (WT['I'], GD)]), 32),
    ('D · staircase (chosen)', svg_of(stair_parts(STS, EM, GD)), 64),
]
html = '<!doctype html><html><body style="margin:0;background:#F6F1E7;width:720px">' + ''.join(
    f'<div style="display:flex;align-items:center;gap:18px;padding:10px 14px;border-bottom:1px solid #e3dccd">'
    f'<div style="width:300px;font:13px Helvetica,Arial;color:#333">{t}</div><img src="{uri_svg(s)}" style="height:{h}px"></div>'
    for t, s, h in cells) + '</body></html>'
compose(html, f'{W}/e1_1x.png', 720, 4 * 85)
subprocess.run(['convert', f'{W}/e1_1x.png', '-filter', 'point', '-resize', '200%', f'{W}/e1.png'], check=True)

# ---- study 2: the one-line hinge at display, I at 784 vs 724
p_784 = P(**dict(DISPLAY, Itop=784, gap=16, ie=37))
w784 = wordmark(p_784); w724 = wordmark(pd)
open(f'{W}/e2.svg', 'w').write(fit([(w784['ink'], EM), (w784['I'], GD)], unit=0.12, padx=60, pady=60, bg=IV))
open(f'{W}/e2b.svg', 'w').write(fit([(w724['ink'], EM), (w724['I'], GD)], unit=0.12, padx=60, pady=60, bg=IV))

# ---- study 3: avatar candidates
hm = hinge_mark(ps)
av = [
    ('hinge glyph (round 3)', square([(hm['n'], IV), (hm['I'], GL)], bg=EM, fill=0.62)),
    ('staircase (chosen)', square(stair_parts(STS, IV, GL), bg=EM, fill=0.86, circle=0.84)),
    ('staircase, one colour', square(stair_parts(STS, IV, IV), bg=EM, fill=0.86, circle=0.84)),
    ('favicon V (≤ 48 px only)', square([(VF, IV)], bg=EM, fill=0.62)),
]
avh = '<!doctype html><html><body style="margin:0;background:#fff;width:720px;display:flex;gap:14px;padding:14px;box-sizing:border-box">' + ''.join(
    f'<div style="text-align:center;font:12px Helvetica,Arial;color:#333"><img src="{uri_svg(s)}" style="width:150px;height:150px;border-radius:50%"><br>'
    f'<img src="{uri_svg(s)}" style="width:56px;height:56px;border-radius:50%;margin:6px 4px 0"> <img src="{uri_svg(s)}" style="width:32px;height:32px;border-radius:50%"><br>{t}</div>'
    for t, s in av) + '</body></html>'
compose(avh, f'{W}/e3.png', 720, 260)

panels = [
    (f'{W}/e1.png', '1 · The name at header size (2× pixel zoom of 1× renders)',
     'A reads "Van\'ndra": the I is hidden behind the n and only its top shows. Lowering the I (B) makes it worse. Releasing the ligature (C) reads, but loses the idea. The staircase (D) keeps both letters whole and shares the stroke in the open: it reads at 21 px cap height.'),
    (f'{W}/e2.svg', '2 · One-line hinge, I at 784 (round 3)',
     'The I rising above every capital looks pasted from a bigger size (judge note), but at the ascender (next panel) it shrinks to an apostrophe. The one-line hinge is retired; the one-line wordmark now sets n and I side by side.'),
    (f'{W}/e2b.svg', '2b · One-line hinge, I at the ascender 724',
     'Reads "Van\'ndra" even at display size. Retired.'),
    (f'{W}/e3.png', '3 · Avatar candidates (150 / 56 / 32 px)',
     'The hinge glyph alone reads "nl" or a mirrored h. The staircase says the name at 150 and 56 px. Below 48 px nothing with two words survives, so the favicon is the V of the wordmark (only there).'),
    ('loops/l0_glyphs.png', '4a · Terminals before: ball a, beak r, flag t, slab-ended s',
     'Ball and beak terminals put the alphabet in the DTC-beauty genre; the t\'s top read as a flag; the s ended in blunt slabs heavier than the a.'),
    ('loops/l2_top.png', '4b · Terminals after: one knife cut everywhere',
     'Every free stroke end is the same straight cut rising about 20°. One rule for a, r, s, C, e, t, y and for the Devanagari dandas and hooks.'),
    ('loops/l4_lockups.png', '5 · Lockup studies',
     'Centred one-line + Creations; staircase + Creations under the I; staircase + Creations right-aligned (chosen: stacked); Creations on line 2 (chosen: horizontal); bilingual; Devanagari in the empty corner (collides, rejected).'),
    ('loops/l3_deva.png', '6 · वनिंद्रा drawn in the same pen, over the font anatomy (grey, Tiro)',
     'Dandas heavy, falling strokes heavy, rising strokes and the shirorekha light, knife-cut ends. To be verified by the team (especially द्र).'),
]
cells = ''.join(f'''<figure style="margin:0;background:#fff;border-radius:6px;padding:14px 14px 12px;box-sizing:border-box">
<div style="font:600 16px/1.2 Helvetica,Arial,sans-serif;color:#0B2A20;margin-bottom:8px">{t}</div>
<div style="height:{h}px;display:flex;align-items:center;justify-content:center;background:#f6f1e7;overflow:hidden"><img src="{uri_file(f, 'image/svg+xml' if f.endswith('.svg') else 'image/png')}" style="max-width:100%;max-height:{h}px"></div>
<figcaption style="font:13px/1.4 Helvetica,Arial,sans-serif;color:#333;margin-top:9px">{c}</figcaption></figure>'''
                for (f, t, c), h in zip(panels, [380, 150, 150, 300, 260, 260, 620, 620]))
html = f'''<!doctype html><html><body style="margin:0;background:#8f8f8f">
<div style="padding:22px;width:1600px;box-sizing:border-box">
<div style="font:700 26px Helvetica,Arial,sans-serif;color:#fff;margin:0 0 4px">R3 · The Hinge, final polish: studies</div>
<div style="font:15px Helvetica,Arial,sans-serif;color:#f1f1f1;margin:0 0 16px">Question: how does "one stroke, two letters" survive a 26 px header, a 110 px avatar and a Reel credit without being misread? (Round-3 exploration of 28 variations is in ../r3_hinge/explore.png.)</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">{cells}</div></div></body></html>'''
compose(html, "explore.png", 1600, 2330)
print('explore ok')
