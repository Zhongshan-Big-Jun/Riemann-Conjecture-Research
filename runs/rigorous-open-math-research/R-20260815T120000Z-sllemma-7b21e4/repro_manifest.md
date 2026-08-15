# Repro Manifest — R-20260815T120000Z-sllemma-7b21e4

## Run inputs (accepted project facts, audited upstream)
- SL statement + role: condp1 `R-20260814T041219Z-condp1-698ec7/candidate_proof.md` §5 (Spectral
  Lemma), §3 (Lemma 3.B), §2 (HL*), status_and_literature.md §5.
- Moment model + exact m_1..m_4 + eliminated models + empirical L=50 moments:
  `F:\LaTeX\Riemann Conjecture\reports\sl-lemma-random-gram-probe.md` (read in full).
- Exact low moments (1, 4/3, 2, 13/4) and Λ_2(0)=5/36 correction: condp1 candidate_proof.md §4.

## Tools/versions (as provided)
- Python `py -3.10`, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, mpmath 1.3.0 (only numpy used).
- web_search for literature pass 7.

## Artifacts produced (this run)
- problem_contract.md
- status_and_literature.md (pass-7 literature + reduction)
- approach_registry.md (7 routes)
- research_ledger.md
- counterexample_log.md
- obligation_graph.md
- candidate_proof.md
- repro_manifest.md
- audit_report.md (from adversarial subagent)
- reproducibility/check_christoffel_criterion.py  (validates Λ criterion; exact 5/36 downstream)
- reproducibility/check_hankel_from_moments.py    (Hankel Λ from sine-Gram moments)
- reproducibility/dpp_higher_moments_probe.py     (FAILED sampler; excluded as evidence, kept for honesty)
- reproducibility/verify_lambda2_536_exact.py     (exact-rational Λ_2=5/36 + monotonicity/CS consistency)
- reproducibility/verify_empirical_hankel_highprec.py (50-digit mpmath; rules out float artifact)
- reproducibility/fit_moment_decay.py

## Commands
```
cd "...\R-20260815T120000Z-sllemma-7b21e4\reproducibility"
$env:PYTHONUTF8=1
py -3.10 check_christoffel_criterion.py
py -3.10 check_hankel_from_moments.py
py -3.10 verify_lambda2_536_exact.py
py -3.10 verify_empirical_hankel_highprec.py
py -3.10 fit_moment_decay.py
```
## Hashes
Top-level md artifacts + each reproducibility script hashed in the run dir `SHA256SUMS`.
reproducibility scripts (sha256, recomputed after audit; definitive in SHA256SUMS):
- check_christoffel_criterion.py  F3532899573A93DF3BA608AC608CE70950BE8607FAA958EF7E56A67FF29E3872
- check_hankel_from_moments.py    8AA96B7A8E7DD7EE439802F2D090AA1AB5B9FC403FD37C96D2C1778A38CCDF5B
- dpp_higher_moments_probe.py     5C21804B2D27A208CF38F664899D28D72A1058BD4D6E6F77A2F57508F418A942 (DEFECTIVE, excluded)
- fit_moment_decay.py             5F77B2312D91E03B368704341F27530237288310581A911DF98BE6EA4B46343B
- verify_lambda2_536_exact.py     and verify_empirical_hankel_highprec.py: see SHA256SUMS (updated 2026-08-15, post-audit)

## Unknowns / restrictions
- The Christoffel atom theorem (Λ_m(x)→μ({x})) is used as a cited theorem (Breuer–Last–Simon;
  Lagomasino–Marcellán–Van Assche), not re-derived; a formal Lean pass would pin it (out of scope).
- The exact high moments m_k, k≥5 of the sine-DPP Gram are UNKNOWN (open sub-ingredient).
- The broken DPP sampler (dpp_higher_moments_probe.py) is defective and excluded; do not reuse.
