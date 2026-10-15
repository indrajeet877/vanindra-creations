import sys, json; sys.path.insert(0, '.')
from kolam import *
E = json.load(open('enum2.json'))
D4 = {k: tuple(v) for k, v in E['D4'].items()}; D6 = {k: tuple(v) for k, v in E['D6'].items()}
items = [(D4, 0.3, s) for s in E['d4']] + [(D6, 0.27, s) for s in E['d6']]
picks = [int(x) for x in sys.argv[1].split(',')]
W = 360; cols = 4; body = ''
for j, i in enumerate(picks):
    D, r, seq = items[i]
    print(i, ' '.join(a + ('+' if d > 0 else '-') for a, d in seq))
    segs = build([(D[a], r, s) for a, s in seq])
    line = outline(segs, 0.07)
    dp = dots_path(list(D.values()), 0.075)
    s, tx, ty = fit(vtype.union(line, dp), (W, W), 0.08)
    cx, cy = (j % cols) * W, (j // cols) * (W + 24)
    body += f'<g transform="translate({cx},{cy})"><rect width="{W}" height="{W}" fill="#F6F1E7" stroke="#ccc"/>'
    body += f'<path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="#0B2A20"/><path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="#A8843A"/>'
    body += f'<text x="6" y="{W+16}" font-family="sans-serif" font-size="13">#{i}</text></g>'
rows = (len(picks) + cols - 1) // cols
open('pick2.svg', 'w').write(vtype.svg_doc(cols * W, rows * (W + 24), body, bg='#fff'))
