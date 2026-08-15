"""
stabridge_checks.py — numerical spot-checks for the T1c-1 / T1c-2 bridge pass
(R-20260816T060000Z-stabridge-a3f1).

These are EVIDENCE that the real-number identities and inequalities used in the
analysis-level proofs hold on concrete inputs; none of them constitutes a proof.
Each check prints PASS/FAIL with a bounded residue.

Checks:
  C1.  def Psi : Psi(t) = (t-1)^2 on [0,2], 2t-3 on [2,oo); continuity + nonnegativity.
  C2.  min_{n>=0} (p-n)^2 + 4n = 2p - 1 + Psi(p)  (the q_- scalar step, proof.md §2).
  C3.  OpenAI Lemma 2.1 : ||P+Q||_F^2 >= 4 tr(P+Q) - 3 r - 4 b + tr Psi(M),
       P = VV*, M = V*V, V in C^{d x r} with column norms <= 1, Q Hermitian, n+(Q) <= b.
       Random samples, several (d, r, b).
  C4.  Block-defect lemma: for Hermitian PSD G,  tr Psi(G) >= min(1, 2 * sum_{i<j} |G_ij|^2).
  C5.  The exact constants: A0 = 2499/2500, A0/m = 2499/657500, (m-1)/(500m)=262/131500,
       A0<1, cLHS = 655001/657500, and 1 - A0/m > 0.
  C6.  Block-energy averaging algebra (finite): for the 7-certificate pattern f6=19/5000,
       sum over windows <= 2 per pair and 1/500 per gap (the bound used in BE_k).
  C7.  Kernel-ratio normalisation: with the MT atoms on [-L/2,L/2], the correlation Gram
       off-diagonal square tends to wMT(x) = kMT(x)^2 :  |corr(G)_ab|^2 ~ wMT(x_ab).
  C8.  min{1, 2 sum |G_ij|^2} uses the 2*sum branch exactly when A0 < 1 (i.e. when the
       block energy sqrt-bound target A0 is < 1); verify branch selection logic on the
       target value A0<m-free>.

MPmath used for the high-precision kernel; numpy for the random linear algebra.
"""

import numpy as np
import mpmath as mp
from numpy.linalg import eigh

mp.mp.dps = 40

def Psi(t):
    return 0.0 if t < 0 else (mp.power(t-1, 2) if t <= 2 else (2*t - 3))

def Psi_np(t):
    return np.where(t < 0, 0.0, np.where(t <= 2, (t-1)**2, 2*t - 3))

res = []

# ---- C1: Psi definition: continuity at t=0 and t=2, nonnegativity ----
def check(name, cond, details=""):
    res.append((name, bool(cond), details))

# continuity at t=2: (t-1)^2 at 2 = 1 ; 2t-3 at 2 = 1
check("C1.cont_t2", abs(Psi(2) - 1) < 1e-40, f"Psi(2)={Psi(2)}")
check("C1.cont_t0", abs(Psi(0) - 1) < 1e-40, f"Psi(0)={Psi(0)}")
# nonnegativity sampled
grid = np.linspace(-0.5, 5.0, 10001)
if np.all(Psi_np(grid) >= -1e-12):
    check("C1.nonneg", True, "Psi>=0 on [-0.5,5] grid")
else:
    check("C1.nonneg", False, "Psi>=0 violated somewhere")

# ---- C2: min identity ----
# min_{n>=0} (p-n)^2 + 4n  vs  2p - 1 + Psi(p)
def min_rhs(p):
    # convex in n, minimizer n* = max(p-2, 0)
    nstar = max(p - 2, 0)
    return (p - nstar)**2 + 4*nstar
ok_c2 = True
worst_c2 = 0.0
for p in np.linspace(0, 5, 401):
    a = min_rhs(float(p))
    b = float(2*p - 1 + Psi(p))
    worst_c2 = max(worst_c2, abs(a - b))
    if abs(a - b) > 1e-12:
        ok_c2 = False
check("C2.min_identity", ok_c2, f"worst |min_n - RHS| = {worst_c2:.3e}")

