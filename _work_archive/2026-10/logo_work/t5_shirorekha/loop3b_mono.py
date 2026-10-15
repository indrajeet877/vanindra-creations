import subprocess, os
from geo import *
from mono2 import va2
import loop1_mono
from loop1_mono import card
loop1_mono.OUT = 'loop3b'; os.makedirs('loop3b', exist_ok=True)
cs = []
cs.append(card('D1', va2(bo=6, bi=-14, t0=5)[0], 'swelling stroke (inner edge bows in)'))
cs.append(card('D2', va2(bo=8, bi=-18, t0=4, S=14)[0], 'more swell, lighter danda'))
cs.append(card('D3', va2(bo=6, bi=-16, t0=5, py=90, yj=0.5, xs=62, px=37)[0], 'swell + lifted bowl'))
cs.append(card('D4', va2(bo=6, bi=-16, t0=5, py=90, yj=0.5, xs=62, px=37, b=11, S=15, ovl=15)[0], 'lifted, heavier headline'))
cs.append(card('D5', va2(bo=4, bi=-20, t0=6, py=90, yj=0.5, xs=62, px=37, b=10, S=15, h=4.2, bindu='stem')[0], 'lifted + bindu'))
cs.append(card('D6', va2(bo=0, bi=-18, t0=6, b=10, S=15, h=4.2)[0], 'straight outer, swelling inner'))
cs.append(card('D7', va2(bo=8, bi=-14, t0=5, py=94, yj=0.55, xs=62, px=37, b=10, S=15, h=4.4, ovl=14, ovr=5)[0], 'mid'))
cs.append(card('D8', va2(bo=6, bi=-16, t0=5, py=90, yj=0.5, xs=62, px=37, b=10, S=15, h=4.4, ovl=24, ovr=5)[0], 'long left headline'))
cs.append(card('D9', va2(bo=6, bi=-16, t0=5, py=90, yj=0.5, xs=62, px=37, b=10, S=15, h=4.4, ovl=10, ovr=10)[0], 'symmetric overhang'))
subprocess.run(['node', '../toolkit/render.js', 'sheet', 'loop3b_mono.png'] + cs, check=True)
