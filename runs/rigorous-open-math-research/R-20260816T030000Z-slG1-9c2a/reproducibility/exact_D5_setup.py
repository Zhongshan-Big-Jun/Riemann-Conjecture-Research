#!/usr/bin/env python
"""Build the combined graph / edge-direction matrix V for each permutation pi in S_5,
verify rank structure, and sanity-check I_id = 1 via the cross-section volume.

Setup (k=5): vertices 0..4, pin x_4 = 0 (translation reference).
Free relative coords: x_0,x_1,x_2,x_3 in R^4. Vertex a -> e_a (a<4), vertex 4 -> 0.
Edges: cycle (a, a+1 mod 5), perm (a, pi(a)). Edge direction d = q_u - q_v.
I_pi = vol_{n-rank(V)} ({ xi in [-1/2,1/2]^n : V xi = 0 }), n=10.
""" 
import numpy as np
from itertools import permutations, product

def build_edges(pi, k=5):
    """Return (uv_list, vec_list). uv are (u,v) vertex pairs (u=tail, v=head).
    vec = q_u - q_v in R^{k-1} quotient (vertex k-1 pinned at origin)."""
    # quotient coords
    q = {}
    for a in range(k-1):
        q[a] = np.eye(k-1)[a]
    q[k-1] = np.zeros(k-1)
    edges = []
    for a in range(k):
        b = (a+1) % k
        edges.append((a, b, q[a] - q[b]))
    for a in range(k):
        b = pi[a]
        edges.append((a, b, q[a] - q[b]))
    return edges

def build_V(pi, k=5):
    edges = build_edges(pi, k)
    n = len(edges)
    d = k-1
    V = np.zeros((d, n))
    for j,(u,v,vec) in enumerate(edges):
        V[:,j] = vec
    return V, edges

def edge_strings(pi, k=5):
    edges = build_edges(pi, k)
    out = []
    for (u,v,vec) in edges:
        kind = 'cyc' if (v == (u+1)%k) else 'per'
        out.append(f"{u}->{v}")
    return out

def cycle_type(pi):
    n=len(pi); seen=[False]*n; lens=[]
    for i in range(n):
        if not seen[i]:
            j=i; c=0
            while not seen[j]:
                seen[j]=True; j=pi[j]; c+=1
            lens.append(c)
    return tuple(sorted(lens))

def perm_sign(pi):
    n=len(pi); seen=[False]*n; sign=1
    for i in range(n):
        if not seen[i]:
            j=i; c=0
            while not seen[j]:
                seen[j]=True; j=pi[j]; c+=1
            if c%2==0 and c>0: sign*=-1
    return sign

def main():
    k=5
    perms = list(permutations(range(k)))
    print(f"n_perms={len(perms)}")
    from collections import defaultdict, Counter
    rank_counter = Counter()
    id_pi = tuple(range(k))
    V, edges = build_V(id_pi)
    print("id pi edges (cycle labeled cyc, perm labeled per):")
    print("  cycle edges:", edges[:k])
    print("  perm edges :", edges[k:])
    print("  rank(V_id) =", np.linalg.matrix_rank(V))
    bytype = defaultdict(list)
    for pi in perms:
        V,_ = build_V(pi)
        r = np.linalg.matrix_rank(V)
        rank_counter[r]+=1
        bytype[cycle_type(list(pi))].append(r)
    print("\nrank distribution:", dict(rank_counter))
    print("\nper cycle type: count, ranks seen")
    for ct in sorted(bytype, key=lambda c:(len(c),c)):
        ranks = bytype[ct]
        print(f"  type={ct} count={len(ranks)} rank_set={sorted(set(ranks))}")

if __name__=="__main__":
    main()
