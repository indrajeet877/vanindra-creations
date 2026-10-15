"""Round 3 / One Dot: exploration sheet of 8 genuinely different lettering systems."""
import sys, subprocess
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/r2_one_dot')
from comp import *


def derive(P_):
    """Devanagari widths follow the Latin ones (one system)."""
    return P_.copy(vaW=P_.aW * 0.98, naW=P_.nW * 0.95, daW=P_.aW * 0.86, dS=P_.S, hgap=P_.sb * 1.25)


VARS = [
    ('E1', 'Hanging grotesk: flat tops, round bottoms, square shoulders', dict(S=90, T=56, ktop=0.80, kin_top=0.80, nW=390, aW=400, vW=390, rW=245)),
    ('E2', 'Geometric round: circle-based, near-monoline', dict(S=78, T=72, ktop=0.56, kbot=0.56, kin_top=0.56, kin_bot=0.56, kAL=0.6, kAiL=0.6, kAR=0.58, kAiR=0.58, apex=0.5, nW=420, aW=450, vW=430, rW=260, Rk=1.06, dotD=98, vthin=70)),
    ('E3', 'Fashion contrast: hairline horizontals, heavy stems', dict(S=98, T=32, ktop=0.70, kbot=0.56, kin_top=0.74, kin_bot=0.58, kAR=0.72, kAiR=0.70, apex=0.60, nW=420, aW=430, vW=420, rW=255, dotD=112, vthin=40)),
    ('E4', 'Kalam cut: every stem foot cut at the reed-pen angle', dict(S=88, T=50, ktop=0.72, term_angle=26, nW=400, aW=410, vW=400, rW=250)),
    ('E5', 'Light luxe: light, wide, one large dot', dict(S=52, T=40, ktop=0.66, kbot=0.56, kin_top=0.66, kin_bot=0.56, kAR=0.66, kAiR=0.66, nW=440, aW=450, vW=440, rW=270, dotD=104, dotGap=60, sb=56, vthin=42, vthick=58, Th=44)),
    ('E6', 'Squared: superellipse forms, square dot', dict(S=92, T=70, ktop=0.90, kbot=0.86, kin_top=0.92, kin_bot=0.88, kAR=0.90, kAiR=0.92, nW=400, aW=410, vW=400, rW=250, dot_shape='square', dotD=100)),
    ('E7', 'Black display: heavy, compact, tight', dict(S=136, T=78, ktop=0.74, kbot=0.58, kin_top=0.78, nW=420, aW=440, vW=430, rW=270, sb=40, sbr=24, dotD=150, dotGap=56, vthin=96, Th=78)),
    ('E8', 'Two lines: Latin also hangs from a hairline (faux-Deva test)', dict(S=90, T=48, ktop=0.76, nW=400, aW=410, vW=400, rW=250)),
]


def ni_mark(P_):
    """'ni' cut from the wordmark: n + i + dot."""
    n = LATIN['n'](P_)
    i = LATIN['i'](P_)
    gap = P_.sb * 2
    x_i = n['w'] + gap
    path = union(n['path'], shift(i['path'], x_i))
    d = dot(P_, x_i + i['dot'][0], i['dot'][1])
    return path, d, x_i + i['w']


def cell(code, label, kw, cw=1000, ch=640):
    P_ = derive(P(**kw))
    ink = Ink()
    lw, ld = latin_art(P_)
    hw, hd = hindi_art(P_)
    s = 560 / lw['width']
    base1 = 60 + (P_.asc + 30) * s + 40
    add_word(ink, lw['path'], ld, s, 50, base1, EMERALD, GOLD)
    if code == 'E8':
        ink.add(place(rect(-20, P_.X, lw['width'] + 20, P_.X + 14), s, 50, base1), EMERALD)
    base2 = base1 + 70 + (P_.H + P_.kam_rise + P_.dotD) * s * 1.05
    s2 = s * 1.05
    add_word(ink, hw['path'], hd, s2, 50 + P_.hl_over * s2, base2 + 40, EMERALD, GOLD)
    # avatar: ni on emerald circle
    mp, md, mw = ni_mark(P_)
    R = 120
    cx, cy = 820, 250
    circ = place(circle(0, 0, R), 1, cx, cy)
    tot_h = P_.X + P_.dotGap + P_.dotD
    sm = (R * 1.05) / tot_h
    ox = cx - mw * sm / 2
    oy = cy + tot_h * sm / 2
    ink.add(circ, EMERALD)
    add_word(ink, mp, [md], sm, ox, oy, IVORY, GOLD_LT)
    # tiny favicon at 32 px and 16 px drawn true size
    for size, x in [(32, 760), (16, 820)]:
        fc = place(rect(0, 0, size, size), 1, x, 520 + size)
        ink.add(fc, EMERALD)
        sf = size * 0.78 / tot_h
        add_word(ink, mp, [md], sf, x + size / 2 - mw * sf / 2, 520 + size - size * 0.11, IVORY, GOLD_LT)
    body = ink.body()
    body += f'<text x="50" y="{ch-24}" font-family="sans-serif" font-size="17" fill="#6b6b5e">{code} — {label}</text>'
    return svg_doc(cw, ch, body, bg=IVORY)


if __name__ == '__main__':
    files = []
    for code, label, kw in VARS:
        f = f'explore/{code}.svg'
        open(f, 'w').write(cell(code, label, kw))
        files.append(f)
    subprocess.run(['node', '../toolkit/render.js', 'sheet', 'explore.png'] + files, check=True)
