# General-k pressure-method chain: symbolic derivation

Run: `R-20260814T045000Z-extpress-2f36ae`. Independently derives the constant
$C_k(m)$ for the consecutive-$k$-zeros pressure method, verifying it reproduces
the k=3 (0.6725197671) and k=7 (0.6730085279277797613) known results, and
furnishes the rigor condition for new k=9 / k=11 certificates.

## Notation

- $h := 2\pi/L$, $x_\rho := L(\gamma_\rho-T)/2\pi$ normalized ordinate.
- $k(x)=K(x)/K(0)$ the normalized Montgomery-Taylor overlap kernel
  ($K$ as in [OpenAI §3], [proof.md §1]); $w(x):=k(x)^2\ge 0$, $w(0)=1$.
- $N=N(T,2T)$ (with multiplicity), $S=N_0^s(T,2T)$ (simple on-line zeros).
- Baseline (Lean-verified Theorem D, `Zeta23.ThmD`): $S \ge H_{\rm MT}N-o(N)$,
  $H_{\rm MT}=\frac32-\frac1{\sqrt2}\cot\frac1{\sqrt2}=0.6725007036794116457\ldots$.

## 1. Stability-enhanced rank-trace inequality (inputs, [OpenAI §2])

Lemma 2.1: $V\in\mathbb C^{d\times r}$, $\|{\rm col}_j\|\le1$, $P=VV^*$, $M=V^*V$,
$Q$ Hermitian with $n_+(Q)=b$:
$$\|P+Q\|_F^2 \ge 4\,{\rm tr}(P+Q)-3r-4b + \Delta(M),\qquad \Delta(M):={\rm tr}\,\Psi(M),$$
with $\Psi(t)=(t-1)^2\cdot1_{t\le2}+(2t-3)\cdot1_{t\ge2}$.
Corollary 2.2: $S\ge H_{\rm MT}N+\Delta(M^\circ)-o(N)$.
These are re-verified in the mainpush run (Entries 3-4) and taken as verified
inputs here; this run's novelty is exclusively the pressure step.

## 2. The k-point pressure function

For $k\ge3$ consecutive ordered points $y_0<\cdots<y_{k-1}$ with nonnegative
gaps $g_i:=y_i-y_{i-1}$ ($1\le i\le k-1$), define

$$F_{k-1}(g_1,\ldots,g_{k-1})
:=\frac{1}{500(k-1)}\sum_{i=1}^{k-1} g_i
+\sum_{s=1}^{k-1}\frac{2}{k-s}\sum_{i=1}^{k-s}
  w\big(g_i+\cdots+g_{i+s-1}\big).$$

Remarks:
- There are $\sum_{s=1}^{k-1}(k-s)=\binom{k}{2}$ pair distances. For $k=7$
  this is 21, matching [OpenAI (13)].
- Linear coefficient $1/[500(k-1)]$: each single gap enters at most $k-1$
  k-windows in the block-energy summation (below), giving net $1/500$ per gap.
- Span-$s$ coefficient $2/(k-s)$: each span-$s$ pair enters at most $k-s$
  windows (weighted equally), so summing windows give coefficient $\le 2$ per
  pair after the pressure cancellation. This is exactly the k=7 structure.

**Certified input.** For $k=7$, $F_6(g_1,\ldots,g_6)\ge 19/5000$ for all
$g_i\ge0$ (Arb-certified, this run AND repo, byte-identical). For general $k$
we seek a certified constant $f_k$:
$$\inf_{g_i\ge0}F_{k-1}(g_1,\ldots,g_{k-1})=:f_k^{\rm true},\quad
\text{we certify }F_{k-1}\ge f_k\le f_k^{\rm true}.$$

## 3. Block energy

For $m$ ordered points $y_1<\cdots<y_m$ set $E_m:=2\sum_{i<j}w(y_j-y_i)$.
Sum the certified inequality $F_{k-1}\ge f_k$ over the $m-k+1$ consecutive
k-windows. A pair spanning $s$ gaps is counted in at most $k-s$ windows with
coefficient $2/(k-s)$, so its total coefficient is $\le 2$, i.e. it contributes
$\le 2w$ to the LHS sum. Each single gap enters at most $k-1$ windows, so the
linear part is $\le \frac{k-1}{500(k-1)}\sum_i g_i=\frac1{500}(y_m-y_1)$.
Therefore

$$E_m + \frac1{500}(y_m-y_1) \ge f_k(m-k+1).\qquad(\mathrm{BE}_k)$$

Check k=7: $f_{7}(m-6)$, exactly [proof.md (4.3)] with $f_7=19/5000$. ✓

## 4. Block defect and the A0<1 rigor condition

Lemma 4.3 [proof.md (16)]: for Hermitian $G\succeq0$,
$$\Delta(G)={\rm tr}\,\Psi(G)\,\ge\,\min\Big(1,\;2\sum_{i<j}|G_{ij}|^2\Big).$$
(If every eigenvalue $\le2$ then $\Psi(G)=(G-I)^2$ and
${\rm tr}(G-I)^2\ge2\sum_{i<j}|G_{ij}|^2$; if some eigenvalue $>2$ then
$\Psi(\lambda)=2\lambda-3>1$.)

