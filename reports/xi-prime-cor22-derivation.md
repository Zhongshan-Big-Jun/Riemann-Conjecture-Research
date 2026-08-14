# ξ′ stability refinement (Cor 2.2-type) — full derivation (2026-08-14)

Purpose: discharge dependency item 3 of reports/xi-prime-pressure-method.md — the
stability-enhanced rank–trace step for the zeros of ξ′ with the Montgomery–Taylor window.
Notation follows the Anthropic v2 paper §2/§4, the OpenAI draft §2 (Lemma 2.1, Cor 2.2),
and the Lean XiPrime infrastructure (zeta-23-lean@3635e748).

## 0. Objects

- ξ(s) the completed zeta function; ξ′(s) its derivative. ξ′(1−s) = −ξ′(s), so ρ is a zero of
  ξ′ of multiplicity m ⟺ 1−ρ is a zero of multiplicity m. All zeros of ξ′ lie in the open
  strip 0 < Re s < 1 (Lean: xiDerivZerosInStrip) and, by Riemann–von Mangoldt for ξ′
  (Lean: XiDerivRvM), N_{ξ′}(T,2T) = #{zeros with T < Im ρ ≤ 2T, with multiplicity} satisfies
  N_{ξ′}(T,2T) = (T/2π)ℓ₁(1+o(1)).
- Counts: S₁ := #{simple zeros of ξ′ with β = 1/2, T < Im ≤ 2T} (call s₁ in the window),
  s₂ := # multiple on-line points (weight 2+), p := # off-line pairs {ρ, 1−ρ̄} (γ ∈ (T,2T]).
  N_{ξ′}(I′) ≥ s₁ + 2s₂ + 2p for I′ = (T − D₀, 2T + D₀].
- Test family: the MT window profile v_MT(s) = cos(√2 s) on [−1/2,1/2] (φ² = v_MT(u/L)·φ₀²,
  φ₀ the fixed taper; cf. ThmD's φ_D and XiPrime's phiV/atV machinery), frequencies
  τ_k = 2πk/L, 0 ≤ k < d, d = ⌊LT/2π⌋ ≈ λ₁N. This is the SAME test family (and hence the
  same overlap kernel w = k²) as in the ζ/MT pressure method; the certificate
  F₈ ≥ 39/10000 (extpress run) transfers verbatim.

## 1. The compression and its structure

Define v_ρ ∈ ℂ^d by (v_ρ)_k = φ̂(γ_ρ − τ_k)/√(aL²) (normalised as in the ζ case; the
Poisson–Gabor identity Σ_k φ̂(τ−τ_k)² = aL² gives ‖v_ρ‖² ≤ 1 with equality up to the
truncation tail o(1)). Let Â := (aL²)^{-1}·G be the ξ′ compression of Weil's form for ξ′
(the explicit formula for ξ′/ξ′ is the XiPrime EF; the matrix is real symmetric because the
functional equation pairs ρ ↦ 1−ρ̄ with v_{1−ρ̄} = v_ρ, using that γ_{1−ρ̄} = γ_ρ — the
involution 1−ρ̄ PRESERVES the imaginary part — and the conjugate pair ρ̄ gives the
conjugate vector, so the imaginary parts cancel).

[Mechanism check for v_{1−ρ̄} = v_ρ, both ζ and ξ′: ρ = β+iγ, 1−ρ̄ = 1−β+iγ; the vector
(v_ρ)_k = φ̂(γ − τ_k) depends only on γ, which is equal for both. No parity of φ̂ is needed —
only that the vector is indexed by ordinates. For the real-symmetry: v_{ρ̄} = conj(v_ρ)
(φ̂ real), and ρ̄ is a zero whenever ρ is (real coefficients), so
v_ρv_ρᵀ + v_{ρ̄}v_{ρ̄}ᵀ = 2(Re v_ρ)(Re v_ρ)ᵀ − 2(Im v_ρ)(Im v_ρ)ᵀ ∈ ℝ^{d×d}. For ξ′ the
same holds: ξ′ has real coefficients and ξ′(1−s) = −ξ′(s), so zeros are closed under
ρ ↦ ρ̄ and ρ ↦ 1−ρ (hence under ρ ↦ 1−ρ̄).]

