"""Find H&P 5th ed. pages: python3 tools/hpfind.py "regex" ... -> (PDF page, printed page)."""
import re,sys
import os,subprocess
# Text of the textbook, extracted once with pdftotext into tools/.hp.txt (ignored by git).
HERE=os.path.dirname(os.path.abspath(__file__))
PDF=os.path.join(HERE,'..','references','Computer Architecture - A Quantitative Approach.pdf')
S=os.path.join(HERE,'.hp.txt')
if not os.path.exists(S):
    subprocess.run(['pdftotext','-layout',PDF,S],check=True)
P=open(S).read().split('\f')
OFF={'':29,'A':523,'B':579,'C':647,'D':736,'E':804,'F':831,'G':949,'H':984,'I':1029,'J':1076,'K':1150}
def printed(i):  # i = 1-based pdf page
    head=' '.join(P[i-1].strip().splitlines()[:2])
    m=re.search(r'\b([A-K])-(\d+)\b',head)
    if m and 520<i: return f"{m.group(1)}-{m.group(2)}"
    if i<=522: return str(i-29)
    return '?'
def find(pat,lo=1,hi=1358,maxn=8,flags=re.I):
    out=[]
    for i in range(lo,hi+1):
        if re.search(pat,P[i-1],flags): out.append((i,printed(i)))
        if len(out)>=maxn: break
    return out
if __name__=='__main__':
    for a in sys.argv[1:]:
        print(a,'->',find(a))
