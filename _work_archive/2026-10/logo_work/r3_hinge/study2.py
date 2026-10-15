import sys; sys.path.insert(0,'.')
from gk2 import *
p=P()
V_,vw=g_V(p); a,aw=g_a(p); n,nw=g_n(p); I,iw=g_I(p); d,dw=g_d(p); r,rw=g_r(p)
rows=[]
def word(h,hw):
    return place([(V_,vw,0),(a,aw,-78),(h,hw,-6),(n,nw,-14),(d,dw,-8),(r,rw,-6),(a,aw,-36)])
plain,_=place([(V_,vw,0),(a,aw,-78),(n,nw,-6),(I,iw,-10),(n,nw,-10),(d,dw,-8),(r,rw,-6),(a,aw,-36)])
variants=[('H1 land .80 spring',dict(land=0.80,arrive=0.0)),('H2 land .62 arrive .4',dict(land=0.62,arrive=0.4)),
          ('H3 land .48 tangent',dict(land=0.48,arrive=0.9)),('H4 land .62, I top 760',dict(land=0.62,arrive=0.4,top=760)),
          ('H5 land .70 arrive .2, I 740',dict(land=0.70,arrive=0.2,top=740))]
body=''; y=760
body+=f'<path d="{to_svg_d(plain,1,40,y)}" fill="#0B2A20"/><text x="3300" y="{y}" font-size="60">plain (no hinge)</text>'
for lab,kw in variants:
    y+=900
    h,hw,_=g_hinge(p,**kw)
    w,_=word(h,hw)
    body+=f'<path d="{to_svg_d(w,1,40,y)}" fill="#0B2A20"/><text x="3300" y="{y}" font-size="60">{lab}</text>'
    # small read test
    body+=f'<path d="{to_svg_d(w,0.12,4300,y-300)}" fill="#0B2A20"/>'
    body+=f'<path d="{to_svg_d(w,0.06,4300,y-150)}" fill="#0B2A20"/>'
open('work/study2.svg','w').write(vt.svg_doc(4800,y+120,body,bg='#F6F1E7'))
