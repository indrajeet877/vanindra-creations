import os, subprocess
from mark import *
EM, IV = PALETTE['emerald'], PALETTE['ivory']
os.makedirs('small_test2', exist_ok=True)
C = {
  'K3_stones': build2(s=0.40, h=60.0, K=3, NL=2, g=7.0, tw=20.0, gold=()),
  'E_solid': build2(s=0.40, h=60.0, K=4, NL=2, g=7.0, tw=20.0, gold=(), small=True, tw_small=20, fuse=False),
  'F_knot_K4': build_small_knot(K=4),
  'F_knot_K3': build_small_knot(K=3, g=8.0, tw=22.0),
  'G_knot_K4_cut': build_small_knot(K=4, rows_cut=(-2,)),
}
for n, r in C.items():
    (p,), _ = place([r['em']], 1000, 960)
    f = f'small_test2/{n}.svg'
    write_svg(f, 1000, 1000, fill(p, EM))
    subprocess.run(['node', 'zoom.js', f, f'small_test2/{n}.png', IV], check=True)
print('ok')
