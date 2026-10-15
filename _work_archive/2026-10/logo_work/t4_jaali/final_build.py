"""VanIndra Creations -- 'The Jaali Stroke' (territory: Jaali).  Builds every deliverable.

Construction (one 22.5-degree grid):
  * Mughal {8/3} jaali star, outer radius R = 100. Its point angle is 45 degrees (the V).
  * The V-unit = one point of that star drawn as a band of thickness T inside the outline,
    cut on the two radii through the star's notches (the joints where the next point begins).
  * 8 units lock into the star (rosette seal); stars on the octagon-square (4.8.8) grid,
    contact angle 67.5 deg, give the jaali canvas -- every point in it is the same V.
"""
import math, os, sys, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jgeo import *  # noqa
from unit import unit, rosette, K83
from brand import optical_word, norm_mark, place
from canvas import canvas
from hankin import oct_star, sq_star

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
CFG = dict(T=9.0, T_SMALL=11.5, SPLIT=0.85, SMALL_COL='#A8843A', CRE=0.31, FONT=('marcellus', 400), GAP_W=0.40, GAP_C=0.98, OUT=HERE, MARK_FILL=0.60)
for a in sys.argv[1:]:
    k, v = a.split('=')
    CFG[k] = type(CFG[k])(v) if not isinstance(CFG[k], tuple) else tuple(v.split(','))
if isinstance(CFG['FONT'][1], str):
    CFG['FONT'] = (CFG['FONT'][0], int(CFG['FONT'][1]))
OUT = CFG['OUT']; os.makedirs(OUT, exist_ok=True)
FAM, WT = CFG['FONT']
TITLE = 'VanIndra Creations'
KERN_W = {'VA': -0.07, 'AN': -0.02, 'RA': -0.04, 'DR': 0.01}
KERN_C = {'TI': 0.04, 'IO': 0.02}


def mark_geom(t, split=None):
    """the V-unit; split = hairline on the tip radius (all three cuts then point to the star's centre)."""
    u = unit(R=100.0, t=t)
    g = CFG['SPLIT'] if split is None else split
    if g > 0:
        u = diff(u, P([(-g / 2, -10), (g / 2, -10), (g / 2, 130), (-g / 2, 130)]))
    return u


def centred(path, size, fill, dy_frac=0.0):
    """centre a path in a size x size square: height = fill*size, optically centred (mix of bbox and area centroid)."""
    x0, y0, x1, y1 = vt.bounds(path)
    s = fill * size / (y1 - y0)
    p = vt.transform(path, s, 0, 0, s, 0, 0)
    x0, y0, x1, y1 = vt.bounds(p)
    # a V carries its mass high: nudge down by a small fraction for optical centre
    return vt.transform(p, 1, 0, 0, 1, size / 2 - (x0 + x1) / 2, size / 2 - (y0 + y1) / 2 + dy_frac * size)


def write(name, w, h, items, bg=None):
    f = os.path.join(OUT, name)
    open(f, 'w').write(svg(w, h, items, bg=bg, title=TITLE))
    return f


def wordmark_parts(cap=100.0):
    w1 = optical_word('VANINDRA', FAM, WT, cap, gap=CFG['GAP_W'], x=0, baseline=cap, clamp=0.30, adjust=KERN_W)
    c2 = cap * CFG['CRE']
    w2 = optical_word('CREATIONS', FAM, WT, c2, gap=CFG['GAP_C'], x=0, baseline=0, clamp=0.30, adjust=KERN_C)
    b1, b2 = vt.bounds(w1), vt.bounds(w2)
    w2 = vt.transform(w2, 1, 0, 0, 1, (b1[0] + b1[2]) / 2 - (b2[0] + b2[2]) / 2, cap + cap * 0.58 + c2)
    return w1, w2


def lock_h(bg, cm, cw, cc, name):
    cap = 100.0
    w1, w2 = wordmark_parts(cap)
    b1, b2 = vt.bounds(w1), vt.bounds(w2)
    text_top, text_bot = b1[1], b2[3]
    mh = (text_bot - text_top) * 1.07
    mk = mark_geom(CFG['T'])
    x0, y0, x1, y1 = vt.bounds(mk)
    s = mh / (y1 - y0)
    mk = vt.transform(mk, s, 0, 0, s, 0, 0)
    mb = vt.bounds(mk)
    # optical: spikes overshoot cap top by ~5% of mark height; tip overshoots CREATIONS baseline
    over = mh * 0.028
    mk = vt.transform(mk, 1, 0, 0, 1, b1[0] - cap * 0.58 - mb[2], text_top - over - mb[1])
    allb = vt.bounds(merge([mk, w1, w2]))
    pad = cap * 0.55
    tr = lambda p: vt.transform(p, 1, 0, 0, 1, pad - allb[0], pad - allb[1])
    W, H = allb[2] - allb[0] + 2 * pad, allb[3] - allb[1] + 2 * pad
    return write(name, round(W), round(H), [(tr(mk), cm), (tr(w1), cw), (tr(w2), cc)], bg=bg)


