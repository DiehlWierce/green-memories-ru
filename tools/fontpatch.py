import struct, collections
from fonts import parse, glyph_pixels, B
from cyr_base import *

FILL=11; OUTL=1; SHADE=12
def ink_of(px,idx=FILL):
    return [(y,x) for y in range(16) for x in range(8) if px[y][x]==idx]

class Style:
    def __init__(s,rom,f):
        s.f=f
        g=lambda ch: glyph_pixels(rom,f['tb'],ord(ch)-0x21)
        cnt=collections.Counter()
        n=(f['te']-f['tb'])//64
        for gi in range(94):
            for r in glyph_pixels(rom,f['tb'],gi):
                cnt.update(r)
        s.outline = cnt[OUTL]>200
        s.bold = cnt[SHADE]>1000
        H=ink_of(g('H')); x=ink_of(g('x')); nn=ink_of(g('n')); p=ink_of(g('p')); b=ink_of(g('b'))
        s.capTop=min(y for y,_ in H); s.capBot=max(y for y,_ in H)
        s.capH=s.capBot-s.capTop+1
        s.left=min(c for _,c in H); s.capW=max(c for _,c in H)-s.left+1
        s.xTop=min(y for y,_ in x); s.xBot=max(y for y,_ in x); s.xH=s.xBot-s.xTop+1
        s.lcW=max(c for _,c in nn)-min(c for _,c in nn)+1
        s.base=s.capBot
        widths=rom[f['wb']:f['we']]
        d=collections.Counter()
        for gi in range(94):
            ink=ink_of(glyph_pixels(rom,f['tb'],gi))
            if not ink: continue
            span=max(c for _,c in ink)-min(c for _,c in ink)+1
            d[widths[gi+1]-span]+=1
        s.wk=d.most_common(1)[0][0]
    def __repr__(s): return f"Style(outline={s.outline} bold={s.bold} cap={s.capH}x{s.capW} top={s.capTop} x={s.xH} xTop={s.xTop} lcW={s.lcW} left={s.left} wk={s.wk})"

def scale(rows,tw,th):
    bh=len(rows); bw=len(rows[0])
    out=[]
    for y in range(th):
        sy=min(bh-1,(y*bh)//th) if th!=bh else y
        row=''
        for x in range(tw):
            sx=min(bw-1,(x*bw)//tw) if tw!=bw else x
            row+=rows[sy][sx]
        out.append(row)
    return out

def render(st,rows,top,left,extra_ink=()):
    """rows: ink strings; returns 16x8 pixel grid"""
    ink=set()
    for dy,r in enumerate(rows):
        for dx,ch in enumerate(r):
            if ch=='X': ink.add((top+dy,left+dx))
    for p in extra_ink: ink.add(p)
    if st.bold:
        ink|={(y,x+1) for y,x in ink}
    grid=[[0]*8 for _ in range(16)]
    def put(y,x,v):
        if 0<=y<16 and 0<=x<8 and grid[y][x]==0: grid[y][x]=v
    for y,x in ink: 
        if 0<=y<16 and 0<=x<8: grid[y][x]=FILL
    if st.outline:
        for y,x in list(ink):
            for dy in (-1,0,1):
                for dx in (-1,0,1): put(y+dy,x+dx,OUTL)
    if st.bold:
        for y,x in list(ink):
            for dy,dx in ((0,1),(1,0),(1,1)): 
                if (y+dy,x+dx) not in ink: put(y+dy,x+dx,SHADE)
    return grid,ink

def make_glyph(rom,st,ch):
    f=st.f
    if ch in COPY:
        gi=ord(COPY[ch])-0x21
        px=glyph_pixels(rom,f['tb'],gi)
        w=rom[f['wb']+gi+1]
        return px,w
    def acc_rows(base_top,left):
        # breve: two rows above, gap row between
        return {(base_top-3,left+1),(base_top-3,left+st.capW//2+1 if False else left+3),(base_top-2,left+2)}
    kind=None
    if ch in CAP: rows=CAP[ch]; kind='cap'
    elif ch in CAP_ACC: rows=CAP[CAP_ACC[ch]]; kind='capacc'
    elif ch in LOW: rows=LOW[ch]; kind='low'
    elif ch in LOW_ACC: rows=LOW[LOW_ACC[ch]]; kind='lowacc'
    elif ch in LOW_DESC: rows=LOW_DESC[ch]; kind='lowdesc'
    elif ch in LOW_ASC: rows=LOW_ASC[ch]; kind='asc'
    elif ch in LOW_ASCDESC: rows=LOW_ASCDESC[ch]; kind='ascdesc'
    if kind in('cap','capacc','asc','ascdesc'): tw=st.capW
    else: tw=st.lcW
    bw=len(rows[0])
    # keep narrow designs narrow
    if bw<5: tw=max(1,round(tw*bw/5))
    if kind in('cap','capacc'): th=st.capH; top=st.capTop
    elif kind in('low','lowacc'): th=st.xH; top=st.xTop
    elif kind=='lowdesc': th=st.xH+1; top=st.xTop
    elif kind=='asc': th=st.capH; top=st.capTop
    elif kind=='ascdesc': th=st.capH+1; top=st.capTop
    r2=scale(rows,tw,th)
    extra=()
    if kind in('capacc','lowacc'):
        t=top
        mid=st.left+tw//2
        extra={(t-3,mid-1),(t-3,mid+1),(t-2,mid)}
    grid,ink=render(st,r2,top,st.left,extra)
    span=max(x for y,x in ink)-min(x for y,x in ink)+1
    w=span+st.wk
    return grid,w

def pack_tiles(grid):
    out=bytearray()
    for half in range(2):
        for y in range(8):
            row=grid[half*8+y]
            for x in range(0,8,2):
                out.append(row[x]|(row[x+1]<<4))
    return bytes(out)
