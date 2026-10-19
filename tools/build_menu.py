import sys
sys.path.insert(0,'/home/claude/work')
from menu_text import *
SPEC={}
def item(*ns):
    def deco(f):
        for n in ns: SPEC[n]=f
        return f
    return deco
def back(im,confirm=True):
    # bottom strip: A CONFIRMAR / B VOLTAR
    if confirm: im.put((140,197,192,206),"ВЫБОР",199,align='l',ref=124)
    im.put((206,197,241,206),"НАЗАД",199,align='l',ref=124)
def title(im,text,cx):
    im.put((cx-29 if cx<100 else cx-22,53,cx+26 if cx>100 else cx+29,68),text,57,cx=cx,ul=True,ref=cx-29 if cx<100 else cx-22)
@item(34,36,38)
def system(im):
    title(im,"СИСТЕМА",159)
    im.put((60,99,200,109),"СОХРАНИТЬ",100,cx=128)
    im.put((60,132,200,141),"УПРАВЛЕНИЕ",133,cx=128)
    im.put((60,162,200,174),"ГЛАВНОЕ МЕНЮ",165,cx=128)
    back(im)
@item(26)
def mission(im):
    title(im,"МИССИЯ",135); back(im,False)
@item(28)
def status(im):
    c=im.a[83,94]
    title(im,"СТАТУС",70)
    im.put((95,79,146,90),"УЛУЧШЕНИЯ",81,cx=121,ref=149,fillbox=True)
    im.a[83,95:147]=c
    im.put((178,89,211,100),"ПАРАМЕТРЫ",91,cx=194,ref=215,fillbox=True)
    im.put((161,140,222,146),"АТАКА",140,align='l',ref=222)
    im.put((161,155,222,161),"ВОССТ. ЭН.",155,align='l',ref=222)
    im.put((38,170,80,179),"ЦИТРА",172,cx=56,ref=80)
    back(im,False)
@item(30,46)
def inv_equip(im):
    title(im,"ИНВЕНТАРЬ",97)
    im.put((30,77,66,89),"ВЕЩИ",79,cx=48,ref=30,fg=7,sh=5,fillbox=True)
    im.put((93,77,168,88),"ЭКИПИРОВКА",79,cx=129,ref=170)
    back(im,False)
@item(32,48)
def inv_items(im):
    title(im,"ИНВЕНТАРЬ",97)
    im.put((100,77,160,88),"ВЕЩИ",79,cx=128,ref=100)
    im.put((184,77,224,89),"ЭКИП.",79,cx=203,ref=223,fg=7,sh=5,fillbox=True)
    back(im,False)
@item(40,42)
def mapt(im):
    title(im,"КАРТА",116)
    back(im,im.n==40)
def pinkof(im,y0,y1,x0,x1):
    from collections import Counter
    c=Counter(int(v) for v in im.a[y0:y1+1,x0:x1+1].ravel())
    bg=c.most_common(1)[0][0]
    # text colour: among colours, the one with highest red-green difference and frequent
    best=max((k for k in c if k!=bg),key=lambda k:(im.pal[k][0]-im.pal[k][1])*1000+c[k])
    return best
def inpaint(im,x0,y0,x1,y1,col):
    a=im.a
    mask=(a[y0:y1+1,x0:x1+1]==col)
    for _ in range(6):
        ys,xs=((mask).nonzero())
        if len(ys)==0: break
        new=a.copy(); done=[]
        for y,x in zip(ys+y0,xs+x0):
            from collections import Counter
            c=Counter()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=y+dy,x+dx
                    if (dy or dx) and not (y0<=yy<=y1 and x0<=xx<=x1 and mask[yy-y0,xx-x0]): c[int(a[yy,xx])]+=1
            if c: new[y,x]=c.most_common(1)[0][0]; done.append((y,x))
        a[:]=new
        for y,x in done: mask[y-y0,x-x0]=False
def dash(im,x0,x1,y,col): im.a[y,x0:x1]=col
@item(44)
def region44(im):
    mapt(im)
    col=pinkof(im,126,133,50,205)
    inpaint(im,48,122,208,150,col)
    t1="НЕИЗВЕСТНЫЙ РЕГИОН"; t2="КАРТА НЕДОСТУПНА"
    x,w=im.put((48,122,208,150),t1,128,cx=127,fg=col,sh=-1,keep=True)
    dash(im,x-14,x-8,131,col); dash(im,x+w+8,x+w+14,131,col)
    im.put((48,122,208,150),t2,140,cx=127,fg=col,sh=-1,keep=True)
@item(50)
def region50(im):
    a=im.a
    col=pinkof(im,126,133,38,165)
    for y in range(122,148): a[y,34:170]=a[y-24,34:170]
    im.put((34,122,170,148),"НЕИЗВЕСТНЫЙ РЕГИОН",128,cx=101,fg=col,sh=-1,keep=True)
    im.put((34,122,170,148),"КАРТА НЕДОСТУПНА",140,cx=101,fg=col,sh=-1,keep=True)
@item(14)
def diary(im):
    im.a[104:161,14:29]=12
    rot_text(im.a,17,131,"ДНЕВНИК",3,True)
