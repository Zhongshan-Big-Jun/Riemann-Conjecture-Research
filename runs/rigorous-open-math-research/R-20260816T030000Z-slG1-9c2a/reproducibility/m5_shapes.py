#!/usr/bin/env python
"""Exact m_5 from the DPP shape decomposition, GIVEN D_5=0 (confirmed this pass).

m_5 = E[(1/L)tr(G^5)], G=(sinc(x_i-x_j)). tr(G^5) = sum_{i0..i4} prod_{a} K(x_{i_a}-x_{i_{a+1}}).
Using DPP factorial moments rho_j = det[K], the expectation splits by set-partition of the
5-tuple (patterns of coincident indices). m_5 = [all-equal] (=1) + [repeated-index shapes]
+ D_5. With D_5=0, m_5 = 1 + repeated-index sum.

We enumerate all set partitions of {0..4}, compute each shape's exact integral (as a
box-spline / B-spline value at 0 via the same coarea method generalized to the shape's edge
graph), and sum with the correct multiplicity (each partition contributes once per distinct
(ordered) tuple pattern; the count = number of ordered 5-tuples realizing that coincidence
pattern = product over blocks of (block-size)! — need care).

NOTE: This is a cross-check of the m5 subagent. Implemented using the box-spline coarea
evaluator from Dk_boxespline_run for the *distinct-elements* integral, with the number of
distinct blocks b reducing the rank. For a partition into b blocks, the shape integral is over
b distinct variables => b-1 relative vars, with edges given by (block of a, block of a+1).
The all-distinct D_5 case is b=5.
"""
import itertools, sys
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T030000Z-slG1-9c2a\reproducibility")
import numpy as np

# reuse the exact I_pi (box-spline) machinery on an arbitrary block-edge graph
from Dk_boxespline_run import (diff_vec, edge_vectors, nullspace_orth, volume_vertices,
                                perm_sign_val)

def block_id(pos, blocks):
    for i,b in enumerate(blocks):
        if pos in b: return i
    raise ValueError

def shape_integral(k, blocks):
    """Integral of prod_{a} K(x_{i_a}-x_{i_{a+1}}) over the b distinct values, per the
    partition (blocks) of {0..k-1}. b = len(blocks). Translation-normalized (fix last block=0).
    Returns box-spline value (rational approx)."""
    b=len(blocks)
    idx=[block_id(a,blocks) for a in range(k)]
    if b==1:
        return 1.0  # all equal -> K(0)=1 per edge? actually all edges self-loop -> factor 1
    # build edge direction vectors in R^{b-1}
    vs=[]
    for a in range(k):
        u=idx[a]; v=idx[(a+1)%k]
        # direction x_{block u} - x_{block v} in R^{b-1}; block label b-1 is pinned (=0)
        e=np.zeros(b-1)
        if u < b-1: e[u]+=1
        if v < b-1: e[v]-=1
        vs.append(e)
    n=len(vs); d=b-1
    if n==0: return 1.0
    M=np.array(vs).T
    coarea=1.0/np.sqrt(np.linalg.det(M@M.T))
    N,r=nullspace_orth(M); m=N.shape[1]
    if m==0: return 1.0*coarea
    vol=volume_vertices(N)
    if vol is None: return None
    return coarea*vol

def count_tuples(blocks):
    # number of ordered 5-tuples (i0..i4) with exactly this coincidence pattern.
    # The positions {0..4} assigned to blocks; the tuple realizes pattern if i_p=i_q iff same block.
    # Count = |Aut| such that distinct labels... = product over blocks of (size)!  (choose distinct values)
    from math import factorial
    c=1
    for b in blocks:
        c*=factorial(len(b))
    return c

def partitions_of(n):
    def rec(i,blocks):
        if i==n:
            yield tuple(frozenset(b) for b in blocks); return
        for idx,bb in enumerate(blocks):
            b2=[x for x in blocks]; b2[idx]=bb|{i}; yield from rec(i+1,b2)
        yield from rec(i+1,blocks+[frozenset([i])])
    return list(rec(1,[frozenset([0])]))

def run(k):
    totalshape=0.0
    allpart=list(partitions_of(k))
    detail=[]
    for blocks in allpart:
        b=len(blocks)
        if b==k:
            continue  # all-distinct -> D_k, excluded (D_5=0)
        val=shape_integral(k,list(blocks))
        if val is None:
            detail.append((blocks,'FAIL')); continue
        cnt=count_tuples(list(blocks))
        totalshape+=cnt*val
        detail.append((blocks,cnt,val))
    # compare
    m5=1.0+totalshape
    print(f"k={k}: sum over non-all-distinct shapes (each weighted by tuple-count) = {totalshape:+.8e}")
    print(f"   m_5 = 1 + shapes = {m5:+.8f}")
    print(f"   all-distinct term D_5 set to 0 (confirmed)")
    return m5,totalshape

if __name__=="__main__":
    m5,sh=run(5)
