import subprocess, os
from geo import *
from mono3 import va3
import loop1_mono
from loop1_mono import card
loop1_mono.OUT = 'loop5'; os.makedirs('loop5', exist_ok=True)
cs = []
cs.append(card('F1', va3()[0], 'point on baseline, junction 0.5'))
cs.append(card('F2', va3(qh=0.76, t0=4)[0], 'smaller solid tip'))
cs.append(card('F3', va3(py=92, yj=0.48, qh=0.66)[0], 'lifted point (pennant risk)'))
cs.append(card('F4', va3(px=40, xs=66, yj=0.56, qh=0.72, S=14, b=9.5)[0], 'wider V, lighter danda'))
cs.append(card('F5', va3(px=40, xs=66, yj=0.56, qh=0.72, S=14, b=9.5, bindu='stem')[0], 'F4 + bindu'))
cs.append(card('F6', va3(px=40, xs=66, yj=0.56, qh=0.72, S=14, b=9.5, ovl=4, ovr=4)[0], 'F4, short overhangs'))
cs.append(card('F7', va3(px=40, xs=66, yj=0.56, qh=0.72, S=14, b=9.5, ovl=20, ovr=4)[0], 'F4, long left'))
cs.append(card('F8', va3(px=42, xs=72, yj=0.62, qh=0.74, S=14, b=9.5, h=4.0)[0], 'wide, low junction'))
cs.append(card('F9', va3(px=38, xs=60, yj=0.44, qh=0.70, S=15, b=10)[0], 'narrow, high junction'))
subprocess.run(['node', '../toolkit/render.js', 'sheet', 'loop5_mono.png'] + cs, check=True)
