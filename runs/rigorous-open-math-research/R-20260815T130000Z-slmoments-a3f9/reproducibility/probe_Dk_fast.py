"""Efficient numerical measurement of the all-distinct terms D_3..D_6 for the sine-DPP Gram,
using the validated projection-DPP discretization.

D_k = E[ (1/N) SUM_{(i1..ik) pairwise distinct} G[i1,i2]G[i2,i3]...G[ik,i1] ].

We compute the all-distinct cyclic sum C_k(G) = SUM_distinct ... efficiently:
  - C_3, C_4: direct vectorized nested sums.
  - C_5: loop over distinct (i1,i2,i3); for fixed prefix, compute the (i4,i5) double sum via a
    masked matrix-vector product (O(N^2) per prefix; vectorized over the (i2,i3) grid).
  - C_6: loop over distinct (i1,i2,i3,i4); for fixed prefix compute the (i5,i6) double sum via
    masked matvec (O(N^2) per prefix).
Then D_k = mean over DPP samples of C_k(G)/N.

EVIDENCE ONLY. The exact statement is attempted in exact_reduction.py.
"""
import numpy as np
from projection_dpp_sampler import sample_points, kernel_matrix, cell_centers, build_gram

def C3(G):
    N=G.shape[0]; tot=0.0
    for a in range(N):
        mask=np.ones(N,bool); mask[a]=False
        b=np.nonzero(mask)[0]
        # sum over c != a,b
        for bb in b:
            m2=np.ones(N,bool); m2[[a,bb]]=False
            c=np.nonzero(m2)[0]
            tot += (G[a,bb]*G[bb,c]*G[c,a]).sum()
    return tot

def C4(G):
    N=G.shape[0]; tot=0.0
    for a in range(N):
        for b in range(N):
            if b==a: continue
            for c in range(N):
                if c in (a,b): continue
                m=np.ones(N,bool); m[[a,b,c]]=False
                d=np.nonzero(m)[0]
                tot += (G[a,b]*G[b,c]*G[c,d]*G[d,a]).sum()
    return tot

def C5(G):
    N=G.shape[0]; tot=0.0
    for a in range(N):
        Ga=G[a]
        for b in range(N):
            if b==a: continue
            Gab=Ga[b]
            for c in range(N):
                if c in (a,b): continue
                Gbc=G[b,c]
                # inner over distinct (i4,i5) not in {a,b,c}
                allowed=np.array([i for i in range(N) if i not in (a,b,c)])
                row = G[c, allowed]                 # u = G[c,i4]
                bv  = G[allowed, a]                 # v = G[i5,a]
                M = G[np.ix_(allowed, allowed)]     # M[i4,i5]=G[i4,i5]
                T = M @ bv                          # T[i4]=sum_i5 G[i4,i5]G[i5,a]
                Td = T - np.diag(M)*bv              # remove i5==i4
                tot += Gab*Gbc*(row * Td).sum()
    return tot

def C6(G):
    N=G.shape[0]; tot=0.0
    for a in range(N):
        for b in range(N):
            if b==a: continue
            Gab=G[a,b]
            for c in range(N):
                if c in (a,b): continue
                Gbc=G[b,c]
                for d in range(N):
                    if d in (a,b,c): continue
                    Gcd=G[c,d]
                    allowed=np.array([i for i in range(N) if i not in (a,b,c,d)])
                    row = G[d, allowed]
                    bv  = G[allowed, a]
                    M = G[np.ix_(allowed, allowed)]
                    T = M@bv
                    Td = T - np.diag(M)*bv
                    tot += Gab*Gbc*Gcd*(row*Td).sum()
    return tot

def measure(L, h, nsamples, kmax, seed=1):
    rng=np.random.default_rng(seed)
    xs,n=cell_centers(L,h)
    Kg=kernel_matrix(xs); A=(h*Kg); A=(A+A.T)*0.5
    accN=0.0
    accm=np.zeros(kmax); accm2=np.zeros(kmax)
    accD={k:0.0 for k in range(3,kmax+1)}; accD2={k:0.0 for k in range(3,kmax+1)}
    from projection_dpp_sampler import trace_moments
    Ns=np.zeros(nsamples)
    for s in range(nsamples):
        sel,r=sample_points(A,rng); N=len(sel); Ns[s]=N; accN+=N
        if N>=kmax:
            G=build_gram(xs[sel],xs)
            m=trace_moments(G,kmax); accm+=m; accm2+=m*m
            for k in range(3,kmax+1):
                if N>=k:
                    C={'C3':C3,'C4':C4,'C5':C5,'C6':C6}[f'C{k}'](G)
                    d=C/N; accD[k]+=d; accD2[k]+=d*d
    m=accm/nsamples
    ms=np.sqrt(np.clip(accm2/nsamples-m*m,0,None)/nsamples)
    D={k:(accD[k]/nsamples, np.sqrt(np.clip(accD2[k]/nsamples-(accD[k]/nsamples)**2,0,None)/nsamples)) for k in range(3,kmax+1)}
    return accN/nsamples, m, ms, D

if __name__=="__main__":
    import time
    # small quick: D3/D4 then D5 then D6 (bounded samples)
    for (L,h,ns,kmax) in [(25.0,0.05,120,5),(25.0,0.05,60,6)]:
        t=time.time()
        Nm,mm,ms,D=measure(L,h,ns,kmax)
        print(f"=== L={L} h={h} ns={ns} kmax={kmax} (t={time.time()-t:.0f}s) E[N]={Nm:.1f} ===",flush=True)
        print("  m_k: "+" ".join(f"{v:.4f}" for v in mm),flush=True)
        for k in sorted(D): print(f"  D{k} = {D[k][0]:+.5f} +- {D[k][1]:.5f}",flush=True)
        print(flush=True)
