import subprocess, os
from geo import *
from mono2 import va2
import loop1_mono
from loop1_mono import card
loop1_mono.OUT = 'loop8'; os.makedirs('loop8', exist_ok=True)
base = dict(t0=4.5, py=90, yj=0.5, xs=62, px=37, b=9.6, S=15, h=4.4, ovl=12, ovr=7)
cs = []
cs.append(card('H1', va2(bo=6, bi=-18, **base)[0], 'current'))
b2 = dict(base); 
cs.append(card('H2', va2(bo=10, bi=-16, **base)[0], 'leaf: both edges convex'))
cs.append(card('H3', va2(bo=13, bi=-14, **base)[0], 'fuller leaf'))
b4 = dict(base, px=38, xs=64, yj=0.52)
cs.append(card('H4', va2(bo=10, bi=-18, **b4)[0], 'leaf, slightly wider'))
b5 = dict(base, h=5.2, S=14.5)
cs.append(card('H5', va2(bo=10, bi=-17, **b5)[0], 'leaf, firmer hairline, lighter danda'))
b6 = dict(base, ovl=9, ovr=9)
cs.append(card('H6', va2(bo=10, bi=-16, **b6)[0], 'leaf, equal overhang'))
b7 = dict(base, py=86, yj=0.47)
cs.append(card('H7', va2(bo=10, bi=-16, **b7)[0], 'leaf, higher tip'))
b8 = dict(base, py=94, yj=0.54)
cs.append(card('H8', va2(bo=10, bi=-16, **b8)[0], 'leaf, lower tip'))
b9 = dict(base, b=11, S=16, h=5)
cs.append(card('H9', va2(bo=10, bi=-17, **b9)[0], 'leaf, heavier frame'))
subprocess.run(['node', '../toolkit/render.js', 'sheet', 'loop8_mono.png'] + cs, check=True)
