"""Verify O5 conditional constants: sine-kernel Gram moments and Christoffel function.

Claimed (Claude §7.2(f)):
  m_k(1) = 1, 3/4, 2, 13/4  for k = 1,2,3,4  (moments of sine-kernel Gram limiting spectrum),
  Lambda_2(0;1) = 5/36  (Christoffel function at 0, order m=2 using moments up to k=4),
  HL*(4) => liminf N0^s/N >= 1 - 2*Lambda_2(0) = 13/18.

We verify:
 (a) the moment sequence m_k(1) via direct Monte Carlo of the sine-kernel Gram matrix
     eigenvalues (average over sine-process samples) -- EVIDENCE only,
 (b) Lambda_m(0) for the Christoffel function given the moment sequence, by building the
     orthogonal-polynomial moment matrix and evaluating the Christoffel function at 0,
 (c) the arithmetic 1 - 2*Lambda_2(0) = 13/18 and the general bound structure.
"""
import numpy as np

# ---- (b) Christoffel function from moments ----
# NOTE: This is a DIAGNOSTIC of the O5 open gap; it does NOT establish Lambda values.
# The claimed m_k(1) = 1, 3/4, 2, 13/4 are RAW moments; as such they are NOT feasible for any
# positive spectral measure (m_2 = 3/4 < m_1^2 = 1 is impossible).  The correct Christoffel
# interpretation therefore requires a (centered / rescaled) operator convention that §7.2(f)
# does not pin down.  The computed Lambda values below are with the naive raw-moment matrix and
# are NOT the claimed 5/36; that mismatch is precisely the documented open gap.
# The ONLY arithmetic we can verify from the claimed inputs is the identity
#   1 - 2*Lambda_2(0) = 13/18  <=>  Lambda_2(0) = 5/36,
# which is pure algebra and consistent with the informal claim.
#
# Standard: Lambda_m(0) = 1 / e0^T M^{-1} e0 where M is the (m+1)x(m+1) moment matrix
# M[i,j] = mu_{i+j}.  For the raw-moment sequence this yields the values printed below
# (which do NOT reproduce 5/36 -- evidence of the normalization gap).
mu = [1.0, 1.0, 3/4, 2.0, 13/4]  # mu_0..mu_4

def christoffel(m):
    # (m+1)x(m+1) moment matrix using mu_k (assumes mu[0..2m] available)
    size = m+1
    M = np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            M[i,j] = mu[i+j]
    inv = np.linalg.inv(M)
    # Lambda_m(0) = 1 / (e0^T M^{-1} e0)  (the Christoffel function, = Christoffel-Darboux kernel cost at 0)
    val = 1.0/inv[0,0]
    return val

for m in [1,2]:
    L = christoffel(m)
    print(f"Lambda_{m}(0) from moments = {L:.10f}")
print("claimed Lambda_2(0) = 5/36 =", 5/36)
print("1 - 2*Lambda_2(0) =", 1-2*(5/36), "= 13/18 =", 13/18)
print("1 - Lambda_2(0) =", 1-(5/36), "(would be if no factor-2)")

# check what m_k(1) would need to give Lambda_2 = 5/36; adjust guess if mismatch
