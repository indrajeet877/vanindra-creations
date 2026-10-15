import sys; sys.path.insert(0,'.')
from gk2 import *
from hinge3 import n_full_arch

def dilate(path, g):
    q=pathops.Path(path)
    q.stroke(2*g, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    q.convertConicsToQuads()
    return U(path, U(q))

def k_behind(p, top=770, gap=16, lsb=22, rsb=34, Iw=None):
    """Returns (n_part, I_part, advance). The n is complete; the I shares its right leg and rises behind
    the shoulder, separated by a hairline cut that follows the shoulder."""
    S=p.S; X=p.X; cw=p.cw
    x0=lsb+p.fe
    arch,xs,xl,xr=n_full_arch(p,x0,cw)
    leg=U(rect(xl,0,xr,X*0.66), cap_slab(p,xl,xr,0,False))
    n_part=U(n_left(p,x0), arch, leg)
    shoulder=U(arch, rect(xl, X*0.30, xr, X*0.66))
    I_full=U(rect(xl,X*0.3,xr,top), cap_slab(p,xl,xr,top,True))
    I_part=D(I_full, dilate(shoulder, gap)) if gap>0 else D(I_full, n_part)
    return n_part, I_part, xr+p.ie+rsb, (xl,xr)

p=P()
V_,vw=g_V(p); a,aw=g_a(p); n,nw=g_n(p); d,dw=g_d(p); r,rw=g_r(p)
EM='#0B2A20'; IV='#F6F1E7'; GD='#A8843A'; GL='#D2B26A'
def word_parts(np_, ip_, hw):
    items=[(V_,vw,0),(a,aw,-78),(np_,hw,-6),(n,nw,-14),(d,dw,-8),(r,rw,-6),(a,aw,-36)]
    w,ww=place(items)
    off=vw+aw-78-6
    return w, T(ip_,off,0), ww
rows=[('B1 behind, gap 16, I 770, mono',dict(top=770,gap=16),False),
      ('B2 behind, gap 24, I 770, mono',dict(top=770,gap=24),False),
      ('B3 behind, gap 16, I 740, two-colour',dict(top=740,gap=16),True),
      ('B4 behind, gap 0 (abut), I 800, two-colour',dict(top=800,gap=0),True),
      ('B5 behind, gap 20, I 800, mono',dict(top=800,gap=20),False)]
body=''; y=0
for lab,kw,gold in rows:
    y+=920
    np_,ip_,hw,_=k_behind(p,**kw)
    w,ig,ww=word_parts(np_,ip_,hw)
    col = GD if gold else EM
    for sc,dx,dy in [(1,40,y),(0.12,3250,y-330),(0.06,3250,y-170),(0.035,3250,y-60)]:
        body+=f'<path d="{to_svg_d(w,sc,dx,dy)}" fill="{EM}"/><path d="{to_svg_d(ig,sc,dx,dy)}" fill="{col}"/>'
    body+=f'<text x="3250" y="{y+40}" font-size="44" font-family="sans-serif">{lab}</text>'
open('work/hinge4.svg','w').write(vt.svg_doc(4300,y+120,body,bg=IV))
# avatar study
body=''; x=0
for i,(lab,kw,gold) in enumerate(rows):
    np_,ip_,hw,_=k_behind(p,**kw)
    allp=U(np_,ip_); b=vt.bounds(allp); cx=(b[0]+b[2])/2; cy=(b[1]+b[3])/2
    for R,yy in [(260,300),(55,700),(16,820),(8,870)]:
        sc=R*1.15/(b[3]-b[1]); X0=x+300
        body+=f'<circle cx="{X0}" cy="{yy}" r="{R}" fill="{EM}"/>'
        body+=f'<path d="{to_svg_d(np_,sc,X0-cx*sc,yy+cy*sc)}" fill="{IV}"/><path d="{to_svg_d(ip_,sc,X0-cx*sc,yy+cy*sc)}" fill="{GL if gold else IV}"/>'
    x+=620
open('work/avatar4.svg','w').write(vt.svg_doc(x,920,body,bg='#ffffff'))
