# Repro manifest — R-20260816T050000Z-m5exact-3f8a

## Environment
- OS: Windows, Python `py -3.10.11` (CPython 3.10), `PYTHONUTF8=1`.
- Packages: numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0, python-flint (present), sympy 1.13.1.
- All computations reproducible from the scripts in `reproducibility/`.

## Inputs (authoritative context, read from prior runs & reports)
- SL reduction (audited): `runs/.../R-20260815T120000Z-sllemma-7b21e4/` (SL ⟺ μ({0})=0 ⟺ Λ_m→0).
- Moment route: `runs/.../R-20260815T130000Z-slmoments-a3f9/` (validated DPP sampler
  `projection_dpp_sampler.py`; exact moments m_1..m_4; measured_moments_L50.txt).
- G1 result (CERTIFIED): `runs/.../R-20260816T030000Z-slG1-9c2a/` (D_3=D_4=D_5=0; D5_exact.json;
  the scaffold `m5_shapes.py` — found here to be WRONG, superseded).
- Probe report: `reports/sl-lemma-random-gram-probe.md` (decomposition machinery, c_{2n}, S_3=1/15).

## Key derived facts
- Exit status: `m_5 = 101/18`, Λ_1=1/4, Λ_2=5/36 (exact).
- Method: exact set-partition shape-integral decomposition + rational box-spline (coarea)
  values, validated by anchor on m_2,m_3,m_4 and an independent high-precision engine.

## Reproducibility steps
1. `py -3.10 enumerate_moments.py 4` → anchors m_2,m_3,m_4.
2. `py -3.10 m5_final.py` → the exact m_5 = 101/18 decomposition.
3. `py -3.10 boxspline2.py` → c_2..c_10 validation.
4. `py -3.10 hankel_exact.py` → Λ_1..Λ_4.
5. `py -3.10 hp_batch.py` / `hp_one.py ...` → independent high-precision cross-checks.
6. `py -3.10 simulate_m5_bias.py` → L=25 DPP; L=50 runs inline in logs.

## Unknown / not pinned
- True m_6,m_7,m_8 (only sampler evidence) — needed for Λ_3,Λ_4.
- Full numerical pin of m_5=101/18 from simulation within tight error (finite-L/h-bias
  corrections uncertain).

## Provenance
All artifacts produced in this run; no external unpublished run data invented. Prior audits and
the D_5=0 certification are cited from the G1 run.
