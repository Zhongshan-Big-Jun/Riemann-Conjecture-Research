"""Engine v4 (final approach): exact shape contributions for the sine-DPP random-Gram trace
moments m_k = E[tr(G^k)]/L  (translation-invariant exact limit).

Shape for set partition pi (b blocks over R):
  M^(pi) = int_{R^{b-1}} (prod cycle edges) * rho_b(y) dy    (anchor block0 -> 0)
Tiled density normalization gives exactly this (b-1)-dim integral.
rho_b = det[K(x_p-x_q)] expanded as signed sum over permutations.

Reduce each det-expansion term's multigraph of K-factors EXACTLY:
  loop(v,v)                    -> factor 1   (=K(0))
  free var degree 1            -> factor c1= int sinc = 1, remove
  free var degree m, all->one q-> factor c_m = int sinc^m (m even; use exact box number), remove
                                 (if m odd we'd need c_m odd: int sinc^odd; those integrate to 1? no:
                                  int sinc^{2t+1} is a nonzero rational; handle if arises)
  free var degree 2, two diff neighbors -> idempotent merge (K*K=K), factor 1
  else (genuine atom)          -> residue, value computed separately (atom table)

Anchors never integrated out. The final value = product of c-factors times atom values.
Only the anchor + genuine-atom structure survives reduction for non-c products.

Validation: reproducing (m2,m3,m4) = (4/3, 2, 13/4).
"""
import itertools
from fractions import Fraction as F
from collections import Counter, defaultdict

# exact box numbers: c_m = int sinc^m  (m>=1), all rational via central box-spline value B_m(0).
# B_m(x) = m-fold normalized box self-convolution = (m-1)-th order B-spline of the symmetric
# box; B_m(0) given by the standard B-spline knot formula.
from math import comb, factorial
def c_CACHE():
    from functools import lru_cache
    @lru_cache(None)
    def c(m):
        m=int(m)
        if m<=0: raise ValueError(m)
        if m==1: return F(1)   # int sinc = 1
        # B-spline value at 0: B_m(0)=1/(m-1)! * sum_{j} (-1)^j C(m,j) (m/2 - j)^{m-1}_{+}
        s=F(0)
        for j in range(0, m+1):
            x=m/2.0 - j
            if x<=0: continue
            s += ((-1)**j)*comb(m,j)*F(x)**(m-1)
        return s/F(factorial(m-1))
    return c
c_mem = c_CACHE()

def c_even(n):
    return c_mem(int(n))

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

def reduce_value(edge_pairs, b, anchor=0):
    """edge_pairs: list of (u,v) undirected, u!=v, over ints 0..b-1.
    Compute exact value = product of c-factors, or return 'ATOM' if a genuine atom blocks.
    Returns (value, atom_edge_multiset or None, remaining_edges)."""
    lines=Counter()
    for (u,v) in edge_pairs:
        if u==v: continue
        if u>v: u,v=v,u
        lines[(u,v)]+=1
    lines=dict(lines)
    val=F(1)
    while True:
        # drop loops (shouldn't be here since u!=v, but after merges there could be self-loop)
        changed_col=False
        newlines={}
        for (u,v),m in lines.items():
            if u==v:
                # loop = K(0)^m = 1
                changed_col=True
                continue
            newlines[(u,v)]=m
        lines=newlines
        # incidence
        inc=defaultdict(int)
        for (u,v),m in lines.items():
            inc[u]+=m; inc[v]+=m
        # candidate free vars to reduce
        acted=False
        for v in sorted(inc):
            if v==anchor: continue
            deg=inc[v]
            # find distinct neighbors and counts
            nbrs=Counter()
            for (u,w),m in lines.items():
                if u==v: nbrs[w]+=m
                elif w==v: nbrs[u]+=m
            neigh=dict(nbrs)
            if deg==1:
                # factor int K = 1 ; remove edge
                val *= F(1)
                u0=next(iter(neigh))
                mp=neigh[u0]
                _remove_edge(lines, (v,u0), mp)
                acted=True; break
            elif len(neigh)==1:
                # all m edges to single neighbor -> c_m
                q=next(iter(neigh)); m=neigh[q]
                val *= c_even(m)
                _remove_edge(lines, (v,q), m)
                acted=True; break
            elif deg==2 and len(neigh)==2:
                # idempotent merge: int K(v-n1)K(v-n2) dv = K(n1-n2)
                n1,m1=list(neigh.items())[0]; n2,m2=list(neigh.items())[1]
                _remove_edge(lines,(v,n1),m1); _remove_edge(lines,(v,n2),m2)
                _add_edge(lines, (min(n1,n2),max(n1,n2)), 1)
                acted=True; break
        if not acted:
            break
    # After reduction, remaining edges among free vars with deg>=3 (genuine atom) or deg 2 cycles
    if lines:
        # genuine atom residue
        return val, lines, True
    return val, None, False

def _remove_edge(lines, edge, m):
    u,v=(edge[0],edge[1])
    a,b=(u,v) if u<=v else (v,u)
    lines[(a,b)]-=m
    if lines[(a,b)]<=0: del lines[(a,b)]

def _add_edge(lines, edge, m):
    u,v=(edge[0],edge[1])
    a,b=(u,v) if u<=v else (v,u)
    lines[(a,b)]=lines.get((a,b),0)+m

def shape_value(k, blocks):
    """Exact value of the shape (set partition blocks) contribution to m_k."""
    b=len(blocks)
    nblk={p:blockid(p,blocks) for p in range(k)}
    cycle_edges=[]
    for a in range(k):
        i,j=nblk[a],nblk[(a+1)%k]
        if i!=j: cycle_edges.append((i,j))
    # note: if b==1, contribution = int rho_1(a) = int 1 dy = 1 (the 'all equal' term)
    if b==1: return F(1), None
    total=F(0)
    atoms=[]
    had_atom=False
    for sig in itertools.permutations(range(b)):
        s=perm_sign(sig)
        det_pairs=[(p,sig[p]) for p in range(b) if p!=sig[p]]
        edges=list(cycle_edges)+list(det_pairs)
        val,resid,isatom=reduce_value(edges,b,anchor=0)
        if isatom:
            had_atom=True
            atoms.append((s,resid))
        else:
            total += s*val
    if had_atom:
        return None, atoms   # blocked by atom (value incompletely closed)
    return total, None

if __name__=="__main__":
    import sys
    k=int(sys.argv[1]) if len(sys.argv)>1 else 4
    total=F(0)
    blocked_list=[]
    for blocks in partitions(k):
        v,atoms=shape_value(k,blocks)
        if v is None:
            blocked_list.append((blocks,atoms)); continue
        total+=v
    print(f"m_{k} = {total} = {float(total)}")
    if blocked_list:
        print("ATOMS unresolved:", len(blocked_list))
        for blocks,atoms in blocked_list[:8]:
            print("  partitions", tuple(tuple(sorted(x)) for x in blocks),
                  "-> atoms", [(s, sorted((u,v,m) for (u,v),m in r.items())) for (s,r) in atoms])