Zero-side decomposition (structural, same as ζ Prop 4.1):

- P₁ := Σ_{ρ ∈ S₁} v_ρ v_ρ^T ⪰ 0;  rank(P₁) ≤ s₁;  tr(P₁) ≤ s₁
  (each term rank-one PSD; ‖v_ρ‖² ≤ 1; sums over the retained simple on-line zeros).
- Off-line pair {ρ, 1−ρ̄}, ρ = β+iγ, β ≠ 1/2: v_ρ = a + ib, v_{1−ρ̄} = v_ρ (both vectors equal
  since the pair shares γ and the window is even), so the pair contributes
  v_ρv_ρ^T + v_ρv_ρ^T = 2(aa^T − bb^T), a block of signature (1,1) — pull-back of
  m_ρ·diag(1,−1) under x ↦ (aᵀx, bᵀx). By the inertia lemma (Lemma 3.1), summing pairs
  and multiple on-line points (rank-one PSD terms) gives
  **n₊(Q₀) ≤ s₂ + p**, Q₀ := Â − P₁.

## 2. Lemma 2.1 (rank–trace with stability term) — verbatim, no ξ′-dependence

For V ∈ ℂ^{d×r} with ‖col_j‖ ≤ 1, P = VV^T ⪰ 0, M = V^T V, Q Hermitian with n₊(Q) ≤ b:
  ‖P + Q‖_F² ≥ 4tr(P+Q) − 3r − 4b + Δ(M),   Δ(M) := tr Ψ(M), Ψ(t) = (t−1)²·1_{t≤2} + (2t−3)·1_{t≥2}.
(Proof: Q = Q₊−Q₋; ‖Q₊‖² ≥ 4trQ₊ − 4b; min_n[(p−n)² + 4n] = 2p − 1 + Ψ(p); von Neumann.
No analytic-number-theory input. — OpenAI Lemma 2.1, audited PASS in oaidraft run.)

## 3. The ξ′ second moment (prime side)

XiPrime Thm 8.1: ‖Ĝ^{(1)}‖_F² = κ₁(λ,v)·N_{ξ′}(1+o(1)) with κ₁(λ,v) = 1/cWin(D₁,λ,v)
(Lean-certified formula; D₁ the ξ′ diagonal density, Defs.lean). For the MT window at λ = 1
(manager computation, cross-validated on flat/quartic):
  κ₁(1, v_MT) = 1.1321111348009480644…,   H_{ξ′}^{MT} := 2 − κ₁(1, v_MT) = 0.86788886519905193555…
tr Â = N_{ξ′}(I′)(1+o(1)) (RvM).

## 4. Corollary (ξ′ stability refinement)

Apply Lemma 2.1 to (P₁, Q₀) with r = s₁, b = s₂ + p (n₊(Q₀) ≤ s₂ + p):
  ‖Â‖_F² ≥ 4trÂ − 3s₁ − 4(s₂+p) + Δ(M°),   M° := VᵀV (the s₁×s₁ Gram of the simple on-line zeros).
Rearrange with trÂ = N(1+o(1)), ‖Â‖_F² = κ₁N(1+o(1)), N ≥ s₁ + 2s₂ + 2p:
  s₁ ≥ (2 − κ₁)N + Δ(M°) − o(N),   i.e.  **S₁ ≥ H_{ξ′}^{MT}·N_{ξ′} + Δ(M°) − o(N_{ξ′})**.
(Algebra: 3s₁ + 4(s₂+p) ≤ 2s₁ + 2(s₁+2s₂+2p) = 2s₁ + 2N − o(N) ⟹ s₁ ≥ 4N − κ₁N − 2N + Δ = (2−κ₁)N + Δ; the
same bookkeeping as OpenAI Cor 2.2 → eq (7) → Theorem 1.1 chain, with the ζ numbers replaced
by the ξ′ ones. No step depends on ζ-specific arithmetic.)

