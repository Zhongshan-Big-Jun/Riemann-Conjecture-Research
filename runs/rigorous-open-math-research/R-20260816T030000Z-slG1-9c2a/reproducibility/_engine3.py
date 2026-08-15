"""Engine v3: EXACT shape reduction via idempotence (K*K=K) leaf/chain contraction + atom
classification. For each set partition of {0..k-1}, expand rho_b = det over all permutations,
reduce each determinant-term's kernel-product multigraph, and classify the residcore atoms.

Goal: enumerate ALL irreducible (atom) multigraphs that arise for m_k (k<=5), so we know the
exact constants we must source. Atoms are evaluated exactly elsewhere; here we only classify.
"""
from collections import Counter, defaultdict

def partitions(n):
    def rec(i, blocks):
        if i == n: yield tuple(frozenset(b) for b in blocks); return
        for idx,b in enumerate(blocks):
            b2=[x for x in blocks]; b2[idx]=b|{i}; yield from rec(i+1,b2)
        yield from rec(i+1, blocks+[frozenset([i])])
    yield from rec(1,[frozenset([0])])

def blockid(pos, blocks):
    for i,blk in enumerate(blocks):
        if pos in blk: return i
    raise ValueError

def perms_of(n):
    import itertools
    return list(itertools.permutations(range(n)))

def reduce_core(edge_list, anchor=0):
    """edge_list: list of (u,v) undirected nonzero edges. anchor=label fixed to 0.
    Returns canonical multigraph (frozenset of ((u,v),m)) after all degree-2 free-var
    contractions; parallel edges allowed. Loop-free (already dropped)."""
    lines = Counter()
    for (u,v) in edge_list:
        if u==v: continue
        if u>v: u,v=v,u
        lines[(u,v)] += 1
    lines=dict(lines)
    while True:
        inc=defaultdict(int)
        for (u,v),m in lines.items():
            inc[u]+=m; inc[v]+=m
        target=None
        for v in inc:
            if v==anchor: continue
            if inc[v]==2:
                target=v; break
        if target is None: break
        others=[]
        for (u,v),m in list(lines.items()):
            if u==target and v!=target: others += [v]*m
            elif v==target and u!=target: others += [u]*m
        o1,o2=others[0],others[1]
        nlines={}
        for (u,v),m in lines.items():
            if u==target or v==target: continue
            nlines[(u,v)]=m
        a,b=(o1,o2) if o1<=o2 else (o2,o1)
        nlines[(a,b)]=nlines.get((a,b),0)+1
        lines=nlines
    # canonical: normalize labels by BFS/sorted relabel keeping anchor as 0
    # keep labels; return frozenset of ((u,v),m)
    return frozenset(( (u,v),m ) for (u,v),m in lines.items())

def all_terms(k, blocks):
    """Return list of (sign, reduced_core) for each det-expansion term of shape(blocks)."""
    b=len(blocks)
    edges=[]  # undirected, cycle edges (loops dropped)
    nblk={p:blockid(p,blocks) for p in range(k)}
    for a in range(k):
        i,j=nblk[a],nblk[(a+1)%k]
        if i!=j: edges.append((i,j))
    results=[]
    for sig in perms_of(b):
        det_pairs=[]
        for p in range(b):
            gp=sig[p]
            if p!=gp: det_pairs.append((p,gp))  # loops K(x_p-x_p)=1 dropped
        # combine
        import itertools
        signed = (-1)**(len([1 for i in range(b) if sig[i]!=i and False] or []))
        # sign of permutation sig (compute properly):
        s=perm_sign(sig)
        full_edges = list(edges)+list(det_pairs)
        core=reduce_core(full_edges, anchor=0)
        results.append((s, core))
    return results

def perm_sign(p):
    s=1
    p=list(p)
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s

if __name__=="__main__":
    import sys
    k=int(sys.argv[1]) if len(sys.argv)>1 else 4
    allp=list(partitions(k))
    print(f"{k=}: {len(allp)} partitions; per partition, det-order b!, classify atoms")
    atom_counter=Counter()
    from collections import defaultdict
    byshape=defaultdict(set)
    for blocks in allp:
        if len(blocks)==1: continue
        terms=all_terms(k,blocks)
        for s,core in terms:
            if core:
                atom_counter[core]+=1
                byshape[blocks].add(core)
    print("distinct atom cores (across all shapes):", len(atom_counter))
    for a,c in sorted(atom_counter.items(), key=lambda x:(len(x[0]),x[1])):
        print("  ", c, "x", sorted((u,v,m) for (u,v),m in a))
