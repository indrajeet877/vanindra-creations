import sys, json; sys.path.insert(0, '.')
from kolam import *
E = json.load(open('enum.json'))
D5 = {'L2': (-1, 2), 'L1': (-0.5, 1), 'B': (0, 0), 'R1': (0.5, 1), 'R2': (1, 2)}
picks = [int(x) for x in sys.argv[1].split(',')]
items = [('d3', s) for s in E['d3']] + [('d5', s) for s in E['d5']]
W = 360; cols = 4; body = ''
for j, i in enumerate(picks):
    k, seq = items[i]
    segs = build([(D5[a], 0.34, s) for a, s in seq])
    line = outline(segs, 0.075)
    dp = dots_path(list(D5.values()), 0.085)
    s, tx, ty = fit(vtype.union(line, dp), (W, W), 0.08)
    cx, cy = (j % cols) * W, (j // cols) * (W + 24)
    body += f'<g transform="translate({cx},{cy})"><rect width="{W}" height="{W}" fill="#F6F1E7" stroke="#ccc"/>'
    body += f'<path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="#0B2A20"/><path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="#A8843A"/>'
    body += f'<text x="6" y="{W+16}" font-family="sans-serif" font-size="13">#{i}</text></g>'
rows = (len(picks) + cols - 1) // cols
open('pick.svg', 'w').write(vtype.svg_doc(cols * W, rows * (W + 24), body, bg='#fff'))
