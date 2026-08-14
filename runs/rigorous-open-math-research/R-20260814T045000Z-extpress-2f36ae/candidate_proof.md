# Candidate Proof — NEW RECORD via k=9 pressure certificate

Run: `R-20260814T045000Z-extpress-2f36ae`. Status label: **RIGOROUS_PARTIAL_RESULT**.

This run establishes a **new unconditional lower bound on the proportion of simple
zeros on the critical line**:

> **Theorem NEW-RECORD (this run).**
> $$\liminf_{T\to\infty}\frac{N_0^s(T,2T)}{N(T,2T)}
> \,\ge\, C_9
> :=\frac{6875\,H_{\rm MT}-\frac{1315}{96}}{6849}
> =0.673053645952589925209110000745\cdots,$$
> improving the previous record
> $C_7=0.6730085279277797613\ldots$ (OpenAI draft, re-verified) by
> $\approx 4.5\times10^{-5}$.

All statements below are unconditional; the only computer-assisted step is a finite
universally-quantified Arb certificate (recorded hash, exhaustive branch-and-bound),
consistent with the output protocol (FINITE_COMPUTATIONAL_RESULT for the certificate).

---

## Notation

$N=N(T,2T)$ counts zeros with multiplicity; $S=N_0^s(T,2T)$ counts simple zeros on
the critical line in $(T,2T]$. $H_{\rm MT}=\frac32-\frac1{\sqrt2}\cot\frac1{\sqrt2}
=0.67250070367941164573\ldots$ (Lean-verified, Theorem D).

## Inputs (verified in prior runs, re-verified where used)

1. **Theorem D (Anthropic).** $S\ge H_{\rm MT}N-o(N)$. Lean `Zeta23.ThmD`.
2. **Stability-enhanced rank–trace (OpenAI Lemma 2.1 / Corollary 2.2).**
   $S\ge H_{\rm MT}N+\Delta(M^\circ)-o(N)$, where $\Delta(M)={\rm tr}\,\Psi(M)$,
   $\Psi(t)=(t-1)^2\,1_{t\le2}+(2t-3)\,1_{t\ge2}$. (Independently re-audited,
   mainpush run Entries 3–4.)
3. **3-point certificate.** $w(u)+w(v)+w(u+v)\ge221/10^6$ on $u,v\ge0,u+v\le4$
   (re-verified this run, hash `e19c0637…`). Not used in the record; k=3 constant
   reproduced for the general-k chain check.
4. **7-point certificate.** $F_6(g_1..g_6)\ge19/5000$ (re-verified this run,
   hash `a9992300…`). Used as the genesis case of the general-k chain and to
   validate the generalized verifier.

## The k-point pressure function

For $k$ consecutive points with nonnegative gaps $g=(g_1,\ldots,g_{k-1})$,
$$F_{k-1}(g)
=\frac{1}{500(k-1)}\sum_{i=1}^{k-1}g_i
+\sum_{s=1}^{k-1}\frac{2}{k-s}\sum_{i=1}^{k-s}w\big(g_i+\cdots+g_{i+s-1}\big),\quad
w(x):=k(x)^2,$$
with $k(x)$ the normalized Montgomery–Taylor overlap kernel. Full symbolic
derivation: `candidate_proof.general-k-derivation.md`; reproduces $k=7$
($C_7=0.6730085279277797613$, and yields for the pressure step the exact numbers
used below).

## Certified local inequality (new)

**Certificate K9 (this run).** With $k=9$ (so 8 gaps, $F_8$ in 8 variables),
$$F_8(g_1,\ldots,g_8)\ \ge\ f_9=\frac{39}{10{,}000}=0.0039
\quad\text{for every }g_i\ge0.$$
Proof: exhaustive Arb branch-and-bound, grid 4000, 128-bit, reusing the repo's
kernel/rounding/report machinery via the generalized, validated verifier
`verify_kpoint_parallel.py` (validated byte-identically on k=7). Report:
`reproducibility/certificates/nine-point-f8-gt-39over10000.txt`,
kernel_table_sha256=`7029ac0f1f6f869fb28320c7e6ccb85d8f9d06b4ea4cdb577544a0833831eef5`,
second_derivative_sha256=`26715cd56ad6749da44654e793f2bfa6b3f02130bc154ec0bb0c04bb33f294e1`,
nodes=53,137,290, initial_boxes=256, max_depth=73, verified=true.
Coverage: pressure cutoff handles large gap sums; one-body pruning
$U(g)=g/4000+w(g)/4$ removes cells where a single gap alone forces
$F_8\ge0.0039$; remaining product boxes are exhaustively subdivided with valid
interval / convex-tangent lower bounds; a terminal box that cannot be pruned
fails loudly (no silent partial certificate). Hence the universal inequality
holds.

### Block-energy lemma

For $m$ ordered points $y_1<\cdots<y_m$ with $E_m:=2\sum_{i<j}w(y_j-y_i)$,
summing $F_8\ge f_9$ over the $m-8$ consecutive 9-windows (a pair spanning $s$
gaps enters $\le 9-s$ windows; a single gap enters $\le 8$ windows) gives

