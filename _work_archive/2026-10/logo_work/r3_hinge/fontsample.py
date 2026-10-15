import sys
S='/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad'
sys.path.insert(0, S+'/logo2/toolkit')
import vtype as vt
fonts=[('cormorant-garamond',600,'normal'),('cormorant',600,'normal'),('fraunces',400,'normal'),('fraunces',600,'normal'),
('playfair-display',500,'normal'),('dm-serif-display',400,'normal'),('gloock',400,'normal'),('libre-caslon-display',400,'normal'),
('marcellus',400,'normal'),('tenor-sans',400,'normal'),('manrope',500,'normal'),('outfit',400,'normal'),('bodoni-moda',500,'normal'),('forum',400,'normal'),('syne',500,'normal')]
body='';y=110
for f,w,s in fonts:
    t=vt.text_path('VanIndra handle', family=f, weight=w, style=s, size=100, x=30, y=y)
    body+=f'<path d="{t.d}" fill="#0B2A20"/><text x="900" y="{y}" font-size="20">{f} {w}</text>'
    y+=130
open('work/fontsample.svg','w').write(vt.svg_doc(1200,y,body,bg='#F6F1E7'))
