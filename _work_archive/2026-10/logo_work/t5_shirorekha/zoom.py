import sys, subprocess
from geo import *
# crop a card svg region into a new svg: re-render card file with viewBox crop
src, out, x, y, w, h, px = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:8])
s = open(src).read()
import re
s = re.sub(r'viewBox="[^"]+" width="[^"]+" height="[^"]+"', f'viewBox="{x} {y} {w} {h}" width="{w}" height="{h}"', s, count=1)
open('study/_crop.svg', 'w').write(s)
subprocess.run(['node', '../toolkit/render.js', 'png', 'study/_crop.svg', out, str(int(px))], check=True)
