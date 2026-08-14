# Problem Contract

Run: `R-20260814T045000Z-extpress-2f36ae` (solve role, obligations O3 + O2).
Task packet: `agenda/task-packets/Q-20260814-criticalline-p1-507bb5.md`.

## Exact statement targeted by this run

Let $\rho=\beta+i\gamma$ run over nontrivial zeros of $\zeta$, $m_\rho$ multiplicity.
For $0\le T_1<T_2$:
- $N(T_1,T_2):=\sum_\rho m_\rho$ over $T_1<\gamma\le T_2$ (with multiplicity);
- $N_0^s(T_1,T_2):=\#\{\rho:\beta=1/2,\ m_\rho=1,\ T_1<\gamma\le T_2\}$ (simple, on-line).

**Obligation O3 (primary, this run).** Extend the consecutive-$k$-zeros "pressure
method" (OpenAI/GPT-5.6 draft, `zeta-simple-zeros`) beyond $k=7$ consecutive zeros:
- Symbolically derive the general-$k$ chain $C_k(m)$: as a function of the
  $k$-point pressure value $f_k=\inf F_{k-1}$ and the block parameters
  $(500, m)$; the $A_0<1$ rigor condition; the $m\to\infty$ class limit.
- Verify it reproduces $k=3$ ($C_3=0.6725197671136777071$) and $k=7$
  ($C_7=0.6730085279277797613$).
- Compute (rigorously, Arb-certified) new pressure constants $f_9$ (and $f_{11}$
  if feasible): certify $F_8\ge f_9$ over 8 variables (and $F_{10}\ge f_{11}$ over
  10 variables) with finite universally-quantified Arb certificates, recorded
  hashes, grids, precisions, and node counts.
- From certified $f_9,f_{11}$, compute $C_9(m),C_{11}(m)$ and class limits, and
  state plainly whether a NEW UNCONDITIONAL RECORD above
  $0.6730085279277797613$ is established.

**Obligation O2 (secondary/support).** Re-verify the OpenAI draft inputs this run
relies on: Lemma 2.1, Corollary 2.2, constant $C_7=(1{,}345{,}000\,H_{\rm MT}-2{,}680)/1{,}340{,}003$,
the 3-point $\epsilon_4\ge221/10^6$ and 7-point $F_6\ge19/5000$ certificates, and
the baseline Theorem D ($H_{\rm MT}=3/2-(1/\sqrt2)\cot(1/\sqrt2)$, Lean-verified).

## Completion criteria

- Status label from the rigorous-open-math-research output protocol.
- Every numerical bound backed by a finite universally-quantified Arb certificate
  with recorded hashes, NOT by floating-point sampling.
- The record question answered plainly: new record > 0.6730085279277797613, or an
  exact obstruction (f_k too small / m-range infeasibility).
- If a new record is proven, `candidate_proof.md` has the complete chain.
- If not, `research_ledger.md` records the exact obstruction; report honestly.
- Standard upstream artifacts under the run root; hashes recorded.

## Constraints

- No RH, no mollifier/zero-density/zero-free-region shortcuts.
- Numerical evidence never labeled as proof.
- The k=9/k=11 certificates must be exhaustive branch-and-bound with Arb, in the
  same certificate format; a coarse/incomplete scan is NOT a certificate.

## User goal addressed

This run contributes to the overarching goal "lim $N_0/N\to1$" via the pressure-
method lower-bound constant. It does not itself reach 1; that is OPEN and reduced
elsewhere (mainpush run R2/R3, and this run's status text). This run squarely
targets whether larger $k$ raises the record constant above 0.673008528.
