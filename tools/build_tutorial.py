import sys
sys.path.insert(0,'/home/claude/work')
import numpy as np
from imgio import load_idx,palette,ITEMS
from imgfont import *
from imgpatch import *
W,Y,R='W','Y','R'
COL={}
def clear(a,y0,y1,x0=14,x1=246,v=1):
    if y1>=188:
        a[y0:188,x0:x1+1]=v; a[188:y1+1,x0:215]=v
    else: a[y0:y1+1,x0:x1+1]=v
BAN_OVR={'Ж':['#..#..#','#..#..#','.#.#.#.','..###..','.#.#.#.','#..#..#','#..#..#']}
def bw(ch):
    if ch==' ': return 5
    rows=BAN_OVR.get(ch) or glyph(ch)[0]
    return len(rows[0])+2
def banner(a,title):
    a[54:68,36:222]=12
    m=(a[52:54,34:223]==3); a[52:54,34:223][m]=12
    w=sum(bw(c) for c in title)-2
    x=34+(222-34-w)//2
    for ch in title:
        if ch==' ': x+=5; continue
        rows=BAN_OVR.get(ch)
        top=0
        if rows is None: rows,top,_=glyph(ch)
        for dy,row in enumerate(rows):
            for dx,c in enumerate(row):
                if c=='#':
                    a[56+top+dy,x+dx]=3; a[56+top+dy,x+dx+1]=3
        x+=len(rows[0])+2
    return w
def cc(c): return COL.get(c,c)
def lines(a,x,y0,ls,pitch=11):
    for i,segs in enumerate(ls):
        if isinstance(segs,str): segs=[(segs,W)]
        xx=x
        for t,c in segs: xx=draw(a,xx,y0+i*pitch,t,cc(c))
def seg_w(segs):
    if isinstance(segs,str): segs=[(segs,W)]
    return sum(width(t)+1 for t,c in segs)-1
def centered(a,cx,y,text,color): draw(a,cx-width(text)//2,y,text,cc(color))
T_WEATHER="ТУТОРИАЛ: ПОГОДА"
T_HP="ТУТОРИАЛ: ВОССТАНОВЛЕНИЕ HP"
T_WEAPON="ТУТОРИАЛ: ОРУЖИЕ"
PAGES={}
def page(n):
    def deco(f): PAGES[n]=f; return f
    return deco
@page(92)
def p1(a):
    banner(a,T_WEATHER); clear(a,74,111)
    lines(a,32,79,["Следите за погодными эффектами!","Если эффект активен, в HUD","появится значок."])
@page(90)
def p2(a):
    banner(a,T_WEATHER); clear(a,100,190)
    lines(a,26,106,[[("Днём действует ",W),("Сильная жара",Y),(".",W)],
     [("Здоровье (HP) будет медленно",R)],[("убывать, пока вы под солнцем.",R)],
     "Спасайтесь в тени облаков или","деревьев, чтобы избежать эффектов!",
     [("Можно выпить ",W),("Газировку",Y),(",",W)],"чтобы временно подавить эффекты."])
@page(88)
def p3(a):
    banner(a,T_WEATHER); clear(a,100,190)
    lines(a,31,109,[[("Ночью действует ",W),("Мороз",Y),(".",W)],
     [("Ваши движения будут замедлены,",R)],[("снижая скорость передвижения.",R)],
     [("Можно выпить ",W),("Горячий напиток",Y),(",",W)],"чтобы временно подавить эффекты."])
@page(86)
def p4(a):
    banner(a,T_HP); clear(a,80,124); clear(a,160,190)
    lines(a,30,88,[[("Здоровье (HP) не восстанавливается",R)],"само. Чтобы его восстановить,","добывайте воду из почвы."])
    lines(a,30,167,["Выберите Флягу в списке предметов","и удерживайте A для использования."])
@page(84)
def p5(a):
    banner(a,T_HP); clear(a,80,132); clear(a,160,190)
    lines(a,44,85,["Вероятность успеха добычи воды","в вашем месте показывается","значком под часами."])
    lines(a,44,167,[[("Помните, ",W),("что добыча воды",R)],[("расходует энергию!",R)]])
@page(82)
def p6(a):
    banner(a,T_WEAPON); clear(a,72,131); clear(a,165,177); clear(a,178,190)
    lines(a,43,77,["Побеждайте врагов оружием.","Выберите любимое оружие в списке","предметов и нажмите A, чтобы взять","его в руки. В начале у вас два","вида оружия:"])
    centered(a,90,167,"Мачете",Y); centered(a,168,167,"Револьвер",Y)
    centered(a,128,179,"Оружие расходует энергию!",R)
@page(80)
def p7(a):
    banner(a,T_WEAPON); clear(a,112,190)
    lines(a,42,119,["Мачете - оружие ближнего боя.","Оно наносит большой урон и","отталкивает некоторых врагов.","Им также можно отражать","некоторые снаряды."])
@page(78)
def p8(a):
    banner(a,T_WEAPON); clear(a,108,190)
    lines(a,27,111,["Револьвер - оружие дальнего боя.","Урон невелик, но стрелять можно","очень быстро.","Также можно зафиксировать прицел:","выберите направление, удерживайте","кнопку R и идите.","Во время прицеливания бегать нельзя."])
def setcols(n):
    pal=palette(ITEMS[n])
    def idx(h):
        for i,c in enumerate(pal):
            if '%02x%02x%02x'%c==h: return i
    COL['W']=3
    COL['R']=idx('f00000')
    COL['Y']=idx('f0b028') or idx('f0d008')
def render_all():
    out={}
    for n,f in PAGES.items():
        setcols(n)
        a=load_idx(ITEMS[n]); f(a); out[n]=a
    return out
if __name__=='__main__':
    out=render_all()
    for n,a in out.items():
        to_png(a,palette(ITEMS[n]),f'/home/claude/work/run/ru_{n}.png',crop=(6,44,246,204),scale=3)
    # width check
    for n,f in PAGES.items(): pass
    print('ok')
