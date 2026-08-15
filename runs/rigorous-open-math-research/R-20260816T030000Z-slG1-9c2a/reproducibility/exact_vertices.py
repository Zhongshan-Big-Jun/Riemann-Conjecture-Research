#!/usr/bin/env python
"""Enumerate EXACT rational vertices of the cross-section polytope
P = { V xi = 0, |xi_i| <= 1/2 }, i=1..n (n=2k). Vertex = 6 coordinates at +-1/2
(generic), solve 4x4 for the other 4, check feasibility |other|<=1/2.
Vertices are rational because V is integer.
Also returns them for triangulation. Uses sympy for exactness.
"""
import numpy as np
from itertools import permutations, combinations
from fractions import Fraction

def build_edges(pi,k=5):
    E=[]
    for a in range(k): E.append((a,(a+1)%k))
    for a in range(k): E.append((a,pi[a]))
    return E

def build_V(pi,k=5):
    d=k-1
    q=[None]*k
    for a in range(d): q[a]=list(np.eye(d)[a])
    q[k-1]=[0]*d
    E=build_edges(pi,k)
    V=[[0]*len(E) for _ in range(d)]
    for j,(u,v) in enumerate(E):
        for r in range(d):
            V[r][j]=q[u][r]-q[v][r]
    return V,E

def solve_fraction(A,b):
    """Solve A x = b with sympy Rational, A m x n, return exact solution or None."""
    import sympy as sp
    A=[list(map(sp.Rational,x)) for x in A]
    b=[sp.Rational(x) for x in b]
    M,dim=len(A),len(A[0])
    mat=sp.Matrix(A); bb=sp.Matrix(b)
    # solve by elimination; augmented
    aug=mat.row_join(bb)
    rref,piv=aug.rref()
    # check consistency
    for r in range(M):
        if all(piv!=c for c in range(dim)) :
            if rref[r,dim]!=0:
                return "INFEASIBLE_ROW"
    sol=[None]*dim
    for r,c in enumerate(piv):
        if c<dim: sol[c]=rref[r,dim]
    return sol  # list of Rational (or None for free = not expected)

def exact_vertices(pi,k=5):
    V,E=build_V(pi,k)
    n=len(E); d=k-1
    verts=set()
    # choose which d coords are FREE (solved), others fixed to +-1/2
    # Actually: fix (n-d-d) = n-d -? A vertex: 6 tight box facets -> we set 6 coords to +-1/2
    tight_count = n-d  # = 6 for k=5
    import itertools
    for free_set in combinations(range(n), d):  # the d solved coords
        fixed = [i for i in range(n) if i not in free_set]
        # fixed has n-d entries, each to +-1/2
        for signs in itertools.product([Fraction(1,2),Fraction(-1,2)], repeat=(n-d)):
            # build A (d x d) for free coords: V[:,free] x_free = - sum_{fixed} V[:,j]*sign_j
            A=[[V[r][j] for j in free_set] for r in range(d)]
            b=[-sum(V[r][j]*signs[fixed.index(j)] for j in fixed) for r in range(d)]
            sol=solve_fraction(A,b)
            if isinstance(sol,str): continue
            if None in sol: continue
            # check all fixed within box (they are exactly +-1/2) and free within box
            pt=[None]*n
            for idx,j in enumerate(fixed): pt[j]=signs[idx]
            for idx,j in enumerate(free_set): pt[j]=sol[idx]
            if all(abs(p)<=Fraction(1,2) for p in pt):
                verts.add(tuple(pt))
    return verts,E

def main():
    k=5
    # a hard permutation: the one from qhull with nverts=48 and I=2/3 e.g. (4,1,2,3,0)
    for pi in [(4,1,2,3,0),(3,4,0,1,2) if False else (2,3,4,0,1)]:
        vt,E=exact_vertices(pi,k)
        print(f"pi={pi}: found {len(vt)} exact vertices")
        # print a couple
        for v in list(vt)[:3]:
            print("   ",v)
    # id check: should be 64 vertices and I=1
    vt,E=exact_vertices((0,1,2,3,4),5)
    print(f"id: {len(vt)} vertices (Qhull said 64)")

if __name__=="__main__":
    main()
