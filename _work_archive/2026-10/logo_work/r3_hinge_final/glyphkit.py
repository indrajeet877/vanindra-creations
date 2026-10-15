"""VanIndra hinge type system — every glyph drawn here from beziers (y-up design units, baseline 0).
No font outlines are used in the final wordmark."""
import sys, math
S_='/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad'
sys.path.insert(0, S_+'/logo2/toolkit')
import vtype as vt
import pathops

class B:
    """tiny path builder in y-up units"""
    def __init__(s): s.p = pathops.Path(); s.cur=None
    def M(s,x,y): s.p.moveTo(x,y); s.cur=(x,y); return s
    def L(s,x,y): s.p.lineTo(x,y); s.cur=(x,y); return s
    def C(s,x1,y1,x2,y2,x,y): s.p.cubicTo(x1,y1,x2,y2,x,y); s.cur=(x,y); return s
    def Q(s,x1,y1,x,y): s.p.quadTo(x1,y1,x,y); s.cur=(x,y); return s
    def hv(s,x,y,k=0.56):   # leave horizontally, arrive vertically
        x0,y0=s.cur; return s.C(x0+k*(x-x0),y0, x,y+k*(y0-y), x,y)
    def vh(s,x,y,k=0.56):   # leave vertically, arrive horizontally
        x0,y0=s.cur; return s.C(x0,y0+k*(y-y0), x+k*(x0-x),y, x,y)
    def Z(s): s.p.close(); return s
    def path(s): return vt.union(s.p)

def rect(x0,y0,x1,y1):
    return B().M(x0,y0).L(x1,y0).L(x1,y1).L(x0,y1).Z().path()

def poly(pts):
    b=B().M(*pts[0])
    for p in pts[1:]: b.L(*p)
    return b.Z().path()

def ellipse(cx,cy,rx,ry,k=0.5523):
    b=B().M(cx,cy+ry)
    b.C(cx+k*rx,cy+ry, cx+rx,cy+k*ry, cx+rx,cy)
    b.C(cx+rx,cy-k*ry, cx+k*rx,cy-ry, cx,cy-ry)
    b.C(cx-k*rx,cy-ry, cx-rx,cy-k*ry, cx-rx,cy)
    b.C(cx-rx,cy+k*ry, cx-k*rx,cy+ry, cx,cy+ry)
    return b.Z().path()

def U(*ps): return vt.union(*ps)
def D(a,b): return vt.difference(a,b)
def T(p,dx=0,dy=0,sx=1,sy=1): return vt.transform(p,sx,0,0,sy,dx,dy)
def rot(p,deg,cx,cy):
    a=math.radians(deg); c,s=math.cos(a),math.sin(a)
    return vt.transform(p,c,s,-s,c,cx-c*cx+s*cy,cy-s*cx-c*cy)

# ------------------------------------------------------------------ parameters
class P:
    def __init__(s, **kw):
        s.X=480; s.C=690; s.A=735      # x-height, cap height, ascender
        s.S=84; s.Sc=94; s.H=27         # lc stem, cap stem, hairline
        s.Ht=31                          # arch / bowl top thickness
        s.Hb=29                          # bowl bottom thickness
        s.o=10                           # overshoot
        s.ft=21; s.fe=33; s.fb=26        # foot serif thickness, extension, bracket
        s.he=38; s.hd=34                 # head wedge extension, depth
        s.ie=40; s.it=23                 # capital I serif extension / thickness
        s.k=0.58                         # curve fullness
        s.ball=1.0                       # terminal ball scale
        s.__dict__.update(kw)

# ------------------------------------------------------------------ serifs
def foot(p, x0, x1, eL=None, eR=None):
    eL = p.fe if eL is None else eL; eR = p.fe if eR is None else eR
    t=p.ft; b=p.fb
    parts=[rect(x0-eL,0,x1+eR,t)]
    if eL>0: parts.append(B().M(x0,t+b*1.15).Q(x0,t, x0-b,t).L(x0,t).Z().path())
    if eR>0: parts.append(B().M(x1,t+b*1.15).Q(x1,t, x1+b,t).L(x1,t).Z().path())
    return U(*parts)

