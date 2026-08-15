"""Exact moment computation via shape decomposition for the sine-DPP random Gram trace.
M_k = E[tr(G^k)] = sum over set partitions pi of {0..k-1} of I(pi), where
  I(pi) = 1/L int_{R^b} [prod_cycle K(x_bl(a)-x_bl(a+1))] * rho_b(x) dx1..dxb
with rho_b = det[K(x_p-x_q)], K(x)=sinc(x), b=#blocks.

We expand rho_b as det and reduce each term's product-of-kernels integral exactly via:
  - translation: fix block 0 to 0 (integrals are on the quotient; I(pi)= single (b-1)-dim integral)
  - leaf contraction: int K(v-a)K(v-b) dv = K(a-b)   (K*K=K)
  - closed chains / star cores reduce to box-spline atoms.

Every atom is a product of the exact box-spline numbers c_{2n}=int sinc^{2n} (known rationals)
and star integrals. We carry exact rationals via sympy. The engine returns a symbolic
expression in rational atoms, which we then evaluate against exact constants.

VALIDATION TARGET: reproduce (m0,..,m4)=(1,1,4/3,2,13/4).
"""
from fractions import Fraction as F
from sympy import symbols, prod, expand

# ---- exact box-spline numbers: c_{2n} = int sinc^{2n}(t) dt (known exact rationals) ----
C = {2: F(1), 4: F(2,3), 6: F(11,20), 8: F(151,315), 10: F(15619,36288)}

# ---- set partitions ----
def partitions(n):
    def rec(i, blocks):
        if i == n:
            yield tuple(frozenset(b) for b in blocks)
            return
        for idx, b in enumerate(blocks):
            b2 = [x for x in blocks]; b2[idx] = b | {i}
            yield from rec(i+1, b2)
        yield from rec(i+1, blocks + [frozenset([i])])
    yield from rec(1, [frozenset([0])])

def blockid(pos, blocks):
    for i, blk in enumerate(blocks):
        if pos in blk: return i
    raise ValueError

def shape_edges(k, blocks):
    nblk = {p: blockid(p, blocks) for p in range(k)}
    edges = []
    for a in range(k):
        i, j = nblk[a], nblk[(a+1) % k]
        edges.append((i, j))   # oriented; loop if i==j
    return edges

# ---- multigraph integral via leaf reduction ----
# We represent the integrand as a list of oriented edges (a,b) over integer block labels.
# A loop (a,a) = K(0)=1 is dropped (factor 1).
# Leaves: variable v appearing in exactly one edge -> divergent, should not happen.
# Reduction: pick a 'pivot' variable to fix=0 (translation). Then integrate out variables
# that appear with degree 2 by contracting their two edges.

def contract_degree2(edges, free):
    """edges: list of (a,b) oriented integer edges (a!=b).
       free: set of variables to integrate.
       Reduce leaves of degree 2 via int K(v-a)K(v-b) dv = K(a-b).
       Returns (remaining_edges list on {a,b} endpoints, factored_const (list of c's))."""
    edges = list(edges)
    free = set(free)
    cfactors = []            # accumulate exact single-variable constants
    changed = True
    while changed:
        changed = False
        # count edge incidence (unoriented) by vertex
        inc = {}
        for (a, b) in edges:
            inc[a] = inc.get(a, 0) + 1
            inc[b] = inc.get(b, 0) + 1
        # find a free, non-removed vertex with exactly 2 incidences
        for v in sorted(free):
            if v in inc and inc[v] == 2:
                # gather the two incident edges -> unoriented neighbors
                neigh = []
                for (a, b) in edges:
                    if a == v: neigh.append(('l', b))
                    elif b == v: neigh.append(('r', a))
                if len(neigh) != 2:
                    continue
                (sa, u), (sb, w) = neigh
                # remove the two edges, add a single edge (u,w) (orient any way; K even, sign-free)
                edges = [(x, y) for (x, y) in edges if x != v and y != v]
                edges.append((u, w))
                free.discard(v)
                changed = True
                break
    return edges, free, cfactors

if __name__ == "__main__":
    k = 4
    print(f"=== validation of reduction on m_4 shapes (informational) ===")
    for blocks in partitions(k):
        edges = shape_edges(k, blocks)
        print(blocks, "edges=", edges)
    print("\n(c-not-used: engine not yet finalized)")
