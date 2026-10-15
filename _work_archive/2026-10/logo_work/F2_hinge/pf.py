"""proof helpers: lay out paths, write svg, render png."""
import sys, subprocess, os
sys.path.insert(0,'.')
from vitype import *
HERE=os.path.dirname(os.path.abspath(__file__))
def bb(*ps):
    bs=[vt.bounds(p) for p in ps if p is not None]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))
def row_svg(rows, unit=0.25, pad=30, bg='#F6F1E7', gap=40, width=None):
    """rows: list of list of (path, colour) groups placed left to right; each row is one line"""
    body=''; y=pad; W=0
    for r in rows:
        allp=[p for p,c in r if p is not None]
        b=bb(*allp); h=(b[3]-b[1])*unit
        dx=pad-b[0]*unit; dy=y+b[3]*unit
        for p,c in r:
            if p is None: continue
            body+=f'<path d="{to_svg_d(p,unit,dx,dy)}" fill="{c}"/>'
        W=max(W,(b[2]-b[0])*unit+2*pad); y+=h+gap
    W=width or W
    return vt.svg_doc(round(W),round(y-gap+pad),body,bg=bg)
def png(svgtext, out, width=None):
    f=out.replace('.png','.svg'); open(f,'w').write(svgtext)
    import re
    w=width or int(float(re.search(r'width="([\d.]+)"',svgtext).group(1)))
    subprocess.run(['node',HERE+'/../toolkit/render.js','png',f,out,str(w)],check=True)
