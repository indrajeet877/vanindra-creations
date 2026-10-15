import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import vtype as V
fams = [('rozha-one',400),('tiro-devanagari-hindi',400),('noto-serif-devanagari',600),('noto-serif-devanagari',300),('yatra-one',400),('martel',800),('gotu',400)]
body=''
y=140
for fam,w in fams:
    t = V.text_path('व  वनिंद्रा  वनिन्द्रा', family=fam, weight=w, subset='devanagari', size=110, x=30, y=y)
    body += f'<path d="{t.d}" fill="#0B2A20"/>'
    lt = V.text_path(fam, family='jost', weight=400, size=18, x=1150, y=y-40)
    body += f'<path d="{lt.d}" fill="#A8843A"/>'
    y += 160
open('study/deva.svg','w').write(V.svg_doc(1400, y, body, bg='#F6F1E7'))
