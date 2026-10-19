import struct
from fonts import parse, B, FONTS
from fontpatch import *
from rompatch import Rom

SEED=0x050c5d1f
def build_buckets(entries,mask):
    cap=mask+1
    bk=[(0,0)]*cap
    used=[False]*cap
    for key,val in entries:
        h=(key^SEED)&mask
        while used[h]: h=(h+1)&mask
        used[h]=True; bk[h]=(key,val|0x80000000)
    return b''.join(struct.pack('<II',k,v) for k,v in bk)

def patch_fonts(r,verbose=True):
    rom=bytes(r.d[:r.orig_len])
    done={}
    structs=[parse(rom,S) for S in FONTS]
    for f in structs:
        key=f['tb']
        if key not in done:
            st=Style(rom,f)
            n=(f['te']-f['tb'])//64
            nex=f['nextra']
            tiles=bytearray(rom[f['tb']:f['te']])
            widths=bytearray(rom[f['wb']:f['we']])
            # old buckets
            old=[]
            cap=f['mask']+1
            for i in range(cap):
                k,v=struct.unpack_from('<II',rom,f['buckets']+i*8)
                if v>>31: old.append((k,v&0x7fffffff))
            assert len(old)==nex,(hex(f['S']),len(old),nex)
            new=[]
            for j,ch in enumerate(ALL):
                grid,w=make_glyph(rom,st,ch)
                tiles+=pack_tiles(grid); widths.append(w)
                new.append((ord(ch),nex+j))
            total=len(old)+len(new)
            mask=0xff if total*2>256 else 0x7f
            bk=build_buckets(old+new,mask)
            ta=r.alloc(bytes(tiles)); wa=r.alloc(bytes(widths)); ba=r.alloc(bk)
            done[key]=dict(tb=ta,te=ta+len(tiles),n=n+len(new),wb=wa,we=wa+len(widths),bk=ba,mask=mask,nex=total)
            if verbose: print(hex(f['S']),st,'new glyphs',len(new),'mask',hex(mask))
        d=done[key]; S=f['S']
        struct.pack_into('<I',r.d,S+0,B+d['tb'])
        struct.pack_into('<I',r.d,S+4,B+d['te'])
        old8=struct.unpack_from('<I',r.d,S+8)[0]
        struct.pack_into('<I',r.d,S+8,(old8&0xffff0000)|d['n'])
        struct.pack_into('<I',r.d,S+28,B+d['bk'])
        struct.pack_into('<I',r.d,S+32,d['mask'])
        struct.pack_into('<I',r.d,S+36,d['nex'])
        struct.pack_into('<I',r.d,S+40,B+d['wb'])
        struct.pack_into('<I',r.d,S+44,B+d['we'])