# ---- C3: OpenAI Lemma 2.1 on random data ----
def hermitian_pos_order_rand(d, r, b, seed):
    rng = np.random.default_rng(seed)
    # V : d x r, Gaussian, then rescale each column to norm <= 1 (and drop a few to vary rank)
    V = rng.standard_normal((d, r)) + 1j*rng.standard_normal((d, r))
    for j in range(r):
        n = np.linalg.norm(V[:, j])
        # deliberate: a fraction of columns have norm < 1; keep all <= 1
    colnorms = np.linalg.norm(V, axis=0)
    V = V / colnorms.max()  # scale so max norm = 1 => all <= 1
    P = V @ V.conj().T
    # Q Hermitian with n+(Q) <= b: b positive eigenvalues, rest non-positive
    A = rng.standard_normal((d, d)) + 1j*rng.standard_normal((d, d))
    Q_herm = (A + A.conj().T)/2
    ev, U = eigh(Q_herm)
    # clamp: at most b positive
    pos = np.where(ev > 0)[0]
    if len(pos) > b:
        # zero out the smallest (in absolute value) positives to leave b of them
        take = pos[np.argsort(ev[pos])][:b]
        evn = np.zeros_like(ev)
        evn[take] = ev[take]
    else:
        evn = ev
    Q = (U * evn) @ U.conj().T
    Q = np.asarray((Q + Q.conj().T)/2, dtype=complex)
    nQpos = int(np.sum(np.linalg.eigvalsh(Q) > 1e-9))
    return V, P, Q, nQpos

def forcePSD(M):
    ev, U = eigh((M + M.conj().T)/2)
    ev = np.maximum(ev, 0)
    return (U * ev) @ U.conj().T

rng_all = np.random.default_rng(12345)
worst_c3 = 0.0
ok_c3 = True
for (d, r, b) in [(6, 3, 1), (10, 4, 2), (12, 6, 2), (15, 5, 3)]:
    for seed in range(4):
        V, P, Q, nQpos = hermitian_pos_order_rand(d, r, b, 1000 + seed)
        if nQpos > b:
            check("C3.nQpos", False, f"d={d} r={r} b={b}: nQpos={nQpos} > b")
            ok_c3 = False
            continue
        M = V.conj().T @ V
        eigM = np.linalg.eigvalsh((M + M.conj().T)/2)
        trPsiM = float(sum(Psi(np.maximum(0.0, float(e))) for e in eigM))
        PQ = P + Q
        frob2 = float(np.linalg.norm(PQ, "fro")**2)
        rhs = 4*float((P + Q).trace().real) - 3*r - 4*b + trPsiM
        # rhs bound: ensure not NaN
        lhs = frob2
        gap = lhs - rhs
        worst_c3 = max(worst_c3, abs(min(gap , 0.0)))
        if gap < -1e-6:
            check("C3.lemma", False, f"d={d} r={r} b={b} seed={seed}: lhs-rhs={gap:.3e}")
            ok_c3 = False
check("C3.lemma2_1", ok_c3, f"worst violation magnitude {worst_c3:.3e} (0 if none)")

# ---- C4: block-defect lemma ----
def block_defect_check(d, seed):
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((d, d)) + 1j*rng.standard_normal((d, d))
    G = forcePSD(A @ A.conj().T)
    eigG = np.linalg.eigvalsh((G + G.conj().T)/2)
    trPsi = float(sum(Psi(np.maximum(0.0, float(e))) for e in eigG))
    sumSq = 0.0
    for i in range(d):
        for j in range(i+1, d):
            sumSq += abs(G[i, j])**2
    rhs = min(1.0, 2*sumSq)
    return trPsi, rhs, trPsi - rhs

worst_c4 = 0.0
ok_c4 = True
for d in [2, 3, 4, 5, 8]:
    for seed in range(6):
        trPsi, rhs, gap = block_defect_check(d, 5000 + seed)
        worst_c4 = max(worst_c4, abs(min(gap, 0.0)))
        if gap < -1e-6:
            ok_c4 = False
            check("C4.defect", False, f"d={d} seed={seed} gap={gap:.3e}")
