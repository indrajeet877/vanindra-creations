import sys; sys.path.insert(0,'.')
from vitype import *
EM='#0B2A20'; IV='#F6F1E7'; GD='#A8843A'
pd=P(**DISPLAY)
wm=wordmark(pd); cr=creations(pd)
body=''
body+=f'<path d="{to_svg_d(wm["ink"],1,60,900)}" fill="{EM}"/><path d="{to_svg_d(wm["I"],1,60,900)}" fill="{EM}"/>'
body+=f'<path d="{to_svg_d(cr["ink"],1,60,1900)}" fill="{EM}"/>'
# small proof of individual new glyphs
x=60
for fn in [g_C,g_e,g_s,g_t,g_i,g_o]:
    g,w=fn(pd); body+=f'<path d="{to_svg_d(g,1.6,x,3300)}" fill="{EM}"/>'; x+=w*1.6+40
open('work/proof2.svg','w').write(vt.svg_doc(4200,3420,body,bg=IV))
