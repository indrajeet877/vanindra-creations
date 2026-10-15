import sys, subprocess
sys.path.insert(0, '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/toolkit')
import vtype
fams = ['pinyon-script', 'great-vibes', 'allura', 'italianno', 'parisienne', 'mrs-saint-delafield', 'monsieur-la-doulaise']
body = ''; y = 150
for f in fams:
    t = vtype.text_path('VanIndra', family=f, size=150, x=30, y=y)
    body += f'<path d="{t.d}" fill="#0B2A20"/><text x="900" y="{y-20}" font-size="20" font-family="sans-serif">{f}</text>'
    y += 170
open('ref.svg', 'w').write(vtype.svg_doc(1100, y, body, bg='#fff'))
subprocess.run(['node', '../toolkit/render.js', 'png', 'ref.svg', 'ref.png', '1100'])
