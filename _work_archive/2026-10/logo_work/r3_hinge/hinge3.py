import sys; sys.path.insert(0,'.')
from gk2 import *

def n_full_arch(p, x0, cw, Sr=None):
    """complete n arch path (outer reaches right stem's RIGHT edge)."""
    S=p.S; X=p.X; o=p.o; Sr=Sr or S
    xs=x0+S; xl=xs+cw; xr=xl+Sr
    b=B(); ax=arch_outer_to_apex(b,p,xs,cw,0.80)
    yR=X*0.64
    b.C(ax+(xr-ax)*0.60, X+o, xr, yR+(X+o-yR)*0.60, xr, yR)
    b.L(xr, X*0.3).L(xl, X*0.3)
    arch_inner(b,p,xs,xl,cw,0.64,X*0.58)
    return b.Z().path(), xs, xl, xr

def k_trunk(p, top=760, land=0.90, lsb=22, rsb=34):
    # arch flows into the stem high and thick, with a bracket (branch into trunk)
    S=p.S; X=p.X; o=p.o; cw=p.cw; Ist=(S+p.Sc)/2
    x0=lsb+p.fe; xs=x0+S; xl=xs+cw; xr=xl+Ist
    b=B(); ax=arch_outer_to_apex(b,p,xs,cw,0.80,apex_k=0.40)
    yl=X*land
    b.C(ax+(xl-ax)*0.5, X+o, xl-30, X+o-4, xl, yl+ (X+o-yl)*0.2+30)
    b.L(xl, yl).L(xl+Ist*0.5, yl-40).L(xl+Ist*0.5, X*0.3).L(xl, X*0.3)
    arch_inner(b,p,xs,xl,cw,0.64,X*0.58)
    parts=[n_left(p,x0), b.Z().path(), rect(xl,0,xr,top), cap_slab(p,xl,xr,top,True), cap_slab(p,xl,xr,0,False)]
    return U(*parts), xr+p.ie+rsb

def k_rise(p, top=760, Iw=0.62, align='c', lsb=22, rsb=30, slab_e=None):
    # complete n; a narrower I rises out of the right shoulder (its base IS the n's right leg)
    S=p.S; X=p.X; cw=p.cw
    x0=lsb+p.fe
    arch,xs,xl,xr=n_full_arch(p,x0,cw)
    w=S*Iw
    if align=='c': i0=xl+(S-w)/2
    elif align=='l': i0=xl
    else: i0=xr-w
    i1=i0+w
    parts=[n_left(p,x0), arch, rect(xl,0,xr,X*0.66), foot(p,xl,xr), rect(i0,X*0.5,i1,top), cap_slab(p,i0,i1,top,True,eL=slab_e,eR=slab_e)]
    return U(*parts), xr+p.fe+rsb

def k_flick(p, top=740, land=0.80, lsb=22, rsb=40):
    # the stem's foot belongs to the n (lowercase exit flick to the right), its head to the I (capital slab)
    S=p.S; X=p.X; o=p.o; cw=p.cw; Ist=(S+p.Sc)/2
    x0=lsb+p.fe; xs=x0+S; xl=xs+cw; xr=xl+Ist
    h,_,_=g_hinge(p, top=top, land=land, arrive=0.1, lsb=lsb)
    h=D(h, rect(xl-60,-50,xr+80,p.it+30))
    # exit flick: stem bends right at the baseline
    f=B().M(xl, p.it+40).L(xl, X*0.18)
    f.C(xl, X*0.02, xl+30, -o, xl+80, -o)
    f.C(xl+120, -o, xr+40, X*0.04, xr+62, X*0.13)
    f.L(xr+46, X*0.16)
    f.C(xr+30, X*0.10, xr+16, X*0.08, xr, X*0.12)
    f.L(xr, p.it+40).Z()
    return U(h, f.path(), rect(xl, p.it, xr, p.it+60)), xr+62+rsb

def k_gold(p, top=760, lsb=22, rsb=34):
    """two-colour: complete n in ink; I (above the shoulder + head) in gold, sharing the n's right leg."""
    S=p.S; X=p.X; cw=p.cw
    x0=lsb+p.fe
    arch,xs,xl,xr=n_full_arch(p,x0,cw)
    n_ink=U(n_left(p,x0), arch, rect(xl,0,xr,X*0.66), cap_slab(p,xl,xr,0,False))
    I_g=D(U(rect(xl,X*0.5,xr,top), cap_slab(p,xl,xr,top,True)), n_ink)
    return n_ink, I_g, xr+p.ie+rsb

p=P()
V_,vw=g_V(p); a,aw=g_a(p); n,nw=g_n(p); I,iw=g_I(p); d,dw=g_d(p); r,rw=g_r(p)
def word(h,hw):
    return place([(V_,vw,0),(a,aw,-78),(h,hw,-6),(n,nw,-14),(d,dw,-8),(r,rw,-6),(a,aw,-36)])
variants=[
 ('K1 trunk: thick high branch, I 760', k_trunk(p)),
 ('K2 rise: narrow I (0.62) out of shoulder, centred', k_rise(p)),
 ('K3 rise: I 0.72 left-aligned', k_rise(p,Iw=0.72,align='l')),
 ('K4 rise: I 0.72 right-aligned, top 780', k_rise(p,Iw=0.72,align='r',top=780)),
 ('K5 flick foot (n) + slab head (I)', k_flick(p)),
]
body=''; y=0
for lab,(h,hw) in variants:
    y+=900
    w,_=word(h,hw)
    body+=f'<path d="{to_svg_d(w,1,40,y)}" fill="#0B2A20"/><text x="3300" y="{y}" font-size="60">{lab}</text>'
    body+=f'<path d="{to_svg_d(w,0.12,3300,y-300)}" fill="#0B2A20"/>'
    body+=f'<path d="{to_svg_d(w,0.06,3300,y-150)}" fill="#0B2A20"/>'
# gold
y+=900
ni,ig,hw=k_gold(p)
w,_=word(ni,hw)
body+=f'<path d="{to_svg_d(w,1,40,y)}" fill="#0B2A20"/><text x="3300" y="{y}" font-size="60">K6 two-colour</text>'
# place gold at hinge offset
off=vw+aw-78-6
body+=f'<path d="{to_svg_d(T(ig,off,0),1,40,y)}" fill="#A8843A"/>'
open('work/hinge3.svg','w').write(vt.svg_doc(4300,y+120,body,bg='#F6F1E7'))
