"""In-order 5-stage MIPS pipeline timing (no forwarding / forwarding) and LaTeX grid output.
Course convention: register write in the first half, read in the second half; a stalled
instruction waits in ID, the one behind waits in IF."""
# In-order 5-stage MIPS pipeline timing (course convention: reg write 1st half, read 2nd half;
# stalled instr waits in ID, the one behind waits in IF).
import sys
def parse(code):
    out=[]
    for s in code:
        op,args=s.split(None,1); a=[x.strip() for x in args.replace('(',',').replace(')','').split(',')]
        if op=='lw': out.append(dict(t=s,op=op,dst=a[0],src=[a[2]],sdata=None))
        elif op=='sw': out.append(dict(t=s,op=op,dst=None,src=[a[2]],sdata=a[0]))
        else: out.append(dict(t=s,op=op,dst=a[0],src=[x for x in a[1:] if x.startswith('$')],sdata=None))
    return out
def sim(code,fwd):
    I=parse(code); R=[]
    for i,x in enumerate(I):
        F = 1 if i==0 else R[i-1]['D']
        D = F+1 if i==0 else max(F+1, R[i-1]['E'])
        E = D+1 if i==0 else max(D+1, R[i-1]['E']+1)
        for j in range(i-1,-1,-1):
            p=I[j]
            for r in x['src']:
                if p['dst']==r and all(I[k]['dst']!=r for k in range(j+1,i)):
                    if not fwd: E=max(E,R[j]['W']+1)
                    else: E=max(E, R[j]['E']+1 if p['op']!='lw' else R[j]['M']+1)
            r=x['sdata']
            if r and p['dst']==r and all(I[k]['dst']!=r for k in range(j+1,i)):
                if not fwd: E=max(E,R[j]['W']+1)
                elif p['op']=='lw': E=max(E,R[j]['M'])
        R.append(dict(F=F,D=D,E=E,M=E+1,W=E+2))
    return I,R
def row(r):
    c={r['F']:'IF'}
    for k in range(r['F']+1,r['D']): c[k]='stall'
    c[r['D']]='ID'
    for k in range(r['D']+1,r['E']): c[k]='stall'
    c[r['E']]='EX'; c[r['M']]='MEM'; c[r['W']]='WB'; return c
def latex(code,fwd,labels=None):
    I,R=sim(code,fwd); n=R[-1]['W']
    lines=[r'\begin{center}\scriptsize\setlength{\tabcolsep}{1.6pt}',
           r'\begin{tabular}{@{}l'+'c'*n+'@{}}', r'\toprule',
           'Instruction & '+' & '.join(str(k) for k in range(1,n+1))+r' \\', r'\midrule']
    for i,(x,r) in enumerate(zip(I,R)):
        c=row(r); lab=(labels[i] if labels else '')+r'\texttt{'+x['t'].replace('$',r'\$')+'}'
        cells=[{'stall':r'\textit{st}'}.get(c.get(k,''),c.get(k,'')) for k in range(1,n+1)]
        lines.append(lab+' & '+' & '.join(cells)+r' \\')
    lines+= [r'\bottomrule',r'\end{tabular}',r'\end{center}']
    stalls=n-(len(I)+4)
    return '\n'.join(lines), n, stalls
if __name__=='__main__':
    lec=['lw $t0,0($t2)','lw $t1,4($t4)','add $t3,$t0,$t1','sw $t3,8($t2)','lw $t0,12($t4)','add $t3,$t0,$t1','sw $t3,16($t2)']
    for fwd in (False,True):
        t,n,s=latex(lec,fwd); print('fwd',fwd,'cycles',n,'stalls',s)
    re=[lec[i] for i in (0,1,2,4,3,5,6)]
    print('reorder', latex(re,True)[1:])
    rn=['lw $t0,0($t2)','lw $t1,4($t4)','lw $t5,12($t4)','add $t3,$t0,$t1','sw $t3,8($t2)','add $t6,$t5,$t1','sw $t6,16($t2)']
    print('renamed', latex(rn,True)[1:])
    h=['add $t1,$t2,$t3','sub $t4,$t1,$t5','lw $t2,0($t4)','or $t1,$t6,$t7','sw $t2,4($t1)']
    print('hz nofwd', latex(h,False)[1:], 'fwd', latex(h,True)[1:])
