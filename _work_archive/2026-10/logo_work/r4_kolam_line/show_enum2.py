import sys, json; sys.path.insert(0, '.')
from kolam import *
E = json.load(open('enum2.json'))
D4 = {k: tuple(v) for k, v in E['D4'].items()}; D6 = {k: tuple(v) for k, v in E['D6'].items()}
items = [(D4, 0.3, s) for s in E['d4']] + [(D6, 0.27, s) for s in E['d6']]
W = 160; cols = 10; body = ''
for i, (D, r, seq) in enumerate(items):
    segs = build([(D[a], r, s) for a, s in seq])
    line = outline(segs, 0.08)
    dp = dots_path(list(D.values()), 0.08)
    s, tx, ty = fit(vtype.union(line, dp), (W, W), 0.08)
    cx, cy = (i % cols) * W, (i // cols) * (W + 16)
    body += f'<g transform="translate({cx},{cy})"><rect width="{W}" height="{W}" fill="#F6F1E7" stroke="#ccc"/>'
    body += f'<path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="#0B2A20"/><path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="#A8843A"/>'
    body += f'<text x="4" y="{W+12}" font-family="sans-serif" font-size="11">#{i}</text></g>'
rows = (len(items) + cols - 1) // cols
open('enum2_sheet.svg', 'w').write(vtype.svg_doc(cols * W, rows * (W + 16), body, bg='#fff'))
