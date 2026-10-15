import sys, math; sys.path.insert(0, '.')
from mark import *
EM, IV, AG = '#0B2A20', '#F6F1E7', '#A8843A'
r, w, rd = 0.30, 0.13, 0.08
segs, line, _ = mark_geo(r=r, w=w, rd=rd)
SC, OX, OY = 260.0, 500.0, 470.0
T = lambda x, y: (OX + x * SC, OY - y * SC)
body = ''
# full 3x3 pulli grid (faint) + grid lines
for i in (-1, 0, 1):
    for j in (-1, 0, 1):
        x, y = T(i, j)
        used = (i, j) in [(-1, 1), (1, 1), (0, 0), (0, -1)]
        body += f'<circle cx="{x}" cy="{y}" r="{rd*SC:.1f}" fill="{EM if used else "#c9c1ae"}"/>'
for i in (-1, 0, 1):
    x0, y0 = T(i, 1.6); x1, y1 = T(i, -1.6)
    body += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#d9d1bf" stroke-width="1"/>'
    x0, y0 = T(-1.6, i); x1, y1 = T(1.6, i)
    body += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#d9d1bf" stroke-width="1"/>'
# construction circles (radius r) around the 4 pulli
for (cx, cy) in GRID.values():
    x, y = T(cx, cy)
    body += f'<circle cx="{x}" cy="{y}" r="{r*SC}" fill="none" stroke="{AG}" stroke-width="1.2" stroke-dasharray="4 4"/>'
# axes L-B, B-R (slope 2) and R-C, C-L (45 deg)
for a, b in (('L', 'B'), ('B', 'R'), ('R', 'C'), ('C', 'L')):
    (x0, y0), (x1, y1) = T(*GRID[a]), T(*GRID[b])
    body += f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{AG}" stroke-width="1" opacity=".7"/>'
# the line itself (centre-line, thin) and outline
ol = vtype.transform(line, SC, 0, 0, SC, OX, OY)
body += f'<path d="{vtype.to_d(ol)}" fill="{EM}" opacity=".88"/>'
xc, yc = T(0, r * math.sqrt(2))
body += f'<circle cx="{xc}" cy="{yc}" r="5" fill="none" stroke="#b33" stroke-width="1.5"/>'
txt = [('3x3 pulli grid; the line wraps four of them: two top corners, centre, bottom-middle', 40, 900),
       ('One radius r = 0.30 for every arc, each concentric with its pulli. One stroke.', 40, 925),
       ('Outer edges: tangents L-B, B-R (2:1 knight move, V = 53.13 deg). Inner strands: tangents R-C, C-L at 45 deg.', 40, 950),
       ('They cross at 90 deg at (0, r*sqrt2) (red ring). Arcs: caps 161.57 deg, vertex 126.87 deg, loop 270 deg.', 40, 975),
       ('Bounding box is exactly square: 2 + 2r + w in both directions.', 40, 1000)]
for t, x, y in txt:
    body += f'<text x="{x}" y="{y}" font-family="Helvetica, Arial, sans-serif" font-size="17" fill="{EM}">{t}</text>'
open('construction.svg', 'w').write(vtype.svg_doc(1000, 1030, body, bg=IV, title='Kolam Line construction'))
