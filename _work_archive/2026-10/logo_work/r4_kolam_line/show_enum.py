import sys, json; sys.path.insert(0, '.')
from kolam import *
E = json.load(open('enum.json'))
D3 = {'L2': (-1, 2), 'B': (0, 0), 'R2': (1, 2)}
D5 = {'L2': (-1, 2), 'L1': (-0.5, 1), 'B': (0, 0), 'R1': (0.5, 1), 'R2': (1, 2)}
items = [('d3', D3, 0.38, s) for s in E['d3']] + [('d5', D5, 0.34, s) for s in E['d5']]
W = 180; cols = 8; body = ''
for i, (k, D, r, seq) in enumerate(items):
    segs = build([(D[a], r, s) for a, s in seq])
    line = outline(segs, 0.09)
    dp = dots_path(list(D.values()), 0.1)
    s, tx, ty = fit(vtype.union(line, dp), (W, W), 0.1)
    cx, cy = (i % cols) * W, (i // cols) * (W + 36)
    lab = ' '.join(a + ('+' if d > 0 else '-') for a, d in seq)
    body += f'<g transform="translate({cx},{cy})"><rect width="{W}" height="{W}" fill="#F6F1E7" stroke="#ccc"/>'
    body += f'<path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="#0B2A20"/><path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="#A8843A"/>'
    body += f'<text x="4" y="{W+14}" font-family="sans-serif" font-size="10">#{i} {lab[:34]}</text><text x="4" y="{W+28}" font-family="sans-serif" font-size="10">{lab[34:]}</text></g>'
rows = (len(items) + cols - 1) // cols
open('enum_sheet.svg', 'w').write(vtype.svg_doc(cols * W, rows * (W + 36), body, bg='#fff'))
