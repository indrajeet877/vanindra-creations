import sys; sys.path.insert(0,'.')
from build import *
def stacked(ratio, lead, desc_p, desc_ink, ink=EM, icol=EM, bg=IV, unit=0.35):
    b=bbox(WM['ink'],WM['I']); wmw=b[2]-b[0]
    crb=vt.bounds(desc_ink); crw=(crb[2]-crb[0])*ratio
    base2=pd.X*lead+desc_p.C*ratio
    crx=b[0]+(wmw-crw)/2-crb[0]*ratio
    crP=T(T(desc_ink,0,0,ratio,ratio),crx,-base2)
    bb=bbox(WM['ink'],WM['I'],crP)
    padx=pd.X*1.25; pady=pd.X*1.1
    W=(bb[2]-bb[0]+2*padx)*unit; H=(bb[3]-bb[1]+2*pady)*unit
    dx=(padx-bb[0])*unit; dy=(pady+bb[3])*unit
    return svg(round(W,1),round(H,1),paths_svg([(WM['ink'],ink),(WM['I'],icol),(crP,ink)],unit,dx,dy),bg=bg)
bw=bbox(WM['ink'],WM['I']); wmw=bw[2]-bw[0]
crb=vt.bounds(CRD['ink']); full=wmw/(crb[2]-crb[0])
open('work/st_a.svg','w').write(stacked(0.46,1.02,pdesc,CR['ink']))
open('work/st_b.svg','w').write(stacked(0.62,0.92,pdesc,CR['ink']))
open('work/st_c.svg','w').write(stacked(full*0.97,0.62,pd,CRD['ink']))
print(full)
