"""Generate every deliverable for 'The Emerald Cut' (VanIndra Creations).

Usage: python make.py [outdir] [variant-json]
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import emv

HERE = os.path.dirname(os.path.abspath(__file__))
BOD = os.path.join(FONT_DIR, 'bodoni-moda-variable', 'package', 'files', 'bodoni-moda-latin-standard-normal.woff2')

P = dict(
    mark=dict(tL=30.0, tR=12.0, clip=9.0, culet=0.0, seam=1.7, mitre=True, two_tone=False),
    small=dict(tL=33.0, tR=15.0, clip=10.0, culet=3.0, mitre=False),
    small_colour=GO,
    word=dict(opsz=14, wght=480, size=100.0, culet=0.030, kern={}),
    sub=dict(family='jost', weight=400, track=0.40, ratio=0.29),
    on_emerald_mark=GL,
    h_align='left',
)


def mark_parts(p=None, small=False):
    import emv2
    p = p or P
    return emv2.build(**(p['small'] if small else p['mark']))


# ---------------------------------------------------------------- wordmark

def wordmark_paths(p=None):
    """VANINDRA in Bodoni Moda (opsz/wght tuned) with culet-cut apexes and optical spacing.
    Returns (path, cap_height, width)."""
    p = p or P
    w = p['word']
    size = w['size']
    var = {'opsz': w['opsz'], 'wght': w['wght']}
    gl = glyph_paths('VANINDRA', file=BOD, size=size, x=0, y=0, variations=var, features={'kern': False})
    capH = -glyph_paths('H', file=BOD, size=size, variations=var)[0].bounds[1]
    k = w['culet'] * size
    # optical spacing: target gaps between glyph outlines (in em) for each pair; tuned by eye
    gaps = dict(VA=-0.045, AN=0.105, NI=0.175, IN=0.175, ND=0.170, DR=0.150, RA=0.070)
    gaps.update(w.get('kern', {}))
    letters = 'VANINDRA'
    paths = []
    x = 0.0
    for i, (ch, g) in enumerate(zip(letters, gl)):
        pth = g.path
        # culet cuts: flatten the pointed vertices exactly like a step-cut stone's culet
        if ch == 'V':
            pth = intersection(pth, poly([(-1e3, -1e3), (1e4, -1e3), (1e4, -k * 0.2), (-1e3, -k * 0.2)]))
        if ch == 'A':
            pth = intersection(pth, poly([(-1e3, -capH + k * 0.55), (1e4, -capH + k * 0.55), (1e4, 1e3), (-1e3, 1e3)]))
        # trim every overshoot beyond cap-height/baseline (N joints, etc.)
        pth = intersection(pth, poly([(-1e3, -capH), (1e4, -capH), (1e4, 0.0), (-1e3, 0.0)]))
        x0, y0, x1, y1 = bounds(pth)
        if i == 0:
            dx = -x0
        else:
            pair = letters[i - 1] + ch
            dx = x - x0 + gaps.get(pair, 0.15) * size
        pth = transform(pth, 1, 0, 0, 1, dx, 0)
        paths.append(pth)
        x = bounds(pth)[2]
    word = union(*paths)
    return word, capH, x


def sub_paths(target_width, cap_ratio, capH, p=None):
    p = p or P
    s = p['sub']
    size = capH * s['ratio'] / 0.70  # Jost cap height ~0.70 em
    t = text_path('CREATIONS', family=s['family'], weight=s['weight'], size=size, x=0, y=0, tracking=s['track'])
    pth = t.path
    x0 = bounds(pth)[0]
    pth = transform(pth, 1, 0, 0, 1, -x0, 0)
    return pth, -bounds(pth)[1]


# ---------------------------------------------------------------- composition helpers

def emit(fn, w, h, layers, bg=None):
    body = ''.join(pth_c(p, col) for p, col in layers)
    open(fn, 'w').write(svg_doc(w, h, body, bg))


def colour(role, scheme):
    return {'ivory': {'A': EM, 'B': GO}, 'emerald': {'A': P['on_emerald_mark'], 'B': GL},
            'gold': {'A': GL, 'B': GL}, 'transparent': {'A': EM, 'B': GO}}[scheme][role]


def area_centroid_x(path):
    """Exact area centroid (x) of a straight-edged pathops path; holes carry opposite winding."""
    A = Cx = 0.0
    for contour in path.contours:
        pts = []
        for verb, ps in contour:
            pts.extend(ps)
        n = len(pts)
        for i in range(n):
            xa, ya = pts[i]; xb, yb = pts[(i + 1) % n]
            cr = xa * yb - xb * ya
            A += cr
            Cx += (xa + xb) * cr
    return Cx / (3 * A) if A else 0.0


def path_area(path):
    tot = 0.0
    for contour in path.contours:
        pts = []
        for verb, ps in contour:
            pts.extend(ps)
        if len(pts) < 3:
            continue
        s = 0.0
        for i in range(len(pts)):
            xa, ya = pts[i]; xb, yb = pts[(i + 1) % len(pts)]
            s += xa * yb - xb * ya
        tot += s / 2
    return abs(tot)


def place_mark(parts, box, align='center', optical=0.5):
    allp = union(*[q for q, _ in parts])
    s, tx, ty = fit(allp, box)
    if optical:
        x0, y0, x1, y1 = bounds(allp)
        cx = area_centroid_x(allp)
        tx += ((x0 + x1) / 2 - cx) * s * optical
    return [(place(q, s, tx, ty), r) for q, r in parts], s


def build_all(outdir, p=None):
    p = p or P
    os.makedirs(outdir, exist_ok=True)
    parts, g = mark_parts(p)
    sparts, sg = mark_parts(p, small=True)

    # mark.svg (transparent, generous clear space: 1/4 of mark width on every side, square)
    S = 512
    m, _ = place_mark(parts, (0, S * 0.12, S, S * 0.76))
    emit(os.path.join(outdir, 'mark.svg'), S, S, [(q, colour(r, 'transparent')) for q, r in m])
    # mark_small.svg - tuned for <= 48 px: solid, heavier hairline, blunted culet, fills the square
    m2, _ = place_mark(sparts, (0, S * 0.04, S, S * 0.92))
    emit(os.path.join(outdir, 'mark_small.svg'), S, S, [(q, p.get('small_colour', EM)) for q, r in m2])
    emit(os.path.join(outdir, 'mark_small_emerald.svg'), S, S, [(q, EM) for q, r in m2])
    # backgrounds
    B = 1024
    mi, _ = place_mark(parts, (0, B * 0.15, B, B * 0.70))
    emit(os.path.join(outdir, 'mark_on_ivory.svg'), B, B, [(q, colour(r, 'ivory')) for q, r in mi], IV)
    emit(os.path.join(outdir, 'mark_on_emerald.svg'), B, B, [(q, colour(r, 'emerald')) for q, r in mi], EM)
    emit(os.path.join(outdir, 'mark_one_colour_gold.svg'), B, B, [(q, GO) for q, r in mi], IV)
    # small-size app/profile icons (solid mark on grounds)
    ms, _ = place_mark(sparts, (0, B * 0.12, B, B * 0.76))
    emit(os.path.join(outdir, 'icon_small_on_emerald.svg'), B, B, [(q, IV) for q, r in ms], EM)

    # wordmark
    word, capH, ww = wordmark_paths(p)
    sub, subH = sub_paths(ww, 0.20, capH, p)
    gap_lines = capH * 0.50
    sw = bounds(sub)[2]

    def block(align):
        sx = 0.0 if align == 'left' else (ww - sw) / 2
        return [(word, 'W'), (transform(sub, 1, 0, 0, 1, sx, gap_lines + subH), 'S')]
    word_block = block('center')
    # wordmark.svg (two lines, transparent)
    pad = capH * 0.6
    bw = ww + 2 * pad
    bh = capH + gap_lines + subH + 2 * pad
    lay = [(transform(q, 1, 0, 0, 1, pad, pad + capH), EM if r == 'W' else GO) for q, r in word_block]
    emit(os.path.join(outdir, 'wordmark.svg'), bw, bh, lay)

    def word_layers(scheme, ox, oy, align='center'):
        wc = EM if scheme == 'ivory' else IV
        sc = GO if scheme == 'ivory' else GL
        return [(transform(q, 1, 0, 0, 1, ox, oy + capH), wc if r == 'W' else sc) for q, r in block(align)]

    # horizontal lockup: mark height spans cap-top of VANINDRA to baseline of CREATIONS, plus optical overshoot
    block_h = capH + gap_lines + subH
    mh = block_h * 1.22
    mw = mh * 90 / 160
    for scheme, bg in (('ivory', IV), ('emerald', EM)):
        padx = capH * 0.85
        pady = capH * 0.62
        gapmw = capH * 0.80
        W_ = padx + mw + gapmw + ww + padx
        H_ = pady * 2 + mh
        mm, s = place_mark(parts, (padx, pady, mw, mh))
        # the mark is fitted by its own bounds; recompute actual width to place wordmark right after it
        mb = bounds(union(*[q for q, _ in mm]))
        ox = mb[2] + gapmw
        oy = pady + (mh - block_h) / 2 - mh * 0.035  # optical: lift text slightly against the pointed culet
        W_ = ox + ww + padx
        lay = [(q, colour(r, scheme)) for q, r in mm] + word_layers(scheme, ox, oy, p.get('h_align', 'left'))
        emit(os.path.join(outdir, f'lockup_horizontal_on_{scheme}.svg'), W_, H_, lay, bg)

    # stacked lockup
    for scheme, bg in (('ivory', IV), ('emerald', EM)):
        mh2 = capH * 3.6
        mw2 = mh2 * 90 / 160
        pad = capH * 1.2
        W_ = max(ww, mw2) + 2 * pad
        top = pad
        mm, s = place_mark(parts, ((W_ - mw2) / 2, top, mw2, mh2))
        mb = bounds(union(*[q for q, _ in mm]))
        oy = mb[3] + capH * 0.95
        ox = (W_ - ww) / 2
        H_ = oy + block_h + pad
        lay = [(q, colour(r, scheme)) for q, r in mm] + word_layers(scheme, ox, oy)
        emit(os.path.join(outdir, f'lockup_stacked_on_{scheme}.svg'), W_, H_, lay, bg)
    return outdir




def construction(outdir, p=None):
    """Construction drawing: the V on the 9:16 Reel grid, 45-degree emerald-cut corners, mitre."""
    import emv2
    from vgem2 import par_line
    p = p or P
    parts, g = mark_parts(p)
    sc, pad = 3.2, 46
    W, H = g['W'], g['H']
    T = lambda q: (q[0] * sc + pad, q[1] * sc + pad)
    body = ''

    def L(a, b, col=GO, w=1.0, dash=None, op=1.0):
        A, B_ = T(a), T(b)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return (f'<line x1="{A[0]:.2f}" y1="{A[1]:.2f}" x2="{B_[0]:.2f}" y2="{B_[1]:.2f}" stroke="{col}" '
                f'stroke-width="{w}" stroke-opacity="{op}"{d}/>')
    for i in range(10):
        body += L((i * 10, 0), (i * 10, H), GO, 0.6, None, 0.35)
    for j in range(17):
        body += L((0, j * 10), (W, j * 10), GO, 0.6, None, 0.35)
    # emerald-cut girdle on the frame (chamfer = the broad stone's corner cut)
    C = g['aL']
    G = octagon(W, H, C)
    Gp = transform(poly(G), sc, 0, 0, sc, pad, pad)
    body += f'<path d="{fmt(to_d(Gp))}" fill="none" stroke="{GO}" stroke-width="1.2"/>'
    from vgem2 import inset_convex, seams_to
    ring = inset_convex(G, 8.0)
    Rp = transform(poly(ring), sc, 0, 0, sc, pad, pad)
    body += f'<path d="{fmt(to_d(Rp))}" fill="none" stroke="{GO}" stroke-width="0.8" stroke-opacity="0.7"/>'
    for a, b in seams_to(G, ring):
        body += L(a, b, GO, 0.8, None, 0.7)
    # V construction lines
    Vb = g['Vb']
    body += L(g['L0'], Vb, GO, 1.0, '5 4') + L(g['R0'], Vb, GO, 1.0, '5 4')
    body += L(g['cr'], Vb, GO, 1.0, '2 3')
    body += L((g['aL'] + 6, -6), (g['aL'] - 22, 22), GO, 1.0)
    body += L((W - g['aR'] - 6, -6), (W - g['aR'] + 14, 14), GO, 1.0)
    for q, r in parts:
        body += pth_c(transform(q, sc, 0, 0, sc, pad, pad), EM)
    # small outlined labels
    lab = lambda s, x, y, sz=11: pth_c(text_path(s, family='jost', weight=400, size=sz, x=x, y=y, tracking=0.12).path, GO)
    body += lab('9', pad + W * sc / 2 - 3, pad - 14) + lab('16', pad + W * sc + 10, pad + H * sc / 2)
    body += lab('45°', T((0, 0))[0] - 40, T((0, 0))[1] + 8)
    body += lab('CULET', T(Vb)[0] - 20, T(Vb)[1] + 24, 10)
    w, h = W * sc + 2 * pad + 20, H * sc + 2 * pad + 20
    open(os.path.join(outdir, 'construction.svg'), 'w').write(svg_doc(w, h, body, IV))


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else HERE
    if len(sys.argv) > 2:
        P.update(json.loads(sys.argv[2]))
    print(build_all(out))
    construction(out)