BIGT=["СОХРАНИТЬ","УПРАВЛЕНИЕ","ТУТОРИАЛ","ГЛАВНОЕ МЕНЮ"]
def bigmenu(im,sel):
    white=im.idx((248,248,248))
    for i,t in enumerate(BIGT):
        top=101+16*i
        if i==sel:
            for y in range(top-1,top+13): im.a[y,10:192]=im.a[y,10]
            big_draw(im.a,189-big_width(t),top,t,white)
        else:
            for y in range(top-1,top+13): im.a[y,12:163]=im.a[y,172]
            big_draw(im.a,15,top,t,white)
@item(16)
def m16(im): bigmenu(im,3)
@item(18)
def m18(im): bigmenu(im,2)
@item(20)
def m20(im): bigmenu(im,1)
@item(22)
def m22(im): bigmenu(im,0)
@item(24)
def hud(im):
    a=im.a; blk=im.idx((0,0,0)); wh=im.idx((248,248,248))
    a[83:93,17:96]=blk; a[131:145,17:100]=blk; a[188:196,15:56]=blk
    pur=a[100,112]
    draw(a,18,84,"АТРИБУТЫ",wh,True)
    draw(a,18,136,"АКСЕССУАРЫ",wh,True)
    draw(a,16,189,"ДЕНЬГИ",wh,False)
    a[196,16:width("ДЕНЬГИ")+17]=wh
    inpaint(im,106,108,125,120,wh); inpaint(im,104,151,124,163,wh)
    draw(a,111,111,"HP",wh,True)
    draw(a,109,154,"ЭН",wh,True)
def tab(im,word,px0,px1,cx,stub=None):
    a=im.a
    # replace text (white) with pink in the pink box
    sub=a[51:70,px0+1:px1]
    sub[sub==3]=2
    mid_draw(a,cx-mid_width(word)//2,54,word,3)
    if stub:
        w,(sx0,sx1),align=stub
        reg=a[54:68,sx0:sx1+1]; reg[reg==15]=14
        mw=mid_width(w)
        x=(sx1-mw+1) if align=='r' else sx0+1
        # inactive word, thin bold light-blue, 8 rows
        draw(a,x,57,w,15,True) if False else mid_draw_small(a,x,w,15,(sx0,sx1))
def mid_draw_small(a,x,w,col,clip):
    import numpy as np
    from imgfont import draw,width
    tmp=np.zeros((10,width(w)+8),int)
    ww=draw(tmp,0,0,w,1,True)
    if clip[0]>x+0 and False: pass
    # right/left anchoring handled by caller via x (computed with mid_width); recompute with small width
    sw=ww
    if x>clip[0]+2: x=clip[1]-sw+1
    for dy in range(tmp.shape[0]):
        for dx in range(tmp.shape[1]):
            if tmp[dy,dx]:
                xx=x+dx
                if clip[0]<=xx<=clip[1]: a[57+dy,xx]=col
@item(52,54)
def t_dep(im): tab(im,"СДАТЬ",40,116,78,("ВЗЯТЬ",(117,132),'r'))
@item(56,58)
def t_ret(im): tab(im,"ВЗЯТЬ",58,131,94,("СДАТЬ",(38,57),'l'))
@item(60,62)
def t_cr(im): tab(im,"КРАФТ",32,100,66)
@item(64,68)
def t_sell(im):
    a=im.a; a[50:71,64:70]=2
    tab(im,"ПРОДАЖА",64,130,97,("КУПИТЬ",(39,63),'l'))
@item(66,70)
def t_buy(im): tab(im,"ПОКУПКА",42,106,74,("ПРОДАЖА",(107,132),'r'))
@item(72)
def gameover(im):
    a=im.a; blk=a[200,9]; wh=im.idx((248,248,248))
    a[188:206,10:246]=blk
    t1="Палящее солнце наказало Цитру"; t2="за её беспечность."
    draw(a,128-width(t1)//2,189,t1,wh); draw(a,128-width(t2)//2,199,t2,wh)
@item(94)
def controls(im):
    a=im.a; blk=a[60,100]; wh=im.idx((248,248,248))
    L=[ # clear box, [(text, center_x, top)]
     ((24,85,100,94),[("Пред. предмет",63,86)]),
     ((24,98,74,118),[("Любимое",47,99),("оружие",47,109)]),
     ((35,135,71,143),[("Ходьба",53,136)]),
     ((42,160,70,170),[("Меню",56,161)]),
     ((96,162,146,182),[("Любимый",121,164),("предмет",121,173)]),
     ((162,82,236,94),[("След. предмет",199,84)]),
     ((165,96,236,105),[("Захват цели",199,97)]),
     ((181,124,240,134),[("Применить",208,125)]),
     ((179,138,240,147),[("Выбрать",207,139)]),
     ((165,158,208,169),[("Бег",185,160)]),
     ((157,172,246,182),[("Выбор предмета",200,173)]),
    ]
    for (x0,y0,x1,y1),ts in L:
        a[y0:y1+1,x0:x1+1]=blk
        for t,cx,top in ts: draw(a,cx-width(t)//2,top,t,wh)
def render(n):
    im=Img(n); SPEC[n](im); return im
if __name__=='__main__':
    for n in [int(x) for x in sys.argv[1].split(',')]:
        render(n).png(f'run/m{n}.png',scale=3)
