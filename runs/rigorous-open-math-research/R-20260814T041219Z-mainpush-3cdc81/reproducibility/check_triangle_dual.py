"""Check the 'dual form' (3.4) triangle case used in the 3-point argument.

Claim: for a 3x3 Gram matrix M of three norm<=1 vectors (i.e. PSD, diag<=1),
   tr Psi(M) >= (3/2) * (M12^2 + M13^2 + M23^2).

Compare with the block-defect lemma giving tr Psi(M) >= 2*sum_{i<j} Mij^2 in the
all-eigenvalues<=2 case; here we only need factor 3/2.

We numerically scan random 3x3 PSD matrices with diag<=1 and check whether
tr Psi(M) / (sum_{i<j} Mij^2) floor >= 1.5.  This is evidence, NOT a proof.
The unconditional part (verifier) certifies eps4 >= 221/1e6.
"""
import random
import numpy as np

def Psi_eval(val):
    if 0 <= val <= 2:
        return (val - 1.0) ** 2
    if val >= 2:
        return 2 * val - 3
    return 0.0  # eigenvalue should be >=0 for PSD

worst_ratio = float('inf')
worst_case = None
random.seed(12345)
rng = np.random.default_rng(7)
for trial in range(200000):
    # Random PSD 3x3: build from a random 3xk factors
    k = rng.integers(1, 5)
    A = rng.normal(size=(3, k))
    M = A @ A.T
    # normalize diagonals to <= 1
    d = M.diagonal()
    scale = max(1.0, float(d.max()))
    M = M / scale
    # PSD, diag<=1
    w = np.linalg.eigvalsh(M)
    # project any tiny negative
    w = np.clip(w, 0, None)
    # re-symmetrize
    diag_sq = sum(float(M[i,j])**2 for i in range(3) for j in range(3) if i<j)
    if diag_sq <= 1e-12:
        continue
    trPsi = sum(Psi_eval(float(x)) for x in w)
    ratio = trPsi / diag_sq
    if ratio < worst_ratio:
        worst_ratio = ratio
        worst_case = (M.copy(), w.copy(), trPsi, diag_sq)

print("worst ratio trPsi / (sum_{i<j} Mij^2) =", worst_ratio)
print("required >= 1.5 :", worst_ratio >= 1.5)
if worst_case:
    M, w, trPsi, ds = worst_case
    print("worst M:\n", M)
    print("eigvals:", w, "trPsi:", trPsi, "sum offdiag^2:", ds)

# Also verify the ZERO-SET sum-free claim empirically + eps4 value on the triangle
import math
sq2 = math.sqrt(2.0)
def K(x):
    # entire sinc form
    if abs(x) < 1e-15:
        return 0.5 * (1.0 + math.sin(1/sq2)/(1/sq2))  # placeholder; use direct
    return 0.5*(math.sin(math.pi*x-1/sq2)/(math.pi*x-1/sq2)
                + math.sin(math.pi*x+1/sq2)/(math.pi*x+1/sq2))
def k(x):
    return K(x)/K(0.0)
def K0():
    return sq2*math.sin(1/sq2)

def kk(x):
    if abs(x) < 1e-14:
        return 1.0
    a = math.pi*x - 1/sq2
    b = math.pi*x + 1/sq2
    Kx = 0.5*(math.sin(a)/a + math.sin(b)/b)
    return Kx/K0()

# sweep the triangle u,v>=0, u+v<=4
best = float('inf'); bestpt=None
for i in range(2001):
    u = 4.0*i/2000
    for j in range(2001):
        v = 4.0*j/2000
        if u+v > 4.0+1e-9: break
        val = kk(u)**2+kk(v)**2+kk(u+v)**2
        if val < best:
            best = val; bestpt=(u,v)
print("empirical min of k(u)^2+k(v)^2+k(u+v)^2 on {u+v<=4}:", best, "at", bestpt)
print("claimed eps4 >= 221/1e6 =", 221/1e6)
print("best < claimed ?", best < 221/1e6)
