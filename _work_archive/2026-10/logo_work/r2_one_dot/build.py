"""One Dot: build every deliverable SVG."""
import sys, os, subprocess, json
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/r2_one_dot')
from comp import *
from system import master, small, light, book, deva_for_scale

OUT = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/r2_one_dot'
U = 0.2  # design units -> svg px


class Art:
    """A group of (y-up path, role) in design units. role: 'ink' | 'dot' | 'ink2'."""

    def __init__(self):
        self.parts = []

    def add(self, path, role, dx=0.0, dy=0.0, s=1.0):
        self.parts.append((transform(path, s, 0, 0, s, dx, dy), role))
        return self

    def merge(self, other, dx=0.0, dy=0.0, s=1.0):
        for p, r in other.parts:
            self.add(p, r, dx, dy, s)
        return self

    def bounds(self):
        bs = [bounds(p) for p, _ in self.parts]
        return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))

    def svg(self, colours, pad=(0, 0, 0, 0), bg=None, square=False, box=None, title='VanIndra Creations'):
        """colours: role -> fill. pad: (left, top, right, bottom) in design units."""
        x0, y0, x1, y1 = box if box else self.bounds()
        x0 -= pad[0]; x1 += pad[2]; y0 -= pad[3]; y1 += pad[1]
        if square:
            w, h = x1 - x0, y1 - y0
            if w > h:
                d = (w - h) / 2; y0 -= d; y1 += d
            else:
                d = (h - w) / 2; x0 -= d; x1 += d
        W, H = (x1 - x0) * U, (y1 - y0) * U
        by_role = {}
        for p, r in self.parts:
            by_role.setdefault(r, []).append(p)
        body = ''
        for r in ['ink', 'ink2', 'dot']:
            if r not in by_role:
                continue
            p = union(*by_role[r])
            p = transform(p, U, 0, 0, -U, -x0 * U, y1 * U)
            body += f'<path d="{fmt(to_d(p))}" fill="{colours[r]}"/>'
        return svg_doc(round(W, 2), round(H, 2), body, bg=bg, title=title)


def latin(P_, word='vanindra', dot_role='dot'):
    w = set_word(word, P_)
    a = Art().add(w['path'], 'ink')
    for d in w['dots']:
        a.add(dot(P_, *d), dot_role)
    return a, w


def hindi(P_, dot_role='dot'):
    h = set_hindi(P_)
    a = Art().add(h['path'], 'ink')
    for d in h['dots']:
        a.add(dot(P_, *d), dot_role)
    return a, h


def ni(P_):
    n = LATIN['n'](P_)
    i = LATIN['i'](P_)
    xi = n["w"] + P_.sb * 1.6   # tighter than in the word: the pair reads as one unit
    a = Art().add(n['path'], 'ink').add(shift(i['path'], xi), 'ink').add(dot(P_, xi + i['dot'][0], i['dot'][1]), 'dot')
    return a


def mark_box(a, P_, fill=0.62):
    """square box around the ni mark: optically centred (body centre slightly above the bbox centre)."""
    x0, y0, x1, y1 = a.bounds()
    w, h = x1 - x0, y1 - y0
    side = max(w, h) / fill
    cx = (x0 + x1) / 2 - P_.S * 0.04
    cy = (y0 + y1) / 2 - P_.X * 0.02
    return (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)


ON_IVORY = dict(ink=EMERALD, ink2=EMERALD, dot=GOLD)
ON_EMERALD = dict(ink=IVORY, ink2=IVORY, dot=GOLD_LT)
GOLD_ONE = dict(ink=GOLD, ink2=GOLD, dot=GOLD)
CLEAR = 1.0  # clear space = 1 x-height (X) around lockups; marks use the box


def write(name, svg):
    open(os.path.join(OUT, name), 'w').write(svg)


def horizontal(Pm, Pl):
    a, w = latin(Pm)
    c, cw = latin(Pl, 'creations', dot_role='ink2')
    a.merge(c, dx=w['width'] + Pm.space * 1.15)
    return a


def stacked(Pm, Pb):
    """vanindra over creations (book weight, 62% of the name's width), both flush left."""
    a, w = latin(Pm)
    c, cw = latin(Pb, 'creations', dot_role='ink2')
    cb = c.bounds()
    f = w['width'] * 0.62 / (cb[2] - cb[0])
    top_c = cb[3] * f
    a.merge(c, dx=-cb[0] * f, dy=-(Pm.X * Pm.stack_gap + top_c), s=f)
    return a


def bilingual_stack(Pm, f=1.0):
    """vanindra over वनिंद्रा; the two dots on one vertical axis."""
    a, w = latin(Pm)
    Pd = deva_for_scale(Pm, f)
    h, hw = hindi(Pd)
    dx = w['dots'][0][0] - hw['dots'][0][0] * f
    top = (Pd.H + Pd.kam_rise) * f
    a.merge(h, dx=dx, dy=-(Pm.X * Pm.bi_gap + top), s=f)
    return a


def bilingual_line(Pm):
    """vanindra वनिंद्रा on one line: the Devanagari headline continues the Latin x-height line;
    both dots float at the same height."""
    a, w = latin(Pm)
    h, hw = hindi(Pm)
    drop = Pm.H - Pm.X
    a.merge(h, dx=w['width'] + Pm.space * 1.6 + Pm.hl_over, dy=-drop)
    return a


