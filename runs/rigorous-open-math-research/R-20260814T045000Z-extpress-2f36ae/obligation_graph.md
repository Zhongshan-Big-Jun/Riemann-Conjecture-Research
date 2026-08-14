# Obligation Graph

Run: `R-20260814T045000Z-extpress-2f36ae`. O3 (extend >7 zeros) + O2 (support).

## Nodes

| Node | Statement | Depends on | Status |
|---|---|---|---|
| **B0** | $S\ge H_{\rm MT}N-o(N)$ (Theorem D) | Lean `Zeta23.ThmD` | VERIFIED (input, mainpush O1) |
| **B1** | Lemma 2.1 / Cor 2.2: $S\ge H_{\rm MT}N+\Delta(M^\circ)-o(N)$ | B0 | RE-AUDITED verified (mainpush; rechecked) |
| **C3** | $w(u)+w(v)+w(u+v)\ge221/10^6$ | Arb | VERIFIED (this run, byte-identical) |
| **C7** | $F_6(g_1..g_6)\ge19/5000$ | Arb | VERIFIED (this run, byte-identical) |
| **B7** | $C_7=(1{,}345{,}000H_{\rm MT}-2{,}680)/1{,}340{,}003=0.6730085279277797613$ | B1, C7, BE/BD/AV | VERIFIED (this run re-derivation + O2) |
| **GEN** | general-$k$ chain: $C_k(m)=\frac{H_{\rm MT}-(m_k-1)/(500m_k)}{1-A_0/m_k}$, $A_0=f_k(m_k-k+1)$, $m_k=(k-1)+\lceil1/f_k\rceil-1$ | B1, BE$_k$/BD$_k$/AV$_k$ | DERIVED (this run), reproduces B7 |
| **GEN-rigor** | $A_0<1$ required (Lemma 4.3 min{1,·} device) | Lemma 4.3 | DERIVED |
| **F9** | certify $F_8\ge f_9$ (8 vars, Arb) | Arb | **DONE** (this run): $F_8\ge39/10000$ certified, grid 4000 |
| **B9** | $C_9=(6875H_{\rm MT}-1315/96)/6849=0.6730536>0.6730085$ | F9, GEN | **DONE** — NEW RECORD |
| **F11** | certify $F_{10}\ge f_{11}$ (10 vars, Arb) | Arb | OPEN/INFEASIBLE in time (10 vars) |
| **B11** | $C_{11}$ record check | F11, GEN | PENDING |

## Edge relations

- Edge F9 → B9 → outcome_of_record.
- Edge F11 → B11.
- B7 is the baseline to beat; this run tests whether adding constraints k=9 (resp
  11) meets the threshold.

## Open / honest notes

- k=9 rigor certificate may be infeasible within time (8D exhaustive subdivision).
  If so, the obstruction is recorded (cost explosion), not silently filled.
- The m→∞ class limit is formal (needs large-block spectral control) and is not
  claimed as a rigor statement.
