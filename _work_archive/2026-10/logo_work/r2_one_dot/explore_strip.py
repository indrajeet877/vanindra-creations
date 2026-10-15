"""Avatar candidates strip for explore.png (10 candidates, early exploration)."""
import sys, subprocess
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/r2_one_dot')
from comp import *
from explore import derive
from marks_explore import KW, m_ni, m_ndot, m_nin, m_hindi_ni, m_word, m_i, fit
from marks_explore2 import m_line_dot, m_line_i, m_kamaan, m_two_line, SMALL
C = [('A1 ni', m_ni, KW, False), ('A2 n + dot', m_ndot, KW, False), ('A3 nin crop', m_nin, SMALL, True),
     ('A4 ni-Hindi', m_hindi_ni, SMALL, False), ('A5 wordmark', m_word, KW, False), ('A6 i', m_i, KW, False),
     ('A7 line + dot', m_line_dot, SMALL, False), ('A8 line + i', m_line_i, SMALL, False),
     ('A9 i-matra + dot', m_kamaan, SMALL, False), ('A10 van/indra', m_two_line, KW, False)]
ink = Ink(); lab = ''
x = 20
for name, fn, kw, crop in C:
    P_ = derive(P(**kw))
    path, dots = fn(P_)
    size = 120
    ink.add(place(circle(0, 0, size / 2), 1, x + size / 2, 20 + size / 2), EMERALD)
    fillf = 0.98 if crop else (0.86 if 'word' in name or 'van/' in name else 0.60)
    s, cx, cy = fit(path, dots, size, fillf, crop=crop)
    if crop:
        cx = dots[0].bounds[0] / 2 + dots[0].bounds[2] / 2
    cl = circle(cx, cy, (size / 2) / s)
    add_word(ink, intersection(path, cl), [intersection(d, cl) for d in dots], s, x + size / 2 - cx * s, 20 + size / 2 + cy * s, IVORY, GOLD_LT)
    # 32 px version below
    sm = 32
    ink.add(place(circle(0, 0, sm / 2), 1, x + size / 2, 170 + sm / 2), EMERALD)
    s2, cx2, cy2 = fit(path, dots, sm, fillf, crop=crop)
    if crop:
        cx2 = cx
    cl2 = circle(cx2, cy2, (sm / 2) / s2)
    add_word(ink, intersection(path, cl2), [intersection(d, cl2) for d in dots], s2, x + size / 2 - cx2 * s2, 170 + sm / 2 + cy2 * s2, IVORY, GOLD_LT)
    lab += f'<text x="{x + size/2}" y="232" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#444">{name.split(" ",1)[0]}</text>'
    lab += f'<text x="{x + size/2}" y="248" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#777">{name.split(" ",1)[1]}</text>'
    x += size + 26
head = '<text x="20" y="290" font-family="sans-serif" font-size="14" fill="#444">Avatar exploration (no V): A1 "ni" chosen for global use; A4 is the Hindi-audience alternate. A3/A9 too abstract at 32 px, A5/A10 illegible at 32 px, A6 reads as an info icon, A7/A8 read as a minus sign / letter T.</text>'
svg = svg_doc(x + 10, 310, ink.body() + lab + head, bg=IVORY)
open('work/strip.svg', 'w').write(svg)
subprocess.run(['node', '../toolkit/render.js', 'png', 'work/strip.svg', 'work/strip.png', str(int(x + 10))], check=True)
