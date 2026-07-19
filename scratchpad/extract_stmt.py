import sys, re
from html.parser import HTMLParser

class T(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables=[]; self.cur=None; self.row=None
        self.in_cell=False; self.buf=''; self.depth=0
    def handle_starttag(self, tag, attrs):
        if tag=='table':
            self.depth+=1
            if self.depth==1:
                self.cur=[]; self.tables.append(self.cur)
        elif tag=='tr' and self.depth==1:
            self.row=[]
        elif tag in ('td','th') and self.depth==1:
            self.in_cell=True; self.buf=''
    def handle_endtag(self, tag):
        if tag=='table':
            if self.depth==1: self.cur=None
            self.depth=max(0,self.depth-1)
        elif tag=='tr' and self.depth==1:
            if self.row is not None: self.cur.append(self.row)
            self.row=None
        elif tag in ('td','th') and self.depth==1:
            self.in_cell=False
            self.row.append(re.sub(r'\s+',' ',self.buf).strip())
            self.buf=''
    def handle_data(self, d):
        if self.in_cell: self.buf+=d

def clean(s):
    s=s.strip()
    neg = s.startswith('(') and s.endswith(')')
    s=s.strip('()')
    s=s.replace('$','').replace(',','').replace('%','').strip()
    if s in ('','—','--','N/A','n/a','*','na','NM','n.m.') : return None
    if neg: s='-'+s
    return s

src=sys.argv[1]
html=open(src,encoding='utf-8',errors='replace').read()
p=T(); p.feed(html)
target=None
for tbl in p.tables:
    if not tbl: continue
    ncols=max((len(r) for r in tbl), default=0)
    if ncols!=4: continue
    txt=' '.join(' '.join(r) for r in tbl).lower()
    if ('revenue' in txt or 'net sales' in txt) and 'net income' in txt:
        target=tbl; break
if target is None:
    cands=[t for t in p.tables if t and max((len(r) for r in t),default=0)==4]
    cands.sort(key=len, reverse=True)
    target=cands[0] if cands else None
if target is None:
    print("NO TABLE FOUND"); sys.exit(1)
print(f"# rows={len(target)} cols=4  (source {src})")
for r in target:
    label=r[0] if r else ''
    vals=r[1:4]
    def cv(v):
        c=clean(v) if v is not None else None
        return c if c is not None else '<BLANK>'
    print("ROW |", label, "||", " | ".join(cv(v) for v in vals))
