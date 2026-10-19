import struct
B=0x08000000
class Rom:
    def __init__(s,path):
        s.d=bytearray(open(path,'rb').read()); s.orig_len=len(s.d)
    def pairs_for(s,addr,end):
        out=[]
        pb=struct.pack('<II',B+addr,B+end)
        i=0
        while True:
            i=s.d.find(pb,i,s.orig_len)
            if i<0: break
            if i%4==0: out.append(i)
            i+=1
        return out
    def alloc(s,data):
        while len(s.d)%4: s.d.append(0)
        a=len(s.d); s.d+=data+b'\0'
        return a
    def replace_string(s,addr,old_len,new):
        pl=s.pairs_for(addr,addr+old_len)
        na=s.alloc(new)
        for p in pl:
            struct.pack_into('<II',s.d,p,B+na,B+na+len(new))
        return len(pl)
    def save(s,path): open(path,'wb').write(s.d)