## 5. Pressure chain (verbatim transfer)

Block-energy/block-defect/pinching (general-k derivation, extpress run) uses only:
(i) the window kernel w = k² and the certificate F₈ ≥ 39/10000 (same kernel — MT window);
(ii) Lemma 4.3 Δ(G) ≥ min(1, 2Σ_{i<j}|G_ij|²) for G ⪰ 0 (pure matrix fact);
(iii) the kernel-limit concentration for consecutive blocks (structural: fixed m, w-sums
     concentrate because each pair distance is a fixed gap sum and w decays);
(iv) pinching convexity/unitary-invariance of Δ (pure matrix fact).
All apply to the ξ′ simple-on-line Gram blocks verbatim. With m₉ = 264, A₀ = 624/625 < 1:
  Δ(M°) ≥ (A₀/m₉)·S₁ − ((m₉−1)/(500m₉))·N_{ξ′} − o(N) = (26/6875)S₁ − (263/132000)N − o(N).

## 6. Conclusion

  (1 − 26/6875)S₁ ≥ (H_{ξ′}^{MT} − 263/132000)N_{ξ′} − o(N),
  liminf N₀ˢ_{ξ′}(T,2T)/N_{ξ′}(T,2T) ≥ (6875·H_{ξ′}^{MT} − 1315/96)/6849 = **0.8691835350528274770389…**
  > 0.86864 (quartic-window record) > 0.85838 (flat).

## 7. Audit requirements (open items)

- A1: verify the ξ′ zero-side block structure (Prop 4.1-type: n₊(Q₀) ≤ s₂ + p, tr P₁ ≤ s₁)
  in full detail against the XiPrime EF. STATUS: the structure is provided by the Lean
  generic ZeroSide machinery instantiated at the ξ′ ZeroConfig — XiPrime's WindowZeroSide
  (poisson/tail/a_half, Assembly.lean §A3) mirrors Zeta23/ThmD/ZeroSideD.lean exactly, and
  the "c = 2, 3 seams" consume the same rank-trace zero side for any zero config. The
  explicit s₁/s₂/p write-up for ξ′ is this note (§1); independent audit of the note's
  bookkeeping remains the open part of A1.
- A2: ✅ VERIFIED (2026-08-14): κ₁(1, v_MT) confirmed by an independent path — analytic
  closed form of the cos autocorrelation vConv(r) = ½[(1−r)cos(√2r) + sin(√2(1−r))/√2]
  (correcting a first-attempt endpoint slip), same D₁ series: gives
  2 − κ₁ = 0.86788886519905193555031471042034…, matching the numeric-quadrature path to 20
  digits; flat window reproduces 0.85838405470921802815… (Lean ≥ 0.85838371).
- A3: the kernel-limit concentration for ξ′ blocks. STATUS: structural (fixed m, window
  kernel w, gap-sum distances; the same argument as the ζ chain); formalized by the ζ
  kernel-limit lemma whose proof uses only the window — transfer flagged for audit.
- A4: N_{ξ′}(I′) ≥ s₁ + 2s₂ + 2p and tr Â = N(1+o(1)). STATUS: covered by the Lean
  RvM/local-count and PoissonSq facts of XiPrime (same spine as ζ Prop 4.2); the MT-window
  instance at λ = 1 is the family-hypotheses instance familyHyps_atV with v = v_MT
  (WindowProfile holds for the smooth cos profile).

Status: CANDIDATE derivation complete; independent audit of A1–A4 recommended before
promoting to a record theorem. A2 closed; A1/A3/A4 remain (A1 is the substantive one).
Manager's own audit of the arithmetic: C₉^{ξ′} value recomputed (mpmath 40 digits) and
cross-checks in reports/xi-prime-pressure-method.md.
