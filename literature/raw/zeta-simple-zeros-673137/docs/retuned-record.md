# Retuned 67.3200117% candidate

## Result and status

Keeping the published window fixed, replace only the pressure and the exact
position weights in the seven-point inequality.  The interval verifier proves

\[
F(g_1,\ldots,g_6)\ge \frac{891}{200000}
\qquad(g_i\ge0)
\]

with pressure \(p=1/2736\).  Every span capacity is exactly 2.  In the same
analytic interface and square-root block deduction used by the accompanying
paper, the optimal integer block length is \(m=272\), giving

\[
\liminf_{T\to\infty}\frac{N_0^s(T,2T)}{N(T,2T)}
\ge 0.6732001170127618568\ldots
>\frac{1683}{2500}=0.6732.
\]

The finite inequality, capacity accounting, stated numerical window bounds,
and final arithmetic are machine-certified.  As with the repository's
67.313763% claim,
an end-to-end theorem still inherits the arbitrary-window analytic interface
from the Anthropic paper and the stability argument from
`ainta/zeta-simple-zeros`; this retuning has not been ported to Lean.  It should
therefore be described as a rigorously certified **record candidate** pending
independent mathematical review, rather than as a peer-reviewed record.

Two independent same-day repositories, located after this certificate and
its initial draft were complete, report candidates at
[`0.673192911473...`](https://github.com/tawanerguo-cn/zeta-simple-zeros) and
[`0.673195198901...`](https://github.com/npip99/zeta-zeros).  The value here
is numerically higher than the latter by
(0.0000049181112412813ldots) in proportion.  Neither repository was an
input to this retuning, and this ordering does not substitute for independent
review of any claim.

## Exact retuning

The complete rational design is in
`data/candidate-retuned-p2736.json` and `src/zeta_ext/design.py`
(`src/zeta_ext/retuned.py` remains a compatibility alias). Numerical
optimization found the design; it is not trusted by the proof.  The observed
floating minimum is about 0.00446236056, while the certified target is
0.004455.

The exhaustive grid-4000 run visited 2,168,370 boxes, reached depth 50, and
closed every box.  Its table hashes and pruning counts are recorded in
`certificates/retuned-p2736-grid4000.txt`.

## Deduction, including the bounded-span case

Let \(q=6\), \(\varepsilon=891/200000\), \(B_p=qp=1/456\), and \(m=272\).
Summing the local certificate over the \(m-q\) consecutive windows in a block
gives

\[
E_B+B_p\operatorname{span}(B)\ge
A:=\varepsilon(m-q)=1.18503.
\]

Put \(R=2\sqrt A-1\) and \(\eta=R/A\).  If
\(B_p\operatorname{span}(B)\ge A\), then the desired block inequality follows
from the pressure term alone.  Otherwise the span is bounded by the fixed
constant \(A/B_p\), so the compact-uniform Gram-kernel asymptotic applies to
every pair in the fixed-size block.  The square-root profile and its chord on
\([0,A]\) then give

\[
\operatorname{tr}\Psi(G_B)
+\eta B_p\operatorname{span}(B)\ge R-o(1),
\]

uniformly over the retained blocks.  Removing the standard endpoint strips of
normalized width \(L^2\) deletes \(o(N)\) zeros.  Shifted block pinching charges each interior
gap in at most \(m-1\) of the \(m\) offsets; the leftover endpoint blocks have
only \(O(m)\) points per offset.  Hence

\[
\operatorname{tr}\Psi(M)\ge
\frac{R}{m}S-\eta B_p\frac{m-1}{m}N-o(N).
\]

Combining this with \(S\ge H(v)N+\operatorname{tr}\Psi(M)-o(N)\) and the
certified \(H(v)\ge3362285207/(5\cdot10^9)=0.6724570414\) gives

\[
\frac SN\ge
\frac{272(3362285207/(5\cdot10^9))-\eta(1/456)271}{272-R}
=0.6732001170127618568\ldots.
\]

The modified window is positive and nonincreasing on \([0,1/2]\).  The
verifier evaluates the removable-zero form

\[
\frac{v'(s)}s=-\sum_jc_j\omega_j^2\operatorname{sinc}(\omega_js)
\]

and obtains an upper bound below \(-0.7763\).  Together with
\(3/4\le v\le1\), multiplying \(\sqrt v\) by the standard outward-monotone
boundary ramp gives \(0\le\varphi\le1\) and total variation at most 2 for both
\(\varphi\) and \(\varphi^2\).  This supplies the missing
monotonicity/bounded-variation check in the window admissibility argument.
The remaining second-derivative bounds follow with a fixed
profile-dependent constant from \(v\ge3/4\), the finite trigonometric sum,
and the standard fixed-width ramp; an explicit Lean `AdmWindow` instance has
not been written.  The same lower bound gives the required fourth-moment
condition eventually, since the ramp occupies only \(O(1)\) of an interval
of length \(L\) and \(\int v^2\ge9/16>1/2\).

## Reproduction

After the repository's normal `pip install -e .` setup:

```bash
zeta-673200-verify fast
zeta-673200-verify main --workers 10
python -m unittest discover -s tests -v
```

The main run uses Arb interval arithmetic through pinned `python-flint==0.9.0`.
It fails closed if any terminal grid cell cannot be certified.

## Why this does not point to 100%

This retuning spends slack inside the same pair-energy certificate class.  It
does not change the information supplied by the analytic interface.  The
Lean artifact's bandwidth-one obstruction is about 0.6818287, and the more
specific pure pair-energy class has a ceiling near 0.674826 in the subsequent
[`campaign-2`](campaign-2.md) analysis.  Reaching 100% would require a
qualitatively stronger bridge (for example, information beyond bandwidth-one
pair data or a new way to charge off-line/multiple-zero defects).  Even a 100%
liminf statement would mean that the exceptions have density zero, not that
no exceptional zero exists.
