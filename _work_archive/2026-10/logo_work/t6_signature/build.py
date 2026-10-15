"""Build every deliverable for the 'Canopy Signature' concept (t6_signature)."""
import os, sys, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pen as P
import sig

RENDER = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit/render.js'
PAL = P.vtype.PALETTE
EMERALD, IVORY, GOLD, GOLD_LT = PAL['emerald'], PAL['ivory'], PAL['gold'], PAL['gold_lt']

# optical sizes of the one pen
WPEN = dict(hair=5.0, shade=18.0)            # wordmark
MPEN = dict(hair=7.0, shade=26.0)            # mark (display)
SPEN = dict(hair=19.0, shade=45.0)           # mark_small (<= 48 px)
CFG = dict(can_rise=0.60, can_k=0.56, can_lift=14.0, can_turn=28.0)
SMALL_INK = GOLD
TRACK = 0.44                                  # CREATIONS tracking (em)


def wordmark_path():
    S, c = sig.wordmark_strokes(CFG)
    return P.render(S, P.Pen(slant=c['slant'], **WPEN))


def mark_path(small=False):
    cfg = dict(CFG)
    if small:
        cfg.update(dict(m_turn=28.0, v_hook=False, m_dIs=84.0))
    S, c = sig.mark_strokes(cfg)
    return P.render(S, P.Pen(slant=c['slant'], **(SPEN if small else MPEN)))


def creations_path(size):
    """CREATIONS in Jost 400, widely tracked, with optical pair corrections."""
    gl = P.vtype.glyph_paths('CREATIONS', family='jost', weight=400, size=size, tracking=TRACK)
    # optical kerning on top of tracking (em): A-T open diagonal pair, T-I narrow, O round
    adj = {('A', 'T'): -0.06, ('T', 'I'): -0.01, ('I', 'O'): -0.015, ('O', 'N'): -0.015, ('R', 'E'): 0.0,
           ('C', 'R'): 0.0}
    txt = 'CREATIONS'
    acc, shift = None, 0.0
    for i, g in enumerate(gl):
        if i > 0:
            shift += adj.get((txt[i - 1], txt[i]), 0.0) * size
        p = P.vtype.transform(g.path, 1, 0, 0, 1, shift, 0)
        acc = p if acc is None else P.vtype.union(acc, p)
    return acc   # SVG y-down, baseline at y=0


def bbox(path):
    return path.bounds


def place_up(path, s, x, y_base):
    """y-up path placed so that its y=0 (baseline) sits at SVG y_base, x-origin at x."""
    return P.flip(path, s, x, y_base)


def d(path):
    return P.d_of(path)


def svg(w, h, body, bg=None, title='VanIndra Creations'):
    return P.vtype.svg_doc(round(w, 2), round(h, 2), body, bg=bg, title=title)


def write(name, text):
    f = os.path.join(HERE, name)
    open(f, 'w').write(text)
    return f


def optical_centre(path, box):
    """Place a y-up path in box (x, y, w, h) scaled to fit; centre = mix of bbox centre and area centroid."""
    xmin, ymin, xmax, ymax = path.bounds
    s = min(box[2] / (xmax - xmin), box[3] / (ymax - ymin))
    # centroid via sampling the outline polygon area (shoelace on flattened contours)
    from fontTools.pens.recordingPen import RecordingPen
    pts_area = centroid(path)
    cx = 0.5 * (xmin + xmax) * 0.6 + pts_area[0] * 0.4
    cy = 0.5 * (ymin + ymax) * 0.6 + pts_area[1] * 0.4
    tx = box[0] + box[2] / 2 - cx * s
    ty = box[1] + box[3] / 2 + cy * s
    return P.flip(path, s, tx, ty), s


def centroid(path):
    from fontTools.pens.statisticsPen import StatisticsPen
    sp = StatisticsPen()
    path.draw(sp)
    return (sp.meanX, sp.meanY)


