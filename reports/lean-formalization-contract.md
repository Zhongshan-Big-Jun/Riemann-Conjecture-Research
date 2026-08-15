# Lean formalization status & contract — C₉ = 0.6730665 record (2026-08-15)

Answers: "lean 验证呢?" — exactly what is machine-verified in Lean for the new record
C₉(ζ) = 0.673066472675939665848… / C₉(ξ′) = 0.86920009109661916184…, and what is not.

## 1. What IS Lean-verified (snapshot zeta-23-lean@3635e748, local toolchain available)

| Statement | Location | Status |
|---|---|---|
| **Theorem D baseline**: thmD₀_simple_mult : N₀ˢ(T,2T) ≥ (2 − 1/c₁*)·N(T,2T), 2 − 1/c₁* = 3/2 − cot(1/√2)/√2 = H_MT = 0.67250… (UNCONDITIONAL; constants enter exactly, decimals are not formalized) | `Zeta23/ThmD/Mult.lean:435` (+ Final.lean thmD₀ family, cumulative forms) | ✅ Lean (imported by the new chain, step 1) |
| thmD₀_simple (comparator/CS form 2c₁*−1 = 0.50659) | `Zeta23/ThmD/Final.lean:119` | ✅ Lean |
| ξ′ baseline formula (C₉(ξ′) record's import) | `Zeta23/XiPrime/…` | ✅ Lean |
| PairCeiling (bandwidth-one ceiling ≈ 0.6818) | `Zeta23/PairCeiling/…` | ✅ Lean |

Toolchain: elan at C:\Users\HuangZY\.elan\bin; lean-toolchain pins leanprover/lean4:v4.33.0-rc2;
lakefile requires mathlib4 @ rev 51e6992e… (not prebuilt locally — .lake absent; a build
needs the mathlib fetch/build, doable in a later session).

## 2. What is NOT Lean-formalized (the new record's own content)

1. **General-k pressure chain** (steps 2–7 of candidate_proof.md): stability refinement
   Δ(M°) (OpenAI Lemma 2.1/Cor 2.2), block-energy E_m, block-defect with
   A₀ = 2499/2500 < 1, pinching/averaging, and the conclusion
   liminf N₀ˢ/N ≥ (H_MT − (m−1)/(500m))/(1 − A₀/m). Paper-level; reproduced symbolically
   for k=3 and k=7 (extpress general-k derivation); manager-audited; **not in Lean**.
2. **The k=9 Arb certificate** (F₈ ≥ 392/100000; 64,748,524 nodes, grid-2000, 128-bit):
   a rigorous finite computation with independently recomputed table hashes, components
   and a full B1–B6 soundness audit — but **not checked by a proof assistant**.
3. Hence the two record statements themselves are paper-level results importing the
   Lean-verified baseline.

## 3. Formalization contract (Stage C roadmap, when lean-verify is dispatchable)

- **T1 (chain, small)**: formalize the general-k chain theorem for k = 9 in ε-form:
  `∀ε>0, ∃T₀, ∀T≥T₀: (1 − A₀/m)·N₀ˢ(T,2T) ≥ (H_MT − (m−1)/(500m) − ε)·N(T,2T)`
  with m = 263, A₀ = 2499/2500, assuming the certified F₈ bound as a hypothesis
  (imports thmD₀_simple_mult; the block algebra is elementary but long).
- **T2 (certificate)**: certify `F₈ ≥ 392/100000` inside Lean. Two viable routes:
  (a) reflection: implement the verifier's interval arithmetic (down-rounded binary64 or
  rational bounds) as a Lean `def` + `native_decide`/`norm_num`-checked computation on the
  certificate's component list (the certificate is a static artifact: the boxes/nodes can
  be enumerated — needs the certificate's full box data, currently not emitted);
  (b) verified verifier: port the RangeMinimum/table machinery with rigorous bounds
  (~months of Lean work). Route (a) is preferred: emit the certificate's surviving-box
  structure from verify_kpoint_parallel.py, then a Lean checker walks the (finite) box
  tree with exact rational arithmetic — a realistic few-weeks task.
- **T3 (ξ′ side)**: import XiPrime.lean + T1 to get C₉(ξ′) (the AdmWindow cos instance
  blueprint is ready: reports/admwindow-cos-instance.md).
- **T4 (optional)**: the SL/conditional-100% theorems (condp1 run) — linear-algebra
  formalization (Christoffel/SOS), not currently planned.

Note: the integers m = 263, A₀ = 2499/2500 and the constants 657,500/655,001 enter
exactly; the decimal displays (0.673066472675939665848…) are documentation only.

## 4. Honest status line

The new record's *baseline* is Lean-verified; its *chain and certificate* are
paper-level with a rigorous computational audit (B1–B6, PASS) — the standard scope
limit shared with the extpress/OpenAI records. Full end-to-end Lean verification is
the Stage C contract above (T1 + T2 route (a) ≈ the realistic next formalization
milestone; dispatchable when the lean-verify skill is available).
