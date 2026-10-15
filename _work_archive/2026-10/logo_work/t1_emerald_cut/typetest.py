import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *

BOD = os.path.join(FONT_DIR, 'bodoni-moda-variable', 'package', 'files', 'bodoni-moda-latin-standard-normal.woff2')
rows = []
y = 90
body = ''
for opsz, wg in [(11, 450), (18, 500), (28, 500), (48, 520), (11, 560)]:
    t = text_path('VANINDRA', file=BOD, size=80, x=30, y=y, tracking=0.16, variations={'opsz': opsz, 'wght': wg})
    body += pth_c(t.path, EM)
    lab = text_path(f'opsz {opsz} wght {wg}', family='jost', weight=400, size=14, x=760, y=y - 30)
    body += pth_c(lab.path, GO)
    y += 110
for fam, w, tr in [('jost', 400, 0.42), ('tenor-sans', 400, 0.42), ('manrope', 500, 0.42), ('marcellus', 400, 0.38)]:
    t = text_path('CREATIONS', family=fam, weight=w, size=26, x=30, y=y, tracking=tr)
    body += pth_c(t.path, EM)
    lab = text_path(f'{fam} {w}', family='jost', weight=400, size=14, x=760, y=y - 10)
    body += pth_c(lab.path, GO)
    y += 50
open('typetest.svg', 'w').write(svg_doc(1000, y + 20, body, IV))
