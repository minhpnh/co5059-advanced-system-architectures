"""Find slides by keywords: python3 tools/slfind.py slides/03-pipelining-lecture.pdf "Forwarding&HW" -> (slide, title)."""
import subprocess,re,sys,functools
@functools.lru_cache(None)
def pages(f):
    t=subprocess.run(['pdftotext','-layout',f,'-'],capture_output=True,text=True).stdout
    return t.split('\f')
def title(pg):
    ls=[l.strip() for l in pg.splitlines() if l.strip() and l.strip() not in ('dce','2026','BK','TP.HCM')]
    return ls[0][:60] if ls else ''
def find(f,*kws):
    out=[]
    for i,pg in enumerate(pages(f),1):
        low=pg.lower()
        if all(k.lower() in low for k in kws): out.append((i,title(pg)))
    return out
if __name__=='__main__':
    f=sys.argv[1]
    for q in sys.argv[2:]:
        print(q,'->',find(f,*q.split('&')))
