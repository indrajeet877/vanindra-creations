"""VanIndra Hinge — the final type system. Every glyph is drawn here from cubic beziers and straight segments
(y-up design units, baseline 0). No font outlines are used in any deliverable.

Two optical cuts:  DISPLAY (>= 64 px tall wordmark)  and  SMALL (headers, favicons, <= 48 px).
"""
import sys, math
from glyphkit import B, rect, poly, ellipse, U, D, T, vt, pathops, to_svg_d

class P:
    def __init__(s, **kw):
        s.X=490; s.C=700; s.A=724; s.Itop=784     # x-height, cap, d ascender, rising I
        s.S=82; s.Sc=90; s.H=24                    # stems + hairline
        s.Ht=29; s.Hb=28; s.o=11
        s.ft=20; s.fe=31; s.fb=22                  # foot serif
        s.he=35; s.hd=30                           # head wedge
        s.ie=37; s.it=21                           # capital slab
        s.ball=0.9
        s.cw=264                                   # n counter
        s.gap=16                                   # hinge cut
        s.r_term='wedge'
        s.__dict__.update(kw)

DISPLAY=dict()
SMALL=dict(S=90, Sc=96, H=34, Ht=38, Hb=36, ft=26, fe=30, fb=16, he=34, hd=34, ie=36, it=28, gap=46, ball=1.0, cw=256, Itop=812)