def head_wedge(p, x0, x1, top):
    """lowercase head serif: sharp wedge to the left, top edge rising to the right."""
    e=p.he; d=p.hd
    tipT=(x0-e, top-d+8); tipB=(x0-e, top-d-3)
    body=B().M(*tipB).L(*tipT).L(x1, top+3).L(x1, top-d-60).L(x0, top-d-60).L(x0, top-d-3-p.fb*1.3)
    body.Q(x0, top-d-3, tipB[0], tipB[1])
    return body.Z().path()

def cap_slab(p, x0, x1, y, up=True, e=None):
    """symmetric bracketed slab serif for capitals (I, V arms). up=True: serif at top (y = top edge)."""
    e = p.ie if e is None else e; t=p.it; b=p.fb*1.1
    if up:
        parts=[rect(x0-e, y-t, x1+e, y),
               B().M(x0, y-t-b*1.2).Q(x0, y-t, x0-b, y-t).L(x0,y-t).Z().path(),
               B().M(x1, y-t-b*1.2).Q(x1, y-t, x1+b, y-t).L(x1,y-t).Z().path()]
    else:
        parts=[rect(x0-e, y, x1+e, y+t),
               B().M(x0, y+t+b*1.2).Q(x0, y+t, x0-b, y+t).L(x0,y+t).Z().path(),
               B().M(x1, y+t+b*1.2).Q(x1, y+t, x1+b, y+t).L(x1,y+t).Z().path()]
    return U(*parts)

# ------------------------------------------------------------------ glyphs
# each returns (path, advance). origin x=0, ink starts at lsb.

def g_I(p, top=None, lsb=46):
    top = top or p.C
    x0=lsb+p.ie; x1=x0+p.Sc
    path=U(rect(x0,0,x1,top), cap_slab(p,x0,x1,top,True), cap_slab(p,x0,x1,0,False))
    return path, x1+p.ie+lsb

def arch(p, x0, x1r, land=None, notch=0.79, crotch=0.64, apex_shift=0.0):
    """n arch from left stem (right edge x0) to right stem [x1r-S, x1r].
    land=None: classic n (outer meets right edge of right stem).
    land=y   : hinge — outer contour lands on the LEFT edge of the right stem at height y (stem continues up)."""
    S=p.S; X=p.X; o=p.o
    xl=x1r-S                       # right stem left edge
    w=xl-x0                        # counter width
    ax=x0+w*(0.50+apex_shift)      # outer apex x
    b=B().M(x0-2, X*notch-30).L(x0, X*notch)
    # notch -> apex (leave rising, arrive horizontal)
    b.C(x0+w*0.16, X*notch+ (X+o-X*notch)*0.62, ax-w*0.36, X+o, ax, X+o)
    if land is None:
        b.C(ax+(x1r-ax)*0.58, X+o, x1r, X*0.80+ (X+o-X*0.80)*0.15, x1r, X*0.62)
        b.L(x1r, X*0.40)
    else:
        # descend and land on the stem's left edge, arriving almost vertically
        b.C(ax+(xl-ax)*0.62, X+o, xl+2, X*0.92, xl+1, land)
        b.L(xl+S*0.5, land-40)
    b.L(xl+S*0.5, X*0.30)
    b.L(xl, X*0.30)
    # inner: up the right stem's left edge, over the counter, down to the crotch
    yi = X*0.56
    b.L(xl, yi)
    ix = x0 + w*0.47
    b.C(xl, yi+(X-p.Ht-yi)*0.66, ix+(xl-ix)*0.60, X-p.Ht, ix, X-p.Ht)
    b.C(ix-(ix-x0)*0.55, X-p.Ht, x0+w*0.07, X*crotch+ (X-p.Ht-X*crotch)*0.40, x0, X*crotch)
    b.L(x0-2, X*crotch-30)
    return b.Z().path()

def g_n(p, lsb=24, cw=None, rsb=24, left_head=True):
    S=p.S; X=p.X
    cw = cw or 196
    x0=lsb+p.fe; xl=x0+S+cw
    parts=[rect(x0,0,x0+S,X-10), rect(xl,0,xl+S,X*0.62), arch(p,x0+S,xl+S),
           foot(p,x0,x0+S), foot(p,xl,xl+S)]
    if left_head: parts.append(head_wedge(p,x0,x0+S,X))
    return U(*parts), xl+S+p.fe+rsb

