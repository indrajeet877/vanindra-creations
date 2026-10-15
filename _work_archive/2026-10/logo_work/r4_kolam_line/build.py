"""Build every Kolam Line deliverable from one parametric source."""
import sys, math
sys.path.insert(0, '.')
from lockup import *

EM, IV, AG, SG, WH = '#0B2A20', '#F6F1E7', '#A8843A', '#D2B26A', '#FFFFFF'
P = dict(r=0.30, w=0.13, rd=0.08)            # master mark (>= 48 px)
PS = dict(r=0.32, w=0.26)                    # small cut (16-40 px), no pulli
S = Spec(s=8.0, asc=146.0)                   # wordmark: x-height 100, stroke 8
S_LIGHT = 0.75                               # 'creations' = 0.75 x stroke
TRACK = 0.035

def d(p): return vtype.to_d(p)
def path(p, fill, tx=0, ty=0, sc=1):
    if p is None: return ''
    t = f' transform="translate({tx:.2f},{ty:.2f}) scale({sc:.5f})"' if (tx or ty or sc != 1) else ''
    return f'<path{t} d="{d(p)}" fill="{fill}"/>'

def bbox(*ps):
    bs = [vtype.bounds(p) for p in ps if p is not None]
    return min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)

def norm(ps, scale=1.0):
    """shift a group so its bbox starts at (0,0); returns shifted paths + w,h"""
    x0, y0, x1, y1 = bbox(*ps)
    out = [vtype.transform(p, scale, 0, 0, scale, -x0 * scale, -y0 * scale) if p is not None else None for p in ps]
    return out, (x1 - x0) * scale, (y1 - y0) * scale

# ------------------------------------------------------------------ mark
def master(scale=100.0):
    segs, line, dp = mark_geo(**P)
    (line, dp), w, h = norm([line, dp], scale)
    return line, dp, w, h

def small(scale=100.0):
    segs, line, _ = mark_geo(r=PS['r'], w=PS['w'], rd=0.1)
    (line,), w, h = norm([line], scale)
    return line, w, h

def square_svg(line, dp, w, h, side, bg, line_c, dot_c, frac=0.58, title='VanIndra Creations mark'):
    sc = side * frac / max(w, h)
    tx = (side - w * sc) / 2
    ty = (side - h * sc) / 2 + side * 0.005
    body = path(line, line_c, tx, ty, sc) + path(dp, dot_c, tx, ty, sc)
    return vtype.svg_doc(side, side, body, bg=bg, title=title)

def tight_svg(parts, w, h, pad, bg=None, title='VanIndra Creations'):
    body = ''.join(path(p, c, pad, pad) for p, c in parts)
    return vtype.svg_doc(round(w + 2 * pad, 2), round(h + 2 * pad, 2), body, bg=bg, title=title)

# ------------------------------------------------------------------ type
def wordmark_parts(with_creations=True, kolam_initial=False, two_line=False):
    """returns list of (path, role) with roles: line, dot, name, desc"""
    parts = []
    vh = S.asc + S.ov
    unit_l = (vh - S.s) / (2 + 2 * P['r'])
    rd_rel = 0.6 * S.s / unit_l
    S.dot = 0.6 * S.s
    if kolam_initial:
        line, dp, wp, W = lockup_inline(S, text='anindra', tracking=TRACK, gap=0.12 * S.X)
        line2, dp2, _, _ = kolam_v(vh, S.s, rd_rel=rd_rel)
        parts += [(line2, 'line'), (dp2, 'dot'), (wp, 'name')]
    else:
        wp, W = word('vanindra', S, tracking=TRACK)
        parts += [(wp, 'name')]
    if with_creations:
        SL = Spec(s=S.s * S_LIGHT, asc=S.asc); SL.dot = S.dot * 0.75
        cp, cw = word('creations', SL, tracking=TRACK + 0.01)
        if two_line:
            sc = 0.50
            x0 = vtype.bounds(parts[-1][0])[0] if kolam_initial else 0
            nb = vtype.bounds(parts[-1][0])
            cp = vtype.transform(cp, sc, 0, 0, sc, 0, 0)
            cb = vtype.bounds(cp)
            nameW = nb[2] - nb[0]
            cp = vtype.transform(cp, 1, 0, 0, 1, nb[0] + (nameW - (cb[2] - cb[0])) / 2 - cb[0], 0.62 * S.X)
        else:
            cp = vtype.transform(cp, 1, 0, 0, 1, W + 0.40 * S.X, 0)
        parts.append((cp, 'desc'))
    return parts

