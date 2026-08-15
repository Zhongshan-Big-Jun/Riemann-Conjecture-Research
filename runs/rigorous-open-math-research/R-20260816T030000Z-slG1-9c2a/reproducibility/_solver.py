"""FINAL integrated exact solver: m_k via shape decomposition with exact reduction + atom
frequency-volume values. Reproduces (m1,m2,m3,m4)=(1,1,4/3,2,13/4), then computes m_5/m_6.
"""
import itertools
from fractions import Fraction as F
from collections import defaultdict
from _atom_value import atom_value

from math import comb, factorial
from functools import lru_cache
@lru_cache(None)
def c_exact(m):
    m=int(m)
    if m==1: return F(1)
    s=F(0)
    for j in range(m+1):
        x=m/2.0-j
        if x<=0: continue
        s += ((-1)**j)*comb(m,j)*F(x)**(m-1)
    return s/F(factorial(m-1))
# quick sanity of c table
print("c:", {m:(c_exact(m) if False else F.__float__(c_exact(m))) for m in [1,2,3,4,5,6,7,8,10]})

def partitions(n):
    def rec(i, blocks):
        if i==n: yield tuple(frozenset(b) for b in blocks); return
        for idx,b in enumerate(blocks):
            b2=[x for x in blocks]; b2[idx]=b|{i}; yield from rec(i+1,b2)
        yield from rec(i+1, blocks+[frozenset([i])])
    yield from rec(1,[frozenset([0])])

def blockid(pos, blocks):
    for i,blk in enumerate(blocks):
        if pos in blk: return i
    return None
def perm_sign(p):
    s=1; p=list(p)
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s

def _remove(lines, edge, m):
    u,v=edge; a,b=(u,v) if u<=v else (v,u)
    lines[(a,b)]-=m
    if lines[(a,b)]<=0: del lines[(a,b)]
def _add(lines, edge, m):
    u,v=edge; a,b=(u,v) if u<=v else (v,u)
    lines[(a,b)]=lines.get((a,b),0)+m

def reduce_value(edge_pairs, b, anchor=0):
    """Returns (rational_value, residual_atom_multigraph_or_None)."""
    lines=defaultdict(int)
    for (u,v) in edge_pairs:
        if u==v: continue
        a,b=(u,v) if u<=v else (v,u)
        lines[(a,b)]+=1
    val=F(1)
    while True:
        # zip through
        newlines={}
        for (u,v),m in lines.items():
            if u==v: continue
            newlines[(u,v)]=m
        lines=newlines
        inc=defaultdict(int)
        for (u,v),m in lines.items():
            inc[u]+=m; inc[v]+=m
        acted=False
        for v in sorted(inc):
            if v==anchor: continue
            deg=inc[v]
            nbrs=defaultdict(int)
            for (u,w),m in lines.items():
                if u==v: nbrs[w]+=m
                elif w==v: nbrs[u]+=m
            neigh=dict(nbrs)
            if deg==1:
                q=next(iter(neigh)); _remove(lines,(v,q),neigh[q])
                val*=F(1); acted=True; break
            elif len(neigh)==1:
                q=next(iter(neigh)); m=neigh[q]
                val*=c_exact(m); _remove(lines,(v,q),m); acted=True; break
            elif deg==2 and len(neigh)==2:
                n1,m1=list(neigh.items())[0]; n2,m2=list(neigh.items())[1]
                _remove(lines,(v,n1),m1); _remove(lines,(v,n2),m2)
                _add(lines,(n1,n2),1); acted=True; break
        if not acted: break
    if lines:
        return val, dict(lines)
    return val, None

def shape_value(k, blocks):
    b=len(blocks)
    nblk={p:blockid(p,blocks) for p in range(k)}
    cycle_edges=[]
    for a in range(k):
        i,j=nblk[a],nblk[(a+1)%k]
        if i!=j: cycle_edges.append((i,j))
    if b==1: return F(1), None
    total=F(0); atoms=[]
    for sig in itertools.permutations(range(b)):
        s=perm_sign(sig)
        det_pairs=[(p,sig[p]) for p in range(b) if p!=sig[p]]
        edges=list(cycle_edges)+list(det_pairs)
        val,resid=reduce_value(edges,b,anchor=0)
        if resid is not None:
            atoms.append((s,resid))
        else:
            total+=s*val
    return total, atoms

def moment(k, use_atoms=True):
    """Return (full_float, per_partition, all_distinct_float) where
    full = sum over partitions of full value; all_distinct = value of the singleton partition.
    Each partition full value = closed_v + sum(atom sign*value)."""
    tot=F(0)
    perp=[]
    ad=F(0)
    for blocks in partitions(k):
        v,atoms=shape_value(k,blocks)
        fv=v
        for s,resid in (atoms or []):
            edict={(min(u,v),max(u,v)):int(m) for (u,v),m in resid.items()}
            fv += s*atom_value(edict)
        tot+=fv
        perp.append((blocks,fv))
        if len(blocks)==k:
            ad=fv
    return tot, perp, ad

if __name__=="__main__":
    import sys
    k=int(sys.argv[1]) if len(sys.argv)>1 else 4
    tot,perp,ad=moment(k)
    print(f"m_{k} = {tot} = {float(tot):.14f}   (all-distinct D_{k} = {ad} = {float(ad):.3e})")
    from collections import defaultdict
    g=defaultdict(F)
    for blocks,fv in perp:
        sig=tuple(sorted(len(x) for x in blocks))
        g[sig]+=fv
    print("  total = ", " + ".join(f"{s}*[{v}]" for s,v in sorted(g.items())))
    print("  by sig:", {s:str(v) for s,v in sorted(g.items())})