def dilate(path, g):
    q=pathops.Path(path)
    q.stroke(2*g, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    q.convertConicsToQuads()
    return U(path, U(q))

def fillet(cx, cy, ux, uy, vx, vy, a, b):
    A=(cx+ux*a, cy+uy*a); Bp=(cx+vx*b, cy+vy*b)
    return B().M(*Bp).Q(cx,cy,*A).L(cx,cy).Z().path()

def foot(p, x0, x1, eL=None, eR=None):
    eL = p.fe if eL is None else eL; eR = p.fe if eR is None else eR
    t=p.ft; b=p.fb; parts=[rect(x0-eL,0,x1+eR,t)]
    if eL>0: parts.append(fillet(x0,t,-1,0,0,1,min(b,eL*0.8),b*1.2))
    if eR>0: parts.append(fillet(x1,t,1,0,0,1,min(b,eR*0.8),b*1.2))
    return U(*parts)

def head_wedge(p, x0, x1, top):
    e=p.he; d=p.hd
    tipT=(x0-e, top-d+9); tipB=(x0-e, top-d-2)
    b=B().M(*tipB).L(*tipT).L(x1, top+2).L(x1, top-120).L(x0, top-120).L(x0, top-d-2-p.fb*1.4)
    b.Q(x0, top-d-2, *tipB)
    return b.Z().path()

def cap_slab(p, x0, x1, y, up=True, eL=None, eR=None):
    eL = p.ie if eL is None else eL; eR = p.ie if eR is None else eR
    t=p.it; b=p.fb*1.05
    if up:
        yb=y-t
        return U(rect(x0-eL, yb, x1+eR, y), fillet(x0,yb,-1,0,0,-1,min(b,eL*.8),b*1.25), fillet(x1,yb,1,0,0,-1,min(b,eR*.8),b*1.25))
    yb=y+t
    return U(rect(x0-eL, y, x1+eR, yb), fillet(x0,yb,-1,0,0,1,min(b,eL*.8),b*1.25), fillet(x1,yb,1,0,0,1,min(b,eR*.8),b*1.25))

def teardrop(cx, cy, r, ang=0.0, stretch=1.12):
    """slightly elongated ball terminal"""
    e=ellipse(0,0,r*0.94,r*stretch)
    a=math.radians(ang); c,s=math.cos(a),math.sin(a)
    return vt.transform(e,c,s,-s,c,cx,cy)

# ------------------------------------------------------------------ n arch pieces
def arch_outer_to_apex(b, p, xs, w, notch, apex_k=0.44):
    X=p.X; o=p.o; N=(xs, X*notch); ax=xs+w*apex_k
    b.M(xs-3, N[1]-40).L(*N)
    b.C(N[0]+w*0.10, N[1]+(X+o-N[1])*0.58, ax-w*0.27, X+o, ax, X+o)
    return ax

def arch_inner(b, p, xs, xl, w, crotch, yi):
    X=p.X; it=X-p.Ht; ix=xs+w*0.42
    b.L(xl, yi)
    b.C(xl, yi+(it-yi)*0.62, ix+(xl-ix)*0.56, it, ix, it)
    b.C(ix-(ix-xs)*0.52, it, xs+w*0.05, X*crotch+(it-X*crotch)*0.50, xs, X*crotch)
    b.L(xs-3, X*crotch-40)
    return b

def n_arch(p, x0, cw, Sr=None):
    S=p.S; X=p.X; o=p.o; Sr=Sr or S
    xs=x0+S; xl=xs+cw; xr=xl+Sr
    b=B(); ax=arch_outer_to_apex(b,p,xs,cw,0.80)
    yR=X*0.64
    b.C(ax+(xr-ax)*0.60, X+o, xr, yR+(X+o-yR)*0.60, xr, yR)
    b.L(xr, X*0.3).L(xl, X*0.3)
    arch_inner(b,p,xs,xl,cw,0.64,X*0.58)
    return b.Z().path(), xs, xl, xr

def n_left(p, x0):
    S=p.S; X=p.X
    return U(rect(x0,0,x0+S,X-60), head_wedge(p,x0,x0+S,X), foot(p,x0,x0+S))

def g_n(p, lsb=22, rsb=22):
    x0=lsb+p.fe
    arch,xs,xl,xr=n_arch(p,x0,p.cw)
    return U(n_left(p,x0), arch, rect(xl,0,xr,p.X*0.66), foot(p,xl,xr)), xr+p.fe+rsb

def g_hinge(p, lsb=22, rsb=34, gap=None):
    """THE HINGE: a complete n whose right leg is also the stem of a capital I.
    The I rises behind the n's shoulder (separated by a cut that follows the shoulder).
    returns (n_part, I_part, advance)."""
    S=p.S; X=p.X; gap=p.gap if gap is None else gap
    x0=lsb+p.fe
    arch,xs,xl,xr=n_arch(p,x0,p.cw)
    leg=U(rect(xl,0,xr,X*0.66), cap_slab(p,xl,xr,0,False))
    n_part=U(n_left(p,x0), arch, leg)
    shoulder=U(arch, rect(xl, X*0.30, xr, X*0.66))
    I_full=U(rect(xl,X*0.3,xr,p.Itop), cap_slab(p,xl,xr,p.Itop,True))
    I_part=D(I_full, dilate(shoulder, gap)) if gap>0 else D(I_full, n_part)
    return n_part, I_part, xr+p.ie+rsb

# ------------------------------------------------------------------ V
def g_V(p, lsb=8, rsb=0, W=596, apex_flat=10):
    C=p.C; o=p.o
    thick=p.Sc*1.06; thin=p.H*1.15
    ax=lsb+36+W/2; lx0=ax-W/2; rx1=ax+W/2; apex=(ax,-o)
    thl=math.atan2(C+o, ax-lx0); thr=math.atan2(C+o, rx1-ax)
    wl=thick/math.sin(thl); wr=thin/math.sin(thr)
    def inter(p1,d1,p2,d2):
        det=d1[0]*(-d2[1])-d1[1]*(-d2[0])
        t=((p2[0]-p1[0])*(-d2[1])-(p2[1]-p1[1])*(-d2[0]))/det
        return (p1[0]+t*d1[0], p1[1]+t*d1[1])
    dl=(apex[0]-lx0, apex[1]-C); dr=(apex[0]-rx1, apex[1]-C)
    I=inter((lx0+wl,C),dl,(rx1-wr,C),dr)
    body=D(poly([(lx0,C),(lx0+wl,C),I,(rx1-wr,C),(rx1,C),apex]), rect(-500,-300,3000,-o+apex_flat))
    t=p.it; yb=C-t
    def unit(v):
        L=math.hypot(*v); return (v[0]/L, v[1]/L)
    ul=unit(dl); ur=unit(dr)
    xl_out=lx0+ul[0]*((yb-C)/ul[1]); xl_in=xl_out+wl
    xr_out=rx1+ur[0]*((yb-C)/ur[1]); xr_in=xr_out-wr
    eo,ei,ro,ri=40,24,34,26; fb=p.fb*1.1
    parts=[body, rect(lx0-eo,yb,lx0+wl+ei,C), rect(rx1-wr-ri,yb,rx1+ro,C),
        fillet(xl_out,yb,-1,0,ul[0],ul[1],min(fb,eo*.8),fb*1.4), fillet(xl_in,yb,1,0,ul[0],ul[1],min(fb,ei*.8),fb*1.2),
        fillet(xr_in,yb,-1,0,ur[0],ur[1],min(fb,ri*.8),fb*1.2), fillet(xr_out,yb,1,0,ur[0],ur[1],min(fb,ro*.8),fb*1.4)]
    return U(*parts), rx1+ro+rsb

# ------------------------------------------------------------------ a
def g_a(p, lsb=30, rsb=16, w=328):
    S=p.S*0.97; X=p.X; o=p.o; H=p.H
    la=lsb; sr=la+w; sl=sr-S
    br=36*p.ball; bcx=la+br+4; bcy=X*0.74
    hx=la+(sr-la)*0.50
    hk=B().M(sr, X*0.55).L(sr, X*0.66)
    hk.C(sr, X*0.66+(X+o-X*0.66)*0.60, hx+(sr-hx)*0.55, X+o, hx, X+o)
    Px=bcx-br*0.94; Py=bcy+br*0.10                 # ball's left flank, arriving vertically
    hk.C(hx-(hx-Px)*0.58, X+o, Px, Py+(X+o-Py)*0.56, Px, Py)
    hk.L(bcx, bcy).L(bcx+br*0.80, bcy+br*0.10)
    hk.C(bcx+br*1.10, X-p.Ht-6, hx-74, X-p.Ht, hx+4, X-p.Ht)
    hk.C(hx+(sl-hx)*0.62, X-p.Ht, sl, X*0.74, sl, X*0.62)
    hk.L(sl, X*0.55)
    ball=teardrop(bcx, bcy, br, ang=-18, stretch=1.05)
    tO=X*0.585; tI=tO-H*1.12; bx=la+(sl-la)*0.50
    bo=B().M(sl+14, tO)
    bo.C(sl-50, tO, la, X*0.47, la, X*0.27)
    bo.C(la, X*0.09, la+48, -o, bx-6, -o)
    bo.C(bx+60, -o, sl-14, X*0.04, sl+14, X*0.14)
    bo.Z()
    li=la+S*1.04
    ci=B().M(sl, tI)
    ci.C(sl-46, tI, li, X*0.45, li, X*0.29)
    ci.C(li, X*0.14, li+26, p.Hb, li+74, p.Hb)
    ci.C(li+126, p.Hb, sl, X*0.12, sl, X*0.24)
    ci.Z()
    bowl=D(bo.path(), ci.path())
    stem=rect(sl,0,sr,X*0.62)
    spur=U(rect(sl,0,sr+22,p.ft), fillet(sr,p.ft,1,0,0,1,18,p.fb*1.2))
    return U(hk.Z().path(), ball, bowl, stem, spur), sr+22+rsb

# ------------------------------------------------------------------ d
def g_d(p, lsb=26, rsb=20, w=356):
    S=p.S; X=p.X; o=p.o; A=p.A
    ld=lsb; sr=ld+w; sl=sr-S; bx=ld+(sl-ld)*0.52
    ou=B().M(sl+12, X*0.84)
    ou.C(sl-34, X+o-4, bx+60, X+o, bx, X+o)
    ou.C(bx-82, X+o, ld, X*0.76, ld, X*0.475)
    ou.C(ld, X*0.18, ld+70, -o, bx, -o)
    ou.C(bx+70, -o, sl-20, X*0.05, sl+12, X*0.14)
    ou.Z()
    li=ld+S*1.06
    ci=B().M(sl, X*0.80)
    ci.C(sl-24, X-p.Ht-2, bx+56, X-p.Ht, bx+6, X-p.Ht)
    ci.C(bx-62, X-p.Ht, li, X*0.70, li, X*0.475)
    ci.C(li, X*0.22, li+40, p.Hb, bx+10, p.Hb)
    ci.C(bx+66, p.Hb, sl-6, X*0.12, sl, X*0.22)
    ci.Z()
    bowl=D(ou.path(), ci.path())
    stem=U(rect(sl,0,sr,A-60), head_wedge(p,sl,sr,A))
    spur=U(rect(sl,0,sr+24,p.ft), fillet(sr,p.ft,1,0,0,1,18,p.fb*1.2))
    return U(bowl, stem, spur), sr+24+rsb

# ------------------------------------------------------------------ r
def g_r(p, lsb=22, rsb=8):
    S=p.S; X=p.X; o=p.o
    x0=lsb+p.fe; xs=x0+S
    br=33*p.ball; bcx=xs+146; bcy=X*0.80
    ex=xs+86
    e=B().M(xs-3, X*0.66).L(xs, X*0.72)
    e.C(xs+16, X*0.72+(X+o-X*0.72)*0.62, ex-44, X+o, ex, X+o)
    if p.r_term=='ball':
        e.C(ex+40, X+o, bcx+br*0.40, X+o-4, bcx+br*0.86, bcy+br*0.50)
        e.L(bcx-br*0.30, bcy+br*0.30)
        e.C(bcx-br*0.75, X-p.Ht+2, ex+16, X-p.Ht, ex-6, X-p.Ht)
        term=teardrop(bcx,bcy,br,ang=20)
        adv=bcx+br+rsb
    else:  # wedge: the ear ends in a sharp downward-cut beak
        tx=xs+170
        e.C(ex+44, X+o, tx-10, X+o-6, tx, X*0.93)
        e.L(tx-4, X*0.76)
        e.C(tx-30, X-p.Ht-6, ex+20, X-p.Ht, ex-6, X-p.Ht)
        term=None; adv=tx+rsb
    e.C(ex-46, X-p.Ht, xs+10, X*0.70, xs, X*0.58)
    e.L(xs-3, X*0.54)
    parts=[rect(x0,0,xs,X-60), head_wedge(p,x0,xs,X), foot(p,x0,xs,p.fe,p.fe+16), e.Z().path()]
    if term is not None: parts.append(term)
    return U(*parts), adv

# ------------------------------------------------------------------ o / e / C / t / i / s  (for "Creations")
def ring(cx, cy, rxo, ryo, rxi, ryi, tilt=-7, ko=0.57, ki=0.555):
    outer=ellipse(cx,cy,rxo,ryo,ko)
    inner=ellipse(0,0,rxi,ryi,ki)
    a=math.radians(tilt); c,s=math.cos(a),math.sin(a)
    inner=vt.transform(inner,c,s,-s,c,cx,cy)
    return D(outer, inner)

def g_o(p, lsb=26, rsb=26, w=448):
    X=p.X; o=p.o; rx=w/2; ry=X/2+o
    cx=lsb+rx
    return ring(cx, X/2, rx, ry, rx-p.S*1.05, ry-p.Ht), lsb+w+rsb

def g_e(p, lsb=26, rsb=18, w=414):
    X=p.X; o=p.o; rx=w/2; ry=X/2+o; cx=lsb+rx; cy=X/2
    rg=ring(cx, cy, rx, ry, rx-p.S*1.0, ry-p.Ht*0.95)
    bar_y0=X*0.50; bar_y1=bar_y0+p.Ht*0.92
    # opening on the lower right (between the bar and the terminal)
    cut=poly([(cx+rx*0.05, bar_y0), (cx+rx+40, bar_y0), (cx+rx+40, X*0.30), (cx+rx*0.05, X*0.19)])
    body=D(rg, cut)
    bar=rect(cx-rx+p.S*0.6, bar_y0, cx+rx-2, bar_y1)
    return U(body, bar), lsb+w+rsb

def g_C(p, lsb=34, rsb=20, w=584):
    C=p.C; o=p.o; rx=w/2; ry=C/2+o; cx=lsb+rx; cy=C/2
    rg=ring(cx, cy, rx, ry, rx-p.Sc*1.08, ry-p.H*1.3, tilt=-6)
    # opening: vertical terminal cuts; upper terminal deeper (a vertical beak), lower one lighter
    xt=cx+rx*0.80; xb=cx+rx*0.86
    cut=U(poly([(xt, cy+ry+50), (cx+rx+80, cy+ry+50), (cx+rx+80, cy), (xt, cy)]),
          poly([(xb, cy), (cx+rx+80, cy), (cx+rx+80, cy-ry-50), (xb, cy-ry-50)]),
          rect(cx+rx*0.40, cy-C*0.215, cx+rx+80, cy+C*0.205))
    return D(rg, cut), lsb+w+rsb

def g_t(p, lsb=14, rsb=10):
    S=p.S*0.95; X=p.X; o=p.o
    x0=lsb+70; x1=x0+S
    stem=B().M(x0, X*1.0).L(x1, X*1.14).L(x1, X*0.20)
    stem.C(x1, X*0.09, x1+20, X*0.06, x1+46, X*0.06)
    stem.C(x1+76, X*0.06, x1+96, X*0.12, x1+110, X*0.19)
    stem.L(x1+128, X*0.16)
    stem.C(x1+108, X*0.04, x1+70, -o, x1+18, -o)
    stem.C(x0+16, -o, x0, X*0.06, x0, X*0.22)
    stem.Z()
    bar=rect(x0-74, X-p.Ht, x1+108, X)
    return U(stem.path(), bar), x1+128+rsb

def g_i(p, lsb=22, rsb=22):
    S=p.S; X=p.X; x0=lsb+p.fe
    dot=ellipse(x0+S/2+4, X+150, S*0.56, S*0.56)
    return U(rect(x0,0,x0+S,X-60), head_wedge(p,x0,x0+S,X), foot(p,x0,x0+S), dot), x0+S+p.fe+rsb

def expand(segs, wfun, n=48):
    """pointed-pen expansion along cubic spine segments; returns filled path."""
    L=[]; R=[]
    tot=len(segs)
    for si,(p0,p1,p2,p3) in enumerate(segs):
        for k in range(n+1):
            if si>0 and k==0: continue
            t=k/n; mt=1-t
            x=mt**3*p0[0]+3*mt*mt*t*p1[0]+3*mt*t*t*p2[0]+t**3*p3[0]
            y=mt**3*p0[1]+3*mt*mt*t*p1[1]+3*mt*t*t*p2[1]+t**3*p3[1]
            dx=3*mt*mt*(p1[0]-p0[0])+6*mt*t*(p2[0]-p1[0])+3*t*t*(p3[0]-p2[0])
            dy=3*mt*mt*(p1[1]-p0[1])+6*mt*t*(p2[1]-p1[1])+3*t*t*(p3[1]-p2[1])
            l=math.hypot(dx,dy) or 1; tx,ty=dx/l,dy/l
            w=wfun((si+t)/tot, tx, ty)
            nx,ny=-ty,tx
            L.append((x+nx*w/2, y+ny*w/2)); R.append((x-nx*w/2, y-ny*w/2))
    pts=L+R[::-1]
    return poly(pts)

def g_s(p, lsb=26, rsb=20, w=318):
    X=p.X; o=p.o; S=p.S; H=p.H
    x0=lsb; x1=lsb+w
    ht=p.Ht; hb=p.Hb
    yt=X+o-ht/2; yb=-o+hb/2
    segs=[
      ((x1-24, X*0.73), (x1-24, X*0.93), (x1-90, yt), (x0+w*0.50, yt)),
      ((x0+w*0.50, yt), (x0+w*0.16, yt), (x0+S*0.50, X*0.90), (x0+S*0.52, X*0.72)),
      ((x0+S*0.52, X*0.72), (x0+S*0.56, X*0.50), (x1-S*0.56, X*0.50), (x1-S*0.52, X*0.27)),
      ((x1-S*0.52, X*0.27), (x1-S*0.50, X*0.08), (x0+w*0.84, yb), (x0+w*0.50, yb)),
      ((x0+w*0.50, yb), (x0+w*0.20, yb), (x0+18, X*0.08), (x0+18, X*0.26)),
    ]
    keys=[(0.0,0.46*S),(0.11,0.36*S),(0.20,ht),(0.30,0.55*S),(0.42,0.92*S),(0.50,1.0*S),(0.58,0.92*S),(0.70,0.55*S),(0.80,hb),(0.89,0.36*S),(1.0,0.46*S)]
    def wf(u, tx, ty):
        ks=[keys[0]]+keys+[keys[-1]]
        for i in range(1,len(ks)-2):
            (u0,w0),(u1,w1),(u2,w2),(u3,w3)=ks[i-1],ks[i],ks[i+1],ks[i+2]
            if u<=u2:
                t=(u-u1)/(u2-u1) if u2>u1 else 0
                m1=(w2-w0)/2; m2=(w3-w1)/2
                h00=2*t**3-3*t*t+1; h10=t**3-2*t*t+t; h01=-2*t**3+3*t*t; h11=t**3-t*t
                return h00*w1+h10*m1+h01*w2+h11*m2
        return keys[-1][1]
    return expand(segs, wf, 60), x1+rsb

def place(items):
    out=[]; x=0
    for (pth, adv, kern) in items:
        x+=kern; out.append(T(pth,x,0)); x+=adv
    return U(*out), x

# ------------------------------------------------------------------ words
KERN=dict(Va=-78, an=0, In=-32, nd=-6, dr=-6, ra=-46)

def wordmark(p):
    """returns dict(ink, I, width, height info)  — ink = everything except the rising I; I = the rising I."""
    V_,vw=g_V(p); a,aw=g_a(p); n,nw=g_n(p); d,dw=g_d(p); r,rw=g_r(p)
    np_,ip_,hw=g_hinge(p)
    items=[(V_,vw,0),(a,aw,KERN['Va']),(np_,hw,KERN['an']),(n,nw,KERN['In']),(d,dw,KERN['nd']),(r,rw,KERN['dr']),(a,aw,KERN['ra'])]
    ink,width=place(items)
    off=vw+aw+KERN['Va']+KERN['an']
    return dict(ink=ink, I=T(ip_,off,0), width=width)

def creations(p, track=0):
    C_,cw_=g_C(p); r,rw=g_r(p); e,ew=g_e(p); a,aw=g_a(p); t,tw=g_t(p); i,iw=g_i(p); o_,ow=g_o(p); n,nw=g_n(p); s,sw=g_s(p)
    items=[(C_,cw_,0),(r,rw,-30+track),(e,ew,-8+track),(a,aw,-14+track),(t,tw,-10+track),(i,iw,-14+track),(o_,ow,-12+track),(n,nw,-6+track),(s,sw,-4+track)]
    ink,width=place(items)
    return dict(ink=ink, width=width)

def hinge_mark(p, gap=None):
    np_,ip_,hw=g_hinge(p, gap=gap)
    return dict(n=np_, I=ip_, width=hw)
