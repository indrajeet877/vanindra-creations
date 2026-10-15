"""Avatar / favicon candidates derived from the wordmark (no V)."""
import sys, subprocess
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/r2_one_dot')
from comp import *
from explore import derive

KW = dict(S=96, T=42, ktop=0.70, kbot=0.56, kin_top=0.74, kin_bot=0.58, kAR=0.72, kAiR=0.70, apex=0.60,
          nW=420, aW=430, vW=420, rW=255, dotD=118, vthin=48, Th=56)


def m_ni(P_):
    n = LATIN['n'](P_); i = LATIN['i'](P_)
    xi = n['w'] + P_.sb * 2
    return union(n['path'], shift(i['path'], xi)), [dot(P_, xi + i['dot'][0], i['dot'][1])]


def m_ndot(P_):
    n = LATIN['n'](P_)
    W = P_.nW
    cx = W - P_.S * P_.Rk / 2
    return n['path'], [dot(P_, cx, P_.X + P_.dotGap + P_.dotD / 2)]


def m_nin(P_):
    w = set_word('nin', P_)
    return w['path'], [dot(P_, *w['dots'][0])]


def m_hindi_ni(P_):
    r = d_i_na(P_, 0)
    hl = rect(-P_.hl_over * 0.6, P_.H - P_.Th, r['x1'] + P_.hl_over * 0.6, P_.H)
    return union(r['path'], hl), [dot(P_, *r['dot'])]


def m_word(P_):
    w = set_word('vanindra', P_)
    return w['path'], [dot(P_, *w['dots'][0])]


def m_i(P_):
    i = LATIN['i'](P_)
    return i['path'], [dot(P_, *i['dot'])]


CANDS = [('M1 ni', m_ni), ('M2 n + dot', m_ndot), ('M3 nin crop', m_nin), ('M4 निं', m_hindi_ni),
         ('M5 wordmark', m_word), ('M6 i', m_i)]


def fit(path, dots, box, fill=0.62, crop=False):
    allp = union(path, *dots)
    b = bounds(allp)
    w, h = b[2] - b[0], b[3] - b[1]
    s = box * fill / max(w, h)
    if crop:
        s = box * fill / h
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return s, cx, cy


def render():
    P_ = derive(P(**KW))
    ink = Ink()
    x = 30
    rows = []
    W = 1400
    y = 30
    labels = ''
    for name, fn in CANDS:
        path, dots = fn(P_)
        crop = name.startswith('M3')
        xx = 30
        for size in [150, 56, 32]:
            c = place(circle(0, 0, size / 2), 1, xx + size / 2, y + 75)
            ink.add(c, EMERALD)
            fillf = 0.95 if crop else (0.86 if name.startswith('M5') else 0.60)
            s, cx, cy = fit(path, dots, size, fillf, crop=crop)
            ox = xx + size / 2 - cx * s
            oy = y + 75 + cy * s
            # clip by circle: approximate with intersection
            circ_local = circle(cx, cy, (size / 2) / s)
            pth = intersection(path, circ_local)
            add_word(ink, pth, [intersection(d, circ_local) for d in dots], s, ox, oy, IVORY, GOLD_LT)
            xx += size + 30
        # favicon squares 16, 24 on emerald and ivory
        for size, bg, fg, dg in [(16, EMERALD, IVORY, GOLD_LT), (24, EMERALD, IVORY, GOLD_LT), (16, IVORY, EMERALD, GOLD), (24, IVORY, EMERALD, GOLD)]:
            sq = place(rect(0, 0, size, size), 1, xx, y + 75 + size / 2)
            ink.add(sq, bg)
            fillf = 1.0 if crop else (0.92 if name.startswith('M5') else 0.80)
            s, cx, cy = fit(path, dots, size, fillf, crop=crop)
            ox = xx + size / 2 - cx * s
            oy = y + 75 + cy * s
            sqloc = rect(cx - size / 2 / s, cy - size / 2 / s, cx + size / 2 / s, cy + size / 2 / s)
            add_word(ink, intersection(path, sqloc), [intersection(d, sqloc) for d in dots], s, ox, oy, fg, dg)
            xx += size + 24
        labels += f'<text x="{xx+20}" y="{y+80}" font-family="sans-serif" font-size="18" fill="#333">{name}</text>'
        y += 170
    svg = svg_doc(W, y + 20, ink.body() + labels, bg='#FFFFFF')
    open('work/marks_explore.svg', 'w').write(svg)
    subprocess.run(['node', '../toolkit/render.js', 'png', 'work/marks_explore.svg', 'explore_marks.png', '900'], check=True)


if __name__ == '__main__':
    render()