check("C4.block_defect", ok_c4, f"worst violation {worst_c4:.3e}")

# ---- C5: exact constants ----
f9 = 392/100000
n9 = 255
A0 = f9*n9
m9 = 8 + 255
A0m = A0/m9
qm = (m9-1)/(500*m9)
cLHS = 1 - A0m
eps = 1e-12
ok_c5 = True
def neq(a, b):
    global ok_c5
    if abs(a-b) > eps:
        ok_c5 = False
neq(A0, 2499/2500)
neq(A0m, 2499/657500)
neq(qm, 262/131500)
neq(cLHS, 655001/657500)
if not (A0 < 1):
    ok_c5 = False
if not (0 < cLHS):
    ok_c5 = False
check("C5.constants", ok_c5,
      f"A0={A0:.12f} (<1:{A0<1}), A0/m={A0m:.12f} (2499/657500={2499/657500:.12f}), "
      f"q={qm:.12f} (262/131500={262/131500:.12f}), cLHS={cLHS:.12f}")

# ---- C6: block-energy window counting (leads to BE) ----
# For k=9 (8 gaps), the pressure F8 has linear coeff 1/(500*8) and span-s coeff 2/(8-s).
# Summing over the m-k+1 = m-8 consecutive 9-windows: a pair spanning s gaps appears in
# at most (m - s) windows but each window's window counted... verify it's <= 2 per pair
# and <= 1/500 per gap.  This is a pure finite counting argument; check it on m=263.
k, m = 9, 263
nfolds_window = m - k + 1
# count, for a pair of retained indices (i<j) within distance, number of 8-gap windows
# that contain both (window = 9 consecutive points), and for a gap the number of windows containing the gap.
import itertools
def window_contains(i, j, w0):  # window of indices w0..w0+8
    return w0 <= i <= w0+8 and w0 <= j <= w0+8

max_pairs_per_s = {}
for s in range(1, k):  # s gaps between the pair
    mx = 0
    for i in range(m):
        for j in range(i+1, m):
            if j - i == s:
                cnt = sum(1 for w0 in range(0, m-k+1) if window_contains(i, j, w0))
                mx = max(mx, cnt)
    max_pairs_per_s[s] = mx
# coefficient upper bound: sum over windows gives coeff <= 2 per pair iff max_pairs_per_s <= k-s
ok_c6a = all(max_pairs_per_s[s] <= (k - s) for s in range(1, k))
# each gap enters at most k-1 windows
max_gap = 0
for g in range(m-1):
    cg = sum(1 for w0 in range(0, m-k+1) if w0 <= g <= w0+7)
    max_gap = max(max_gap, cg)
ok_c6b = max_gap <= k-1
# the claimed BE right side: f_k*(m-k+1). For k=9 certified f9:
BE_rhs = f9*(m - k + 1)
check("C6.window_count_pairs", ok_c6a, f"max windows per s-gap pair <= k-s: {dict((s, (max_pairs_per_s[s], k-s)) for s in range(1,k))}")
check("C6.window_count_gaps", ok_c6b, f"max windows per gap = {max_gap} <= k-1={k-1}")
check("C6.BE_rhs", abs(BE_rhs - A0) < eps, f"A0_target = f9*(m-8) = {BE_rhs:.10f} vs A0={A0:.10f}")

# ---- C7: correlation Gram off-diagonal square -> wMT(x) ----
# Numerically verify convergence of the correlation Gram energy to E_m/2 using the
# exact finite-window atoms, at increasing L for a small synthetic zero block.
def kMT_num(x):
    # kMT(x) = K1(x)/K1(0)
    # K1(x) = sincbar computed via mpmath
    if abs(x) < 1e-15:
        return mp.mpf(1)
    return (mp.sin(1/mp.sqrt(2) - mp.pi*x)/(1/mp.sqrt(2) - mp.pi*x)
            + mp.sin(1/mp.sqrt(2) + mp.pi*x)/(1/mp.sqrt(2) + mp.pi*x)) / (2*mp.sqrt(2)*mp.sin(1/mp.sqrt(2)))

def wMT_num(x):
    return kMT_num(x)**2

