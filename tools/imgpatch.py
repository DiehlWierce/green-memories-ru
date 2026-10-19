import sys,struct
sys.path.insert(0,'/home/claude/work')
import numpy as np
from PIL import Image
from imgio import load_idx,palette,ITEMS
from rompatch import B
def retile(arr):
    h,w=arr.shape; th,tw=h//8,w//8
    tiles=[bytes(32)]  # tile 0 blank
    index={tiles[0]:0}
    def pack(blk):
        out=bytearray(32)
        for y in range(8):
            for x in range(4):
                out[y*4+x]=int(blk[y,2*x])|(int(blk[y,2*x+1])<<4)
        return bytes(out)
    cells=[]
    for ty in range(th):
        for tx in range(tw):
            blk=arr[ty*8:ty*8+8,tx*8:tx*8+8]
            found=None
            for hf in (0,1):
                for vf in (0,1):
                    b=blk
                    if hf: b=b[:,::-1]
                    if vf: b=b[::-1,:]
                    k=pack(b)
                    if k in index: found=(index[k],hf,vf);break
                if found:break
            if not found:
                k=pack(blk); index[k]=len(tiles); tiles.append(k); found=(index[k],0,0)
            t,hf,vf=found
            cells.append(t|(hf<<10)|(vf<<11))
    return b''.join(tiles),struct.pack('<%dH'%len(cells),*cells),len(tiles)
def patch_item(rom,n,arr):
    it=ITEMS[n]; a=it[0]
    tiles,cells,nt=retile(arr)
    ta=rom.alloc(tiles); ma=rom.alloc(cells)
    struct.pack_into('<I',rom.d,a+0,B+ta)
    struct.pack_into('<I',rom.d,a+4,B+ta+len(tiles))
    struct.pack_into('<I',rom.d,a+0x18,B+ma)
    return nt
def to_png(arr,pal,path,crop=None,scale=3):
    h,w=arr.shape
    im=Image.new('RGB',(w,h)); px=im.load()
    for y in range(h):
        for x in range(w): px[x,y]=pal[arr[y,x]]
    if crop: im=im.crop(crop)
    if scale!=1: im=im.resize((im.width*scale,im.height*scale),Image.NEAREST)
    im.save(path)
