import sys; sys.path.insert(0,'.')
from glyphkit import *
p=P()
items=[]
V_,vw=g_V(p); a,aw=g_a(p); n,nw=g_n(p); I,iw=g_I(p); d,dw=g_d(p); r,rw=g_r(p)
h,hw,_=g_hinge(p)
word,ww=place([(V_,vw,0),(a,aw,-60),(h,hw,-10),(n,nw,0),(d,dw,0),(r,rw,0),(a,aw,-30)])
plain,pw=place([(V_,vw,0),(a,aw,-60),(n,nw,-10),(I,iw,0),(n,nw,0),(d,dw,0),(r,rw,0),(a,aw,-30)])
body=f'<path d="{to_svg_d(word,1,40,800)}" fill="#0B2A20"/>'
body+=f'<path d="{to_svg_d(plain,1,40,1700)}" fill="#0B2A20"/>'
# glyph proof row
x=40
for g,w in [(V_,vw),(a,aw),(n,nw),(I,iw),(d,dw),(r,rw),(h,hw)]:
    body+=f'<path d="{to_svg_d(g,0.5,x,2300)}" fill="#0B2A20"/>'; x+=w*0.5+30
open('work/study1.svg','w').write(vt.svg_doc(3200,2400,body,bg='#F6F1E7'))
