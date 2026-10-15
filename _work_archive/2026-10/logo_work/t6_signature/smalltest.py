import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, mono
from explore import place, RENDER
def mk(strokes, name, boost=0.0, hair=4.2, shade=17, slant=18, pad=0.14, bg=None, ink='#0B2A20'):
    pth = P.render(strokes, P.Pen(slant=slant, hair=hair, shade=shade), hair_boost=boost)
    S = 512; m = S * pad
    body = place(pth, (m, m, S - 2 * m, S - 2 * m), ink)
    open(name, 'w').write(P.vtype.svg_doc(S, S, body, bg=bg))
    return name
if __name__ == '__main__':
    os.makedirs('tmp', exist_ok=True)
    for key, S in [('A', mono.m_canopy({}, rise=.6)), ('F', mono.m_canopy({}, rise=.75, rc=30, foot='ball')),
                   ('H', mono.m_canopy({}, rise=.6, dIs=50, apex=272, foot='ball'))]:
        for b in (0, 6):
            f = mk(S, f'tmp/s_{key}_{b}.svg', boost=b)
            subprocess.run(['node', RENDER, 'sizes', f'tmp/sizes_{key}_{b}.png', f], check=True)
