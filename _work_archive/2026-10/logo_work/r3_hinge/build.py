"""Build every deliverable for R3 'The Hinge'."""
import sys, re, math, json
sys.path.insert(0,'.')
from vitype import *

EM='#0B2A20'; IV='#F6F1E7'; GD='#A8843A'; GL='#D2B26A'; WH='#FFFFFF'
OUT='.'
DESC=dict(S=88, Sc=95, H=31, Ht=35, Hb=34, ft=24, fe=30, fb=18, ie=36, it=26, ball=1.0)
MARK_SMALL=dict(SMALL, gap=52, H=40, Ht=46, Hb=42, S=104, Sc=108, ft=32, fe=34, fb=12, he=40, hd=40, ie=46, it=38, Itop=800, cw=272)

def rnd(d, nd=1):
    return re.sub(r'-?\d+\.\d+', lambda m: f'{float(m.group()):.{nd}f}'.rstrip('0').rstrip('.'), d)

def D_(path, s, dx, dy):
    return rnd(to_svg_d(path, s, dx, dy))

def bbox(*ps):
    bs=[vt.bounds(p) for p in ps if p is not None]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))

def svg(w,h,body,bg=None,title='VanIndra Creations'):
    return vt.svg_doc(w,h,body,bg=bg,title=title)

def write(name, s):
    open(f'{OUT}/{name}','w').write(s)

def paths_svg(parts, s, dx, dy):
    return ''.join(f'<path d="{D_(p,s,dx,dy)}" fill="{c}"/>' for p,c in parts if p is not None)

# ---------------------------------------------------------------- geometry
pd=P(**DISPLAY); ps=P(**SMALL); pdesc=P(**DESC); pms=P(**MARK_SMALL)
WM=wordmark(pd)                # display wordmark
WMS=wordmark(ps)               # header / small cut
CR=creations(pdesc)            # descriptor
CRD=creations(pd)              # descriptor at display weight (one-line lockup)
HM=hinge_mark(pd)              # mark
HMS=hinge_mark(pms)            # small mark

def mark_layout(hm, size=1000, fill=0.64, circle=None):
    """Fit hinge glyph in a square; optical centring = bbox centre nudged toward the area centroid."""
    b=bbox(hm['n'],hm['I'])
    h=b[3]-b[1]; w=b[2]-b[0]
    s=size*fill/h
    cx=(b[0]+b[2])/2; cy=(b[1]+b[3])/2
    # area centroid via raster sampling
    allp=U(hm['n'],hm['I'])
    sx=sy=n=0
    for i in range(60):
        for j in range(80):
            x=b[0]+w*(i+0.5)/60; y=b[1]+h*(j+0.5)/80
            if allp.contains((x,y)): sx+=x; sy+=y; n+=1
    gx,gy=sx/n, sy/n
    ocx=cx*0.55+gx*0.45; ocy=cy*0.75+gy*0.25
    if circle:
        pts=[pt for c in allp.contours for pt in c.points] if hasattr(allp,'contours') else []
        far=max(math.hypot(px-ocx, py-ocy) for (px,py) in pts)
        s=min(s, size*circle/far)
    dx=size/2-ocx*s; dy=size/2+ocy*s
    return s,dx,dy

def mark_svg(hm, ncol, icol, bg=None, size=1000, fill=0.70, circle=0.455, title='VanIndra Creations — hinge mark'):
    s,dx,dy=mark_layout(hm,size,fill,circle)
    return svg(size,size,paths_svg([(hm['n'],ncol),(hm['I'],icol)],s,dx,dy),bg=bg,title=title)

def wordmark_svg(wm, ink, icol, bg=None, pad=None, unit=0.5, title='VanIndra Creations'):
    b=bbox(wm['ink'],wm['I'])
    pad = pad if pad is not None else 0
    W=(b[2]-b[0])*unit+2*pad; H=(b[3]-b[1])*unit+2*pad
    dx=pad-b[0]*unit; dy=pad+b[3]*unit
    return svg(round(W,1),round(H,1),paths_svg([(wm['ink'],ink),(wm['I'],icol)],unit,dx,dy),bg=bg,title=title)

def lockup_one_line(ink, icol, bg, unit=0.5, padx=None):
    """VanIndra Creations, one line, same drawn system (display weight)."""
    gapw=250
    crT=T(CRD['ink'], WM['width']+gapw, 0)
    b=bbox(WM['ink'],WM['I'],crT)
    X=pd.X
    pad=X*1.0*unit
    W=(b[2]-b[0])*unit+2*pad; H=(b[3]-b[1])*unit+2*pad*0.9
    dx=pad-b[0]*unit; dy=pad*0.9+b[3]*unit
    return svg(round(W,1),round(H,1),paths_svg([(WM['ink'],ink),(WM['I'],icol),(crT,ink)],unit,dx,dy),bg=bg)

def lockup_stacked(ink, icol, bg, unit=0.5, lead=0.62):
    """Two-line block: Creations is scaled (never letter-spaced) to the wordmark's width."""
    b=bbox(WM['ink'],WM['I'])
    wmw=b[2]-b[0]
    crb0=vt.bounds(CRD['ink']); ratio=0.97*wmw/(crb0[2]-crb0[0])
    CRs=CRD
    crb=crb0; crw=(crb[2]-crb[0])*ratio
    base2=pd.X*lead+ pd.C*ratio
    crx=b[0]+(wmw-crw)/2-crb[0]*ratio
    crP=T(CRs['ink'],0,0,ratio,ratio); crP=T(crP,crx,-base2)
    bb=bbox(WM['ink'],WM['I'],crP)
    padx=pd.X*1.25; pady=pd.X*1.1
    W=(bb[2]-bb[0]+2*padx)*unit; H=(bb[3]-bb[1]+2*pady)*unit
    dx=(padx-bb[0])*unit; dy=(pady+bb[3])*unit
    return svg(round(W,1),round(H,1),paths_svg([(WM['ink'],ink),(WM['I'],icol),(crP,ink)],unit,dx,dy),bg=bg)

if __name__=='__main__':
    write('mark.svg', mark_svg(HM, EM, EM))
    write('mark_small.svg', mark_svg(HMS, EM, EM, fill=0.86, circle=None, title='VanIndra Creations — small hinge mark (48 px and below)'))
    write('mark_small_ivory.svg', mark_svg(HMS, IV, GL, fill=0.86, circle=None))
    write('mark_on_ivory.svg', mark_svg(HM, EM, EM, bg=IV))
    write('mark_on_emerald.svg', mark_svg(HM, IV, GL, bg=EM))
    write('mark_one_colour_gold.svg', mark_svg(HM, GD, GD))
    write('wordmark.svg', wordmark_svg(WM, EM, EM, pad=0))
    write('wordmark_small.svg', wordmark_svg(WMS, EM, EM, pad=0))
    write('lockup_horizontal_on_ivory.svg', lockup_one_line(EM, EM, IV))
    write('lockup_horizontal_on_emerald.svg', lockup_one_line(IV, GL, EM))
    write('lockup_stacked_on_ivory.svg', lockup_stacked(EM, EM, IV))
    write('lockup_stacked_on_emerald.svg', lockup_stacked(IV, GL, EM))
    write('global.svg', lockup_one_line(EM, EM, WH))
    # helper files for context / header renders (transparent)
    write('_header_emeraldink.svg', wordmark_svg(WMS, EM, EM, pad=0))
    write('_header_ivoryink.svg', wordmark_svg(WMS, IV, GL, pad=0))
    print('built')
