import struct,json
import numpy as np
d=open('/home/claude/work/gm150.gba','rb').read()
ITEMS=json.load(open('/home/claude/work/run/items.json'))
def load_idx(it):
    a,tb,te,pb,pe,mp,mw,mh,fl,c0,c1=it
    assert (pe-pb)//2<=16
    arr=np.zeros((mh*8,mw*8),dtype=np.uint8)
    for ty in range(mh):
        for tx in range(mw):
            e=struct.unpack_from('<H',d,mp+(ty*mw+tx)*2)[0]
            t=e&0x3ff; hf=(e>>10)&1; vf=(e>>11)&1
            blk=np.zeros((8,8),dtype=np.uint8)
            for y in range(8):
                for x in range(4):
                    b=d[tb+t*32+y*4+x]; blk[y,2*x]=b&15; blk[y,2*x+1]=b>>4
            if hf: blk=blk[:,::-1]
            if vf: blk=blk[::-1,:]
            arr[ty*8:ty*8+8,tx*8:tx*8+8]=blk
    return arr
def palette(it):
    a,tb,te,pb,pe=it[:5]
    return [((c&31)*8,((c>>5)&31)*8,((c>>10)&31)*8) for c in struct.unpack_from('<%dH'%((pe-pb)//2),d,pb)]