def build():
    Pm = master()
    Pm.stack_gap = 0.42
    Pm.bi_gap = 0.72
    Ps = small()
    Pl = light()
    X = Pm.X
    pad = (X * 0.6,) * 4

    # marks
    m = ni(Pm)
    box = mark_box(m, Pm)
    write('mark.svg', m.svg(ON_IVORY, box=box))
    ms = ni(Ps)
    write('mark_small.svg', ms.svg(ON_IVORY, box=mark_box(ms, Ps, fill=0.80)))
    write('mark_on_ivory.svg', m.svg(ON_IVORY, box=box, bg=IVORY))
    write('mark_on_emerald.svg', m.svg(ON_EMERALD, box=box, bg=EMERALD))
    write('mark_one_colour_gold.svg', m.svg(GOLD_ONE, box=box))
    write('mark_small_on_emerald.svg', ms.svg(ON_EMERALD, box=mark_box(ms, Ps, fill=0.80), bg=EMERALD))
    # circle-safe small cut for round avatars at 32-64 px (Instagram comments, stories ring)
    write('mark_small_avatar_on_emerald.svg', ms.svg(ON_EMERALD, box=mark_box(ms, Ps, fill=0.66), bg=EMERALD))
    # Devanagari avatar (alternate)
    r = d_i_na(Pm, 0)
    hm = Art().add(union(r['path'], rect(-Pm.hl_over * 0.6, Pm.H - Pm.Th, r['x1'] + Pm.hl_over * 0.6, Pm.H)), 'ink').add(dot(Pm, *r['dot']), 'dot')
    write('mark_hindi_on_emerald.svg', hm.svg(ON_EMERALD, box=mark_box(hm, Pm, fill=0.62), bg=EMERALD))

    # wordmarks
    wm, w = latin(Pm)
    write('wordmark.svg', wm.svg(ON_IVORY, pad=pad))
    write('wordmark_on_emerald.svg', wm.svg(ON_EMERALD, pad=pad, bg=EMERALD))
    hwm, hw = hindi(Pm)
    write('wordmark_hindi.svg', hwm.svg(ON_IVORY, pad=pad))

    # lockups
    hz = horizontal(Pm, Pl)
    write('lockup_horizontal_on_ivory.svg', hz.svg(ON_IVORY, pad=pad, bg=IVORY))
    write('lockup_horizontal_on_emerald.svg', hz.svg(ON_EMERALD, pad=pad, bg=EMERALD))
    st = stacked(Pm, book())
    write('lockup_stacked_on_ivory.svg', st.svg(ON_IVORY, pad=(X,) * 4, bg=IVORY))
    write('lockup_stacked_on_emerald.svg', st.svg(ON_EMERALD, pad=(X,) * 4, bg=EMERALD))
    bs = bilingual_stack(Pm, f=1.0)
    write('lockup_bilingual_on_ivory.svg', bs.svg(ON_IVORY, pad=(X,) * 4, bg=IVORY))
    write('lockup_bilingual_on_emerald.svg', bs.svg(ON_EMERALD, pad=(X,) * 4, bg=EMERALD))
    bl = bilingual_line(Pm)
    write('lockup_bilingual_line_on_ivory.svg', bl.svg(ON_IVORY, pad=pad, bg=IVORY))
    # small / production cut of the wordmark: heavier hairlines + larger dot (embroidery, foil, < 120 px wide)
    wms, _ = latin(Ps)
    write('wordmark_small.svg', wms.svg(ON_IVORY, pad=pad))
    # header cut: wordmark only, tight padding (for 32-56 px tall headers)
    write('header_wordmark_on_ivory.svg', wm.svg(ON_IVORY, pad=(X * 0.25,) * 4))
    write('global.svg', hz.svg(ON_IVORY, pad=pad, bg=IVORY))
    # helpers for presentation renders (transparent)
    os.makedirs(os.path.join(OUT, 'parts'), exist_ok=True)
    TRANS_IVORY = dict(ink=IVORY, ink2=IVORY, dot=GOLD_LT)
    write('parts/mark_small_ivory.svg', ms.svg(TRANS_IVORY, box=mark_box(ms, Ps, fill=0.80)))
    write('parts/lockup_h_emerald.svg', hz.svg(ON_IVORY, pad=(X * 0.2,) * 4))
    write('parts/lockup_h_ivory.svg', hz.svg(TRANS_IVORY, pad=(X * 0.2,) * 4))
    write('parts/wordmark_emerald.svg', wm.svg(ON_IVORY, pad=(X * 0.2,) * 4))
    write('parts/wordmark_ivory.svg', wm.svg(TRANS_IVORY, pad=(X * 0.2,) * 4))
    # 'edit by vanindra' credit: 'edit by' in the light cut (ink dot), name in the master cut (the one gold dot)
    eb, ebw = latin(Pl, 'edit by', dot_role='ink2')
    tag = Art().merge(eb)
    nm, nmw = latin(Pm)
    tag.merge(nm, dx=ebw['width'] + Pm.space * 1.0)
    write('parts/edit_by_ivory.svg', tag.svg(TRANS_IVORY, pad=(0, 0, 0, 0)))
    write('parts/edit_by_emerald.svg', tag.svg(ON_IVORY, pad=(0, 0, 0, 0)))


if __name__ == '__main__':
    build()
