"""explore.png: the genuinely different topologies tried before choosing a direction."""
import sys, json, math; sys.path.insert(0, '.')
from kolam import *
from ropev import rope_v
E1 = json.load(open('enum.json')); E2 = json.load(open('enum2.json'))
D5 = {'L2': (-1, 2), 'L1': (-0.5, 1), 'B': (0, 0), 'R1': (0.5, 1), 'R2': (1, 2)}
D3 = {'L2': (-1, 2), 'B': (0, 0), 'R2': (1, 2)}
D4 = {k: tuple(v) for k, v in E2['D4'].items()}; D6 = {k: tuple(v) for k, v in E2['D6'].items()}
def seqv(D, seq, r): return [(D[a], r, s) for a, s in seq]
it1 = [s for s in E1['d3']] + [s for s in E1['d5']]
it2 = E2['d4'] + E2['d6']
cells = []
# 1 rope-5 (proper sikku rope bent into V)
Dr, rad, vis, rb = rope_v(beta_deg=26, d=(0.55, 1.4), r=(0.25, 0.22, 0.30))
cells.append(('01 Sikku rope, 5 pulli', vis, list(Dr.values()), False))
# 2 capsule V
cells.append(('02 Twin capsules + drop', seqv(D5, E1['d5'][8 - 4], 0.34) if False else seqv(D5, it1[8][0:] if False else it1[8], 0.34), list(D5.values()), False))
# 3 antler skip-under
cells.append(('03 Skip-under (antler)', seqv(D5, it1[33], 0.34), list(D5.values()), False))
# 4 45deg classic lattice
Dc = {'L2': (-2, 2), 'L1': (-1, 1), 'B': (0, 0), 'R1': (1, 1), 'R2': (2, 2)}
cells.append(('04 Square-lattice rope 90deg', seqv(Dc, [('L2',1),('L1',-1),('B',1),('R1',-1),('R2',1),('R1',-1),('B',1),('L1',-1)], 0.5), list(Dc.values()), False))
# 5 pretzel 3-dot
cells.append(('05 Pretzel, 3 pulli', seqv(D3, it1[1], 0.38), list(D3.values()), False))
# 6 inner cup
cells.append(('06 V with inner cup', seqv(D6, it2[11 + 59 - 11], 0.27), list(D6.values()), False))
# 7 fishtail
cells.append(('07 Fish-tail vertex', seqv(D6, it2[71], 0.27), list(D6.values()), False))
# 8 double crossing ribbon
cells.append(('08 Two crossings, 6 pulli', seqv(D6, it2[12], 0.27), list(D6.values()), False))
# 9 crotch loop (chosen)
cells.append(('09 Crotch loop, 4 pulli  (chosen)', seqv(D4, it2[2], 0.3), list(D4.values()), True))
# 10 ring Y
cells.append(('10 Hanging ring', seqv(D6, it2[19], 0.27), list(D6.values()), False))
# 11 trefoil
cells.append(('11 Top-bar triangle', seqv(D5, it1[7], 0.34), list(D5.values()), False))
# 12 3-dot crossing at centre
cells.append(('12 Crossed lasso', seqv(D3, it1[1 - 1], 0.38) if False else seqv(D4, it2[0], 0.3), list(D4.values()), False))
W = 300; cols = 4; body = ''
for i, (name, vis, dots, chosen) in enumerate(cells):
    segs = build(vis)
    line = outline(segs, 0.08)
    dp = dots_path(dots, 0.085)
    s, tx, ty = fit(vtype.union(line, dp), (W, W), 0.12)
    cx, cy = (i % cols) * (W + 12) + 12, (i // cols) * (W + 40) + 60
    stroke = '#A8843A' if chosen else '#d8d2c4'
    body += f'<g transform="translate({cx},{cy})"><rect width="{W}" height="{W}" fill="#F6F1E7" stroke="{stroke}" stroke-width="{4 if chosen else 1}"/>'
    body += f'<path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="#0B2A20"/><path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="#A8843A"/>'
    body += f'<text x="2" y="{W+22}" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#0B2A20">{name}</text></g>'
rows = (len(cells) + cols - 1) // cols
H = rows * (W + 40) + 80
head = ('<text x="12" y="34" font-family="Helvetica, Arial, sans-serif" font-size="20" fill="#0B2A20">'
        'Kolam Line: exploration. One closed line, true arcs around pulli + straight tangents. '
        '125 symmetric topologies enumerated; 12 shown.</text>')
open('explore.svg', 'w').write(vtype.svg_doc(cols * (W + 12) + 12, H, head + body, bg='#ffffff'))