def lock_s(bg, cm, cw, cc, name):
    cap = 100.0
    w1, w2 = wordmark_parts(cap)
    b1 = vt.bounds(w1)
    mk = mark_geom(CFG['T'])
    x0, y0, x1, y1 = vt.bounds(mk)
    mh = cap * 2.7
    s = mh / (y1 - y0)
    mk = vt.transform(mk, s, 0, 0, s, 0, 0)
    mb = vt.bounds(mk)
    mk = vt.transform(mk, 1, 0, 0, 1, (b1[0] + b1[2]) / 2 - (mb[0] + mb[2]) / 2, b1[1] - cap * 0.95 - mb[3])
    allb = vt.bounds(merge([mk, w1, w2]))
    padx, pady = cap * 1.4, cap * 1.2
    tr = lambda p: vt.transform(p, 1, 0, 0, 1, padx - allb[0], pady - allb[1])
    W, H = allb[2] - allb[0] + 2 * padx, allb[3] - allb[1] + 2 * pady
    return write(name, round(W), round(H), [(tr(mk), cm), (tr(w1), cw), (tr(w2), cc)], bg=bg)


def construction(name):
    """the idea in one drawing: the jaali star, its tile, the eight units, our V highlighted."""
    Z = 1000.0
    c = (500.0, 470.0)
    R = 330.0
    s = R / 100.0
    items = []
    # 4.8.8 tile (octagon) and the star outline as hairlines
    a = 2 * R  # octagon apothem = R
    octo = P(ngon_pts(c[0], c[1], R / math.cos(22.5 * D2R), 8, a0=22.5))
    items.append((vt.stroke_to_path(octo, 1.6), '#B9AE98'))
    st = star_pts(c[0], c[1], R, 8, 3, a0=90)
    items.append((vt.stroke_to_path(P(st), 1.6), '#B9AE98'))
    # radii through the notches
    for k in range(8):
        items.append((vt.stroke_to_path(P([c, polar(c[0], c[1], R * 1.12, 247.5 + 45 * k), polar(c[0], c[1], R * 1.12, 247.5 + 45 * k + 1e-3)]), 1.0), '#CFC5B0'))
    # the eight units, ours in emerald, the others in gold
    for k in range(8):
        items.append((vt.stroke_to_path(P([c, polar(c[0], c[1], R * 1.12, 270 + 45 * k), polar(c[0], c[1], R * 1.12, 270 + 45 * k + 1e-3)]), 0.8), '#DDD4C2'))
    for k in range(8):
        u = unit(R=R, t=CFG['T'] * s, k=k, cx=c[0], cy=c[1], slit=2.2 * s)
        a = 270 + 45 * k
        u = diff(u, vt.stroke_to_path(P([c, polar(c[0], c[1], R * 1.2, a), polar(c[0], c[1], R * 1.2, a + 1e-4)]), CFG['SPLIT'] * s))
        items.append((u, EMERALD if k == 0 else GOLD))
    # angle annotation
    lab = vt.text_path('45°', family='jost', weight=400, size=26, x=c[0] - 18, y=c[1] + R + 64).path
    items.append((lab, '#6E6656'))
    t1 = vt.text_path('ONE POINT OF THE MUGHAL EIGHT-POINT JAALI STAR IS OUR V', family='jost', weight=400, size=22, tracking=0.16).path
    b = vt.bounds(t1); t1 = vt.transform(t1, 1, 0, 0, 1, 500 - (b[0] + b[2]) / 2, 905)
    t2 = vt.text_path('EVERY CUT POINTS TO THE STAR CENTRE  ·  EIGHT VS MAKE THE STAR  ·  STARS MAKE THE JAALI', family='jost', weight=400, size=16, tracking=0.14).path
    b = vt.bounds(t2); t2 = vt.transform(t2, 1, 0, 0, 1, 500 - (b[0] + b[2]) / 2, 940)
    items += [(t1, EMERALD), (t2, '#6E6656')]
    return write(name, 1000, 1000, items, bg=IVORY)


