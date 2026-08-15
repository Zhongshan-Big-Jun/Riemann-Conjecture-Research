"""Exact shape-contribution evaluator for the sine-DPP random Gram trace moments.

M_k = E[tr(G^k)], G_ab = K(x_a - x_b), K = sinc (projection, K*K = K).

For a set partition pi of {0..k-1} into b blocks, contribution:
  I(pi) = (1/L) * int_{R^b} EdgeProd(x) * rho_b(x) dx
  EdgeProd = prod_{a} K(x_bl(a)-x_bl(a+1)), loops a,b in same block -> K(0)=1
  rho_b(x) = det[K(x_p - x_q)]_{p,q}

By translation-invariance with the standard density normalization, I(pi) equals a single
integral over R^{b-1} (one block fixed). Implement EXACT reduction:

1. Expand rho_b = det into a signed sum over permutations (each determinant term is a product
   of b single K-factors on block-differences).
2. Each integrand term = product of single K(block_i - block_j) factors (multigraph).
3. Reduce each term to atoms using:
     L2:  int K(v-a)K(v-b) dv       = K(a-b)                     (K*K=K)
     - path chains collapse to a single K edge; a chain whose two live endpoints coincide
       with the fixed anchor degenerates to K(0)=1.
4. The remaining (non-reducible, every live var of degree>=2 and not degree-2-leaf)
   components are "atoms": irreducible box-spline integrals. Their multigraph is enumerated
   and given a canonical key; values looked up in ATOM table (computed separately).

The engine returns I(pi) as an exact sympy/rational expression.
"""
from fractions import Fraction as F
from collections import Counter, defaultdict

def partitions(n):
    def rec(i, blocks):
        if i == n:
            yield tuple(frozenset(b) for b in blocks); return
        for idx,b in enumerate(blocks):
            b2=[x for x in blocks]; b2[idx]=b|{i}; yield from rec(i+1,b2)
        yield from rec(i+1, blocks+[frozenset([i])])
    yield from rec(1,[frozenset([0])])

def blockid(pos, blocks):
    for i,blk in enumerate(blocks):
        if pos in blk: return i
    raise ValueError

def shape_edges(k, blocks):
    nblk={p:blockid(p,blocks) for p in range(k)}
    edges=[]
    for a in range(k):
        i,j=nblk[a],nblk[(a+1)%k]
        edges.append((i,j))
    return edges

# ---------- multigraph integral reduction ----------
# Represent an integrand term as a multiset of undirected edges (u,v) over integer labels,
# with a distinguished 'anchor' label A (fixed to 0). Loops (v,v) are dropped (=1).
# We integrate all labels != A.

def reduce_term(edge_list, anchor):
    """Reduce a product of K-edges (edge_list: list of (u,v) undirected, u!=v) integrated
    over all variables != anchor. Returns a factor (a Fraction/product-of-c) times a list
    of irreducible atom multigraphs (as canonical frozenset-of-multiedges)."""
    # multiset of edges
    lines = Counter()
    for (u,v) in edge_list:
        if u==v: 
            continue  # K(0)=1
        if u>v: u,v=v,u
        lines[(u,v)] += 1
    lines = dict(lines)
    cnum = F(1)
    # Repeat: contract degree-2 free vars (and collapse parallel edges).
    while True:
        # compute incidence
        inc = defaultdict(int)
        for (u,v),m in lines.items():
            inc[u]+=m; inc[v]+=m
        # find a non-anchor var with total incidence exactly 2 that we can eliminate
        target=None
        for v in inc:
            if v==anchor: continue
            if inc[v]==2:
                target=v; break
        if target is None:
            break
        # gather the two incident edge-ends
        parts=[]
        # edges incident to target, each occurrence
        for (u,v),m in list(lines.items()):
            if u==target and v!=target:
                parts += ['r']*m   # connects target->v (both K even, undirected)
            elif v==target and u!=target:
                parts += ['l']*m
        # degree 2 => two ends; their other-vertices
        others=[]
        for (u,v),m in list(lines.items()):
            o=-1
            if u==target: o=v
            elif v==target: o=u
            if o==target: continue
            if o>=0: others += [o]*m
        # removing this variable: two edges (target,o1),(target,o2) -> one edge (o1,o2)
        o1,o2=others[0],others[1]
        # delete all edges incident to target
        nlines={}
        for (u,v),m in lines.items():
            if u==target or v==target:
                continue
            nlines[(u,v)]=m
        # add merged edge o1-o2
        a,b=(o1,o2) if o1<=o2 else (o2,o1)
        nlines[(a,b)]=nlines.get((a,b),0)+1
        lines=nlines
    # Now no non-anchor var has degree 2. Remaining free vars have degree>=3 or degree1.
    # A degree-1 free var hanging off would give divergent integral; but in a valid closed
    # trace shape after det-expansion, the balance should prevent degree-1. We assert none.
    inc=defaultdict(int)
    for (u,v),m in lines.items():
        inc[u]+=m; inc[v]+=m
    for v in inc:
        if v!=anchor and inc[v]==1:
            raise ValueError(f"degree-1 free var {v} in integrand -> divergent, bug")
    # Remaining: connected components = atoms. Split edges into components among live vars.
    return cnum, lines, inc

if __name__=="__main__":
    # test on m_2 partition {{0},{1}}: edges ((0,1),(1,0)) = 2x K(0-1)
    blocks=(frozenset([0]), frozenset([1]))
    edges=shape_edges(2,blocks)
    print(blocks, edges)
    # without det (rho_2) this is just tr reduction; for now test reduce on the pure-edge product:
    # standardize: color each block distinctly? Blocks are the variables. rho_2 not included here.
    # We'll incorporate det in main solver. Quick smoke test of reduction:
    fac,lines,inc=reduce_term([(0,1),(1,0)], anchor=0)
    print("reduce {00?}:",fac,lines,inc)