Let $G_B$ be the Gram matrix of a consecutive $k$-block $B$ of $k$ retained
simple zeros. Set
$$A_0:=f_k(m-k+1).$$
**Rigor condition:** $A_0<1$. Then for every k-block $B$, combining (BE$_k$)
and the defect lemma with $\sum_{i<j}|G_{ij}|^2=\frac12 E_m+o(1)$ (uniform, by
the kernel-limit lemma since a block has fixed $m$ and $w$-sums concentrate) gives
$$\Delta(G_B)+\frac1{500}\,{\rm span}(B)\ge A_0-o(1).\qquad(\mathrm{BD}_k)$$
The $o(1)$ is uniform in $B$. This is the [OpenAI §4] device, general-k.

**Max rigorous block length:** largest $m$ with $f_k(m-k+1)<1$, i.e.
$$m_k = (k-1) + n_k,\qquad n_k:=\Big\lceil\tfrac1{f_k}\Big\rceil-1,$$
and $\;A_0=f_k\,n_k<1$. For $k=7$, $f_7=19/5000$: $n_7=263$, $m_7=269$,
$A_0=4997/5000<1$. ✓

## 5. Shifted block pinching / averaging

For each of the $m_k$ offsets partition the retained central simple zeros into
consecutive k-blocks (equivalently m-blocks as in the paper; the block-defect
(BD$_k$) holds per *k-point pressure window*, and the window/block equivalence
is the same as [OpenAI §5]). Averaging over all offsets and using the
convexity+unitary-invariance of $\Delta$ under pinching ([OpenAI (20)]),
$$\Delta(M^\circ)\ge \frac{A_0}{m_k}N_0^s - \frac{m_k-1}{500\,m_k}N-o(N).\qquad(\mathrm{AV}_k)$$
Both defect numbers: $A_0/m_k$ and $(m_k-1)/(500 m_k)$.

## 6. Final constant

From Corollary 2.2, $S\ge H_{\rm MT}N+\Delta(M^\circ)-o(N)$; insert (AV$_k$):
$$S\ge H_{\rm MT}N+\frac{A_0}{m_k}S-\frac{m_k-1}{500\,m_k}N-o(N),$$
$$\Big(1-\frac{A_0}{m_k}\Big)S\ge\Big(H_{\rm MT}-\frac{m_k-1}{500\,m_k}\Big)N-o(N).$$
Hence
$$\liminf_{T\to\infty}\frac{N_0^s(T,2T)}{N(T,2T)}
\ge\, C_k(m_k)
:=\frac{H_{\rm MT}-\dfrac{m_k-1}{500\,m_k}}{1-\dfrac{A_0}{m_k}},\qquad
A_0=f_k(m_k-k+1).$$

**Check k=7.** $m_7=269$, $A_0=4997/5000$,
$1-A_0/m_7=1-\frac{4997}{1{,}345{,}000}=\frac{1{,}340{,}003}{1{,}345{,}000}$;
$(m_7-1)/(500 m_7)=\frac{268}{134{,}500}$. So
$$C_7=\frac{H_{\rm MT}-\frac{268}{134{,}500}}{\frac{1{,}340{,}003}{1{,}345{,}000}}
=\frac{1{,}345{,}000\,H_{\rm MT}-2{,}680}{1{,}340{,}003}
=0.6730085279277797613\ldots\quad \checkmark$$

**Check k=3 (triangle mechanism, [proof.md §3]).** The 3-point result is NOT the
block-pressure mechanism (it uses the dual triangle form): with
$\epsilon_4:=\min_{u,v\ge0,u+v\le4}[w(u)+w(v)+w(u+v)]\ge221/10^6$,
$\Delta(M)\ge\frac{\epsilon_4}{2}(S-\frac N2)$, giving
$$C_3=\frac{H_{\rm MT}-\epsilon_4/4}{1-\epsilon_4/2}
=\frac{H_{\rm MT}-221/4{,}000{,}000}{1-221/2{,}000{,}000}
=0.6725197671136777071\ldots\quad \checkmark$$
So both known constants are reproduced by the appropriate formula.

## 7. Formal class limit and record threshold

Formal large-$m$ limit (needs uncontrolled large-block spectral monotonicity;
not a rigor statement on its own):
$$C_k^{\infty}:=\lim_{m\to\infty}\frac{H_{\rm MT}-\frac{m-1}{500m}}{1-\frac{f_k(m-k+1)}{m}}
=\frac{H_{\rm MT}-\frac1{500}}{1-f_k}
=\frac{0.670500703679\ldots}{1-f_k}.$$

**Record thresholds.** Writing $m=m_k,n=n_k$,
$$C_k(m)=\frac{H_{\rm MT}-\frac{m-1}{500m}}{1-\frac{f_k n}{m}},\quad m=(k-1)+n,\quad
n=\lceil1/f_k\rceil-1.$$
The k=7 certificate value is $t_7=0.6730085279277797613$. For $k=9$,
$C_9>t_7$ holds exactly when $f_9\ge f_9^*\approx0.0038296$ (computed in
`threshold_analysis.py`; the fine scan crosses at $f\approx0.0038296$). The
formal class limit exceeds $t_7$ when $f_k>1-\frac{H_{\rm MT}-0.002}{t_7}\approx0.0037263$.
Hence even a modest certified $f_9>0.0038296$ yields a **new unconditional
record**; $f_9\le0.0038296$ yields no improvement.

*Implication for the numerical task:* the certified minimum of $F_8$ (8
variables) must exceed the certified minimum of $F_6$ (0.0038), and in fact
exceed $\approx0.0038296$, for $k=9$ to improve on the k=7 record. Whether the
true $f_9^{\rm true}$ meets this is a computational question (section: scoping
in this run).