def pattern(name, bg, fg):
    cv = canvas(a=100.0, t=CFG['T'] * 0.5, slit=1.6, xr=4, yr=4)
    box = P([(-260, -260), (260, -260), (260, 260), (-260, 260)])
    cv = inter(cv, box)
    cv = vt.transform(cv, 1000 / 520, 0, 0, 1000 / 520, 500, 500)
    return write(name, 1000, 1000, [(cv, fg)], bg=bg)


def seal(name, bg, fg):
    r = rosette(R=100.0, t=CFG['T'], slit=2.4)
    r = diff(r, merge([vt.stroke_to_path(P([(0, 0), polar(0, 0, 200, 270 + 45 * k), polar(0, 0, 200, 270 + 45 * k + 1e-4)]), CFG['SPLIT']) for k in range(8)]))
    p = centred(r, 1000, 0.70)
    return write(name, 1000, 1000, [(p, fg)], bg=bg)


def main():
    F = CFG['MARK_FILL']
    m = mark_geom(CFG['T'])
    ms = mark_geom(CFG['T_SMALL'], split=0.0)
    out = {}
    out['mark'] = write('mark.svg', 1000, 1000, [(centred(m, 1000, F, 0.012), EMERALD)])
    out['mark_small'] = write('mark_small.svg', 1000, 1000, [(centred(ms, 1000, 0.84, 0.006), CFG['SMALL_COL'])])
    out['mark_on_ivory'] = write('mark_on_ivory.svg', 1000, 1000, [(centred(m, 1000, F, 0.012), EMERALD)], bg=IVORY)
    out['mark_on_emerald'] = write('mark_on_emerald.svg', 1000, 1000, [(centred(m, 1000, F, 0.012), GOLD_LT)], bg=EMERALD)
    out['mark_one_colour_gold'] = write('mark_one_colour_gold.svg', 1000, 1000, [(centred(m, 1000, F, 0.012), GOLD)])
    # small icons on grounds (for sizes/context)
    out['mark_small_on_emerald'] = write('mark_small_on_emerald.svg', 1000, 1000, [(centred(ms, 1000, 0.70, 0.008), GOLD_LT)], bg=EMERALD)
    w1, w2 = wordmark_parts(100.0)
    allb = vt.bounds(merge([w1, w2])); pad = 60
    tr = lambda p: vt.transform(p, 1, 0, 0, 1, pad - allb[0], pad - allb[1])
    out['wordmark'] = write('wordmark.svg', round(allb[2] - allb[0] + 2 * pad), round(allb[3] - allb[1] + 2 * pad), [(tr(w1), EMERALD), (tr(w2), GOLD)])
    out['lh_i'] = lock_h(IVORY, EMERALD, EMERALD, GOLD, 'lockup_horizontal_on_ivory.svg')
    out['lh_e'] = lock_h(EMERALD, GOLD_LT, IVORY, GOLD_LT, 'lockup_horizontal_on_emerald.svg')
    out['ls_i'] = lock_s(IVORY, EMERALD, EMERALD, GOLD, 'lockup_stacked_on_ivory.svg')
    out['ls_e'] = lock_s(EMERALD, GOLD_LT, IVORY, GOLD_LT, 'lockup_stacked_on_emerald.svg')
    out['construction'] = construction('construction.svg')
    out['seal'] = seal('seal_rosette_on_emerald.svg', EMERALD, GOLD_LT)
    out['pattern'] = pattern('pattern_jaali_on_emerald.svg', EMERALD, GOLD_LT)
    sheet = [out[k] for k in ('mark', 'mark_small', 'wordmark', 'mark_on_ivory', 'mark_on_emerald', 'mark_one_colour_gold',
                              'lh_i', 'lh_e', 'construction', 'ls_i', 'ls_e', 'seal', 'pattern')]
    subprocess.run(['node', RENDER, 'sheet', os.path.join(OUT, 'sheet.png')] + sheet, check=True)
    subprocess.run(['node', RENDER, 'sizes', os.path.join(OUT, 'sizes.png'), out['mark_small']], check=True)
    subprocess.run(['node', RENDER, 'context', os.path.join(OUT, 'context.png'), out['mark_on_emerald'], out['lh_e']], check=True)
    for k, v in out.items():
        print(k, os.path.getsize(v))


if __name__ == '__main__':
    main()
