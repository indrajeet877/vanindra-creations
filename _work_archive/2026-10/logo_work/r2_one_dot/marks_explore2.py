import sys, subprocess
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/r2_one_dot')
from comp import *
from explore import derive
from marks_explore import KW, m_ni, m_nin, m_hindi_ni, fit

SMALL = dict(KW, T=62, S=104, dotD=132, dotGap=58, Th=70, vthin=64)


def m_line_dot(P_):
    L = P_.nW * 1.5
    bar = rect(0, P_.X - P_.Th, L, P_.X)
    return bar, [dot(P_, L / 2, P_.X + P_.dotGap + P_.dotD / 2)]


def m_line_i(P_):
    L = P_.nW * 1.4
    bar = rect(0, P_.X - P_.Th, L, P_.X)
    st = rect(L / 2 - P_.S / 2, 0, L / 2 + P_.S / 2, P_.X)
    return union(bar, st), [dot(P_, L / 2, P_.X + P_.dotGap + P_.dotD / 2)]


def m_kamaan(P_):
    r = d_i_na(P_, 0)
    S, H, Th, T = P_.dS, P_.H, P_.Th, P_.T
    # keep only the i-matra stem + arch + headline stub
    keep = rect(-200, -10, r['na_danda'][0] - 10, H + 1000)
    p = intersection(r['path'], keep)
    hl = rect(-P_.hl_over * 0.6, H - Th, r['na_danda'][1], H)
    return union(p, hl), [dot(P_, *r['dot'])]


def m_two_line(P_):
    a = set_word('van', P_)
    b = set_word('indra', P_)
    lead = P_.X * 1.75
    return union(shift(a['path'], 0, lead), b['path']), [dot(P_, *b['dots'][0])]


CANDS = [('M1s ni (small cut)', m_ni, SMALL, False), ('M3s nin crop', m_nin, SMALL, True),
         ('M7 line+dot', m_line_dot, SMALL, False), ('M8 line+i', m_line_i, SMALL, False),
         ('M9 kamaan+dot', m_kamaan, SMALL, False), ('M4s निं', m_hindi_ni, SMALL, False),
         ('M11 van/indra', m_two_line, KW, False)]


def render():
    ink = Ink(); labels = ''
    y = 30
    for name, fn, kw, crop in CANDS:
        P_ = derive(P(**kw))
        path, dots = fn(P_)
        xx = 30
        for size in [150, 56, 32]:
            ink.add(place(circle(0, 0, size / 2), 1, xx + size / 2, y + 75), EMERALD)
            fillf = 0.98 if crop else (0.80 if name.startswith('M11') else 0.60)
            s, cx, cy = fit(path, dots, size, fillf, crop=crop)
            if crop:
                # centre on the dot's x
                cx = dots[0].bounds[0] / 2 + dots[0].bounds[2] / 2
            ox = xx + size / 2 - cx * s; oy = y + 75 + cy * s
            cl = circle(cx, cy, (size / 2) / s)
            add_word(ink, intersection(path, cl), [intersection(d, cl) for d in dots], s, ox, oy, IVORY, GOLD_LT)
            xx += size + 30
        for size, bg, fg, dg in [(16, EMERALD, IVORY, GOLD_LT), (24, EMERALD, IVORY, GOLD_LT), (16, IVORY, EMERALD, GOLD), (24, IVORY, EMERALD, GOLD)]:
            ink.add(place(rect(0, 0, size, size), 1, xx, y + 75 + size / 2), bg)
            fillf = 1.0 if crop else (0.92 if name.startswith('M11') else 0.80)
            s, cx, cy = fit(path, dots, size, fillf, crop=crop)
            if crop:
                cx = dots[0].bounds[0] / 2 + dots[0].bounds[2] / 2
            ox = xx + size / 2 - cx * s; oy = y + 75 + cy * s
            sq = rect(cx - size / 2 / s, cy - size / 2 / s, cx + size / 2 / s, cy + size / 2 / s)
            add_word(ink, intersection(path, sq), [intersection(d, sq) for d in dots], s, ox, oy, fg, dg)
            xx += size + 24
        labels += f'<text x="{xx+20}" y="{y+80}" font-family="sans-serif" font-size="18" fill="#333">{name}</text>'
        y += 170
    open('work/marks_explore2.svg', 'w').write(svg_doc(900, y + 20, ink.body() + labels, bg='#FFFFFF'))
    subprocess.run(['node', '../toolkit/render.js', 'png', 'work/marks_explore2.svg', 'work/marks_explore2.png', '900'], check=True)


if __name__ == '__main__':
    render()
