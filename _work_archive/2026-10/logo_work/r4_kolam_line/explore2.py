import math, sys
sys.path.insert(0, '.')
from kolam import *
S3 = math.sqrt(3)

def V(n_arm, dx, dy):
    """dots of a V: arm k=0..n_arm (k=0 is vertex)."""
    d = {'B': (0, 0)}
    for k in range(1, n_arm + 1):
        d[f'L{k}'] = (-k * dx, k * dy); d[f'R{k}'] = (k * dx, k * dy)
    return d

def seq_of(D, spec, r):
    out = []
    for tok in spec.split():
        name, s = tok[:-1], (+1 if tok[-1] == '+' else -1)
        rr = r
        if '@' in name:
            name, rr = name.split('@'); rr = float(rr)
        out.append((D[name], rr, s))
    return out

V_ = []
def add(name, D, spec, r, w=0.09, rd=0.1, dots=None):
    V_.append((name, D, spec, r, w, rd, dots))

D2 = V(2, 0.5, 1.0)          # slope-2 lattice (opening 53 deg)
D60 = V(2, 0.5, S3 / 2)      # 60 deg
D3 = V(3, 0.5, 1.0)
add('S1 skip-under slope2', D2, 'L2+ L1- B+ R1- R2+ R1- L1-', 0.36)
add('S1 skip-under 60', D60, 'L2+ L1- B+ R1- R2+ R1- L1-', 0.33)
add('S2 skip-over slope2', D2, 'L2+ L1- B+ R1- R2+ R1+ L1+', 0.36)
add('S3 full rope r.3', D2, 'L2+ L1- B+ R1- R2+ R1- B+ L1-', 0.30)
add('S4 7-dot skip', D3, 'L3+ L2- L1+ B- R1+ R2- R3+ R2- R1- L1- L2-', 0.36)
add('S5 7-dot skip alt', D3, 'L3+ L2- L1+ B- R1+ R2- R3+ R2- R1+ L1+ L2-', 0.36)
add('S6 inner-only weave', D2, 'L2- L1+ B- R1+ R2- R1- L1-'.replace('R1- L1-','R1+ L1+'), 0.36)
add('S7 caps big, B small', D2, 'L2@0.42+ L1@0.3- B@0.3+ R1@0.3- R2@0.42+ R1@0.3- L1@0.3-', 0.3)
add('S8 vertex only rope', D2, 'L2+ B- R2+ R1+ L1+', 0.36)
add('S9 outer belt + inner weave', D2, 'L2- L1+ B- R1+ R2- B+'.replace(' B+',''), 0.36)
add('S10 skip-under r.42', D2, 'L2+ L1- B+ R1- R2+ R1- L1-', 0.42)
add('S11 skip-under 60 r.4', D60, 'L2+ L1- B+ R1- R2+ R1- L1-', 0.40)

W = 300; cols = 4; body = ''
for idx, (name, D, spec, r, w, rd, dots) in enumerate(V_):
    seq = seq_of(D, spec, r)
    try:
        segs = build(seq)
    except Exception as e:
        print(name, 'fail', e); continue
    line = outline(segs, w)
    used = sorted(set(t[:-1].split('@')[0] for t in spec.split()))
    dp = dots_path([D[k] for k in used], rd)
    allp = vtype.union(line, dp)
    s, tx, ty = fit(allp, (W, W), 0.12)
    cx, cy = (idx % cols) * W, (idx // cols) * (W + 30)
    body += f'<g transform="translate({cx},{cy})"><rect width="{W}" height="{W}" fill="#F6F1E7" stroke="#ccc"/>'
    body += f'<path d="{vtype.to_d(tf(line, s, tx, ty))}" fill="#0B2A20"/>'
    body += f'<path d="{vtype.to_d(tf(dp, s, tx, ty))}" fill="#A8843A"/>'
    body += f'<text x="8" y="{W+20}" font-family="sans-serif" font-size="14">{name}</text></g>'
rows = (len(V_) + cols - 1) // cols
open('explore1.svg', 'w').write(vtype.svg_doc(cols * W, rows * (W + 30), body, bg='#ffffff'))