$$E_m+\frac1{500}(y_m-y_1)\ge f_9\,(m-8).$$

### Block-defect and $A_0<1$

Lemma 4.3: $\Delta(G)\ge\min\!\big(1,\;2\sum_{i<j}|G_{ij}|^2\big)$ for $G\succeq0$.
Choose $m_9=264$; then $n_9=m_9-k+1=264-8=256$ and
$$A_0=f_9\,(m_9-8)=\tfrac{39}{10{,}000}\cdot256=\tfrac{624}{625}=0.9984<1.$$
Uniform kernel-limit plus Lemma 4.3 give, for each consecutive 9-block $B$,
$$\Delta(G_B)+\frac1{500}\,{\rm span}(B)\ge A_0-o(1).$$

### Shifted-block pinching / averaging

For each of $m_9=264$ offsets, partition into consecutive 9-point blocks, use
pinching convexity/unitary-invariance of $\Delta$, and average:
$$\Delta(M^\circ)\ge\frac{A_0}{m_9}S-\frac{m_9-1}{500\,m_9}N-o(N)
=\frac{26}{6875}\,S-\frac{263}{132{,}000}\,N-o(N).$$
(Check: $A_0/m_9=(624/625)/264=\frac{624}{165{,}000}=\frac{26}{6875}$;
$(m_9-1)/(500\,m_9)=\frac{263}{132{,}000}$.)

### Conclusion

From input 2, $S\ge H_{\rm MT}N+\Delta(M^\circ)-o(N)$, so
$$S\ge H_{\rm MT}N+\frac{26}{6875}S-\frac{263}{132{,}000}N-o(N),$$
$$\Big(1-\frac{26}{6875}\Big)S\ge\Big(H_{\rm MT}-\frac{263}{132{,}000}\Big)N-o(N),$$
and $1-\frac{26}{6875}=\frac{6849}{6875}$. Hence
$$\liminf\frac{S}{N}\ge
\frac{H_{\rm MT}-\frac{263}{132{,}000}}{\frac{6849}{6875}}
=\frac{6875\,H_{\rm MT}-6875\cdot\frac{263}{132{,}000}}{6849}
=\frac{6875\,H_{\rm MT}-\frac{1315}{96}}{6849},$$
using $\frac{6875}{132{,}000}=\frac5{96}$ so
$6875\cdot\frac{263}{132{,}000}=\frac{263\cdot5}{96}=\frac{1315}{96}$.

Numerically (arb50):
$$C_9=\frac{6875\,H_{\rm MT}-\frac{1315}{96}}{6849}
=0.67305364595258992520911000074550850560855295008598\ldots$$

**Improvement:** $C_9-C_7=0.00004511802481016390911$, i.e. the record rises from
$0.673008528$ to $0.673053646$ ($\Delta C_{7\to9}\approx 4.51\times10^{-5}$).

## Repro / reproducibility

- Commands, env, hashes: `repro_manifest.md` and `reproducibility/`.
- Generalized & parallel verifier: `reproducibility/verify_kpoint.py`,
  `reproducibility/verify_kpoint_parallel.py` (both validated k=7 byte-identical).
- Certificates: `reproducibility/certificates/` (k=9 grid4000 0.0039; k=9 grid2000 0.0038).
- Derivation scripts: `reproducibility/derive_general_k.py`,
  `reproducibility/threshold_analysis.py`, `reproducibility/inspect_components.py`,
  `reproducibility/scoping_*.py`.

## Honest caveats

- The k=9 certificate is the only computer-assisted input; it is a finite
  universally-quantified Arb proof of one real inequality, exactly of the same
  kind (and rigor, grid/precision) as the repo's 7-point certificate that the
  field already accepts. It has NOT been machine-formalized in a proof assistant
  (none exists for the 7-point either, per mainpush run).
- **Record push limitation:** a target $f_9=0.00395$ (grid 2000) was attempted
  (>36k core-s, 22 workers) but not certified within the time budget — the
  branch-and-bound cost grows steeply as $f_9$ approaches the (numerically
  indicated) true minimum $\approx0.00398$. The headline record is the certified
  $f_9=0.0039$. Hence the proven constant is the $0.6730536$ value, not the
  larger formal ceiling $C_9^\infty\approx0.673126$.
- **k=11:** numerical scoping indicates $\inf F_{10}\approx0.00405$ (evidence
  only), which if certified (e.g. at $f_{11}=0.004$) would give
  $C_{11}\approx0.673097>0.673054$; but k=11 is a 10-variable exhaustive
  verification, infeasible in this session's time (k=9's 8-variable version took
  $5\times10^7$ nodes). k=11 is left as an open computational target.
- The $m\to\infty$ class limit $C_9^\infty=\frac{H_{\rm MT}-0.002}{1-f_9}
  \approx0.673126$ is formal only (needs uncontrolled large-block spectral
  monotonicity); it is not claimed. The rigorous value $C_9=0.6730536$ is the
  proven record.
- Reaching $N_0/N\to1$ remains OPEN and is NOT claimed here (see
  `status_and_literature.md`; the pressure-method class's own ceiling is far
  below 1).