COL = {'ivory': {'line': EM, 'dot': AG, 'name': EM, 'desc': EM, 'bg': IV},
       'emerald': {'line': IV, 'dot': SG, 'name': IV, 'desc': IV, 'bg': EM},
       'white': {'line': EM, 'dot': AG, 'name': EM, 'desc': EM, 'bg': WH},
       'trans': {'line': EM, 'dot': AG, 'name': EM, 'desc': EM, 'bg': None}}

def lockup_svg(parts, ground, pad_rel=0.55, title='VanIndra Creations'):
    ps = [p for p, _ in parts]
    shifted, w, h = norm(ps)
    c = COL[ground]
    vh = S.asc + S.ov
    pad = pad_rel * vh
    body_parts = [(p, c[role]) for p, (_, role) in zip(shifted, parts)]
    return tight_svg(body_parts, w, h, pad, bg=c['bg'], title=title), w + 2 * pad, h + 2 * pad

def stacked_svg(ground):
    c = COL[ground]
    line, dp, mw, mh = master(scale=100.0)
    # name block: 'vanindra' + 'creations' (light, smaller) centred
    wp, W = word('vanindra', S, tracking=TRACK)
    SL = Spec(s=S.s * S_LIGHT * 1.25, asc=S.asc); SL.dot = S.dot * 0.8
    cp, cw = word('creations', SL, tracking=TRACK + 0.04)
    k = 0.52
    cp = vtype.transform(cp, k, 0, 0, k, 0, 0)
    MARK_H = 260.0
    sc = MARK_H / mh
    line = vtype.transform(line, sc, 0, 0, sc, 0, 0); dp = vtype.transform(dp, sc, 0, 0, sc, 0, 0)
    mw *= sc
    nb = vtype.bounds(wp); cb = vtype.bounds(cp)
    nw = nb[2] - nb[0]; cwid = cb[2] - cb[0]
    Wt = max(mw, nw, cwid)
    line = vtype.transform(line, 1, 0, 0, 1, (Wt - mw) / 2, 0); dp = vtype.transform(dp, 1, 0, 0, 1, (Wt - mw) / 2, 0)
    y_name = MARK_H + 0.62 * S.X + S.asc       # baseline of name (SVG y-down); asc space for d
    wp = vtype.transform(wp, 1, 0, 0, 1, (Wt - nw) / 2 - nb[0], y_name)
    y_desc = y_name + 0.95 * S.X
    cp = vtype.transform(cp, 1, 0, 0, 1, (Wt - cwid) / 2 - cb[0], y_desc)
    parts = [(line, 'line'), (dp, 'dot'), (wp, 'name'), (cp, 'desc')]
    return lockup_svg(parts, ground, pad_rel=0.75)

def write(name, svg):
    open(name, 'w').write(svg)

if __name__ == '__main__':
    line, dp, mw, mh = master()
    write('mark.svg', tight_svg([(line, EM), (dp, AG)], mw, mh, mh * 0.04, title='VanIndra Creations mark'))
    write('mark_one_colour_emerald.svg', tight_svg([(line, EM), (dp, EM)], mw, mh, mh * 0.04, title='VanIndra Creations mark'))
    write('mark_one_colour_ivory.svg', tight_svg([(line, IV), (dp, IV)], mw, mh, mh * 0.04, title='VanIndra Creations mark'))
    write('mark_one_colour_gold.svg', tight_svg([(line, AG), (dp, AG)], mw, mh, mh * 0.04, title='VanIndra Creations mark'))
    write('mark_on_ivory.svg', square_svg(line, dp, mw, mh, 1000, IV, EM, AG))
    write('mark_on_emerald.svg', square_svg(line, dp, mw, mh, 1000, EM, IV, SG))
    write('avatar_on_emerald.svg', square_svg(line, dp, mw, mh, 1000, EM, IV, SG, frac=0.50))
    sl, sw, sh = small()
    write('mark_small.svg', tight_svg([(sl, EM)], sw, sh, sh * 0.03, title='VanIndra Creations mark (small)'))
    write('mark_small_ivory.svg', tight_svg([(sl, IV)], sw, sh, sh * 0.03, title='VanIndra Creations mark (small)'))
    write('favicon.svg', square_svg(sl, None, sw, sh, 64, EM, IV, IV, frac=0.80))
    # wordmark (plain v), lockups
    svg, _, _ = lockup_svg(wordmark_parts(True, False), 'trans', 0.3); write('wordmark.svg', svg)
    svg, _, _ = lockup_svg(wordmark_parts(False, True), 'trans', 0.3); write('lockup_compact.svg', svg)
    for g in ('ivory', 'emerald'):
        svg, _, _ = lockup_svg(wordmark_parts(True, True), g); write(f'lockup_horizontal_on_{g}.svg', svg)
        svg, _, _ = lockup_svg(wordmark_parts(False, True), g); write(f'lockup_compact_on_{g}.svg', svg)
        svg, _, _ = stacked_svg(g); write(f'lockup_stacked_on_{g}.svg', svg)
    svg, _, _ = lockup_svg(wordmark_parts(True, True), 'white'); write('global.svg', svg)
    print('built')

