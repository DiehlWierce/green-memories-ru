import struct,sys
sys.path.insert(0,'/home/claude/work')
import numpy as np
d=open('/home/claude/work/gm150.gba','rb').read()
def item_at(off):
    w=struct.unpack_from('<10I',d,off)
    return dict(off=off,tb=w[0]&0xffffff,te=w[1]&0xffffff,pb=w[3]&0xffffff,pe=w[4]&0xffffff,mp=w[6]&0xffffff,mw=w[7],mh=w[8],fl=w[9])
def load(it,d=d):
    mw,mh=it['mw'],it['mh']
    arr=np.zeros((mh*8,mw*8),dtype=np.uint8)
    tiles=np.frombuffer(d[it['tb']:it['te']],dtype=np.uint8).reshape(-1,8,4)
    t=np.zeros((len(tiles),8,8),dtype=np.uint8); t[:,:,0::2]=tiles&15; t[:,:,1::2]=tiles>>4
    maps=np.frombuffer(d[it['mp']:it['mp']+mw*mh*2],dtype='<u2').reshape(mh,mw)
    for ty in range(mh):
        for tx in range(mw):
            e=int(maps[ty,tx]); n=e&0x3ff
            blk=t[n] if n<len(t) else np.zeros((8,8),np.uint8)
            if (e>>10)&1: blk=blk[:,::-1]
            if (e>>11)&1: blk=blk[::-1,:]
            arr[ty*8:ty*8+8,tx*8:tx*8+8]=blk
    return arr
def pal(it,d=d):
    return [((c&31)*8,((c>>5)&31)*8,((c>>10)&31)*8) for c in struct.unpack_from('<%dH'%((it['pe']-it['pb'])//2),d,it['pb'])]
def png(it,path,scale=1,crop=None):
    from PIL import Image
    a=load(it); p=pal(it)
    im=Image.new('RGB',(a.shape[1],a.shape[0]))
    px=im.load()
    for y in range(a.shape[0]):
        for x in range(a.shape[1]): px[x,y]=p[a[y,x]] if a[y,x] else (40,0,40)
    if crop: im=im.crop(crop)
    if scale!=1: im=im.resize((im.width*scale,im.height*scale),Image.NEAREST)
    im.save(path)
if __name__=='__main__':
    off=int(sys.argv[1],16)
    png(item_at(off),sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 1)
