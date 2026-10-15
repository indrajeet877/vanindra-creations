import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, mono
from smalltest import mk
from explore import RENDER
fs = []
for key, S in [('A', mono.m_canopy({}, rise=.6)), ('H', mono.m_canopy({}, rise=.6, dIs=50, apex=272, foot='ball')),
               ('crook', mono.m_crook({}))]:
    for (h, s) in ((8, 30), (11, 36)):
        f = mk(S, f'tmp/h_{key}_{h}.svg', hair=h, shade=s, pad=0.1)
        subprocess.run(['node', RENDER, 'sizes', f'tmp/hs_{key}_{h}.png', f], check=True)
        fs.append(f'tmp/hs_{key}_{h}.png')
subprocess.run(['node', 'stack.js', 'tmp/hs_all.png'] + fs, check=True)
