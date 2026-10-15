"""VanIndra hinge type system v2 — glyphs drawn from beziers in y-up units (baseline 0)."""
import sys, math
from glyphkit import B, rect, poly, ellipse, U, D, T, rot, vt, pathops, to_svg_d

class P:
    def __init__(s, **kw):
        s.X=490; s.C=700; s.A=730
        s.S=84; s.Sc=92; s.H=25
        s.Ht=30; s.Hb=29; s.o=11
        s.ft=20; s.fe=31; s.fb=22       # foot serif: thickness, extension, bracket
        s.he=36; s.hd=30                # head wedge: extension, depth at tip
        s.ie=38; s.it=21                # capital slab: extension, thickness
        s.ball=1.0
        s.cw=262                        # n counter width
        s.__dict__.update(kw)

def fillet(cx, cy, ux, uy, vx, vy, a, b):
    """concave bracket at corner c between a slab edge (direction u, length a) and a stem edge (direction v, length b)."""
    A=(cx+ux*a, cy+uy*a); Bp=(cx+vx*b, cy+vy*b)
    return B().M(*Bp).Q(cx,cy,*A).L(cx,cy).Z().path()

def foot(p, x0, x1, eL=None, eR=None):
    eL = p.fe if eL is None else eL; eR = p.fe if eR is None else eR
    t=p.ft; b=p.fb
    parts=[rect(x0-eL,0,x1+eR,t)]
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

# ---------------------------------------------------------------- n family
def n_left(p, x0):
    S=p.S; X=p.X
    return U(rect(x0,0,x0+S,X-6), head_wedge(p,x0,x0+S,X), foot(p,x0,x0+S))

def arch_outer_to_apex(b, p, xs, w, notch, apex_k=0.44):
    X=p.X; o=p.o
    N=(xs, X*notch); ax=xs+w*apex_k
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

def g_n(p, lsb=22, rsb=22, cw=None):
    S=p.S; X=p.X; o=p.o; cw=cw or p.cw
    x0=lsb+p.fe; xs=x0+S; xl=xs+cw; xr=xl+S
    b=B(); ax=arch_outer_to_apex(b,p,xs,cw,0.80)
    yR=X*0.64
    b.C(ax+(xr-ax)*0.60, X+o, xr, yR+(X+o-yR)*0.60, xr, yR)
    b.L(xr, X*0.3).L(xl, X*0.3)
    arch_inner(b,p,xs,xl,cw,0.64,X*0.58)
    parts=[n_left(p,x0), b.Z().path(), rect(xl,0,xr,yR+2), foot(p,xl,xr)]
    return U(*parts), xr+p.fe+rsb

def g_hinge(p, top=None, land=0.62, land_dx=0.0, lsb=22, rsb=34, cw=None, arrive=0.35, Ist=None, foot_n=True):
    """n whose right stem IS the capital I.
    land  : height (fraction of X) where the n's outer shoulder lands on the I stem's left edge.
    arrive: 0 -> arrives horizontally (springs, h-like), 1 -> arrives vertically (tangent)."""
    S=p.S; X=p.X; o=p.o; cw=cw or p.cw
    top = top or p.C
    Ist = Ist or (S+p.Sc)/2
    x0=lsb+p.fe; xs=x0+S; xl=xs+cw; xr=xl+Ist
    b=B(); ax=arch_outer_to_apex(b,p,xs,cw,0.80)
    yl=X*land
    # shoulder: from apex, sweep right past the stem edge line then land at (xl, yl)
    c1=(ax+(xl+S*land_dx-ax)*0.62, X+o)
    c2=(xl+S*land_dx, yl+(X+o-yl)*(0.25+0.45*arrive))
    b.C(*c1, *c2, xl+1, yl)
    b.L(xl+Ist*0.5, yl-30).L(xl+Ist*0.5, X*0.3).L(xl, X*0.3)
    arch_inner(b,p,xs,xl,cw,0.64,X*0.58)
    parts=[n_left(p,x0), b.Z().path(), rect(xl,0,xr,top), cap_slab(p,xl,xr,top,True), cap_slab(p,xl,xr,0,False)]
    return U(*parts), xr+p.ie+rsb, (xl,xr)

def g_I(p, top=None, lsb=34, rsb=34):
    top=top or p.C
    x0=lsb+p.ie; x1=x0+p.Sc
    return U(rect(x0,0,x1,top), cap_slab(p,x0,x1,top,True), cap_slab(p,x0,x1,0,False)), x1+p.ie+rsb

