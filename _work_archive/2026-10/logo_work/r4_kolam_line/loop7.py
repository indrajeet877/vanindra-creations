import sys, math; sys.path.insert(0, '.')
from mark import *
EM, IV, AG, SG = '#0B2A20', '#F6F1E7', '#A8843A', '#D2B26A'
def geo(grid, spec, r, w, rd, use=None):
    visits = [(grid[a], r if not isinstance(r, dict) else r[a], s) for a, s in spec]
    segs = build(visits)
    line = outline(segs, w)
    dp = dots_path([grid[k] for k in (use or grid)], rd)
    return line, dp
G6 = {'L2': (-1, 1), 'L1': (-0.5, 0), 'C': (0, -0.1), 'B': (0, -1), 'R1': (0.5, 0), 'R2': (1, 1)}
V = []
V.append(('A current 4 pulli, gold', *geo(GRID, [('L',1),('B',1),('R',1),('C',1)], 0.30, 0.13, 0.10), SG, AG))
V.append(('B 4 pulli = line weight, same colour', *geo(GRID, [('L',1),('B',1),('R',1),('C',1)], 0.30, 0.13, 0.075), IV, EM))
# 6-pulli two-crossing (08): L2+ L1+ B- R1+ R2+ C+  on a 3x4-ish lattice
G6b = {'L2': (-1.0, 2.0), 'L1': (-0.5, 1.0), 'C': (0.0, 0.85), 'B': (0.0, -0.3), 'R1': (0.5, 1.0), 'R2': (1.0, 2.0)}
V.append(('C two crossings, 6 pulli', *geo(G6b, [('L2',1),('L1',1),('B',-1),('R1',1),('R2',1),('C',1)], 0.27, 0.11, 0.075), SG, AG))
# 6-pulli crotch loop (#11): L2+ L1+ B+ R1+ R2+ C+
G6c = {'L2': (-1.0, 2.0), 'L1': (-0.5, 1.0), 'C': (0.0, 0.9), 'B': (0.0, 0.0), 'R1': (0.5, 1.0), 'R2': (1.0, 2.0)}
V.append(('D crotch loop, 6 pulli', *geo(G6c, [('L2',1),('L1',1),('B',1),('R1',1),('R2',1),('C',1)], 0.27, 0.11, 0.075), SG, AG))
G34 = {'L': (-1.0, 2.0), 'R': (1.0, 2.0), 'C': (0.0, 0.0), 'B': (0.0, -1.0)}
V.append(('E 3x4 tall', *geo(G34, [('L',1),('B',1),('R',1),('C',1)], 0.30, 0.13, 0.085), SG, AG))
V.append(('F 4 pulli, C pulli only gold', *geo(GRID, [('L',1),('B',1),('R',1),('C',1)], 0.30, 0.13, 0.075), SG, AG))
body = ''
for i, (name, line, dp, dc_dark, dc_light) in enumerate(V):
    allp = vtype.union(line, dp)
    y = i * 210
    s, tx, ty = fit(allp, (190, 190), 0.1)
    if name.startswith('F'):
        cdot = dots_path([GRID['C']], 0.075); others = dots_path([GRID[k] for k in 'LRB'], 0.075)
        body += f'<g transform="translate(10,{y+10})"><rect width="190" height="190" fill="{IV}"/><path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="{EM}"/><path d="{vtype.to_d(tf(others, s, tx, ty))}" fill="{EM}"/><path d="{vtype.to_d(tf(cdot, s, tx, ty))}" fill="{AG}"/></g>'
        body += f'<g transform="translate(210,{y+10})"><rect width="190" height="190" fill="{EM}"/><path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="{IV}"/><path d="{vtype.to_d(tf(others, s, tx, ty))}" fill="{IV}"/><path d="{vtype.to_d(tf(cdot, s, tx, ty))}" fill="{SG}"/></g>'
    else:
        body += f'<g transform="translate(10,{y+10})"><rect width="190" height="190" fill="{IV}"/><path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="{EM}"/><path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="{dc_light}"/></g>'
        body += f'<g transform="translate(210,{y+10})"><rect width="190" height="190" fill="{EM}"/><path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="{IV}"/><path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="{dc_dark}"/></g>'
    s2, tx2, ty2 = fit(allp, (110, 110), 0.22)
    body += f'<g transform="translate(420,{y+50})"><circle cx="55" cy="55" r="55" fill="{EM}"/><path d="{vtype.to_d(tf(line, s2, tx2, ty2))}" fill="{IV}"/><path d="{vtype.to_d(tf(dp, s2, tx2, ty2))}" fill="{dc_dark}"/></g>'
    body += f'<text x="550" y="{y+110}" font-family="sans-serif" font-size="15">{name}</text>'
open('work/loop7.svg', 'w').write(vtype.svg_doc(860, len(V) * 210 + 10, body, bg='#fff'))
