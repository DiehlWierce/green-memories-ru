import sys
sys.path.insert(0,'/home/claude/work')
import numpy as np
from collections import Counter
from imgio import load_idx,palette,ITEMS
from imgfont import draw,width,glyph
def lum(c): return 0.3*c[0]+0.59*c[1]+0.11*c[2]
class Img:
    def __init__(s,n):
        s.n=n; s.a=load_idx(ITEMS[n]).copy(); s.pal=palette(ITEMS[n])
    def idx(s,rgb):
        best=min(range(len(s.pal)),key=lambda i:sum((s.pal[i][k]-rgb[k])**2 for k in range(3)))
        return best
    def detect(s,span,rx=None):
        rx=span[0] if rx is None else rx
        x0,y0,x1,y1=span
        sub=s.a[y0:y1+1,x0:x1+1]
        bgs=[s.a[y,rx] for y in range(y0,y1+1)]
        bgc=Counter(bgs).most_common(1)[0][0]
        cnt=Counter(); 
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                v=s.a[y,x]
                if v!=s.a[y,rx]: cnt[v]+=1
        if not cnt: return None,None
        bl=lum(s.pal[bgc])
        fg=max(cnt,key=lambda v:(abs(lum(s.pal[v])-bl)))
        sc=Counter()
        for y in range(y0,y1):
            for x in range(x0,x1):
                if s.a[y,x]==fg:
                    v=s.a[y+1,x+1]
                    if v!=fg and v!=s.a[y,rx]: sc[v]+=1
        sh=sc.most_common(1)[0][0] if sc else None
        return fg,sh
    def put(s,span,text,top,align='c',cx=None,fg=None,sh=None,ul=False,x=None,bold=False,keep=False,ref=None,halo=False,fillbox=False):
        x0,y0,x1,y1=span
        rx=x0 if ref is None else ref
        f,h=s.detect(span,rx)
        fg=f if fg is None else fg; sh=h if sh is None else sh
        if not keep:
            for y in range(y0,y1+1): s.a[y,x0:x1+1]=s.a[y,rx]
        w=width(text)+(1 if bold else 0)
        if x is None:
            if align=='c':
                c=cx if cx is not None else (x0+x1)//2
                x=c-w//2
            elif align=='l': x=x0+1
            else: x=x1-w
        if fillbox and sh is not None and sh>=0:
            s.a[top-1:top+8,x-1:x+w+1]=sh
        if halo and sh is not None and sh>=0:
            for dx in (-1,0,1):
                for dy in (-1,0,1): draw(s.a,x+dx,top+dy,text,sh,bold)
        elif sh is not None and sh>=0:
            for dx,dy in ((1,1),(1,0),(0,1)): draw(s.a,x+dx,top+dy,text,sh,bold)
        draw(s.a,x,top,text,fg,bold)
        if ul:
            yy=top+9
            s.a[yy,x:x+w]=fg
            if sh is not None and sh>=0: s.a[yy+1,x+1:x+w+1]=sh
        return x,w
    def png(s,path,crop=(0,40,256,210),scale=3):
        from PIL import Image
        im=Image.new('RGB',(256,256)); px=im.load()
        for y in range(256):
            for x in range(256): px[x,y]=s.pal[s.a[y,x]]
        im=im.crop(crop); im=im.resize((im.width*scale,im.height*scale),Image.NEAREST); im.save(path)

from imgfont import glyph as _glyph
_H=[2,2,1,2,1,2,2]
def big_glyph(ch):
    rows,top,w=_glyph(ch)
    # only caps (top==0, 7 rows) handled
    out=[]
    for r,h in zip(rows,_H):
        line=''
        for c in r: line+=(c*2)
        line=''.join('#' if (line[i]=='#' or (i>0 and line[i-1]=='#')) else '.' for i in range(len(line)))+('#' if line[-1]=='#' else '.')
        for _ in range(h): out.append(line)
    return out
def big_width(text):
    s=0
    for ch in text:
        s+= 6 if ch==' ' else len(big_glyph(ch)[0])+1
    return s-1
def big_draw(a,x,y,text,color):
    for ch in text:
        if ch==' ': x+=6; continue
        g=big_glyph(ch)
        for dy,row in enumerate(g):
            for dx,c in enumerate(row):
                if c=='#': a[y+dy,x+dx]=color
        x+=len(g[0])+1
    return x
def rot_text(a,x,ycenter,text,color,bold=True):
    import numpy as np
    from imgfont import draw,width
    w=width(text)+2
    tmp=np.zeros((10,w+8),int)
    draw(tmp,0,0,text,1,bold)
    r=np.rot90(tmp)  # CCW
    h,ww=r.shape
    y0=ycenter-h//2
    for yy in range(h):
        for xx in range(ww):
            if r[yy,xx]: a[y0+yy,x+xx]=color

def gl2(ch,colw,rowh):
    rows,top,w=_glyph(ch)
    out=[]
    for r,h in zip(rows,rowh):
        line=''.join(('#' if c=='#' else '.')*cw for c,cw in zip(r,colw)) if len(r)==len(colw) else ''.join(('#' if c=='#' else '.')*(2 if i%2==0 else 1) for i,c in enumerate(r))
        for _ in range(h): out.append(line)
    return out
MID_C=[2,1,2,1,2]
def mid_glyphs(text):
    gs=[]
    for ch in text:
        if ch==' ': gs.append(None); continue
        rows,top,w=_glyph(ch)
        # pad narrow glyphs (e.g. '.', 'Ь' trimmed) to their width using generic mapping
        colw=[2,1,2,1,2][:w] if w<=5 else [2]*w
        if w==3: colw=[2,2,2]
        if w==2: colw=[2,2]
        if w==4: colw=[2,1,2,2]
        gs.append(gl2(ch,colw,_H))
    return gs
def mid_width(text):
    s=0
    for g in mid_glyphs(text): s+= 5 if g is None else len(g[0])+1
    return s-1
def mid_draw(a,x,y,text,color,clip=None):
    for g in mid_glyphs(text):
        if g is None: x+=5; continue
        for dy,row in enumerate(g):
            for dx,c in enumerate(row):
                if c=='#':
                    xx=x+dx
                    if clip and not (clip[0]<=xx<=clip[1]): continue
                    a[y+dy,xx]=color
        x+=len(g[0])+1
    return x
