# Counterexample Log / Failed Routes

Run: `R-20260814T041219Z-mainpush-3cdc81`.

## Tested / probed edge cases
1. **Psi identity** min_{n≥0}[(p−n)²+4n] = 2p−1+Ψ(p): tested at p ∈ {0, 0.5, 1, 1.5, 1.99, 2, 2.5, 4, 10};
   exact equality confirmed each time (mpmath). No counterexample.
2. **3-point dual form (3.4) triangle** tr Ψ(M) ≥ (3/2)Σ_{i<j}M_ij²: swept 200,000 random 3×3
   PSD Gram matrices; worst ratio 1.6723 (no violation of 1.5). Evidence only (not a full proof),
   but consistent. No counterexample found.
3. **ε4 positivity**: numerical min of k(u)²+k(v)²+k(u+v)² on {u,v≥0,u+v≤4} = 0.0002229 at
   (1.054, 2.012), above claimed 0.000221. No counterexample; matches certified 221/10^6.
4. **m>269 block defect**: attempted plugging m>269 into the OpenAI A0/m formula. The min{1,·}
   device fails for m>269 (A0 = 19(m−6)/5000 > 1) — the naive scaling is INVALID there.
   This is a failed route (needs large-block spectral control). Recorded as probe_blocks.py.
5. **HL* moments m_k(1)=1,3/4,2,13/4**: tried (a) as raw positive-measure moments → infeasible
   (m₂=3/4 < m₁²=1); (b) via GUE/sine-process Monte-Carlo Gram matrices → obtained m₂≫1, not 3/4
   (wrong normalization model). Both failed to reproduce the claimed values. The values are
   taken only as informal §7.2(f) input; flagged open (see audit_report).

## Failed lemmas / routes
- **Unconditional improvement beyond 0.6730085:** not achieved. The class ceiling ≈ 0.673058
  (m→∞) and requires spectral control not available; rigorous value stays 0.6730085 (m=269).
  Route not fruitfully extendable by longer blocks / better Ψ / window changes alone.
- **Independent reproduction of HL* moment sequence:** failed; normalization subtlety open.
