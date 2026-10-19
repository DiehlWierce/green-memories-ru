# Base Cyrillic stroke designs. 'X' = ink.
# kinds: cap (5 rows at cap height), low (4 rows at x-height), capdesc (cap rows + tail rows below), lowdesc, asc (5 rows, top one above x-height),
#        ascdesc (6 rows from asc top), capacc/lowacc: body with breve above.
CAP = {
 'Б': ["XXXXX","X....","XXXX.","X...X","XXXX."],
 'Г': ["XXXX.","X....","X....","X....","X...."],
 'Д': ["..XXX",".X..X",".X..X","XXXXX","X...X"],
 'Ж': ["X.X.X",".XXX.","..X..",".XXX.","X.X.X"],
 'З': ["XXXX.","....X",".XXX.","....X","XXXX."],
 'И': ["X...X","X..XX","X.X.X","XX..X","X...X"],
 'Л': ["..XXX",".X..X",".X..X","X...X","X...X"],
 'П': ["XXXXX","X...X","X...X","X...X","X...X"],
 'У': ["X...X","X...X",".XXXX","....X","XXXX."],
 'Ф': [".XXX.","X.X.X","X.X.X",".XXX.","..X.."],
 'Ц': ["X..X.","X..X.","X..X.","XXXXX","....X"],
 'Ч': ["X...X","X...X",".XXXX","....X","....X"],
 'Ш': ["X.X.X","X.X.X","X.X.X","X.X.X","XXXXX"],
 'Щ': ["X.X.X","X.X.X","X.X.X","XXXXX","....X"],
 'Ъ': ["XX...",".X...",".XXX.",".X..X",".XXX."],
 'Ы': ["X...X","X...X","XXX.X","X..XX","XXX.X"],
 'Ь': ["X....","X....","XXXX.","X...X","XXXX."],
 'Э': ["XXXX.","....X",".XXXX","....X","XXXX."],
 'Ю': ["X.XX.","X.X.X","XXX.X","X.X.X","X.XX."],
 'Я': [".XXXX","X...X",".XXXX","..X.X",".X..X"],
}
CAP_DESC = {'Ц','Щ','Д'}   # last row sits below baseline (Д,Ц,Щ: last row is a tail row)
CAP_ACC = {'Й':'И'}
LOW = {
 'в': ["XXXX.","X..X.","XXXXX","XXXX."],
 'г': ["XXXX","X...","X...","X..."],
 'ж': ["X.X.X",".XXX.",".XXX.","X.X.X"],
 'з': ["XXX.","...X",".XX.","XXX."],
 'и': ["X...X","X..XX","X.X.X","XX..X"],
 'к': ["X..X","X.X.","XXX.","X..X"],
 'л': ["..XXX",".X..X","X...X","X...X"],
 'м': ["X...X","XX.XX","X.X.X","X...X"],
 'н': ["X...X","X...X","XXXXX","X...X"],
 'п': ["XXXXX","X...X","X...X","X...X"],
 'т': ["XXXXX","..X..","..X..","..X.."],
 'ч': ["X...X","X...X",".XXXX","....X"],
 'ш': ["X.X.X","X.X.X","X.X.X","XXXXX"],
 'ы': ["X...X","XXX.X","X..XX","XXX.X"],
 'ь': ["X....","XXXX.","X...X","XXXX."],
 'э': ["XXX.","...X","XXXX","XXX."],
 'ю': ["X.XX.","XXX.X","X.X.X","X.XX."],
 'я': [".XXX","X..X",".XXX","X..X"],
}
LOW_DESC = {  # 4 body rows + 1 tail row
 'д': ["..XXX",".X..X",".X..X","XXXXX","X...X"],
 'ц': ["X..X.","X..X.","X..X.","XXXXX","....X"],
 'щ': ["X.X.X","X.X.X","X.X.X","XXXXX","....X"],
}
LOW_ASC = {  # 5 rows, first row above x-height
 'б': [".XXXX","X....","XXXX.","X...X",".XXX."],
 'ъ': ["XX...",".X...",".XXX.",".X..X",".XXX."],
}
LOW_ASCDESC = {'ф': ["..X..",".XXX.","X.X.X","X.X.X",".XXX.","..X.."]}
LOW_ACC = {'й':'и'}
# lookalikes: Cyrillic char -> Latin char to copy glyph from
COPY = {'А':'A','В':'B','Е':'E','К':'K','М':'M','Н':'H','О':'O','Р':'P','С':'C','Т':'T','Х':'X',
        'а':'a','е':'e','о':'o','р':'p','с':'c','х':'x','у':'y','Ё':'E','ё':'e'}
ALL = [chr(c) for c in range(0x410,0x450)]+['Ё','ё']