# ------------------------------------------------------------------ v2: jewel colouring + new lockups
def master_split(scale=100.0):
    """line, quiet pulli (L,R,B), jewel pulli (C)"""
    segs, line, _ = mark_geo(**P)
    quiet = dots_path([GRID[k] for k in 'LRB'], P['rd'])
    jewel = dots_path([GRID['C']], P['rd'])
    (line, quiet, jewel), w, h = norm([line, quiet, jewel], scale)
    return line, quiet, jewel, w, h

def kolam_initial(vh, stroke, rd_abs):
    unit = (vh - stroke) / (2 + 2 * P['r'])
    w_rel = stroke / unit
    segs, line, _ = mark_geo(r=P['r'], w=w_rel, rd=rd_abs / unit)
    quiet = dots_path([GRID[k] for k in 'LRB'], rd_abs / unit)
    jewel = dots_path([GRID['C']], rd_abs / unit)
    x0, y0, x1, y1 = vtype.bounds(line)
    T = lambda p: vtype.transform(p, unit, 0, 0, unit, -x0 * unit, -y1 * unit)
    return T(line), T(quiet), T(jewel), (x1 - x0) * unit

def place_after(Vp, word_p, gap, S):
    ys = [-S.X * f for f in (0.12, 0.3, 0.5, 0.7, 0.88)]
    lo, hi = -2000, 2000
    for _ in range(50):
        mid = (lo + hi) / 2
        g = h_gap_at(Vp, vtype.transform(word_p, 1, 0, 0, 1, mid, 0), ys)
        if g is None or g < gap: lo = mid
        else: hi = mid
    return hi

def name_parts(creations='inline', initial_scale=1.0):
    """creations: None | 'inline' | 'below' (drop-cap two-line)"""
    S.dot = 0.6 * S.s
    vh = (S.asc + S.ov) * initial_scale
    line, quiet, jewel, vw = kolam_initial(vh, S.s * (1.0 if initial_scale == 1.0 else 1.18), S.dot * (1.0 if initial_scale == 1.0 else 1.25))
    Vp = vtype.union(line, quiet, jewel)
    wp, W = word('anindra', S, tracking=TRACK)
    x = place_after(Vp, wp, 0.115 * S.X, S)
    wp = vtype.transform(wp, 1, 0, 0, 1, x, 0)
    parts = [(line, 'line'), (quiet, 'quiet'), (jewel, 'dot'), (wp, 'name')]
    if creations:
        SL = Spec(s=S.s * S_LIGHT, asc=S.asc); SL.dot = S.dot * 0.85
        if creations == 'inline':
            cp, cw = word('creations', SL, tracking=TRACK + 0.01)
            cp = vtype.transform(cp, 1, 0, 0, 1, x + W + 0.36 * S.X, 0)
        else:
            k = 1.0
            cp, cw = word('creations', SL, tracking=TRACK + 0.01)
            nb = vtype.bounds(wp)
            cp = vtype.transform(cp, k, 0, 0, k, nb[0] - vtype.bounds(cp)[0] * k + 0.0, 1.0 * S.X + 0.62 * S.X)
        parts.append((cp, 'desc'))
    return parts

