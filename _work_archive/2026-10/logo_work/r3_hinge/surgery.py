"""Font-skeleton surgery used ONLY for the exploration phase: build the n|I hinge from stock glyphs."""
import sys
S='/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad'
sys.path.insert(0, S+'/logo2/toolkit')
import vtype as vt
import pathops

def rect(x0,y0,x1,y1):
    p=pathops.Path(); p.moveTo(x0,y0); p.lineTo(x1,y0); p.lineTo(x1,y1); p.lineTo(x0,y1); p.close(); return p

def spans(path, y, big=1e5):
    band = vt.intersection(path, rect(-big, y-0.25, big, y+0.25))
    out=[]
    for c in band.contours:
        b=c.bounds; out.append((b[0],b[2]))
    return sorted(out)

def tr(p, dx, dy=0): return vt.transform(p,1,0,0,1,dx,dy)

def build(font, weight=400, style='normal', size=100, mode='double', i_top=None, head_scale=1.0,
          sans_head=None, track=0.0, gold=False, i_stem_scale=1.0):
    """mode: 'none' | 'single' | 'double'.  i_top: I height as multiple of cap height (None=cap)."""
    kw=dict(family=font, weight=weight, style=style, size=size)
    gs = vt.glyph_paths('VanIndra', **kw)
    # metrics
    xg = vt.text_path('x', **kw); xh = -xg.bounds[1]
    Ig = gs[3]; cap = -Ig.bounds[1]
    # origins
    xs=[0]
    for g in gs[:-1]: xs.append(xs[-1]+g.width+track*size)
    paths=[g.path for g in gs]
    if mode=='none':
        allp=[tr(p,0) for p in paths]
        return dict(ink=vt.union(*allp), gold=None, xh=xh, cap=cap)
    n1, I, n2 = paths[2], paths[3], paths[4]
    ymid = -xh*0.45
    s1 = spans(n1, ymid); r0, r1 = s1[-1]
    sI = spans(I, -cap*0.5); i0, i1 = sI[0][0], sI[-1][1]
    stem_w = (r1-r0)*i_stem_scale
    cx = (r0+r1)/2
    top = cap*(i_top or 1.0)
    # head serif from I glyph: top band
    Ib = I.bounds
    band_h = cap*0.22
    head = vt.intersection(I, rect(Ib[0]-5, -cap-5, Ib[2]+5, -cap+band_h))
    icx = (i0+i1)/2
    head = vt.transform(head, head_scale, 0, 0, 1, icx*(1-head_scale), 0)
    # scale head stem width to match
    head = tr(head, cx-icx, -(top-cap))
    if sans_head:  # draw a flat slab cap for sans voices
        hw, hh = sans_head
        head = vt.union(rect(cx-stem_w/2, -top, cx+stem_w/2, -top+band_h), rect(cx-hw/2, -top, cx+hw/2, -top+hh))
    stem = rect(cx-stem_w/2, -top+band_h*0.6, cx+stem_w/2, 0)
    # foot of I: use n's foot (already there). Build I piece
    Ipiece = vt.union(head, stem)
    # shift everything after the I
    shift_I = 0
    out=[paths[0], paths[1], n1]
    if mode=='single':
        # place n2 after I: I origin aligned so its stem centre = cx
        I_origin = xs[3] + (cx - icx)
        n2_origin = I_origin + gs[3].width + track*size
        d = n2_origin - xs[4]
        rest=[tr(p, d) for p in paths[4:]]
        out += rest
        hinge = vt.union(n1, Ipiece)
    else:
        s2 = spans(n2, ymid); l0, l1 = s2[0]
        d = cx - (l0+l1)/2
        n2s = tr(n2, d)
        # remove n2's left head serif (left of stem, upper part)
        n2s = vt.difference(n2s, rect(cx-stem_w/2-200, -xh-200, cx-stem_w/2+0.01, -xh*0.55))
        out.append(n2s)
        out += [tr(p, d) for p in paths[5:]]
        hinge = vt.union(n1, Ipiece, n2s)
    ink = vt.union(*out, Ipiece)
    return dict(ink=ink, hinge=hinge, gold=(Ipiece if gold else None), xh=xh, cap=cap, cx=cx, stem_w=stem_w, top=top)

def hinge_only(res, pad=0):
    """clip the hinge glyph (n + I [+ n]) out of a built wordmark"""
    return res
