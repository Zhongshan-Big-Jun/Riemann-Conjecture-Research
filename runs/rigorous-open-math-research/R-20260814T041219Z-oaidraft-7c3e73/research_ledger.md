# Research ledger — OpenAI draft audit (O2 + O7)

Timeline of audit activities, 2026-08-14.

## Steps (chronological)

1. Discovered the pre-existing `audit_report.md` in the run root dated from an earlier pass:
   it reported `UNCERTAIN — ARTIFACTS ABSENT` over an empty run root (prior snapshot). Recorded as history;
   superseded by this audit's artifacts.
2. Read task packet `Q-20260814-criticalline-p1-507bb5` (obligations O2 and O7), draft `paper/riemann.pdf/.tex/.txt`,
   `docs/proof.md`, `docs/verifier.md`, verifier source (`verify_three`, `verify_seven`, `kernel`, `rounding`,
   `report`, `cli`, `constants`), certificates, tests.
3. Read the Anthropic v2 paper in full (2277 lines) — Theorem D, Theorem 5.8, Prop 4.1/4.2/4.4/4.5, Lemma 2.2,
   3.1/3.2/3.4, §7.1 optimal window, §7.5 limits, Appendix B Lean mapping.
4. Read Lean `ThmD/Mult.lean` (the multiplicity-aware Theorem D = draft's base), `ThmD/Final.lean`,
   `ZeroSide/RankTraceMult.lean` (Lemma R), confirmed the base constant matches the draft.
5. Installed `zeta-simple-zeros` editable; ran `zeta-zero-verify three` (reproduced byte-for-byte),
   `zeta-zero-verify seven --progress-every 1000000` (reproduced byte-for-byte), unit tests (OK).
   Recorded machine/python-flint/FLINT versions.
6. Re-derived Lemma 2.1, Corollary 2.2 (caught and resolved a would-be §1→(7) sign/step), Lemma 3.1,
   Lemma 4.2, 4.3, §5 pinching/averaging, final constant. All passed.
7. Verified constant identities at 60-digit precision (H_MT, c1*, final bound) — exact match.
8. Resolved bibliographic IDs from [1] reference list; confirmed GS25=arXiv:2511.20059 local file.

## Decisions / failures

- No fatal defect found. The most delicate joints (Ψ(0)≠0 pinching; eq(1)→(7) direction; kernel ½ factor;
  F6 cutoff `Σg=11.4`) were stress-checked and hold.
- Decided verdict `INDEPENDENTLY_AUDITED_PROOF` (not `FORMALLY_VERIFIED_PROOF`: F6 step is computer-assisted,
  not Lean-checked). Lemma 3.1 is a paper-level sketch citing [1]; noted as non-blocking robustness wish.

## Open (non-blocking) items

- Formalize `F6 ≥ 19/5000` (Lean/verified-exact-real) and Lemma 3.1 for a fully machine-checked closure.
- Not part of O2/O7 to improve the constant (that is run `mainpush-3cdc81`, O3); noted for the pipeline.