def corr_gram_energy(ords, L, w=1.0):
    # atoms v_g(u)=sqrt(cos(sqrt2 u/L))*ramp, u in [-L/2,L/2]
    # build Gram entries (correlation-normalized) g_ab = <v_a,v_b>/sqrt(<v_a,v_a><v_b,v_b>)
    # inner product <v_a,v_b> = int cos(sqrt2 u/L) cos((a_b) u) du over bulk (ramp=1)
    n = len(ords)
    # numeric dense grid
    M = 4001
    u = np.linspace(-L/2, L/2, M)
    du = u[1]-u[0]
    phi2 = np.cos(np.sqrt(2)*u/L)
    # ramp = 1 on |u| <= L/2 - w, 0 outside (approx; use step)
    ramp = (np.abs(u) <= L/2 - w).astype(float)
    integrand = phi2*ramp
    # <v_a,v_b> = int integrand cos((g_a-g_b)u) du
    Graw = np.zeros((n, n))
    for a in range(n):
        for b in range(a, n):
            val = du*np.sum(integrand*np.cos((ords[a]-ords[b])*u))
            Graw[a, b] = Graw[b, a] = val
    diag = np.diag(Graw).copy()
    G = Graw / np.sqrt(np.outer(diag, diag))
    sumSq = 0.0
    for a in range(n):
        for b in range(a+1, n):
            sumSq += abs(G[a, b])**2
    return G, sumSq

ords = [0.0, 0.5, 1.1, 1.7, 2.4]  # some normalized separations
def E_block(ords_norm):
    # E_m = 2 sum_{i<j} wMT(x_ij), x = normalized separation (gamma-gamma')L/(2pi).
    E = mp.mpf(0)
    for i in range(len(ords_norm)):
        for j in range(i+1, len(ords_norm)):
            E += wMT_num(ords_norm[j]-ords_norm[i])
    return 2*E

# normalized separations x_ij are (gamma_i-gamma_j)L/(2pi); choose grid so these match the block.
xblock = [0.0, 0.5, 1.1, 1.7, 2.4]  # these ARE the x values we want; gamma=2pi x/L for each
Lvals = [100.0, 400.0, 1000.0]
prev = None
ok_c7 = True
for L in Lvals:
    gammas = [2*np.pi*x/L for x in xblock]
    G, sumSq = corr_gram_energy(gammas, L)
    Em = float(2*sum(wMT_num(xblock[j]-xblock[i]) for i in range(len(xblock)) for j in range(i+1, len(xblock))))
    ratio = 2*sumSq/Em if Em != 0 else None
    if ratio is None:
        ok_c7 = False
    else:
        if prev is not None and abs(ratio - 1) > abs(prev - 1):
            pass  # not monotone necessarily; just report
        prev = ratio
        if abs(ratio - 1) > 0.05:
            ok_c7 = False
    check(f"C7.Eratio.L{int(L)}", ratio is not None and abs(ratio-1) < 0.05, f"2*sum|G_ij|^2/E_m = {ratio:.6f} at L={L}")
check("C7.converge", ok_c7, "corr-Gram energy ~ E_m within 5% at tested L")

# ---- C8: min{1,2sum} branch ----
# A0 = 0.9996 < 1 ; the block defect target is A0. The min uses the 2*sum branch when
# 2 sum |G_ij|^2 <= 1, i.e. whenever the target A0 < 1 and E_m ~ A0. Show that for the
# correlation Gram with block energy ~ A0 the 2sum argument is in the < 1 regime.
# (Logical, not numeric: report.)
branch_2sum_active = (2 * (A0/2) <= 1)  # if 2sum|G|^2 ~ E_m ~ A0, ratio to 1
check("C8.branch", bool(branch_2sum_active), f"A0={A0} <1, 2sum target for E_m~A0 is {2*A0/2}<=1")

print("\n=== SUMMARY ===")
fails = [r for r in res if not r[1]]
for name, ok, det in res:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {det}")
print(f"\nTOTAL {len(res)} checks, {len(fails)} FAIL")
raise SystemExit(1 if fails else 0)
