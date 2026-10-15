import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import vtype as V
body=''
y=200
for fam,w in [('tiro-devanagari-hindi',400),('noto-serif-devanagari',400),('rozha-one',400),('martel',400)]:
    t = V.text_path('व प ब ष य  वं  वंदना', family=fam, weight=w, subset='devanagari', size=160, x=20, y=y)
    body += f'<path d="{t.d}" fill="#0B2A20"/>'
    y+=230
open('study/vapa.svg','w').write(V.svg_doc(1400, y, body, bg='#F6F1E7'))
