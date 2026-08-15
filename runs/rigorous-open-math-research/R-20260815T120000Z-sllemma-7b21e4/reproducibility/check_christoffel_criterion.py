# Verify the Christoffel/Hankel ratio criterion used in SL approach.
# 1) For a probability measure with an ATOM at 0: Lambda_m(0) -> mu({0}).
# 2) For a measure with continuous density (rho(0)>0), no atom: Lambda_m(0) -> 0.
# 3) The Hankel-ratio identity Lambda_m(0) = det(H_m with 0th row/col deleted)/det(H_m).
# Evidence only; used to validate the criterion that would turn SL into a moment-growth question.
import numpy as np
import math

def moments_from(lo, hi):
    """moments of several model measures; return callable(fn)->np array."""
    return None

def hankel_det(moms, order):
    # (order+1)x(order+1) Hankel matrix of moments mom[0..2*order]
    H = np.zeros((order+1, order+1))
    for i in range(order+1):
        for j in range(order+1):
            H[i, j] = moms[i+j]
    return np.linalg.det(H)

def lambda_m(moms, order):
    # Lambda_m(0) = 1/K_m(0,0) = det(H_m) / det(H_m with 0th row & col deleted).
    # min_{p(0)=1, deg<=m} int p^2 dmu = 1/( [H_m^{-1}]_{00} ) = det(H_m)/det(minor00).
    numerator = hankel_det(moms, order)
    denominator = hankel_det(moms[2:], order-1)
    return numerator / denominator

# ---- Test case 1: atom at 0 of mass c, plus exponential tail on (0,inf).
# mu = c*delta_0 + (1-c)*(Exponential(rate))   so moments m_k = (1-c)*k!
# 
def atom_moments(c, N):
    out=[1.0]  # m_0 = total mass = 1 always
    for k in range(1, N+1):
        out.append((1-c)*float(math.factorial(k)))
    return np.array(out)

print("=== Test 1: atom at 0 of mass c, exp(1) tail. Lambda_m(0) should -> c ===")
for c in [0.3, 0.5, 0.7]:
    row=[]
    moms = atom_moments(c, 24)
    for m in [1,2,3,4,5,6,7,8,10,12]:
        row.append(f"{lambda_m(moms,m):.4f}")
    print(f"c={c}: " + " ".join(row))

# ---- Test case 2: no atom, continuous density rho(x) = 2*(1-x) on [0,1] (triangular). 
# moments m_k = int_0^1 2(1-x)x^k dx = 2/(k+1) - 2/(k+2) = 2/((k+1)(k+2))
def tri_moments(N):
    return np.array([2.0/((k+1)*(k+2)) for k in range(N+1)])

print("\n=== Test 2: triangular density on [0,1], rho(0)=2>0. Lambda_m(0) should -> 0 ===")
row=[]
moms = tri_moments(24)
for m in [1,2,3,4,5,6,8,10,12]:
    row.append(f"{lambda_m(moms,m):.4f}")
print("tri: " + " ".join(row))

# ---- Test case 3: density vanishing at 0: rho(x)= x on [0,1] (no atom at 0 BUT 0 in supp,
# density ->0). Lambda_m(0) -> ?  m_k = int_0^1 x^(k+1) dx = 1/(k+2).
def linear_moments(N):
    return np.array([1.0/((k+2)) for k in range(N+1)])
print("\n=== Test 3: linear density rho(x)=x on [0,1] (rho(0)=0, still 0 in supp). ===")
row=[]
moms = linear_moments(24)
for m in [1,2,3,4,5,6,8,10,12]:
    row.append(f"{lambda_m(moms,m):.4f}")
print("lin: " + " ".join(row))

# ---- Test case 4: support strictly away from 0: uniform-ish on [a,b], a>0. 
# Here mu({0})=0 BUT 0 not in support. Lambda_m(0) -> 0 STILL (no atom). This confirms the
# theorem needs only no-atom, not 0-in-supp for the bound mu((0,inf))=1.
def away_moments(N, a, b):
    # uniform on [a,b]: m_k = (b^{k+1}-a^{k+1})/((k+1)(b-a))
    return np.array([(b**(k+1)-a**(k+1))/((k+1)*(b-a)) for k in range(N+1)])
print("\n=== Test 4: uniform on [1,2] (support away from 0; no atom at 0; 0 NOT in supp). ===")
row=[]
moms = away_moments(24,1.0,2.0)
for m in [1,2,3,4,5,6,8,10,12]:
    row.append(f"{lambda_m(moms,m):.4f}")
print("U[1,2]: " + " ".join(row))

print("\nDONE. If test1 -> c, tests2/3/4 -> 0, the criterion Lambda_m(0)=minor/det -> mu({0}) "
      "is numerically validated, i.e. SL reduces to showing the moment Hankel ratio -> 0.")
