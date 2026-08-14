# Status and Literature

Run: `R-20260814T045000Z-extpress-2f36ae`. Obligations O3 (extend pressure method
beyond 7 zeros) + O2 (re-verification).

## Current best known (verified as of 2026-08-14)

| Constant | Value | Status | Source |
|---|---|---|---|
| $H_{\rm MT}$ (Montgomery-Taylor) | 0.6725007036794116… | Lean-verified | Anthropic Theorem D (`Zeta23.ThmD`), mainpush run O1 |
| 3-point | 0.6725197671136777… | verified (Arb cert) | OpenAI draft; mainpush O2 |
| **9-point (NEW RECORD, this run)** | **0.673053645952589925…** | verified (Arb cert, k=9 grid 4000) | THIS RUN O3 |
| 7-point (prior record) | 0.6730085279277797613… | verified (Arb cert) | OpenAI draft; mainpush O2; THIS RUN O2 re-verified byte-identically |
| 7-point class ceiling (formal limit) | 0.673058325… | formal (needs large-block control) | mainpush O3 (`probe_blocks.py`) |
| bandwidth-one ceiling | 0.6818287… | Lean-certified | mainpush R3 / Lean |
| N0*/N | 0.83625… | Lean-verified | Anthropic |
| proportion=1 | OPEN | — | reduces to PCC(ES)/GLSS25, HL*(-k0) |

## Theorem chain this run relies on (re-verified / inputs)

1. **Theorem D [Anthropic]:** $S\ge H_{\rm MT}N-o(N)$, $H_{\rm MT}=3/2-(1/\sqrt2)\cot(1/\sqrt2)$,
   verified in `zeta-23-lean` (`thmD₀_simple_mult`). Input.
2. **OpenAI Lemma 2.1 / Corollary 2.2:** stability-enhanced rank-trace
   $S\ge H_{\rm MT}N+\Delta(M^\circ)-o(N)$. Re-audited (mainpush Entries 3-4); input.
3. **3-point cert:** $w(u)+w(v)+w(u+v)\ge221/10^6$ on $u,v\ge0,u+v\le4$
   (Arb, grid 16000); re-verified this run byte-identically (hash
   `e19c0637…`).
4. **7-point cert:** $F_6\ge19/5000$ (Arb, grid 4000); re-verified this run
   byte-identically (hash `a9992300…`, `7913c551…`).
5. **Block-energy/defect/pinching chain [OpenAI §4-6]:** re-derived generally in
   this run (see `candidate_proof.general-k-derivation.md`).

## Novelty

An unconditional constant $c>0.6730085279277797613$ for $\liminf N_0^s/N$ with a
full proof is novel. This run's contribution is precisely the question of whether
$k=9$ (or $k=11$) pressure certificates raise the record. If $f_9\ge0.0038296$ is
certified, a new record follows (details in `candidate_proof.general-k-derivation.md` §7).

## Literature notes (see `status_and_literature.md` of mainpush run for full audit)

- GLSS25 (arXiv:2503.15449): PCC ⇒ ES without RH; PCC-full-support ⇒ proportion 1.
- GS25 (arXiv:2511.20059): proportions of critical simple/on-line zeros; C<2 ⇒ ≥2−C.
- CCLM17 traceability gap flagged in mainpush run Entry 11 (unresolved).

## Open questions for this run

- $f_9^{\rm true}=\inf F_8$: certified value and whether it exceeds the record
  threshold $\approx0.0038296$.
- $f_{11}$: feasibility/certified value.
