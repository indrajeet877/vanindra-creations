import sys; sys.path.insert(0, '.')
from mark import *
C = [('Sa', dict(r=0.30, w=0.20, rd=0.10), 'LRCB'),
     ('Sb', dict(r=0.32, w=0.24, rd=0.12), 'C'),
     ('Sc', dict(r=0.32, w=0.26, rd=0.10), ''),
     ('Sd', dict(r=0.36, w=0.26, rd=0.13), 'C'),
     ('Se', dict(r=0.36, w=0.24, rd=0.11), 'CB'),
     ('Sf', dict(r=0.40, w=0.28, rd=0.15), 'C')]
for name, kw, use in C:
    segs, line, _ = mark_geo(**kw)
    parts = [line]
    if use:
        parts.append(dots_path([GRID[k] for k in use], kw['rd']))
    allp = vtype.union(*parts)
    x0, y0, x1, y1 = vtype.bounds(allp)
    side = max(x1 - x0, y1 - y0) * 1.06
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    vb = f'{cx - side/2:.4f} {cy - side/2:.4f} {side:.4f} {side:.4f}'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><path d="{vtype.to_d(allp)}" fill="#0B2A20"/></svg>'
    open(f'small/{name}.svg', 'w').write(svg)
