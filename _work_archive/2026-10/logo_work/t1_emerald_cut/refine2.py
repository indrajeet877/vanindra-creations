"""Refinement loop 2: give the two-stone V an unmistakable emerald-cut identity without bevels."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
import explore
import vgem2
from explore5 import gem_seams

explore.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refine')


def table_line(kw, seam=1.4, inset=6.0):
    parts, g = vgem2.build(facets=False, **kw)
    left = g['left']
    t = vgem2.inset_convex(left, inset)
    line = polyline(t + [t[0]])
    parts[0] = (cut(parts[0][0], [line], seam), 'A')
    return parts


R = [
    ('r2a_perp_equalclips', lambda: vgem2.build(top='p', thin_top='p', chO=8, chI=8, chT=4.5, facets=False, seam=2.0)[0]),
    ('r2b_h_45', lambda: vgem2.build(top='h', thin_top='h', chO=12, chI=3, chT=5, facets=False, seam=2.0)[0]),
    ('r2c_perp_tableline', lambda: table_line(dict(top='p', thin_top='p', chO=8, chI=8, chT=4.5, seam=2.0))),
    ('r2d_perp_hairfacets', lambda: vgem2.build(top='p', thin_top='p', chO=8, chI=8, chT=4.5, insets=(6.0,), seam=1.2)[0]),
    ('r2e_perp_balanced', lambda: vgem2.build(top='p', thin_top='p', tL=30, tR=11.5, chO=7.5, chI=7.5, chT=5, facets=False, seam=2.0)[0]),
    ('r2f_lineart_gem', lambda: gem_seams(seam=2.0, step=10)),
]

if __name__ == '__main__':
    for n, f in R:
        print(explore.cell(n, f()))
