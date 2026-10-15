import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, sig, build
from explore import RENDER
fs = []
for key, pk, extra in [('a', dict(hair=13, shade=36), {}), ('b', dict(hair=17, shade=42), dict(m_turn=26)),
                       ('c', dict(hair=17, shade=42), dict(m_turn=26, v_hook=False)), ('d', dict(hair=20, shade=46), dict(m_turn=28, v_hook=False, m_dIs=84))]:
    cfg = dict(build.CFG); cfg.update(dict(ball=7.5)); cfg.update(extra)
    S, c = sig.mark_strokes(cfg)
    pth = P.render(S, P.Pen(slant=c['slant'], **pk))
    p, _ = build.optical_centre(pth, (512 * .06, 512 * .06, 512 * .88, 512 * .88))
    f = f'tmp/sm_{key}.svg'
    open(f, 'w').write(P.vtype.svg_doc(512, 512, f'<path d="{P.d_of(p)}" fill="#A8843A"/>'))
    subprocess.run(['node', RENDER, 'sizes', f'tmp/sm_{key}.png', f], check=True)
    fs.append(f'tmp/sm_{key}.png')
subprocess.run(['node', 'stack.js', 'tmp/sm_all.png'] + fs, check=True)
