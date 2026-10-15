"""Generate VanIndra Creations logo directions as outlined SVGs."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typeset import shape, measure, centered, glyph_bbox  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'out')
os.makedirs(OUT, exist_ok=True)

INK = '#0B2A20'      # deep emerald ink
IVORY = '#F6F1E7'    # warm ivory paper
GOLD = '#A8843A'     # antique gold for light grounds
GOLD_LT = '#D2B26A'  # soft gold for dark grounds

THEMES = {
    'ivory': {'bg': IVORY, 'fg': INK, 'acc': GOLD},
    'emerald': {'bg': INK, 'fg': IVORY, 'acc': GOLD_LT},
}


def svg(w, h, body, bg=None, title='VanIndra Creations'):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{rect}{body}</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(content)


def glyph_center(key, ch, size, cx, cy):
    """Path for a single glyph centred on (cx, cy) by its ink box."""
    x0, y0, x1, y1 = glyph_bbox(key, ch, size)  # already y-down, relative to baseline at 0
    ox = cx - (x0 + x1) / 2
    baseline = cy - (y0 + y1) / 2
    d, _ = shape(key, ch, size, x=ox, y=baseline)
    return d


# ---------------------------------------------------------------------------
# Direction A — "Maison": Bodoni wordmark + 9:16 arch monogram
# ---------------------------------------------------------------------------
def arch_path(cx, top, w, h):
    r = w / 2
    x0, x1 = cx - r, cx + r
    bottom = top + h
    return (f'M{x0:.2f},{bottom:.2f} L{x0:.2f},{top + r:.2f} '
            f'A{r:.2f},{r:.2f} 0 0 1 {x1:.2f},{top + r:.2f} L{x1:.2f},{bottom:.2f} Z')


def mark_maison(cx, cy, scale, t):
    w, h = 96 * scale, 170 * scale
    top = cy - h / 2
    stroke = 2.0 * scale
    inner = arch_path(cx, top + 7 * scale, w - 14 * scale, h - 14 * scale)
    v = glyph_center('bodoni-display', 'V', 84 * scale, cx, cy + 14 * scale)
    dsz = 5.5 * scale
    dy = cy - 40 * scale
    diamond = f'M{cx:.2f},{dy - dsz:.2f} L{cx + dsz:.2f},{dy:.2f} L{cx:.2f},{dy + dsz:.2f} L{cx - dsz:.2f},{dy:.2f} Z'
    return (f'<path d="{arch_path(cx, top, w, h)}" fill="none" stroke="{t["fg"]}" stroke-width="{stroke:.2f}"/>'
            f'<path d="{inner}" fill="none" stroke="{t["acc"]}" stroke-width="{stroke * 0.55:.2f}"/>'
            f'<path d="{v}" fill="{t["fg"]}"/><path d="{diamond}" fill="{t["acc"]}"/>')


def wordmark_maison(x, y, scale, t, align='left'):
    """VANINDRA (Bodoni) / rule / CREATIONS (Jost). y = baseline of VANINDRA."""
    s1, s2 = 64 * scale, 15 * scale
    tr1, tr2 = 0.14, 0.62
    w1 = measure('bodoni', 'VANINDRA', s1, tr1)
    w2 = measure('jost-400', 'CREATIONS', s2, tr2)
    if align == 'center':
        x1, x2 = x - w1 / 2, x - w2 / 2
    else:
        x1, x2 = x, x + (w1 - w2) / 2
    d1, _ = shape('bodoni', 'VANINDRA', s1, tr1, x=x1, y=y)
    ry = y + 20 * scale
    y2 = ry + 26 * scale
    d2, _ = shape('jost-400', 'CREATIONS', s2, tr2, x=x2, y=y2)
    rl = (w1 - w2) / 2 - 18 * scale
    left_rule = f'M{x1:.2f},{ry:.2f} h{rl:.2f}' if rl > 0 else ''
    right_rule = f'M{x1 + w1:.2f},{ry:.2f} h{-rl:.2f}' if rl > 0 else ''
    rule_y = y2 - s2 * 0.36
    rules = (f'<path d="M{x1:.2f},{rule_y:.2f} h{rl:.2f} M{x1 + w1:.2f},{rule_y:.2f} h{-rl:.2f}" '
             f'stroke="{t["acc"]}" stroke-width="{1.1 * scale:.2f}"/>') if rl > 0 else ''
    return (f'<path d="{d1}" fill="{t["fg"]}"/><path d="{d2}" fill="{t["fg"]}"/>{rules}', w1, y2)


def direction_a():
    for tn, t in THEMES.items():
        # icon (square 512)
        save(f'A_maison_icon_{tn}.svg', svg(512, 512, mark_maison(256, 256, 2.2, t), t['bg']))
        # horizontal lockup
        sc = 1.0
        markw = 96
        body = mark_maison(40 + markw / 2, 110, sc, t)
        wm, w1, _ = wordmark_maison(40 + markw + 44, 108, sc, t)
        W = 40 + markw + 44 + w1 + 48
        save(f'A_maison_horizontal_{tn}.svg', svg(W, 220, body + wm, t['bg']))
        # stacked lockup
        body = mark_maison(260, 150, 1.25, t)
        wm, w1, y2 = wordmark_maison(260, 340, 1.0, t, align='center')
        save(f'A_maison_stacked_{tn}.svg', svg(520, 420, body + wm, t['bg']))


# ---------------------------------------------------------------------------
# Direction B — "Editorial": Cormorant wordmark, italic gold "Creations", V seal
# ---------------------------------------------------------------------------
def mark_editorial(cx, cy, r, t, filled=False):
    v = glyph_center('cormorant-italic-500', 'V', r * 1.28, cx + r * 0.03, cy + r * 0.04)
    if filled:
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["fg"]}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r * 0.88:.2f}" fill="none" stroke="{t["acc"]}" stroke-width="{r * 0.012:.2f}"/>'
                f'<path d="{v}" fill="{t["bg"]}"/>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["fg"]}" stroke-width="{r * 0.022:.2f}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.88:.2f}" fill="none" stroke="{t["acc"]}" stroke-width="{r * 0.012:.2f}"/>'
            f'<path d="{v}" fill="{t["fg"]}"/>')


def wordmark_editorial(x, y, size, t, align='left'):
    w1 = measure('cormorant-500', 'VanIndra', size, 0.01)
    s2 = size * 0.62
    w2 = measure('cormorant-italic-500', 'Creations', s2, 0.02)
    gap = size * 0.18
    total = w1 + gap + w2
    x0 = x - total / 2 if align == 'center' else x
    d1, _ = shape('cormorant-500', 'VanIndra', size, 0.01, x=x0, y=y)
    d2, _ = shape('cormorant-italic-500', 'Creations', s2, 0.02, x=x0 + w1 + gap, y=y)
    return f'<path d="{d1}" fill="{t["fg"]}"/><path d="{d2}" fill="{t["acc"]}"/>', total


def direction_b():
    for tn, t in THEMES.items():
        save(f'B_editorial_icon_{tn}.svg', svg(512, 512, mark_editorial(256, 256, 200, t), t['bg']))
        save(f'B_editorial_icon_filled_{tn}.svg', svg(512, 512, mark_editorial(256, 256, 236, t, filled=True), t['bg']))
        wm, total = wordmark_editorial(0, 0, 84, t)
        r = 52
        body = mark_editorial(40 + r, 100, r, t)
        wm, total = wordmark_editorial(40 + 2 * r + 34, 128, 84, t)
        W = 40 + 2 * r + 34 + total + 44
        save(f'B_editorial_horizontal_{tn}.svg', svg(W, 200, body + wm, t['bg']))
        body = mark_editorial(300, 130, 78, t)
        wm, total = wordmark_editorial(300, 320, 80, t, align='center')
        tag, _ = centered('jost-400', 'CONTENT  STRATEGY  ·  VIRAL  SCRIPTING  ·  STUDIO  EDITING', 11.5, 300, 362, 0.22)
        save(f'B_editorial_stacked_{tn}.svg', svg(600, 400, body + wm + f'<path d="{tag}" fill="{t["fg"]}" fill-opacity="0.72"/>', t['bg']))


# ---------------------------------------------------------------------------
# Direction C — "Vertical Frame": 9:16 reel frame with a V drawn corner-to-centre
# ---------------------------------------------------------------------------
def mark_frame(cx, cy, h, t, stroke_ratio=0.03, vscale=1.0):
    w = h * 9 / 16
    x0, y0 = cx - w / 2, cy - h / 2
    rx = w * 0.18
    sw = h * stroke_ratio
    frame = (f'<rect x="{x0 + sw / 2:.2f}" y="{y0 + sw / 2:.2f}" width="{w - sw:.2f}" height="{h - sw:.2f}" rx="{rx:.2f}" '
             f'fill="none" stroke="{t["fg"]}" stroke-width="{sw:.2f}"/>')
    # Didone V: heavy left stem, hairline right stem, sharp vertex
    top = y0 + h * 0.20
    bot = y0 + h * 0.80
    half = w * 0.30 * vscale
    thick = w * 0.13 * vscale
    thin = w * 0.035 * max(vscale, 0.9)
    top = y0 + h * (0.5 - 0.30 * vscale)
    bot = y0 + h * (0.5 + 0.30 * vscale)
    lx, rxx = cx - half, cx + half
    v = (f'M{lx - thick * 0.5:.2f},{top:.2f} L{lx + thick * 0.5:.2f},{top:.2f} L{cx + thin * 0.3:.2f},{bot - h * 0.09:.2f} '
         f'L{rxx - thin * 0.5:.2f},{top:.2f} L{rxx + thin * 0.5:.2f},{top:.2f} L{cx + thin * 0.2:.2f},{bot:.2f} L{cx - thin * 0.2:.2f},{bot:.2f} Z')
    serif = w * 0.10 * vscale
    serifs = (f'M{lx - thick * 0.5 - serif * 0.45:.2f},{top:.2f} h{thick + serif * 0.9:.2f} '
              f'M{rxx - serif * 0.55:.2f},{top:.2f} h{serif * 1.1:.2f}')
    return (frame + f'<path d="{v}" fill="{t["acc"]}"/>'
            f'<path d="{serifs}" stroke="{t["acc"]}" stroke-width="{sw * 0.55:.2f}"/>'), w


def wordmark_frame(x, y, size, t, align='left'):
    tr = 0.30
    a = measure('jost-500', 'VANINDRA', size, tr)
    sp = size * 0.55
    b = measure('jost-300', 'CREATIONS', size, tr)
    total = a + sp + b
    x0 = x - total / 2 if align == 'center' else x
    d1, _ = shape('jost-500', 'VANINDRA', size, tr, x=x0, y=y)
    d2, _ = shape('jost-300', 'CREATIONS', size, tr, x=x0 + a + sp, y=y)
    return f'<path d="{d1}" fill="{t["fg"]}"/><path d="{d2}" fill="{t["fg"]}" fill-opacity="0.78"/>', total


def direction_c():
    for tn, t in THEMES.items():
        m, _ = mark_frame(256, 256, 360, t)
        save(f'C_frame_icon_{tn}.svg', svg(512, 512, m, t['bg']))
        m, mw = mark_frame(40 + 28, 100, 100, t)
        wm, total = wordmark_frame(40 + 56 + 30, 100 + 34 * 0.36, 34, t)
        W = 40 + 56 + 30 + total + 44
        save(f'C_frame_horizontal_{tn}.svg', svg(W, 200, m + wm, t['bg']))
        m, _ = mark_frame(300, 135, 170, t)
        wm, total = wordmark_frame(300, 300, 30, t, align='center')
        save(f'C_frame_stacked_{tn}.svg', svg(600, 360, m + wm, t['bg']))


if __name__ == '__main__':
    direction_a()
    direction_b()
    direction_c()
    print('\n'.join(sorted(os.listdir(OUT))))
