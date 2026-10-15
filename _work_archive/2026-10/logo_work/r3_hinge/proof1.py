import sys; sys.path.insert(0,'.')
from vitype import *
EM='#0B2A20'; IV='#F6F1E7'; GD='#A8843A'
pd=P(**DISPLAY); ps=P(**SMALL)
wm=wordmark(pd); cr=creations(pd)
body=''
body+=f'<path d="{to_svg_d(wm["ink"],1,60,900)}" fill="{EM}"/><path d="{to_svg_d(wm["I"],1,60,900)}" fill="{EM}"/>'
body+=f'<path d="{to_svg_d(cr["ink"],1,60,1900)}" fill="{EM}"/>'
pw=P(**DISPLAY, r_term='wedge'); wm2=wordmark(pw)
body+=f'<path d="{to_svg_d(wm2["ink"],1,60,2900)}" fill="{EM}"/><path d="{to_svg_d(wm2["I"],1,60,2900)}" fill="{GD}"/>'
wms=wordmark(ps)
body+=f'<path d="{to_svg_d(wms["ink"],1,60,3900)}" fill="{EM}"/><path d="{to_svg_d(wms["I"],1,60,3900)}" fill="{EM}"/>'
body+=f'<text x="3300" y="900" font-size="50">display</text><text x="3300" y="2900" font-size="50">display, wedge r, gold I</text><text x="3300" y="3900" font-size="50">small cut</text>'
open('work/proof1.svg','w').write(vt.svg_doc(4200,4050,body,bg=IV))
