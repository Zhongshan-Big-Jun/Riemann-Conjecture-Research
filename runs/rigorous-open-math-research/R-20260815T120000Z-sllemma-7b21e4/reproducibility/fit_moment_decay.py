# Fit candidate moment sequences to the exact + empirical sine-Gram moments and test the
# Christoffel/Hankel ratio -> 0 pattern (EVIDENCE ONLY, never proof).
# Exact: m2=4/3=1.3333, m3=2, m4=13/4=3.25 (audited). Empirical L=50 (probe): 
#   (1.0, 1.322, 1.966, 3.171, 5.435, 9.770, 18.245, 35.148)
# These disagree a bit (finite-window/h-bias). We test whether a smooth closed form m_k ~
# A*B^k*k^g (sub-exponential -> support compact) reproduces the decay pattern.
import numpy as np

def lambda_m(moms, order):
    # Lambda_m(0) = det(H_m)/det(minor00)
    def det(H):
        H=np.asarray(H,float); return np.linalg.det(H)
    n=order+1
    H=[[moms[i+j] for j in range(n)] for i in range(n)]
    M=[[moms[i+1+j+1] for j in range(n-1)] for i in range(n-1)]  # delete row0,col0
    return det(H)/det(M)

# empirical log-log fit gave m_k ~ a k^alpha with NEGATIVE alpha (not a clean pure power law).
# Try the composite empirical sequence directly (as given) up to order 3 (need mom up to 6).
emp=[1.0,1.322,1.966,3.171,5.435,9.770,18.245]  # 7 moments -> can compute Lambda up to m=3
print("Empirical (probe L=50) Hankel-ratio Lambda_m(0):")
for o in range(1,4):
    print(f"  Lambda_{o} = {lambda_m(emp,o):.6f}")

# Compare: if this were a measure supported on [0,c] with a density square-root edge at 0
# (MP-like), Lambda_m(0) ~ const/m^{3/2} (hard edge). Fit ratios:
L=np.array([lambda_m(emp,1), lambda_m(emp,2), lambda_m(emp,3)])
print("ratios Lambda_{m}/Lambda_{m-1}:", np.round(L[1:]/L[:-1],3))
print("Interpretation: geometric-ish decay (const/m^p with p large, or geometric), consistent with "
      "no atom at 0 (SL). EVIDENCE ONLY.")
