"""F1 polish: mark_small drawn on the 16 px grid (judge: 'mark_small at 16 px is not pixel-fitted').
Every horizontal and vertical edge lands on a whole pixel at 16 px, and so also at 32, 48 and 64 px:
line 2 px, danda 2 px, one empty row under the line, the loop's top stroke exactly one full row, and the loop
leaves the danda on a whole row. Only the curves (shoulder, arm, point, return stroke) are anti-aliased.
Coordinates are in pixels of a 16 x 16 canvas."""
from r3geo import *
from r4mark import va_vloop

GRID_PX = 14            # the mark's height (line top to danda foot) in px at 16 px
G = 100.0 / GRID_PX     # va_vloop units per pixel

SMALL16 = dict(b=2 * G, S=2 * G, jt=3 * G, ht=1 * G, h=1.7 * G, yj=8 / GRID_PX,
               K=(-2.0, 43.0), ks=(34.0, 15.0), Ki=(17.0, 47.0), kis=(25.0, 12.0),
               karm=(12.0, 0.6), kiarm=(12.0, -1.0), P=(31.0, 97.0), ovr=1 * G)


def small16(px=16, top=1, left=None, **kw):
    """Returns the mark as a path in px of a px x px canvas (px must be 16; scale the SVG for 32/48/64)."""
    p = dict(SMALL16); p.update(kw)
    # make the left overhang end on a whole pixel: xs - xL = n px
    g0, info0 = va_vloop(**dict(p, ovl=0.0))
    span = 58.0 - info0['xmin']
    n = math.ceil(span / G + 0.55)
    p['ovl'] = n * G - span
    g, info = va_vloop(**p)
    s = 1.0 / G
    w_px = (info['x1'] - info['xL']) * s
    if left is None:
        left = round((px - w_px) / 2 + 0.25)
    return tr(g, s, left - info['xL'] * s, top), info, (left, w_px)
