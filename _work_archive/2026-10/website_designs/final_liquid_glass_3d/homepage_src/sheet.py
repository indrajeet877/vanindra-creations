import sys
from PIL import Image
src,dst,parts,colw=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
im=Image.open(src); w,h=im.size; seg=(h+parts-1)//parts
sh=int(seg*colw/w)
out=Image.new('RGB',(parts*colw+(parts-1)*8, sh),'#888')
for i in range(parts):
    c=im.crop((0,i*seg,w,min(h,(i+1)*seg))).resize((colw,int((min(h,(i+1)*seg)-i*seg)*colw/w)))
    out.paste(c,(i*(colw+8),0))
out.save(dst)