COL2 = {'ivory': {'line': EM, 'quiet': EM, 'dot': AG, 'name': EM, 'desc': EM, 'bg': IV},
        'emerald': {'line': IV, 'quiet': IV, 'dot': SG, 'name': IV, 'desc': IV, 'bg': EM},
        'white': {'line': EM, 'quiet': EM, 'dot': AG, 'name': EM, 'desc': EM, 'bg': WH},
        'trans': {'line': EM, 'quiet': EM, 'dot': AG, 'name': EM, 'desc': EM, 'bg': None},
        'gold': {'line': AG, 'quiet': AG, 'dot': AG, 'name': AG, 'desc': AG, 'bg': None},
        'ivory1': {'line': IV, 'quiet': IV, 'dot': IV, 'name': IV, 'desc': IV, 'bg': None}}

def svg_parts(parts, ground, pad, title='VanIndra Creations'):
    ps = [p for p, _ in parts]
    shifted, w, h = norm(ps)
    c = COL2[ground]
    body = ''.join(path(p, c[role], pad, pad) for p, (_, role) in zip(shifted, parts))
    return vtype.svg_doc(round(w + 2 * pad, 2), round(h + 2 * pad, 2), body, bg=c['bg'], title=title)

def build_v2():
    line, quiet, jewel, mw, mh = master_split()
    pad = mh * 0.04
    write('mark.svg', svg_parts([(line, 'line'), (quiet, 'quiet'), (jewel, 'dot')], 'trans', pad, 'VanIndra Creations mark'))
    write('mark_one_colour_gold.svg', svg_parts([(line, 'line'), (quiet, 'quiet'), (jewel, 'dot')], 'gold', pad, 'VanIndra Creations mark'))
    write('mark_one_colour_ivory.svg', svg_parts([(line, 'line'), (quiet, 'quiet'), (jewel, 'dot')], 'ivory1', pad, 'VanIndra Creations mark'))
    for g, bg, lc, dc in (('ivory', IV, EM, AG), ('emerald', EM, IV, SG)):
        side = 1000; frac = 0.58
        sc = side * frac / max(mw, mh); tx = (side - mw * sc) / 2; ty = (side - mh * sc) / 2
        body = path(line, lc, tx, ty, sc) + path(quiet, lc, tx, ty, sc) + path(jewel, dc, tx, ty, sc)
        write(f'mark_on_{g}.svg', vtype.svg_doc(side, side, body, bg=bg, title='VanIndra Creations mark'))
    vh = S.asc + S.ov
    write('wordmark.svg', svg_parts([(word('vanindra', S, tracking=TRACK)[0], 'name')] +
                                    [(vtype.transform(word('creations', Spec(s=S.s * S_LIGHT, asc=S.asc), tracking=TRACK + 0.01)[0], 1, 0, 0, 1,
                                                      word('vanindra', S, tracking=TRACK)[1] + 0.36 * S.X, 0), 'desc')], 'trans', 0.25 * vh))
    for g in ('ivory', 'emerald'):
        write(f'lockup_horizontal_on_{g}.svg', svg_parts(name_parts('inline'), g, 0.55 * vh))
        write(f'lockup_compact_on_{g}.svg', svg_parts(name_parts(None), g, 0.55 * vh))
        write(f'lockup_stacked_on_{g}.svg', svg_parts(name_parts('below', initial_scale=1.0), g, 0.7 * vh))
    write('lockup_compact.svg', svg_parts(name_parts(None), 'trans', 0.2 * vh))
    write('lockup_horizontal.svg', svg_parts(name_parts('inline'), 'trans', 0.2 * vh))
    write('global.svg', svg_parts(name_parts('inline'), 'white', 0.55 * vh))

if __name__ == '__main__':
    build_v2()
    print('v2 built')

