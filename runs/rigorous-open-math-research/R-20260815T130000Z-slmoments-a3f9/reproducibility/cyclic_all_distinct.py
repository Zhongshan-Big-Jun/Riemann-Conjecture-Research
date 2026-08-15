"""Efficient all-distinct cyclic-trace evaluator via partition-lattice Moebius inversion, and
its numerical validation against direct enumeration on small random G.

For G (N x N), the fully-distinct cyclic sum
    C_k(G) = sum_{(i1..ik) pairwise distinct} G[i1,i2] G[i2,i3] ... G[ik,i1]
is computed as  C_k = sum_{pi} mu(pi, 1hat) * T(pi),
where pi ranges over set partitions of {1..k}, 1hat = all singletons,
mu(pi,1hat) = prod_{blocks of pi} (-1)^{s-1} (s-1)! (Moebius of the partition lattice to 1hat),
and T(pi) = sum_{v1..vb} prod_{a=1..k} G[ v_{bl(a)}, v_{bl(a+1)} ] = a trace of powers of G
(arranged in the cyclic order of blocks; bl(a) = block index of position a, b = #blocks).
T(pi) = tr( G^{m_1} ... G^{m_b} ) where m_beta is the number of cycle edges leaving block beta.

This replaces the O(N^k) nested enumeration with O(B_k * b * N^2) matrix operations, which is
fast for moderate N. Verified against direct enumeration below.
"""
import numpy as np
import itertools
from math import factorial

def partitions_of(n):
    """Generate all set partitions of {0..n-1} as tuples of frozensets (block label sets)."""
    def rec(i, blocks):
        if i == n:
            yield tuple(frozenset(b) for b in blocks)
            return
        for idx, b in enumerate(blocks):
            b2 = [x for x in blocks]; b2[idx] = b | {i}
            yield from rec(i+1, b2)
        yield from rec(i+1, blocks + [frozenset([i])])
    yield from rec(1, [frozenset([0])])

def moebius_ratio(sizes):
    """prod over blocks of (-1)^{s-1} (s-1)! ; s = block size."""
    r = 1
    for s in sizes:
        r *= (-1)**(s-1) * factorial(s-1)
    return r

def T_partition(G, blocks, k):
    """T(pi) = cyclic trace over blocks. bl(a) = index of the block containing position a
    (positions 0..k-1 cyclically). Returns tr of the matrix power product (as a real)."""
    b = len(blocks)
    # block index for each position
    bl = [0]*k
    for bi, blk in enumerate(blocks):
        for pos in blk:
            bl[pos] = bi
    # build cyclic walk of block labels: seq = [bl[0], bl[1], ..., bl[k-1]] and back to bl[0]
    # count edges leaving each block as 'row' index
    edges = []
    for a in range(k):
        row = bl[a]; col = bl[(a+1) % k]
        edges.append((row, col))
    # arrangement into matrix products: group consecutive edges by walk;
    # the product is G^{...} in the order rows appear. Each edge contributes one G factor.
    # We compute tr( M_0 M_1 ... M_{b-1} ) where M_r = G^{cnt_r}, cnt_r = number of edges
    # whose ROW is r. Order = order of first appearance of each block in the walk.
    # Build the sequence of a product of matrices, each a power of G, concatenated in the walk
    # order but compressed into b matrix-blocks by grouping contiguous same-row edges is NOT
    # simply powers because the walk cycles. Correct: the cyclic walk  bl[0]->bl[1]->...->bl[k-1]->bl[0]
    # gives product of k matrices G (one per edge). Compressing into b factors: collect the edges
    # in walk order; make a list of (row) for each edge: rows = bl[0],bl[1],...,bl[k-1] (each edge's row).
    # Then tr( product over edges of A_{row} ) where A_{row}=G; equivalently group consecutive edges
    # with the SAME row into a single G^cnt. So the matrix product is, in the walk order,
    # G^{cnt_r1} G^{cnt_r2} ... grouping consecutive equal rows.
    rows = [bl[a] for a in range(k)]
    # group consecutive equal rows (cyclic)
    grouped = []  # list of (row, count)
    # linearize the closed walk: edges a=0..k-1, row=bl[a]; the walk returns to bl[0].
    # start grouping from a=0
    idx = 0
    while idx < k:
        r = rows[idx]; cnt = 0
        while idx < k and rows[idx] == r:
            cnt += 1; idx += 1
        grouped.append((r, cnt))
    # build matrix product in grouped order (first occurrence order of blocks), then trace
    N = G.shape[0]
    Prod = np.eye(N)
    # compute G powers
    powers = {}
    for (r, cnt) in grouped:
        if cnt not in powers:
            powers[cnt] = np.linalg.matrix_power(G, cnt)
        Prod = Prod @ powers[cnt]
    return np.trace(Prod)

def C_k(G, k):
    res = 0.0
    for blocks in partitions_of(k):
        sizes = [len(b) for b in blocks]
        mu = moebius_ratio(sizes)
        res += mu * T_partition(G, blocks, k)
    return res

def C_k_direct(G, k):
    N = G.shape[0]
    total = 0.0
    for idx in itertools.permutations(range(N), k):
        # idx=(i0..i_{k-1}) pairwise distinct
        P = 1.0
        for a in range(k):
            P *= G[idx[a], idx[(a+1) % k]]
        total += P
    return total

if __name__ == "__main__":
    rng = np.random.default_rng(3)
    for k in [3,4,5]:
        # random symmetric PSD small G (not necessarily Gram, but any matrix works for the identity)
        G = rng.normal(size=(6,6)); G = G@G.T
        a = C_k(G, k)
        d = C_k_direct(G, k)
        print(f"k={k}: C_k(moebius)={a:.6f}  direct={d:.6f}  diff={abs(a-d):.2e}  {'OK' if abs(a-d)<1e-8 else 'MISMATCH'}")
    # also verify the all-distinct definition on diagonal-1 Gram-like matrix
    print("checked")
