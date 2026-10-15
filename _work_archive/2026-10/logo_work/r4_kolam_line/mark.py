"""The Kolam Line mark: one closed line on a 3x3 pulli grid.
Pulli (y up): L=(-1,1), R=(1,1) top corners; C=(0,0) centre; B=(0,-1) bottom-middle.
Visit order L(ccw) -> B(ccw) -> R(ccw) -> C(ccw): outer edges are tangents L-B / B-R (slope 2),
inner strands are tangents R-C / C-L (exactly 45 deg), crossing at 90 deg at (0, r*sqrt2)."""
import math, sys
sys.path.insert(0, '.')
from kolam import *

GRID = {'L': (-1.0, 1.0), 'R': (1.0, 1.0), 'C': (0.0, 0.0), 'B': (0.0, -1.0)}

def mark_geo(r=0.34, w=0.12, rd=0.11, rC=None, rB=None, rCap=None, dots=True, grid=GRID):
    rC = rC or r; rB = rB or r; rCap = rCap or r
    visits = [(grid['L'], rCap, +1), (grid['B'], rB, +1), (grid['R'], rCap, +1), (grid['C'], rC, +1)]
    segs = build(visits)
    line = outline(segs, w)
    dp = dots_path(list(grid.values()), rd) if dots else None
    return segs, line, dp

def info(segs):
    out = []
    for s in segs:
        if s[0] == 'A':
            out.append('arc r=%.3f span=%.1f' % (s[2], math.degrees(s[4])))
    return out

if __name__ == '__main__':
    print(info(mark_geo()[0]))
    W = 300; body = ''
    combos = []
    for r in (0.30, 0.35, 0.40):
        for w, rd in ((0.10, 0.10), (0.14, 0.11), (0.18, 0.12)):
            combos.append((r, w, rd))
    cols = 3
    for i, (r, w, rd) in enumerate(combos):
        segs, line, dp = mark_geo(r, w, rd)
        allp = vtype.union(line, dp)
        s, tx, ty = fit(allp, (W, W), 0.14)
        cx, cy = (i % cols) * (W + 10), (i // cols) * (W + 26)
        body += f'<g transform="translate({cx},{cy})"><rect width="{W}" height="{W}" fill="#F6F1E7"/>'
        body += f'<path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="#0B2A20"/><path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="#0B2A20"/>'
        # small previews 16/24/32/48
        x = 8
        for px in (16, 24, 32, 48):
            ss, stx, sty = fit(allp, (px, px), 0.06)
            body += f'<g transform="translate({x},{W - px - 8})"><path d="{vtype.to_d(tf(allp, ss, stx, sty))}" fill="#0B2A20"/></g>'
            x += px + 8
        body += f'<text x="4" y="{W+18}" font-family="sans-serif" font-size="13">r={r} w={w} rd={rd}</text></g>'
    rows = (len(combos) + cols - 1) // cols
    open('loop1_params.svg', 'w').write(vtype.svg_doc(cols * (W + 10), rows * (W + 26), body, bg='#fff'))