def build():
    W = wordmark_path()
    M = mark_path()
    MS = mark_path(small=True)
    out = {}

    # ---------------------------------------------------------------- mark.svg (transparent, square)
    def mark_doc(path, ink, bg=None, fill=0.62, size=512):
        m = size * (1 - fill) / 2
        p, _ = optical_centre(path, (m, m, size - 2 * m, size - 2 * m))
        return svg(size, size, f'<path d="{d(p)}" fill="{ink}"/>', bg=bg)

    out['mark.svg'] = write('mark.svg', mark_doc(M, EMERALD, fill=0.80))
    out['mark_small.svg'] = write('mark_small.svg', mark_doc(MS, SMALL_INK, fill=0.88))
    out['mark_on_ivory.svg'] = write('mark_on_ivory.svg', mark_doc(M, EMERALD, IVORY, fill=0.60))
    out['mark_on_emerald.svg'] = write('mark_on_emerald.svg', mark_doc(M, GOLD_LT, EMERALD, fill=0.60))
    out['mark_one_colour_gold.svg'] = write('mark_one_colour_gold.svg', mark_doc(M, GOLD, fill=0.80))
    # small-size app/DP icons (for favicons & avatars at <= 48 px)
    write('mark_small_on_emerald.svg', mark_doc(MS, GOLD_LT, EMERALD, fill=0.64))
    write('mark_small_on_ivory.svg', mark_doc(MS, EMERALD, IVORY, fill=0.64))

    # ---------------------------------------------------------------- wordmark.svg
    xmin, ymin, xmax, ymax = W.bounds
    pad = 0.06 * (xmax - xmin)
    s = 1.0
    ww, wh = (xmax - xmin) + 2 * pad, (ymax - ymin) + 2 * pad
    p = P.flip(W, 1, -xmin + pad, ymax + pad)
    out['wordmark.svg'] = write('wordmark.svg', svg(ww, wh, f'<path d="{d(p)}" fill="{EMERALD}"/>'))

    # ---------------------------------------------------------------- lockups
    # unit: signature x-height X=100 design units -> lockup design units 1:1
    X = 100.0
    cap_size = 0.36 * X / 0.70          # Jost cap height ~0.70 em -> CREATIONS cap = 0.36 X
    CR = creations_path(cap_size)
    cr_b = CR.bounds
    cr_w = cr_b[2] - cr_b[0]

    def horizontal(ink_w, ink_m, ink_t, bg, rule_ink):
        cr_gap = 0.30 * X                                # baseline -> top of CREATIONS caps
        cr_cap = 0.50 * X
        CRh = creations_path(cr_cap / 0.70)
        hb = CRh.bounds
        block_top, block_bot = -ymax, (-ymin) + cr_gap + cr_cap   # relative to baseline (svg y)
        block_h = block_bot - block_top
        mb = M.bounds
        ms = 0.86 * block_h / (mb[3] - mb[1])
        mark_w = (mb[2] - mb[0]) * ms
        margin = 0.5 * X
        x0 = margin
        top = margin
        base = top - block_top
        # mark optically centred on the block
        cy_mark = 0.5 * (mb[1] + mb[3]) * 0.6 + centroid(M)[1] * 0.4
        mid = top + block_h / 2
        pm = P.flip(M, ms, x0 - mb[0] * ms, mid + cy_mark * ms)
        rule_x = x0 + mark_w + 0.55 * X
        wx = rule_x + 0.62 * X - xmin
        pw = P.flip(W, 1, wx, base)
        sig_right = wx + xmax
        cr_y = base + (-ymin) + cr_gap + cr_cap        # CREATIONS baseline
        cr_x = sig_right - (hb[2] - hb[0]) - hb[0] - 0.12 * X
        body = f'<path d="{d(pm)}" fill="{ink_m}"/>'
        body += f'<rect x="{rule_x:.2f}" y="{top + 0.12 * block_h:.2f}" width="{0.025 * X:.2f}" height="{0.76 * block_h:.2f}" fill="{rule_ink}"/>'
        body += f'<path d="{d(pw)}" fill="{ink_w}"/>'
        body += f'<path d="{d(CRh)}" transform="translate({cr_x:.2f},{cr_y:.2f})" fill="{ink_t}"/>'
        return svg(sig_right + margin, top + block_h + margin, body, bg=bg)

    def stacked(ink_w, ink_m, ink_t, bg):
        mb = M.bounds
        ms = 1.05 * (ymax - 0) / (mb[3] - mb[1])
        mark_w, mark_h = (mb[2] - mb[0]) * ms, (mb[3] - mb[1]) * ms
        sw = xmax - xmin
        Wd = sw + 2 * 70.0
        cx = Wd / 2
        top = 60.0
        # mark centred (optically: use centroid mix)
        cxm = 0.5 * (mb[0] + mb[2]) * 0.6 + centroid(M)[0] * 0.4
        pm = P.flip(M, ms, cx - cxm * ms, top + mb[3] * ms)
        y_after_mark = top + mark_h + 0.70 * X
        base = y_after_mark + ymax
        cxw = 0.5 * (xmin + xmax)
        pw = P.flip(W, 1, cx - cxw, base)
        cr_y = base + (-ymin) + 0.66 * X + cap_size * 0.70
        cr_x = cx - (cr_b[0] + cr_b[2]) / 2
        body = f'<path d="{d(pm)}" fill="{ink_m}"/><path d="{d(pw)}" fill="{ink_w}"/>'
        body += f'<path d="{d(CR)}" transform="translate({cr_x:.2f},{cr_y:.2f})" fill="{ink_t}"/>'
        Hd = cr_y + 60.0
        return svg(Wd, Hd, body, bg=bg)

    out['lockup_horizontal_on_ivory.svg'] = write('lockup_horizontal_on_ivory.svg', horizontal(EMERALD, EMERALD, GOLD, IVORY, GOLD))
    out['lockup_horizontal_on_emerald.svg'] = write('lockup_horizontal_on_emerald.svg', horizontal(IVORY, GOLD_LT, GOLD_LT, EMERALD, GOLD_LT))
    out['lockup_stacked_on_ivory.svg'] = write('lockup_stacked_on_ivory.svg', stacked(EMERALD, EMERALD, GOLD, IVORY))
    out['lockup_stacked_on_emerald.svg'] = write('lockup_stacked_on_emerald.svg', stacked(IVORY, GOLD_LT, GOLD_LT, EMERALD))
    return out


def renders(out):
    order = ['mark.svg', 'mark_small.svg', 'wordmark.svg', 'mark_on_ivory.svg', 'mark_on_emerald.svg',
             'mark_one_colour_gold.svg', 'lockup_horizontal_on_ivory.svg', 'lockup_horizontal_on_emerald.svg',
             'lockup_stacked_on_ivory.svg', 'lockup_stacked_on_emerald.svg']
    files = [os.path.join(HERE, f) for f in order]
    subprocess.run(['node', RENDER, 'sheet', os.path.join(HERE, 'sheet.png')] + files, check=True)
    subprocess.run(['node', RENDER, 'sizes', os.path.join(HERE, 'sizes.png'), os.path.join(HERE, 'mark_small.svg')], check=True)
    subprocess.run(['node', RENDER, 'context', os.path.join(HERE, 'context.png'), os.path.join(HERE, 'mark_on_emerald.svg'),
                    os.path.join(HERE, 'lockup_horizontal_on_emerald.svg')], check=True)
    sizes = {f: os.path.getsize(os.path.join(HERE, f)) // 1024 for f in order}
    print(json.dumps(sizes))


if __name__ == '__main__':
    o = build()
    renders(o)
