import sys,json,struct
sys.path.insert(0,'/home/claude/work')
from rompatch import Rom,B
from build_font import patch_fonts
from trload import parse_files,check
groups=json.load(open('/home/claude/work/groups.json'))
UI={1:'Центральный лагерь',3:'Восточный сектор',5:'Северная развилка',7:'Северо-восточный сектор',
9:'Редкий луг',11:'Долина птиц',13:'Северный пляж',15:'Долина костей',
17:'Южная пещера',19:'Южная пещера',21:'Южная пещера',23:'Южная пещера',25:'Южная пещера',27:'Южная пещера',
29:'Хотите сохраниться?',31:'Деньги:',33:'Недоступно',35:'Читать',37:'надеть',39:'записать',41:'ВЫБРАТЬ',
43:'НАЗАД',45:'Выход',47:'Создать',49:'Применить',51:'нет',53:'да',55:'Да        Нет',57:'это место?',
59:'Отправиться в',61:'закат',63:'рассвет',65:'назад',67:'Спать   ',69:'нажмите start снова',
71:'нажмите start',73:'язык',75:'продолжить',77:'новая игра'}
def build(out):
    r=Rom('/home/claude/work/gm150.gba')
    patch_fonts(r,False)
    # intro/narration font: final layout must match typewriter (fixed 7px advance for Cyrillic)
    from fonts import parse
    from cyr_base import ALL
    f=parse(bytes(r.d),0x82ce98)
    base=f['we']-f['wb']-len(ALL)
    for j in range(len(ALL)): r.d[f['wb']+base+j]=7
    res,errs=parse_files(); assert not errs,errs
    assert not check(res)
    n=0
    for (gi,k),ru in res.items():
        _,a,b=groups[gi][k]
        n+=r.replace_string(a,b-a,ru.encode('utf8'))
    for i,ru in UI.items():
        _,a,b=groups[11][i]
        n+=r.replace_string(a,b-a,ru.encode('utf8'))
    import build_tutorial, imgpatch
    for n,a in build_tutorial.render_all().items():
        nt=imgpatch.patch_item(r,n,a); print('tutorial item',n,'tiles',nt)
    import build_menu
    for n in sorted(build_menu.SPEC):
        nt=imgpatch.patch_item(r,n,build_menu.render(n).a); print('menu item',n,'tiles',nt)
    import build_hdr
    print('hdr tiles',build_hdr.patch_at(r,0x827258,build_hdr.header_strip()))
    for off in build_hdr.CAT_PT: print('cat tiles',build_hdr.patch_at(r,off,build_hdr.cat_strip(off)[0]))
    # language label
    na=r.alloc('русский'.encode('utf8'))
    struct.pack_into('<I',r.d,0x28b88,B+na)
    r.save(out); print('patched pairs',n,'size',len(r.d))
if __name__=='__main__': build(sys.argv[1])
