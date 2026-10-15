import subprocess, os
from geo import *
from mono2 import va2
import loop1_mono
from loop1_mono import card
loop1_mono.OUT = 'loop3'; os.makedirs('loop3', exist_ok=True)
cs = []
cs.append(card('C1', va2()[0], 'crescent stroke, pointed foot on baseline'))
cs.append(card('C2', va2(bo=16, bi=6, t0=3.5)[0], 'fuller crescent'))
cs.append(card('C3', va2(py=86, yj=0.48, px=36, xs=60)[0], 'lifted bowl (truer va)'))
cs.append(card('C4', va2(bo=14, bi=5, bindu='stem')[0], 'crescent + bindu (vam)'))
cs.append(card('C5', va2(b=11, S=16, h=4.5, bo=13, bi=5, t0=6, ovl=16)[0], 'heavier headline, long left'))
cs.append(card('C6', va2(b=7, S=13, h=3, bo=13, bi=4, t0=3, ovl=10, ovr=4)[0], 'light'))
cs.append(card('C7', va2(px=34, xs=56, yj=0.62, bo=12, bi=4)[0], 'narrow, low junction'))
cs.append(card('C8', va2(px=40, xs=70, yj=0.5, bo=10, bi=3, h=4.2)[0], 'wide, high junction'))
cs.append(card('C9', va2(bo=14, bi=5, bindu='centre')[0], 'bindu centred'))
subprocess.run(['node', '../toolkit/render.js', 'sheet', 'loop3_mono.png'] + cs, check=True)
