import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pen as P, sig
from explore import place, label, RENDER
WPEN = dict(hair=4.2, shade=17.0)
MPEN = dict(hair=6.5, shade=25.0)
def wpath(cfg=None, pk=None):
    S, c = sig.wordmark_strokes(cfg)
    k = dict(WPEN); k.update(pk or {})
    return P.render(S, P.Pen(slant=c['slant'], **k))
def mpath(cfg=None, pk=None, boost=0):
    S, c = sig.mark_strokes(cfg)
    k = dict(MPEN); k.update(pk or {})
    return P.render(S, P.Pen(slant=c['slant'], **k), hair_boost=boost)
def view(rows, out, W=1500):
    body = ''; y = 20
    for name, cfg in rows:
        body += place(wpath(cfg), (260, y, W - 300, 300)) + place(mpath(cfg), (20, y + 40, 220, 220))
        body += label(name, 20, y + 300, 18, '#555')
        y += 330
    open(out + '.svg', 'w').write(P.vtype.svg_doc(W, y, body, bg='#F6F1E7'))
    subprocess.run(['node', RENDER, 'png', out + '.svg', out + '.png', str(W)], check=True)
if __name__ == '__main__':
    view([('base', {}), ('lift 0, turn 18', dict(can_lift=0, can_turn=18)), ('rise .64 k .6 lift 16', dict(can_rise=.64, can_k=.6, can_lift=16))], 'view1')
