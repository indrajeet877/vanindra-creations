import sys, math; sys.path.insert(0, '.')
from mark import mark_geo, GRID
from letters import *

R_PULLI = 0.30
def kolam_v(height, stroke_abs, rd_rel=0.085, r=R_PULLI, dots=True, grid=GRID):
    """Mark scaled so its outer height == height; line weight == stroke_abs (absolute units).
    Returns (line, dots, width) positioned with bottom outer point at y=0 (baseline) in SVG coords, left at x=0."""
    total = 2 + 2 * r          # centre-line extent; outer extent adds w
    # solve unit so that unit*(total + w_rel) = height, w_rel = stroke_abs/unit
    unit = (height - stroke_abs) / total
    w_rel = stroke_abs / unit
    segs, line, dp = mark_geo(r=r, w=w_rel, rd=rd_rel, grid=grid)
    x0, y0, x1, y1 = vtype.bounds(line)
    T = lambda p: vtype.transform(p, unit, 0, 0, unit, -x0 * unit, -y1 * unit)
    return T(line), (T(dp) if dots else None), (x1 - x0) * unit, unit

def h_gap_at(pathA, pathB, ys):
    """min horizontal gap between right edge of A and left edge of B sampled at SVG y values."""
    gaps = []
    for y in ys:
        ra = edge_x(pathA, y, 'right'); lb = edge_x(pathB, y, 'left')
        if ra is not None and lb is not None:
            gaps.append(lb - ra)
    return min(gaps) if gaps else None

def edge_x(path, y, side):
    # sample by intersecting with a thin horizontal band
    band = pathops.Path(); band.moveTo(-1e5, y - 0.25); band.lineTo(1e5, y - 0.25); band.lineTo(1e5, y + 0.25); band.lineTo(-1e5, y + 0.25); band.close()
    I = vtype.intersection(path, band)
    try:
        x0, _, x1, _ = vtype.bounds(I)
    except Exception:
        return None
    if x1 - x0 <= 0: return None
    return x1 if side == 'right' else x0

def lockup_inline(S, text='anindra', vh=None, gap=None, tracking=0.02, dots=True):
    vh = vh or (S.asc + S.ov)
    line, dp, vw, unit = kolam_v(vh, S.s, dots=dots)
    V = vtype.union(line, dp) if dots else line
    word_p, ww = word(text, S, tracking=tracking)
    # place word: find x so that horizontal gap between V and first letter at mid x-height ~= gap
    gap = gap if gap is not None else 0.13 * S.X
    ys = [-S.X * f for f in (0.15, 0.35, 0.5, 0.65, 0.85)]
    lo, hi = -vw, vw * 2
    for _ in range(40):
        mid = (lo + hi) / 2
        wp = vtype.transform(word_p, 1, 0, 0, 1, mid, 0)
        g = h_gap_at(V, wp, ys)
        if g is None or g < gap: lo = mid
        else: hi = mid
    wp = vtype.transform(word_p, 1, 0, 0, 1, hi, 0)
    return line, dp, wp, hi + ww

if __name__ == '__main__':
    body = ''; y = 0
    for s in (9.0, 11.0):
        S = Spec(s=s)
        line, dp, wp, W = lockup_inline(S)
        body += f'<g transform="translate(40,{y + 200})"><path d="{vtype.to_d(line)}" fill="#0B2A20"/><path d="{vtype.to_d(dp)}" fill="#0B2A20"/><path d="{vtype.to_d(wp)}" fill="#0B2A20"/></g>'
        y += 230
        line, dp, wp, W = lockup_inline(S, text='anindra creations')
        body += f'<g transform="translate(40,{y + 200})"><path d="{vtype.to_d(line)}" fill="#0B2A20"/><path d="{vtype.to_d(dp)}" fill="#A8843A"/><path d="{vtype.to_d(wp)}" fill="#0B2A20"/></g>'
        y += 230
    open('loop4_lockups.svg', 'w').write(vtype.svg_doc(1500, y + 30, body, bg='#F6F1E7'))
