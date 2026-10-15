import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import vtype as V
body=''
x=20
for fam,w in [('rozha-one',400),('tiro-devanagari-hindi',400),('noto-serif-devanagari',500),('martel',300),('gotu',400)]:
    t = V.text_path('व', family=fam, weight=w, subset='devanagari', size=300, x=x, y=300)
    body += f'<path d="{t.d}" fill="#0B2A20"/>'
    x += 260
y=480
for fam,w,st in [('bodoni-moda',500,'normal'),('jost',400,'normal'),('cormorant-garamond',500,'normal'),('fraunces',400,'normal')]:
    t = V.text_path('vanindra VANINDRA', family=fam, weight=w, style=st, size=90, x=20, y=y)
    body += f'<path d="{t.d}" fill="#0B2A20"/>'
    y+=110
open('study/va.svg','w').write(V.svg_doc(1400, y, body, bg='#F6F1E7'))
