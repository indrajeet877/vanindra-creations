import subprocess, os
from geo import *
from mono import va_mark
from loop1_mono import card
import loop1_mono
loop1_mono.OUT = 'loop2'; os.makedirs('loop2', exist_ok=True)
cs = []
base = dict(b=10, S=16, Td=17, h=4.0, ovl=14, ovr=6)
cs.append(card('N1', va_mark(yb=1.0, yj=0.55, **base)[0], 'lighter bar, point on baseline'))
cs.append(card('N2', va_mark(yb=0.86, yj=0.50, vx=38, **base)[0], 'bowl lifted above baseline (truer va)'))
cs.append(card('N3', va_mark(yb=0.86, yj=0.50, vx=38, curve=9, **base)[0], 'lifted + bowed bowl'))
cs.append(card('N4', va_mark(yb=0.86, yj=0.50, vx=38, bindu='stem', **base)[0], 'lifted + bindu (vam)'))
cs.append(card('N5', va_mark(yb=1.0, yj=0.58, curve=8, bindu='stem', **base)[0], 'bowed, baseline point, bindu'))
cs.append(card('N6', va_mark(yb=0.92, yj=0.62, vx=40, b=8, S=15, Td=16, h=3.4, ovl=18, ovr=4)[0], 'hairline-ish bar, long left headline'))
cs.append(card('N7', va_mark(yb=0.9, yj=0.55, vx=40, b=12, S=15, Td=15, h=7.5, ovl=10, ovr=5)[0], 'low contrast wrap'))
cs.append(card('N8', va_mark(yb=0.8, yj=0.42, vx=36, b=10, S=16, Td=17, h=4, ovl=12, ovr=6)[0], 'short bowl, tall danda'))
cs.append(card('N9', va_mark(yb=1.0, yj=0.62, vx=42, b=10, S=16, Td=17, h=4, ovl=12, ovr=6, bindu='centre')[0], 'baseline point, bindu centred'))
subprocess.run(['node', '../toolkit/render.js', 'sheet', 'loop2_mono.png'] + cs, check=True)
