#!/usr/bin/env python
"""Degree-2 cascade reduction of the integral I_pi.

Integral over FREE variables x_0..x_{k-2} (x_{k-1}=0 pinned) of a product of K-factors
(edges of combined graph).  Use convolution identities to integrate out free variables:

  deg 1 at v  (factor K(x_v - y)):  int K(x_v - y) dx_v = 1
  deg 2 at v with distinct neighbors u,w (factors K(x_u-x_v)K(x_v-x_w)):
        int = K(x_u - x_w)   [replaces two edges by one edge (u,w)]

Vertices with degree >= 3 (or with loops/duplicate edges) block exact collapse and leave
a box-spline core.  We count how many of the 120 permutations reduce to an empty core
(fully exact, trivial) vs leave a residual box-spline.
"""
from itertools import permutations
from collections import Counter

K = 5
PINNED = K-1  # vertex label k-1 is pinned at 0, not free

def build_edges(pi):
    edges=[]  # multiset of (u,v) undirected-ish; loop (v,v) is a self-loop
    for a in range(K):
        edges.append((a,(a+1)%K))
    for a in range(K):
        edges.append((a,pi[a]))
    return edges

def degree_factors(edges, v):
    """Return list of neighbor(s) w for each factor K(x_v - x_w) incident to v.
    Factor K(x_v - x_w) means the edge contributes (v,w) in either orientation.
    A self-loop (v,v) appears when w==v."""
    fs=[]
    for (a,b) in edges:
        if a==v and b==v:
            fs.append(('loop',v))
        elif a==v:
            fs.append(('n',b))
        elif b==v:
            fs.append(('n',a))
    return fs

def reduce_exact(pi):
    """Attempt to collapse all FREE variables to empty core. Return True if all free vars
    integrated out exactly (then the constant factor is fully determined), else False."""
    edges = build_edges(pi)
    free = set(range(K-1))   # free variables to integrate out
    edges_c = list(edges)    # working edge multiset
    # We integrate out free variables greedily; each successful removal reduces free count.
    # We'll do repeated passes over free variables, removing those of degree<=2.
    changed=True
    processed=set()
    while changed:
        changed=False
        for v in list(free):
            if v in processed: continue
            fs = degree_factors(edges_c, v)
            deg = len(fs)
            if deg==0:
                free.discard(v); processed.add(v); changed=True
                continue
            if deg==1:
                n_only=[w for (t,w) in fs if t=='n']
                if len(n_only)==1 and fs[0][0]=='n':
                    w=n_only[0]
                    # int K(x_v - x_w) dx_v = 1 ; remove the single edge (v,w)
                    edges_c=[e for e in edges_c if v not in e]
                    free.discard(v); processed.add(v); changed=True
                    continue
                elif fs[0][0]=='loop':
                    # factor K(x_v-x_v)=K(0)=1 constant; drop loop, v effectively deg0
                    edges_c=[e for e in edges_c if e!=(v,v)]
                    free.discard(v); processed.add(v); changed=True
                    continue
            if deg==2:
                neighbors=sorted(w for (t,w) in fs)
                if 'loop' in [t for (t,_) in fs]:
                    # e.g. one loop + one neighbor -> like deg 1
                    n_edges=[e for e in edges_c if v in e and e!=(v,v)]
                    if len(n_edges)==1:
                        (a,b)=n_edges[0]; w = b if a==v else a
                        edges_c=[e for e in edges_c if e!=(v,v) and v not in e]
                        free.discard(v); processed.add(v); changed=True
                        continue
                if neighbors[0]!=neighbors[1]:
                    # two distinct neighbors u,w from two edges (v,u),(v,w)
                    # convolution -> one edge (u,w)
                    # identify the two neighbor edges
                    ne=[e for e in edges_c if v in e]
                    # ne has exactly two entries (u,v),(w,v)
                    us=[]
                    for (a,b) in ne:
                        us.append(b if a==v else a)
                    u,w=us
                    edges_c=[e for e in edges_c if v not in e]
                    edges_c.append((u,w))
                    free.discard(v); processed.add(v); changed=True
                    continue
                # else degree 2 but both neighbors same (double edge) -> cannot reduce simply
                # Actually int K(x_v-x_w)^2 dx_v is NOT K; blocked.
                processed.add(v)
                continue
        # end for
    return (len(free)==0), edges_c, sorted(free)

def main():
    perms=list(permutations(range(K)))
    tally=Counter()
    leftover_free=Counter()
    examples={}
    for pi in perms:
        ok,edges_c,remain=reduce_exact(pi)
        tally[ok]+=1
        leftover_free[len(remain)]+=1
        if not ok:
            examples.setdefault(len(remain),[]).append((tuple(pi),edges_c))
    print(f"k=5, {len(perms)} permutations")
    print("covolume to empty core:", dict(tally))
    print("leftover free-variable count distribution (for non-empty):", dict(leftover_free))
    for rf,exs in examples.items():
        print(f"\nnon-reducible with {rf} free vars remaining, example:")
        for pi,ec in exs[:6]:
            print("   ",pi, [tuple(e) for e in ec])

if __name__=="__main__":
    main()
