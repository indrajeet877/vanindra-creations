import sys
from geo import *
body=''
y=120
for fam,w in [('jost',400),('manrope',500),('tenor-sans',400),('outfit',300),('marcellus',400),('cormorant-garamond',500)]:
    try:
        t = V.text_path('CREATIONS', family=fam, weight=w, size=60, x=40, y=y, tracking=0.42)
    except Exception as e:
        print(fam, e); continue
    body += f'<path d="{t.d}" fill="#0B2A20"/>'
    l = V.text_path(fam, family='jost', weight=400, size=16, x=900, y=y-20)
    body += f'<path d="{l.d}" fill="#A8843A"/>'
    y += 100
open('study/desc.svg','w').write(V.svg_doc(1200, y, body, bg='#F6F1E7'))