def stacked_dropcap():
    """Kolam initial spans line 1 ascender -> line 2 baseline; 'anindra' and 'creations' left-aligned beside it."""
    S.dot = 0.6 * S.s
    lead = 1.62 * S.X                      # baseline-to-baseline
    vh = S.asc + S.ov + lead               # from ascender top of line 1 to baseline of line 2
    stroke = S.s * 1.30
    line, quiet, jewel, vw = kolam_initial(vh, stroke, 0.6 * S.s * 1.5)
    # kolam_initial puts the V's bottom at y=0 (baseline) -> shift down by lead so bottom sits on line-2 baseline
    line, quiet, jewel = [vtype.transform(p, 1, 0, 0, 1, 0, lead) for p in (line, quiet, jewel)]
    Vp = vtype.union(line, quiet, jewel)
    wp, W = word('anindra', S, tracking=TRACK)
    x = place_after(Vp, wp, 0.14 * S.X, S)
    SL = Spec(s=S.s * S_LIGHT, asc=S.asc); SL.dot = S.dot * 0.85
    cp, cw = word('creations', SL, tracking=TRACK + 0.01)
    # creations follows the V's diagonal: tuck it as close as the gap rule allows on line 2
    ys2 = [lead - S.X * f for f in (0.12, 0.3, 0.5, 0.7, 0.88)]
    lo, hi = -2000, 2000
    for _ in range(50):
        mid = (lo + hi) / 2
        g = h_gap_at(Vp, vtype.transform(cp, 1, 0, 0, 1, mid, lead), ys2)
        if g is None or g < 0.14 * S.X: lo = mid
        else: hi = mid
    x2 = max(hi, x)  # never left of line 1 -> clean left edge for both lines
    x2 = x
    wp = vtype.transform(wp, 1, 0, 0, 1, x, 0)
    cp = vtype.transform(cp, 1, 0, 0, 1, x2, lead)
    return [(line, 'line'), (quiet, 'quiet'), (jewel, 'dot'), (wp, 'name'), (cp, 'desc')]

if __name__ == '__main__':
    vh = S.asc + S.ov
    for g in ('ivory', 'emerald'):
        write(f'lockup_stacked_on_{g}.svg', svg_parts(stacked_dropcap(), g, 0.55 * vh))
    print('stacked dropcap built')

def tag_parts():
    """'edit by Vanindra' credit: light 'edit by' + kolam initial + 'anindra'."""
    S.dot = 0.6 * S.s
    SL = Spec(s=S.s * 0.85, asc=S.asc); SL.dot = S.dot * 0.9
    eb, ebw = word('edit by', SL, tracking=TRACK + 0.01)
    parts = name_parts(None)
    shift = ebw + 0.42 * S.X
    parts = [(vtype.transform(p, 1, 0, 0, 1, shift, 0), r) for p, r in parts]
    return [(eb, 'desc')] + parts

if __name__ == '__main__':
    write('tag_edit_by_emerald.svg', svg_parts(tag_parts(), 'trans', 2))
    COL2['ivory_t'] = {'line': IV, 'quiet': IV, 'dot': SG, 'name': IV, 'desc': IV, 'bg': None}
    write('tag_edit_by_ivory.svg', svg_parts(tag_parts(), 'ivory_t', 2))
    COL2['em_t'] = {'line': EM, 'quiet': EM, 'dot': AG, 'name': EM, 'desc': EM, 'bg': None}
    write('lockup_horizontal_emerald_ink.svg', svg_parts(name_parts('inline'), 'em_t', 2))
    write('lockup_compact_emerald_ink.svg', svg_parts(name_parts(None), 'em_t', 2))
    write('lockup_horizontal_ivory_ink.svg', svg_parts(name_parts('inline'), 'ivory_t', 2))
    write('lockup_compact_ivory_ink.svg', svg_parts(name_parts(None), 'ivory_t', 2))
    print('tags + inks built')

if __name__ == '__main__':
    line, quiet, jewel, mw, mh = master_split()
    for name, frac in (('avatar_on_emerald.svg', 0.50),):
        side = 1000; sc = side * frac / max(mw, mh); tx = (side - mw * sc) / 2; ty = (side - mh * sc) / 2
        body = path(line, IV, tx, ty, sc) + path(quiet, IV, tx, ty, sc) + path(jewel, SG, tx, ty, sc)
        write(name, vtype.svg_doc(side, side, body, bg=EM, title='VanIndra Creations avatar'))
    sl, sw, sh = small()
    write('avatar_small_on_emerald.svg', square_svg(sl, None, sw, sh, 1000, EM, IV, IV, frac=0.58, title='VanIndra Creations avatar (small)'))
    write('favicon.svg', square_svg(sl, None, sw, sh, 64, EM, IV, IV, frac=0.80, title='VanIndra Creations'))
    print('avatars built')
