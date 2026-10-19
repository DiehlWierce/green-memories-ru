import re,json,glob,sys
sys.path.insert(0,'/home/claude/work')
from classify import groups,rom
from measure import pw
import mkutts
utts=json.load(open('/home/claude/work/utts.json'))
PTL={}   # gi -> list of (k,text) PT lines in order
for u in utts:
    PTL.setdefault(u['gi'],[]).extend(u['lines'])
def parse_files(pattern='/home/claude/work/tr/tr*.txt'):
    res={}; errs=[]
    for fn in sorted(glob.glob(pattern)):
        cur=None; blocks=[]
        for ln in open(fn,encoding='utf8').read().split('\n'):
            if ln.startswith('@'):
                cur=[ln[1:].strip(),[]]; blocks.append(cur)
            elif cur is not None:
                cur[1].append(ln)
        for key,lines in blocks:
            while lines and lines[-1]=='' : lines.pop()
            gi,k=map(int,key.split('.'))
            seq=[kk for kk,_ in PTL.get(gi,[])]
            if k not in seq: errs.append(f'{key}: not a PT line start'); continue
            pos=seq.index(k)
            ustarts={u['k0'] for u in utts if u['gi']==gi}
            endpos=pos+len(lines)
            if endpos<len(seq) and seq[endpos] not in ustarts: errs.append(f'{key}: block ends mid-utterance (lines {len(lines)}; next PT line {gi}.{seq[endpos]} not an utterance start)')
            if endpos>len(seq): errs.append(f'{key}: too many lines')
            for j,l in enumerate(lines):
                if pos+j>=len(seq): errs.append(f'{key}: too many lines ({len(lines)})'); break
                kk=seq[pos+j]
                if (gi,kk) in res: errs.append(f'{gi}.{kk}: duplicate translation')
                res[(gi,kk)]=l
    return res,errs
SPK=re.compile(r'^<b>[^<]*:\s*</>')
def check(res,limit=195,qlimit=270):
    errs=[]
    for (gi,k),ru in sorted(res.items()):
        pt=dict(PTL[gi])[k]
        lim=qlimit if gi<=5 else limit
        # tags: per-line balance
        opens=sum(ru.count(tg) for tg in ('<b>','<y>','<g>','<r>'))
        if opens!=ru.count('</>'): errs.append(f'{gi}.{k} unbalanced tags: {ru}')
        if bool(SPK.match(ru))!=bool(SPK.match(pt)): errs.append(f'{gi}.{k} speaker-tag mismatch: PT={pt!r} RU={ru!r}')
        if pt.startswith('  ')!=ru.startswith('  '): errs.append(f'{gi}.{k} indent mismatch {ru!r}')
        try:
            w=pw(ru)
            if w>lim: errs.append(f'{gi}.{k} width {w}>{lim}: {ru}')
        except KeyError as e: errs.append(f'{gi}.{k} bad char {e}: {ru}')
    return errs
def missing(res):
    return [(gi,k,t) for gi,l in PTL.items() for k,t in l if (gi,k) not in res]
if __name__=='__main__':
    res,e=parse_files(); print('translated',len(res),'parse errors',len(e)); print('\n'.join(e))
    ce=check(res); print('check errors',len(ce)); print('\n'.join(ce))
    m=missing(res); print('missing',len(m),'of',sum(len(v) for v in PTL.values()))
