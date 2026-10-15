import math, sys
sys.path.insert(0, '.')
from kolam import *

S3 = math.sqrt(3)
def V5(slope_dx=0.5, h=1.0):
    # five dots in a V: TL, L1, B, R1, TR (y up)
    return {'TL': (-2*slope_dx, 2*h), 'L1': (-slope_dx, h), 'B': (0, 0), 'R1': (slope_dx, h), 'TR': (2*slope_dx, 2*h)}

def rope(names, D, r, first=+1):
    seq = []
    s = first
    fwd = names
    for n in fwd:
        seq.append((D[n], r, s)); s = -s
    # come back along interior dots (exclude ends)
    for n in reversed(fwd[1:-1]):
        seq.append((D[n], r, s)); s = -s
    return seq

variants = []
# A rope over 3 dots, slope 2
D3 = {'TL': (-1, 2), 'B': (0, 0), 'TR': (1, 2)}
variants.append(('A rope-3 slope2', rope(['TL', 'B', 'TR'], D3, 0.42), D3, None))
# B rope-5 on 60deg lattice
D = V5(0.5, S3/2)
variants.append(('B rope-5 60deg', rope(['TL','L1','B','R1','TR'], D, 0.36), D, None))
# C rope-5 square lattice 90deg
D = V5(1.0, 1.0)
variants.append(('C rope-5 45deg lattice', rope(['TL','L1','B','R1','TR'], D, 0.5), D, None))
# D two petals with pivot
Dp = {'TL': (-1, 2.2), 'TR': (1, 2.2), 'P': (0, 0)}
seq = [(Dp['TL'], 0.42, -1), (Dp['P'], 0.42, +1), (Dp['TR'], 0.42, +1), (Dp['P'], 0.42, -1)]
variants.append(('D petals (pivot dot)', seq, Dp, None))
# E trefoil V
Dt = {'TL': (-1, 2), 'B': (0, 0), 'TR': (1, 2)}
seq = [(Dt['TL'], 0.5, -1), (Dt['B'], 0.5, +1), (Dt['TR'], 0.5, -1)]
variants.append(('E trefoil 3 crossings', seq, Dt, None))
# F rope-5 slope-2 lattice
D = V5(0.5, 1.0)
variants.append(('F rope-5 slope2', rope(['TL','L1','B','R1','TR'], D, 0.40), D, None))
# G petals with 4 dots: pivot dot + arms of 2
Dg = {'TL': (-1.2, 2.4), 'L1': (-0.6, 1.2), 'P': (0, 0), 'R1': (0.6, 1.2), 'TR': (1.2, 2.4)}
seq = [(Dg['TL'], 0.4, -1), (Dg['L1'], 0.4, +1), (Dg['P'], 0.4, -1), (Dg['R1'], 0.4, +1), (Dg['TR'], 0.4, -1),
       (Dg['R1'], 0.4, +1), (Dg['P'], 0.4, -1), (Dg['L1'], 0.4, +1)]
variants.append(('G rope-5 opposite phase', seq, Dg, None))
# H 3x3 grid: V-dots rope + side loops
G = {(i, j): (i, j) for i in (-1, 0, 1) for j in (-1, 0, 1)}
seq = [(G[(-1, 1)], 0.3, +1), (G[(-1, 0)], 0.3, -1), (G[(0, -1)], 0.3, +1), (G[(1, 0)], 0.3, -1), (G[(1, 1)], 0.3, +1),
       (G[(0, 0)], 0.3, -1), (G[(0, 1)], 0.3, +1), (G[(0, 0)], 0.3, -1)]
variants.append(('H 3x3 partial weave', seq, {k: v for k, v in G.items() if k in [(-1,1),(-1,0),(0,-1),(1,0),(1,1),(0,0),(0,1)]}, None))
# I diamond-lattice 3 dots wide-turn (B gets a loop)
D3b = {'TL': (-1, 2), 'B': (0, 0), 'TR': (1, 2)}
seq = [(D3b['TL'], 0.4, +1), (D3b['B'], 0.4, -1), (D3b['TR'], 0.4, +1), (D3b['B'], 0.55, -1)]
variants.append(('I rope-3 double-ring vertex', seq, D3b, None))
# J petals, no pivot dot shown, crossing high
Dj = {'TL': (-0.9, 2.3), 'TR': (0.9, 2.3)}
seq = [(Dj['TL'], 0.45, -1), ((0, 0), 0.3, +1), (Dj['TR'], 0.45, +1), ((0, 0), 0.3, -1)]
variants.append(('J petals, hidden pivot', seq, Dj, None))
# K 3-2-1 triangle kolam: rope over V + top centre loop
Dk = {'TL': (-1, 2), 'TC': (0, 2), 'TR': (1, 2), 'L1': (-0.5, 1), 'R1': (0.5, 1), 'B': (0, 0)}
seq = [(Dk['TL'], 0.36, +1), (Dk['L1'], 0.36, -1), (Dk['B'], 0.36, +1), (Dk['R1'], 0.36, -1), (Dk['TR'], 0.36, +1),
       (Dk['TC'], 0.36, -1)]
variants.append(('K 3-2-1 ring', seq, Dk, None))
# L rope-4 per arm (7 dots) slope 2
D7 = {'T3L': (-1.5, 3), 'T2L': (-1, 2), 'T1L': (-0.5, 1), 'B': (0, 0), 'T1R': (0.5, 1), 'T2R': (1, 2), 'T3R': (1.5, 3)}
variants.append(('L rope-7 slope2', rope(['T3L','T2L','T1L','B','T1R','T2R','T3R'], D7, 0.4), D7, None))

cells = []
W = 300
body = ''
cols = 4
for idx, (name, seq, dots, loops) in enumerate(variants):
    try:
        segs = build(seq, loops)
    except Exception as e:
        print(name, 'fail', e); continue
    w = 0.10
    line = outline(segs, w)
    dp = dots_path(list(dots.values()), 0.11)
    allp = vtype.union(line, dp)
    s, tx, ty = fit(allp, (W, W), 0.14)
    cx, cy = (idx % cols) * W, (idx // cols) * (W + 30)
    body += f'<g transform="translate({cx},{cy})"><rect width="{W}" height="{W}" fill="#F6F1E7" stroke="#ccc"/>'
    body += f'<path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="#0B2A20"/>'
    body += f'<path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="#A8843A"/>'
    body += f'<text x="8" y="{W+20}" font-family="sans-serif" font-size="14">{name}</text></g>'
rows = (len(variants) + cols - 1) // cols
open('explore0.svg', 'w').write(vtype.svg_doc(cols * W, rows * (W + 30), body, bg='#ffffff'))
print('done', len(variants))
