import subprocess, os
from geo import *
from mono4 import va4
import loop1_mono
from loop1_mono import card
loop1_mono.OUT = 'loop6'; os.makedirs('loop6', exist_ok=True)
cs = []
cs.append(card('G1', va4()[0], 'two strokes: sweeping blade into the danda'))
cs.append(card('G2', va4(yj=0.94, wj=26)[0], 'blade lands near the foot'))
cs.append(card('G3', va4(yj=0.78, wj=20, oc1=(0.05, 0.5), oc2=(0.45, 0.85))[0], 'fuller sweep, higher landing'))
cs.append(card('G4', va4(straight=True, yj=0.88, wj=24)[0], 'straight wedge into danda'))
cs.append(card('G5', va4(yj=0.86, wj=24, bindu='stem')[0], 'G1 + bindu (vam)'))
cs.append(card('G6', va4(yj=0.86, wj=22, xs=66, oc1=(0.0, 0.55), oc2=(0.5, 0.95), ic1=(0.35, 0.35), ic2=(0.8, 0.62))[0], 'wider, rounder bowl'))
cs.append(card('G7', va4(yj=0.86, wj=22, xs=54, S=16)[0], 'narrow'))
cs.append(card('G8', va4(yj=0.86, wj=24, b=12, S=16, ovl=8, ovr=8)[0], 'heavier, symmetric overhang'))
cs.append(card('G9', va4(yj=0.86, wj=24, b=8, S=13, t0=3, ovl=14, ovr=6)[0], 'light'))
subprocess.run(['node', '../toolkit/render.js', 'sheet', 'loop6_mono.png'] + cs, check=True)