def g_hinge(p, top=None, land=None, lsb=24, cw=None, rsb=40, notch=0.79, crotch=0.64):
    """n + I sharing one stem.  The I keeps symmetric slab serifs (it is a capital), the n keeps its wedge head."""
    S=p.S; X=p.X
    cw = cw or 196
    top = top or p.C
    land = land if land is not None else X*0.80
    x0=lsb+p.fe; xl=x0+S+cw
    Ist = S+ (p.Sc-S)*0.5         # shared stem: between lc and cap weight
    xr = xl+Ist
    parts=[rect(x0,0,x0+S,X-10), head_wedge(p,x0,x0+S,X), foot(p,x0,x0+S),
           arch(p,x0+S,xl+S,land=land,notch=notch,crotch=crotch),
           rect(xl,0,xr,top), cap_slab(p,xl,xr,top,True), cap_slab(p,xl,xr,0,False)]
    return U(*parts), xr+p.ie+rsb, (xl, xr)

def g_r(p, lsb=24, rsb=6):
    S=p.S; X=p.X; o=p.o
    x0=lsb+p.fe; x1=x0+S
    # ear
    tx = x1+150; ty = X*0.80          # ball centre
    br = 37*p.ball
    ear=B().M(x1-2, X*0.70).L(x1, X*0.74)
    ear.C(x1+20, X*0.74+ (X+o-X*0.74)*0.7, x1+52, X+o, x1+88, X+o)
    ear.C(x1+118, X+o, tx+br*0.55, X+o-6, tx+br*0.92, ty+br*0.45)
    ear.L(tx-br*0.2, ty+br*0.1)
    ear.C(tx-br*0.6, X-p.Ht+2, x1+100, X-p.Ht, x1+70, X-p.Ht)
    ear.C(x1+40, X-p.Ht, x1+12, X*0.70, x1, X*0.56)
    ear.L(x1-2, X*0.52)
    ball=ellipse(tx, ty, br*0.98, br*1.06)
    parts=[rect(x0,0,x1,X-10), head_wedge(p,x0,x1,X), foot(p,x0,x1,p.fe,p.fe+22), ear.Z().path(), ball]
    return U(*parts), tx+br+rsb

def g_a(p, lsb=34, rsb=20):
    S=p.S*0.97; X=p.X; o=p.o
    la = lsb                      # leftmost ink of bowl
    ra = la+300                   # stem right edge
    sl = ra-S                     # stem left edge
    # stem
    stem=rect(sl, 22, ra, X*0.62)
    # hook (top arch)
    hb_ = 36*p.ball               # ball radius
    bx, by = la+44, X*0.735
    hook=B().M(ra, X*0.50).L(ra, X*0.66)
    hook.C(ra, X*0.66+(X+o-X*0.66)*0.62, ra-(ra-(la+150))*0.42, X+o, la+150, X+o)
    hook.C(la+150-62, X+o, bx+hb_*0.4, X-4, bx+hb_*0.2, by+hb_*0.98)
    hook.L(bx+hb_*0.75, by+hb_*0.25)
    hook.C(bx+hb_*1.2, X-p.Ht-4, la+150-40, X-p.Ht, la+158, X-p.Ht)
    hook.C(la+158+70, X-p.Ht, sl, X*0.70, sl, X*0.56)
    hook.L(sl, X*0.50)
    ball=ellipse(bx, by, hb_*0.95, hb_*1.05)
    # bowl
    top_o = X*0.585; top_i = top_o - p.H*1.05
    bowl=B().M(sl+12, top_o)
    bowl.C(sl-60, top_o, la, X*0.47, la, X*0.27)
    bowl.C(la, X*0.09, la+52, -o, la+120, -o)
    bowl.C(la+180, -o, sl-6, X*0.06, sl+12, X*0.15)
    bowl.L(sl+12, top_o).Z()
    cnt=B().M(sl, top_i)
    cnt.C(sl-56, top_i, la+S*1.02, X*0.44, la+S*1.02, X*0.29)
    cnt.C(la+S*1.02, X*0.15, la+S*1.02+30, p.Hb, la+S*1.02+76, p.Hb)
    cnt.C(la+S*1.02+130, p.Hb, sl, X*0.13, sl, X*0.25)
    cnt.Z()
    bowlp=D(bowl.path(), cnt.path())
    # foot: small right-only slab (spur)
    ft = U(rect(sl, 0, ra+24, p.ft), B().M(ra, p.ft+p.fb*1.1).Q(ra,p.ft, ra+p.fb,p.ft).L(ra,p.ft).Z().path(), rect(sl,0,ra,40))
    return U(stem, hook.Z().path(), ball, bowlp, ft), ra+24+rsb

