# Refined block deduction: Φ_m trace–energy envelope + window-in-frame pressure counting

**Effect.** Applied to this repository's already-certified finite inequality
(F ≥ 891/200000, p = 1/2736, q = 6, H_cert = 3362285207/5·10⁹ — nothing new
is certified), the two refinements below sharpen the assembled bound from
0.673200117012… (m = 272) to

    0.6732425893558967029402653869425161870133…  >  6732425893/10¹⁰,

at block length m = 235. Verified three ways: derivation + exact rationals
(validation lane), independent line-by-line re-derivation + 256-bit Arb
arithmetic (orchestrator), and an adversarial countersign of every checklist
item (design lane). Records: `certificates/refined-deduction-fast.txt`.

**Attribution.** The sharpened trace–energy envelope Φ_m and the
window-in-frame pressure accounting are due to the repository
[`tawanerguo-cn/zeta-simple-zeros`](https://github.com/tawanerguo-cn/zeta-simple-zeros)
(files `docs/trace_energy_envelope.md` and `paper/riemann.tex` §5–6,
published 2026-08-12, MIT), whose 67.3192911% Bellman-coboundary candidate
first used both. We re-derived both statements independently; the versions
used here avoid coboundaries entirely and apply to position-weighted
windows.

## Lemma 1 (trace–energy envelope)

Let G be an m×m positive-semidefinite matrix with unit diagonal (so the
eigenvalues λ_i ≥ 0 satisfy Σλ_i = m). With the repository's
Ψ(t) = (t−1)² on [0,2], 2t−3 beyond, put D = tr Ψ(G),
E = Σ_i (λ_i − 1)², and

    Φ_m(E) = E                          for 0 ≤ E ≤ m/(m−1),
             2√((m−1)E/m) − 1 + E/m     for E ≥ m/(m−1).

Then for every A ≥ m/(m−1): if E + P ≥ A with P ≥ 0, then D + P ≥ Φ_m(A).

*Proof sketch* (full case analysis in the verification records): with
x_i = λ_i − 1 (Σx_i = 0) and L = {x_i > 1}, the identity
D = E + 2Σ_L x − |L| − Σ_L x² holds. |L| = 0 gives D = E and
D + P ≥ A ≥ Φ_m(A) (the identity A − Φ_m(A) = (√((m−1)A/m) − 1)² ≥ 0).
|L| ≥ 2 forces D ≥ |L|m/(m−|L|) ≥ 2m/(m−2) > 2 > Φ_m(A) at our A. For
|L| = 1 with large coordinate r: Cauchy–Schwarz on the complementary m−1
coordinates gives r ≤ √((m−1)E/m), and minimizing 2r − r² at that endpoint
yields D ≥ Φ_m(E); conclude by monotonicity and the 1-Lipschitz property of
Φ_m (branch-2 derivative √((m−1)/(mE)) + 1/m ≤ 1 exactly when
E ≥ m/(m−1)). ∎

In the assembly the lemma is applied to the simple-zero atom Gram blocks,
whose diagonal is 1 + o(1) and trace m(1 + o(1)) under the compact-uniform
asymptotic; for fixed m this perturbs the envelope by o(1) per block,
absorbed in the existing o(N) — the same robustness step the previous
√-tail profile used.

## Lemma 2 (window-in-frame pressure counting)

Summing the certified window inequality over the (q+1)-point windows fully
inside an m-point block and averaging over the m cyclic shifts: a
(q+1)-point window is cut by a block boundary in exactly q of the m shifts,
hence fully contained in exactly m−q of them. Therefore the averaged
pressure tax is (m−q)·B_p/m per unit normalized length (B_p = qp), replacing
the previous per-gap charge η·B_p·(m−1)/m — and the Φ_m envelope absorbs
the pressure at slope 1, eliminating the chord factor η entirely.

## Refined assembly

    A = ε(m−q),   bound(m) = ( m·H_cert − (m−q)·B_p ) / ( m − Φ_m(A) ).

Blocks whose pressure alone reaches A satisfy the envelope directly
(Φ_m(A) ≤ A); the rest have span ≤ A/p = O(1), so the compact-uniform
interface applies unchanged. With ε = 891/200000, p = 1/2736, q = 6,
H_cert = 3362285207/5·10⁹:

    A = 204039/200000,   (m−1)A/m = 23872563/23500000  (m = 235),
    Φ₂₃₅(A) = 1.020132657901123501755857262416…,
    bound   = 0.6732425893558967029402653869425161870133…,

with m = 235 optimal (integer scan: m = 234 → 0.67324258703…,
m = 236 → 0.67324256389…). The old formula with the same inputs reproduces
0.6732001170127618568… exactly, which is the consistency gate.
