import sys,struct
sys.path.insert(0,'/home/claude/work')
import numpy as np
import bigitems as BI
from menu_text import gl2,_glyph
from imgpatch import retile
from rompatch import B
def patch_at(rom,off,arr):
    tiles,cells,nt=retile(arr)
    ta=rom.alloc(tiles); ma=rom.alloc(cells)
    struct.pack_into('<I',rom.d,off+0,B+ta)
    struct.pack_into('<I',rom.d,off+4,B+ta+len(tiles))
    struct.pack_into('<I',rom.d,off+0x18,B+ma)
    return nt
def colw_for(w,thick,inner):
    if w<=2: return [thick]*w
    mid=[inner[i%len(inner)] for i in range(w-2)]
    return [thick]+mid+[thick]
def glyph_scaled(ch,thick,inner,rowh):
    rows,top,w=_glyph(ch)
    colw=colw_for(w,thick,inner)
    out=[]
    for r,h in zip(rows,rowh):
        line=''.join(('#' if c=='#' else '.')*cw for c,cw in zip(r,colw))
        out+= [line]*h
    return out
def text_glyphs(text,thick,inner,rowh,space):
    gs=[]
    for ch in text:
        gs.append(None if ch==' ' else glyph_scaled(ch,thick,inner,rowh))
    return gs
def hdr_width(text):
    s=0
    for g in text_glyphs(text,3,[2,1],[3,1,1,3,1,1,3],6):
        s+= 6 if g is None else len(g[0])+1
    return s-1
def hdr_draw(a,x,y,text,color):
    for g in text_glyphs(text,3,[2,1],[3,1,1,3,1,1,3],6):
        if g is None: x+=6; continue
        for dy,row in enumerate(g):
            for dx,c in enumerate(row):
                if c=='#': a[y+dy,x+dx]=color
        x+=len(g[0])+1
    return x
HDR=["СТАТУС","ИНВЕНТАРЬ","КАРТА","МИССИЯ","ДНЕВНИК","СИСТЕМА"]
def header_strip():
    it=BI.item_at(0x827258); a=BI.load(it)
    for k in range(6):
        blk=a[:,256*k:256*k+256]
        col=(blk[50:72]==3).any(0)
        segs=[];s=None
        for x,v in enumerate(col):
            if v and s is None: s=x
            if not v and s is not None: segs.append((s,x-1)); s=None
        m=[]
        for sg in segs:
            if m and sg[0]-m[-1][1]<=2: m[-1]=(m[-1][0],sg[1])
            else: m.append(sg)
        # icon = first cluster if narrower than 30 and followed by gap; text starts at 2nd cluster, except inventory (icon,I..)
        icon_end={0:81,1:66,2:94,3:88,4:72,5:75}[k]
        start={0:86,1:70,2:101,3:93,4:79,5:82}[k]
        end=m[-1][1]
        reg=blk[49:72,start-1:end+2]; reg[reg==3]=12
        hdr_draw(blk,start,55,HDR[k],3)
        a[:,256*k:256*k+256]=blk
    return a
CAT_PT={0x827168:14,0x8271b8:2}
CATS=["РАСХОД.","РЕСУРСЫ","КЛЮЧЕВЫЕ","АКСЕССУАРЫ","ОРУЖИЕ"]
def rot_scaled(a,x,ycenter,text,color):
    gs=text_glyphs(text,2,[1,1,1],[2,1,1,2,1,1,1],6)
    # unrotated glyph 7x9; rotate CCW so text reads bottom-to-top
    tot=0
    for g in gs: tot+= 6 if g is None else 8
    tot-=1
    # build unrotated canvas
    W=0
    cw=[]
    for g in gs: cw.append(5 if g is None else len(g[0])+1)
    canvas=np.zeros((9,sum(cw)),int); xx=0
    for g,c in zip(gs,cw):
        if g:
            for dy,row in enumerate(g):
                for dx,ch in enumerate(row):
                    if ch=='#': canvas[dy,xx+dx]=1
        xx+=c
    r=np.rot90(canvas)
    h,w=r.shape
    y0=ycenter-h//2
    for yy in range(h):
        for xx2 in range(w):
            if r[yy,xx2]: a[y0+yy,x+xx2]=color
def cat_strip(off):
    it=BI.item_at(off); a=BI.load(it)
    barc=a[3,12]
    reg=a[:,14:38]
    ys=np.nonzero((reg==3).any(1))[0]
    # clusters
    cl=[];s=ys[0];p=ys[0]
    for y in ys[1:]:
        if y-p>12: cl.append((s,p)); s=y
        p=y
    cl.append((s,p))
    assert len(cl)==5,cl
    cen=[(s+p)//2 for s,p in cl]
    reg[reg==3]=barc
    for t,c in zip(CATS,cen): rot_scaled(a,21,c,t,3)
    return a,cl
if __name__=='__main__':
    from PIL import Image
    a=header_strip(); it=BI.item_at(0x827258); p=BI.pal(it)
    im=Image.new('RGB',(1536,40)); px=im.load()
    for y in range(40):
        for x in range(1536): px[x,y]=p[a[40+y,x]]
    im.save('run/hdr_new.png')
    for off in CAT_PT:
        a,cl=cat_strip(off); print(hex(off),cl)
        it=BI.item_at(off); p=BI.pal(it)
        im=Image.new('RGB',(40,1280)); px=im.load()
        for y in range(1280):
            for x in range(40): px[x,y]=p[a[y,x]]
        im.save(f'run/cat_{off:x}.png')
