import struct
from PIL import Image
B=0x08000000
FONTS=[0x81a9e4,0x81ac90,0x81ba00,0x82ce98,0x82d1c4,0x82d1f8,0x82f61c]
def w(rom,o,n): return struct.unpack_from('<%dI'%n,rom,o)
def parse(rom,S):
    a=w(rom,S,13)
    return dict(S=S,tb=a[0]-B,te=a[1]-B,n=a[2]&0xffff,pb=a[3]-B,pe=a[4]-B,buckets=a[7]-B,mask=a[8],nextra=a[9],wb=a[10]-B,we=a[11]-B)
def pal(rom,o):
    out=[]
    for i in range(16):
        c=struct.unpack_from('<H',rom,o+i*2)[0]; out.append((((c&31)*255)//31,(((c>>5)&31)*255)//31,(((c>>10)&31)*255)//31))
    return out
def glyph_pixels(rom,tb,g):
    px=[]
    for half in range(2):
        o=tb+g*64+half*32
        for y in range(8):
            px.append([(rom[o+y*4+x//2]>>(4*(x&1)))&15 for x in range(8)])
    return px
def sheet_img(rom,f,cols=16,scale=3):
    n=(f['te']-f['tb'])//64
    rows=(n+cols-1)//cols
    img=Image.new('RGB',(cols*10,rows*18),(50,50,80)); P=img.load()
    p=pal(rom,f['pb'])
    for g in range(n):
        px=glyph_pixels(rom,f['tb'],g)
        for y in range(16):
            for x in range(8):
                v=px[y][x]
                if v: P[(g%cols)*10+x+1,(g//cols)*18+y+1]=(255,255,255) if v==11 else (0,0,0) if v==1 else (200,0,0)
    return img.resize((img.width*scale,img.height*scale),Image.NEAREST)
