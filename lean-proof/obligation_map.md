# Obligation map — C₉ = 0.6730665 record (lean-verify Phase 1/2)

Target Lean project: literature/raw/zeta-23-lean (snapshot @3635e748, pinned
leanprover/lean4:v4.33.0-rc2, mathlib4 @ 51e6992e). Verification workspace: lean-proof/.

| Obl | Contract statement | Lean declaration(s) | Fidelity | Status |
|---|---|---|---|---|
| O1 | Baseline: ∀ε>0 ∃T₀ ∀T≥T₀: (H_MT − ε)·N(T,2T) ≤ N₀ˢ(T,2T), H_MT = 3/2 − (1/√2)cot(1/√2) | `Zeta23.ThmD.Mult.thmD₀_simple_mult` (HD 1 − ε form) and `thmD₀_simple_mult'` (constant written out: 3/2 − (√2)⁻¹·cos(1/√2)/sin(1/√2)); cumulative form `thmD₀_simple_mult_cumulative` | **FAITHFUL** (checked line-by-line 2026-08-15: ε-form, dyadic (T,2T], Ncount = N with multiplicity, N0simple = simple-on-line; unconditional via zetaZeroConfig + paperInputs_zeta) | ✅ formalized upstream; **machine build in progress** |
| O2 | Chain: (1 − A₀/m)·N₀ˢ(T,2T) ≥ (H_MT − (m−1)/(500m) − ε)·N(T,2T) given certified F₈ ≥ 392/100000 (m=263, A₀=2499/2500) | (target: `Zeta23.ThmD.chain9_eps`) — NOT yet written | — (contract audited paper-level; general-k chain reproduces k=7, k=3) | ❌ OPEN (T1) |
| O3 | Certificate: F₈ ≥ 392/100000 (grid-2000, 128-bit, 64,748,524 nodes; kernel table 31368 entries) | (target: `Zeta23.Pressure.f8_cert`) — NOT yet written | — (B1–B6 computational audit PASS; certificate sha 7F25401A…) | ❌ OPEN (T2, reflection route) |
| O4 | Conclusion: liminf N₀ˢ/N ≥ (657,500·H_MT − 1,310)/655,001 | (target: `Zeta23.ThmD.record_c9`; arithmetic verified dps=130) | — (exact rational identity (657,500/65,750 = 10) verified) | ❌ OPEN (O2+O3) |
| O5 | ξ′ record: liminf N₀ˢ_{ξ′}/N_{ξ′} ≥ (657,500·H_{ξ′} − 1,310)/655,001 | (target: `Zeta23.XiPrime.record_c9xip`; imports `Zeta23.XiPrime.*` + O2) | — (A1–A6 manager PASS; AdmWindow cos blueprint ready) | ❌ OPEN (T3) |
| O6 | Evidence discipline: no numerical evidence labeled as proof | candidate_proof.md honest status; this map | **FAITHFUL** | ✅ |

## Fidelity notes (O1, 2026-08-15)

- `thmD₀_simple_mult` quantifier order: ∀ε>0, ∃T₀, ∀T≥T₀ — matches the informal ε-form.
- `HD 1` is definitionally 2 − 1/c₁* = 3/2 − cot(1/√2)/√2 (checked in ThmD/ParamsD.lean
  HD_one; `thmD₀_simple_mult'` displays the constant explicitly). Decimals are documentation.
- N0simple/Ncount are the multiplicity-counted simple-on-line / total counts — matches the
  record theorem's N₀ˢ / N conventions (N0* = distinct; N0simple = simple).
- Boundary: T real, dyadic window (T, 2T]; the cumulative form covers liminf on (0, T].