# ---------------------------------------------------------------- V
def g_V(p, lsb=8, rsb=0, W=600, thick=None, thin=None, apex_flat=10):
    C=p.C; o=p.o
    thick = thick or p.Sc*1.06; thin = thin or p.H*1.12
    ax = lsb + 36 + W/2
    lx0 = ax - W/2; rx1 = ax + W/2
    apex=(ax, -o)
    thl = math.atan2(C+o, ax-lx0); thr = math.atan2(C+o, rx1-ax)
    wl = thick/math.sin(thl); wr = thin/math.sin(thr)
    # inner edges: left inner from (lx0+wl, C) parallel to left outer; right inner from (rx1-wr, C) parallel to right outer
    def inter(p1,d1,p2,d2):
        # p1 + t d1 = p2 + s d2
        det = d1[0]*(-d2[1]) - d1[1]*(-d2[0])
        t = ((p2[0]-p1[0])*(-d2[1]) - (p2[1]-p1[1])*(-d2[0]))/det
        return (p1[0]+t*d1[0], p1[1]+t*d1[1])
    dl=(apex[0]-lx0, apex[1]-C); dr=(apex[0]-rx1, apex[1]-C)
    I=inter((lx0+wl,C),dl,(rx1-wr,C),dr)
    body=poly([(lx0,C),(lx0+wl,C),I,(rx1-wr,C),(rx1,C),apex])
    body=D(body, rect(-500,-300,3000,-o+apex_flat))
    # serifs: slabs at the arm tops with fillets along the diagonal edges
    t=p.it; yb=C-t
    def unit(v):
        L=math.hypot(*v); return (v[0]/L, v[1]/L)
    ul=unit(dl); ur=unit(dr)
    # x of edges at y=yb
    xl_out = lx0 + ul[0]*( (yb-C)/ul[1]); xl_in = xl_out+wl
    xr_out = rx1 + ur[0]*((yb-C)/ur[1]); xr_in = xr_out-wr
    eo, ei = 40, 26      # thick arm: outer / inner extension
    ro, ri = 34, 28      # thin arm
    fb=p.fb*1.1
    parts=[body,
        rect(lx0-eo, yb, lx0+wl+ei, C), rect(rx1-wr-ri, yb, rx1+ro, C),
        fillet(xl_out,yb,-1,0,ul[0],ul[1],min(fb,eo*.8),fb*1.4), fillet(xl_in,yb,1,0,ul[0],ul[1],min(fb,ei*.8),fb*1.2),
        fillet(xr_in,yb,-1,0,ur[0],ur[1],min(fb,ri*.8),fb*1.2), fillet(xr_out,yb,1,0,ur[0],ur[1],min(fb,ro*.8),fb*1.4)]
    return U(*parts), rx1+ro+rsb

# ---------------------------------------------------------------- a
def g_a(p, lsb=30, rsb=16, w=330):
    S=p.S*0.97; X=p.X; o=p.o; H=p.H
    la=lsb; sr=la+w; sl=sr-S
    # --- hook
    br=38*p.ball; bcx=la+br+6; bcy=X*0.745
    hx=la+(sr-la)*0.50           # apex x
    hk=B().M(sr, X*0.55).L(sr, X*0.66)
    hk.C(sr, X*0.66+(X+o-X*0.66)*0.60, hx+(sr-hx)*0.55, X+o, hx, X+o)
    hk.C(hx-(hx-bcx)*0.52, X+o, bcx-br*0.55, X-6, bcx-br*0.92, bcy+br*0.40)   # into ball top-left
    hk.L(bcx+br*0.60, bcy+br*0.10)
    hk.C(bcx+br*1.05, X-p.Ht+3, hx-70, X-p.Ht, hx+4, X-p.Ht)
    hk.C(hx+(sl-hx)*0.62, X-p.Ht, sl, X*0.74, sl, X*0.62)
    hk.L(sl, X*0.55)
    ball=ellipse(bcx, bcy, br*0.96, br*1.04)
    # --- bowl
    tO=X*0.585; tI=tO-H*1.12
    bx=la+(sl-la)*0.50
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
    stem=rect(sl, 0, sr, X*0.62)
    spur=U(rect(sl,0,sr+22,p.ft), fillet(sr,p.ft,1,0,0,1,18,p.fb*1.2))
    return U(hk.Z().path(), ball, bowl, stem, spur), sr+22+rsb

# ---------------------------------------------------------------- d
def g_d(p, lsb=26, rsb=20, w=356, A=None):
    S=p.S; X=p.X; o=p.o; A=A or p.A
    ld=lsb; sr=ld+w; sl=sr-S
    bx=ld+(sl-ld)*0.52
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
    stem=U(rect(sl,0,sr,A), head_wedge(p,sl,sr,A))
    spur=U(rect(sl,0,sr+24,p.ft), fillet(sr,p.ft,1,0,0,1,18,p.fb*1.2))
    return U(bowl, stem, spur), sr+24+rsb

# ---------------------------------------------------------------- r
def g_r(p, lsb=22, rsb=8):
    S=p.S; X=p.X; o=p.o
    x0=lsb+p.fe; xs=x0+S
    br=35*p.ball; bcx=xs+150; bcy=X*0.80
    ex=xs+86
    e=B().M(xs-3, X*0.66).L(xs, X*0.72)
    e.C(xs+16, X*0.72+(X+o-X*0.72)*0.62, ex-44, X+o, ex, X+o)
    e.C(ex+40, X+o, bcx+br*0.40, X+o-4, bcx+br*0.88, bcy+br*0.48)
    e.L(bcx-br*0.30, bcy+br*0.30)
    e.C(bcx-br*0.75, X-p.Ht+2, ex+16, X-p.Ht, ex-6, X-p.Ht)
    e.C(ex-46, X-p.Ht, xs+10, X*0.70, xs, X*0.58)
    e.L(xs-3, X*0.54)
    ball=ellipse(bcx,bcy,br*0.95,br*1.05)
    parts=[rect(x0,0,xs,X-6), head_wedge(p,x0,xs,X), foot(p,x0,xs,p.fe,p.fe+16), e.Z().path(), ball]
    return U(*parts), bcx+br+rsb

def place(items):
    out=[]; x=0
    for (pth, adv, kern) in items:
        x+=kern; out.append(T(pth,x,0)); x+=adv
    return U(*out), x
