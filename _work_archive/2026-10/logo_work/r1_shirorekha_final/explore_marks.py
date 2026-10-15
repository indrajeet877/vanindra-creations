"""Mark study: from T5's bar-hung leaf (reads as pa in a Devanagari word) to a leaf-loop hung from the danda
(reads as va; its counter is a V). -> explore_marks.png"""
import subprocess
from r3geo import *
from r3mark import va_mark, va_loop, va_trueloop, va_cloop
import vtype as V
OUT = os.path.join(HERE, 'explore'); os.makedirs(OUT, exist_ok=True)
def ref(ch, fam, w=400):
    t = V.text_path(ch, family=fam, weight=w, subset='devanagari', size=100)
    n = V.text_path('न', family=fam, weight=w, subset='devanagari', size=100)
    top = -n.bounds[1]; s = 100/top
    return tr(t.path, s, 0, top*s)
cells = [
  ('M1 T5 lineage: leaf hung from the line (V strong; = pa topology)', va_mark(px=26, py=87, yj=0.48, h=8.5, leaf=dict(ko1=11, ko2=9, ki1=-1, ki2=-18))[0]),
  ('M2 open notch (reads as a glitch)', va_mark(notch=6.0, px=26, py=87, yj=0.48, h=8.5, leaf=dict(ko1=11, ko2=9, ki1=-1, ki2=-18))[0]),
  ('M3 gap under the line (still pa in a word)', va_mark(gap=8.0, px=26, py=87, yj=0.48, h=8.5, leaf=dict(t0=6, ko1=11, ko2=9, ki1=-1, ki2=-18))[0]),
  ('M4 rounded lower third (drifts to pa U)', va_loop()[0]),
  ('M5 true loop, straight lid (va; pennant risk)', va_trueloop(top=(2.0,30.0), jt=26.0)[0]),
  ('M6 one-stroke loop, thin (va; weak)', va_cloop()[0]),
  ('M7 one-stroke loop, leaf belly (va; reads a)', va_cloop(jt=24, ht=5.5, o1=(-13,-1), o2=(-12,0.56), i1=(12,0), i2=(14,0.73), P=(26,89), yj=0.55, h=9.5)[0]),
  ('M8 leaf-loop, V counter  <- chosen', va_cloop(jt=20, ht=5, o1=(-8,-3), o2=(-12,0.5), i1=(0,0), i2=(18,0.5), P=(28,92), yj=0.56, h=10)[0]),
  ('ref: Martel 700 va / Rozha pa', None),
]
files=[]
for i,(lab,g) in enumerate(cells):
    layers=[]
    if g is None:
        a = ref('व','martel',700); b = ref('प','rozha-one',400)
        ab=bbox(a); bb=bbox(b)
        layers += [(tr(a,2.2,60-ab[0]*2.2,60),'#777'),(tr(b,2.2,300-bb[0]*2.2,60),'#777')]
    else:
        x0,y0,x1,y1=bbox(g); s=230/(y1-y0)
        layers.append((tr(g,s,190-x0*s,40-y0*s),EM))
        for k,sz in enumerate([32,20]):
            q=sz/(y1-y0); layers.append((tr(g,q,470+k*50-x0*q,240-y0*q),EM))
    t = V.text_path(lab, family='manrope', weight=500, size=17, x=24, y=330)
    layers.append((t.path,'#6b5a35'))
    files.append(write(os.path.join(OUT,f'M{i+1}.svg'), svg(600,350,layers,bg=IV)))
subprocess.run(['node', os.path.join(SCRATCH,'logo2','toolkit','render.js'),'sheet',os.path.join(HERE,'explore_marks.png')]+files, check=True)
