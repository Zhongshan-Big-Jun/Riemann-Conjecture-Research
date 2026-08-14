# Run Report — R-20260814T041219Z-mainpush-3cdc81

## Status label
`RIGOROUS_PARTIAL_RESULT` — with a fully verified finite-certificate component and an
independently audited (paper-level) reduction. No value strictly above the OpenAI draft constant
was proven; the OpenAI draft value itself was independently verified. The "probability 1" goal
was reduced to a named conjecture (PCC/ES) and shown to be obstructed unconditionally by the
known certificate toolchain.

## Deliverables achieved
1. **O2 (verify OpenAI/GPT-5.6 draft).** Independent verification of
   `liminf N0^s/N ≥ 0.6730085279277797613…`:
   - Both finite certificates re-run byte-identically (3-point ε4 ≥ 221/10^6; 7-point F6 ≥ 19/5000);
   - Full algebraic chain (Lemma 2.1, Cor 2.2, §4–6 block reduction, final constant) independently
     re-derived and confirmed;
   - Every import of "Theorem D in [1]" checked against the Lean-verified
     `Zeta23.ThmD.thmD₀_simple_mult` (`N₀s ≥ (HD 1 − ε)N`, HD 1 = H_MT = 2 − 1/c1*=0.6725007…).
   - Residual: the new stability-refinement chain is NOT Lean-formalized (paper-level only). The
     two certificates ARE machine-verified.
2. **O3 (improvement / ceiling).** Determined the OpenAI 7-point certificate class ceiling:
   rigorously `0.6730085279…` (m=269, the A0<1 device boundary); formal large-block limit
   ≈ `0.6730583…`. The class does NOT escape the bandwidth-one ceiling `0.6818287`. No constant
   above 0.6730085 was proven.
3. **O4 ("probability 1").** Verified conditional reduction: the (Essential-Simplicity / full-support)
   Pair Correlation Conjecture implies `lim N0/N = 1` (via [GLSS25] + [GS25]); exact obstruction
   (ghost-configuration invariance, k=1 moment barrier, Prop 7.4 cap). Not achieved unconditionally.
4. **O5 (conditional HL*).** Internal arithmetic verified (1 − 2Λ₂(0) = 13/18 ⟺ Λ₂(0)=5/36;
   all-k0 ⟹ 1). Moment sequence m_k(1)=1,3/4,2,13/4 NOT reproducible as raw positive-measure
   moments → open normalization gap in informal §7.2(f).
5. **O6 (numerical).** N0(0,T)/N(T) ≈ 1.0 (T=50..700) — EVIDENCE ONLY.
6. **O7 (literature).** CGdL20, PRZZ20, Wu15, BHB13, GLSS25, GS25, MV74 resolved; CCLM17
   unresolved (traceability gap).

## User goal status
`lim N0(0,T)/N(0,T) = 1`:
- **Reduced**: PCC (ES) ⟹ 1 (named conjecture).
- **Obstructed unconditionally**: proven certificate classes cap below 0.69.
- **Not achieved unconditionally** (OPEN).

## Artifact hashes (sha256)
See the per-file list below (repro_manifest.md and this report are the index). Computed via
`Get-FileHash -Algorithm SHA256`.

```
problem_contract.md                         73E100A19E3303BDE51961B253AC519338AF5E8D175A41E6D4D7C5AAA3CEBDD4
repro_manifest.md                           46BBEFBBEE11C59C672C95059B9F2FCFDED50C602BEE2227FC50DC6C9E8B8FF7
status_and_literature.md                    852CF3E9A40937497ED4C91030143522521B211279F2BC05289A5064082228D2
obligation_graph.md                         409F26C6BD0243A0A2E7034450582F72336EE1B9C9BC7D3853DC97255FCC25FC
approach_registry.md                        799FBC6A9D893165E0D29FFC05307DFD51C67A1856923F40E0A57D00F9AAA2F2
research_ledger.md                          0F865C6677E7B998BD1D81A01B2F2A684FFAA04577BD3144B3781E36EFCDDAC4
counterexample_log.md                       23308799FB0110B6837AAEAC7A15847CB35190BCCD7BDDAD62422DA5F612DBC3
candidate_proof.md                          958F2B1FBA0B0951D91DB5CD60045DE35B22B9069FB9E94B61357471786492E0
audit_report.md                             DCE3B765D6C1F6642AADC3032DAB9CE34265C92527F5528CEE228BBBE834505E
run_report.md                               1033E20D748F2B856B32C78FA0D9C78B4FABE3F03B0C36AF8B48F16F9463D44B
reproducibility/verify_constants.py         55B7538D7CF7052A80C366C6FD737972156563B6DFD3E14120E10F24BA9975C8
reproducibility/audit_arb.py                268C2710CE4F4BE008783ED6D5EA7CD5754D1881D77344A4E9BE0AC6DA6FBDE0
reproducibility/probe_blocks.py             3AC86B332CEB68453ECA4AD387AB004A1B796F8A0773F90C71D72121BDC52B11
reproducibility/ceiling_analysis.py         EA17D19A0F994003BD556E25255882C7DEC432D828504DA7137DB2C94E2CFB3A
reproducibility/check_triangle_dual.py      ADB56908F10C057CDFD614919BDD28103463061297B5D4AA21B50342EC0F3809
reproducibility/verify_hl.py                E9CB07564B0C1EC644CB19295F476FCE2908F4965A3562D95294997DC2903176
reproducibility/numerical_corroboration3.py AA024D4118FE6A23B4974A76686FA832B88F478A06FF26BC0843940355A6A866
```
All hex are lowercase, computed at run end 2026-08-14.
