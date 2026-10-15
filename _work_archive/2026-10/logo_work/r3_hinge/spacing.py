import sys; sys.path.insert(0,'.')
from vitype import *
from glyphkit import rect
def spans(path, y):
    band=vt.intersection(path, rect(-1e5,y-0.5,1e5,y+0.5))
    return sorted((c.bounds[0],c.bounds[2]) for c in band.contours)
for name,p in [('display',P(**DISPLAY)),('small',P(**SMALL))]:
    wm=wordmark(p); allp=U(wm['ink'],wm['I'])
    for frac in (0.25,0.5):
        sp=spans(allp,p.X*frac)
        gaps=[round(b[0]-a[1]) for a,b in zip(sp,sp[1:])]
        print(name, frac, 'ink spans:',len(sp),'gaps:',gaps)
