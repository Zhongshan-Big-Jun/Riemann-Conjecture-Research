# Audit request — ξ′ pressure-method candidate record (packet for independent auditor)

Run roots to audit: `reports/xi-prime-cor22-derivation.md`, `reports/xi-prime-pressure-method.md`,
`reports/xi-prime-mt-window.py`, `reports/linked-ladder.md` (project `F:\LaTeX\Riemann Conjecture`).

## Status update (2026-08-15): manager-level audit CLOSED for A1–A6

Manager audit report: `reports/xi-prime-audit-manager.md` — PASS (math level) on all six
items; two open non-math items: (1) Lean AdmWindow instance for cos(√2s) (template/AtOne
work, Stage C); (2) the f₉ = 0.00395 certificate itself (in progress). A1's AdmWindow
bounds for v_MT verified numerically (‖v′‖₁ = 0.4795, ‖(v²)′‖₁ = 0.8441, ‖v″‖₁ = 1.8375,
‖(v²)″‖₁ = 2.7938, a = 0.8492 ∈ [1/2,1]). An independent human/formal audit remains
welcomed; this packet is retained for that purpose.

## Claim

Unconditional (pending audit):

    liminf N0^s_{ξ′}(T,2T)/N_{ξ′}(T,2T) ≥ C₉^{ξ′} := (6875·H_{ξ′}^{MT} − 1315/96)/6849
                                        = 0.8691835350528274770392388622387462383907877798872344889847675481490341…
    H_{ξ′}^{MT} := 2 − κ₁(1, v_MT) = 0.86788886519905193555031471042034031322264966515680426…,
    v_MT(s) = cos(√2 s), κ₁(λ,v) = 1/cWin(D₁,λ,v) (Lean XiPrime formula, zeta-23-lean@3635e748).

This exceeds the quartic-window record 0.86864 (Anthropic/Lean) and flat 0.85838.

## Audit items (from the derivation note §7)

- A1 (substantive): the ξ′ zero-side block structure — explicit s₁/s₂/p decomposition,
  n₊(Q₀) ≤ s₂ + p, tr P₁ ≤ s₁, with the v_{1−ρ̄} = v_ρ mechanism (involution 1−ρ̄ preserves
  ordinates) and real symmetry via conjugate pairs. The Lean generic ZeroSide machinery
  (XiPrime WindowZeroSide mirrors ThmD/ZeroSideD) is claimed to cover this; verify the
  claimed correspondence.
- A2 (CLOSED): κ₁(1, v_MT) verified two ways — numeric quadrature and analytic closed form
  vConv(r) = ½[(1−r)cos(√2r) + sin(√2(1−r))/√2], matching to 20 digits; flat/quartic
  reproduce the Lean-certified values (0.8583840547…, 0.86864051…).
- A3: kernel-limit concentration transfer (same window kernel ⇒ same concentration argument).
- A4: N_{ξ′}(I′) ≥ s₁+2s₂+2p, tr Â = N(1+o(1)) via XiPrime RvM/PoissonSq facts.
- A5: the arithmetic of C₉^{ξ′} (recompute; check 6875/6849, 1315/96, 263/132000, 26/6875,
  A₀ = 624/625 < 1, m₉ = 264, n₉ = 256 — f₉ = 0.0039 fixed).
- A6: dependency honesty — the certificate F₈ ≥ 39/10000 (extpress run, audited
  PASS-with-limits) transfers because the pressure kernel is window-determined only.

## Expected verdict format

PASS / F-xxx with exact locations; open obligations; audit report path + sha256.

## Note for the 0.00395 instance

The 0.00395 record (certificate pending) uses the general formula
C₉^{ξ′}(0.00395) = (26,100,000·H_{ξ′}^{MT} − 52,000)/26,000,065 = 0.8692247262341557806822…
(n = 253, m = 261, A₀ = 99935/100000 < 1) instead of the closed form; the audit items are
unchanged (A5 arithmetic verified at 70 digits; A6 re-run on the new certificate file when
it lands).