def g_d(p, lsb=30, rsb=24):
    S=p.S; X=p.X; o=p.o; A=p.A
    ld=lsb; rd=ld+318; sl=rd-S
    stem=rect(sl,0,rd,A)
    head=head_wedge(p,sl,rd,A)
    outer=B().M(sl+10, X*0.86)
    outer.C(sl-40, X+o-2, ld+200, X+o, ld+150, X+o)
    outer.C(ld+62, X+o, ld, X*0.76, ld, X*0.47)
    outer.C(ld, X*0.17, ld+60, -o, ld+148, -o)
    outer.C(ld+205, -o, sl-30, X*0.06, sl+10, X*0.13)
    outer.Z()
    ci=ld+S*1.06
    cnt=B().M(sl, X*0.78)
    cnt.C(sl-26, X-p.Ht-2, sl-80, X-p.Ht, ci+90, X-p.Ht)
    cnt.C(ci+22, X-p.Ht, ci, X*0.70, ci, X*0.47)
    cnt.C(ci, X*0.20, ci+30, p.Hb, ci+90, p.Hb)
    cnt.C(sl-60, p.Hb, sl-6, X*0.12, sl, X*0.22)
    cnt.Z()
    bowl=D(outer.path(), cnt.path())
    ft=U(rect(sl,0,rd+28,p.ft), B().M(rd, p.ft+p.fb*1.1).Q(rd,p.ft, rd+p.fb,p.ft).L(rd,p.ft).Z().path())
    return U(stem, head, bowl, ft), rd+28+rsb

def g_V(p, lsb=10, rsb=0, W=600):
    C=p.C; Sc=p.Sc*1.04; H=p.H*1.15
    # arms defined by their outer top x and apex
    ax = lsb + W*0.5                      # apex x
    half = W*0.5 - 40                     # top-centre offset of arms
    # thick left arm: centreline from (ax-half, C) to (ax-?, 0)
    lt = ax-half                          # left arm top centre
    ang = math.atan2(C, half)
    wl = Sc/math.sin(ang)                 # horizontal width of thick arm
    wr = H/math.sin(ang)
    apex_y = -12
    left=poly([(lt-wl/2, C), (lt+wl/2, C), (ax+wl*0.10, apex_y+ (wl*0.0)), (ax-wl*0.22, apex_y)])
    rt = ax+half
    right=poly([(rt-wr/2, C), (rt+wr/2, C), (ax+wl*0.08+wr*0.2, apex_y+28), (ax-wl*0.0, apex_y+30)])
    # clip apex to a small flat
    body=U(left,right)
    body=D(body, rect(-1000,-200,2000,apex_y+4))
    sl=cap_slab(p, lt-wl/2, lt+wl/2, C, True, e=36)
    sr=cap_slab(p, rt-wr/2, rt+wr/2, C, True, e=30)
    return U(body, sl, sr), rt+wr/2+30+rsb

def place(glyphs):
    """glyphs: list of (path, advance, kern_before)"""
    out=[]; x=0
    for (pth, adv, kern) in glyphs:
        x+=kern
        out.append(T(pth, x, 0))
        x+=adv
    return U(*out), x

def to_svg_d(path, scale=1.0, dx=0, dy=0):
    """flip y-up design units into SVG y-down"""
    return vt.to_d(vt.transform(path, scale, 0, 0, -scale, dx, dy))
