# Candidate proof / verification note — OpenAI draft

Run: `R-20260814T041219Z-oaidraft-7c3e73` — independent audit (O2 + O7). See `audit_report.md` (full) and
`repro_manifest.md` (commands/versions).

## Audited claim (held)

`liminf_{T→∞} N0^s(T,2T)/N(T,2T) ≥ (1,345,000·H_MT − 2,680)/1,340,003` with `H_MT = 3/2 − (1/√2)cot(1/√2)`.
Numerically `0.6730085279277797613…`; verified to 60 digits:
- `H_MT = 0.672500703679411645734…`
- final = `0.673008527927779761323475…`
- `2 − 1/c1* = H_MT`, `c1* = 0.7532960678560706…`, `1/c1* = 1.3274992963205883…`

## Two new inequalities — status

1. Lemma 2.1 (`D(M)=trΨ(M)` rank–trace): **proved analytically**.
2. Prop 4.1 `F6 ≥ 19/5000`: **proved by finite, universally-quantified Arb verification** (all g ≥ 0);
   certificate reproduced byte-for-byte (kernel table sha256 `a9992300…`, nodes 707901, all counters).

## Machine / versions (see repro_manifest.md)

Python 3.10.11, python-flint 0.9.0 (FLINT 3.6.0, Arb), Intel Core Ultra 7 155H, Windows x64.

## Result template (abridged)

- Exact result: yes — theorem holds (independently audited).
- Verification performed: analytic re-derivation + exact computational reproduction + Lean constant cross-check.
- Remaining gaps (non-blocking): formal (Lean) proof of `F6 ≥ 19/5000`; fully self-contained Lemma 3.1.
- Confidence by axis: semantic fidelity high; mathematical correctness high (no found error); completeness of
  *this* audit high; novelty of the draft vs. prior lower bound confirmed; reproducibility — certificates match.
