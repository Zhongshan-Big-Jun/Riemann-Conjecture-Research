# A 67.3312742272% lower-bound candidate for simple zeros of zeta

This repository gives a reproducibly certified candidate for

$$
\liminf_{T\to\infty}\frac{N_0^s(T,2T)}{N(T,2T)}
\;\ge\;0.6733127422722459\ldots
\;>\;\frac{6733127422}{10^{10}},
$$

where $N(T,2T)$ counts nontrivial zeros with multiplicity and
$N_0^s(T,2T)$ counts simple zeros on the critical line.

**[Paper (PDF)](paper/main.pdf)** · [LaTeX source](paper/main.tex) ·
[Proof outline](docs/proof.md) · [Verifier docs](docs/verifier.md) ·
[Exact candidate](data/candidate-retuned-p2736.json) ·
[Provenance](docs/provenance.md)

## Results

| Construction | Bound |
| --- | ---: |
| Anthropic Theorem D (`anthropics/zeta-23-lean`) | 0.672500703679… |
| `ainta/zeta-simple-zeros` | 0.673008527927… |
| preceding `trmdy/zeta-simple-zeros-673137` design | 0.673137630699… |
| [`tawanerguo-cn/zeta-simple-zeros`](https://github.com/tawanerguo-cn/zeta-simple-zeros) (same-day public candidate) | 0.673192911473… |
| [`npip99/zeta-zeros`](https://github.com/npip99/zeta-zeros) (same-day public candidate) | 0.673195198901… |
| this repository, retuned 7-point certificate (viva97) | 0.673200117012… |
| this repository + refined deduction ([docs/refined-deduction.md](docs/refined-deduction.md)) | 0.673242589355… |
| this repository, nine-point certificate ([docs/nine-point.md](docs/nine-point.md)) | 0.673311015335… |
| **this repository, nine-point final (LP-converged, cross-host certified)** | **0.673312742272…** |

The two same-day candidates above were located only after this certificate
and its initial draft were complete.  The present figure is numerically
larger than the closer `npip99` value by
$0.0000049181112412813\ldots$ in proportion.  This comparison is context,
not an independent validation or a claim of accepted priority; all of these
new results still require mathematical review.

The bandwidth-one certificate-class obstruction in the Anthropic Lean
artifact is approximately $0.681828687464$.  Thus this optimization does not
suggest a route to 100% within the same information class.

## Ingredients

1. **A re-optimized window.**  The Montgomery–Taylor profile is replaced by
   an exact rational seven-term cosine polynomial.  Arb certifies
   $3/4\le v\le1$, monotonicity on $[0,1/2]$, and
   $H(v)\ge0.6724570414$.
2. **A retuned position-weighted inequality.**  With pressure $p=1/2736$ and
   reflection-symmetric rational pair weights whose six span capacities are
   exactly 2,
   $$F(g_1,\ldots,g_6)\ge\frac{891}{200000}$$
   for every nonnegative gap vector.  The exhaustive interval run visits
   2,168,370 boxes and reaches depth 50.
3. **A sharp square-root block profile.**  For the Gram defect,
   $\operatorname{tr}\Psi(G)\ge h(E)$ with $h(E)=E$ for $E\le1$ and
   $h(E)=2\sqrt E-1$ for $E\ge1$.
4. **A refined block deduction.**  The Φ_m trace–energy envelope and
   window-in-frame pressure counting (due to
   [`tawanerguo-cn/zeta-simple-zeros`](https://github.com/tawanerguo-cn/zeta-simple-zeros);
   independently re-derived and triple-verified here, see
   [docs/refined-deduction.md](docs/refined-deduction.md)) sharpen the
   assembly of the same certified inequality: no chord factor, tax
   $(m{-}q)B_p/m$, optimal $m=235$, bound $0.6732425893558967\ldots$
5. **Explicit asymptotic bookkeeping.**  The proof separates blocks whose
   pressure term already wins from bounded-span blocks where the compact-
   uniform kernel asymptotic applies, and it records endpoint trimming and
   shifted-block errors explicitly.

For $m=272$,

$$
A=\frac{891}{200000}(272-6)=1.18503,
\qquad R=2\sqrt A-1,
\qquad \eta=R/A,
$$

and the final deduction is

$$
\frac SN\ge
\frac{272H_{\rm cert}-\eta(1/456)271}{272-R}
=0.6732001170127618\ldots>0.6732.
$$

## Verify it yourself

Python 3.10 or newer is required.  The sole dependency is pinned because the
certificate records hashes of the outward-rounded binary64 tables.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

zeta-673200-verify fast
zeta-673200-verify main --workers 10
zeta-673200-verify gate
zeta-673200-verify legacy-main --workers 10
python -m unittest discover -s tests -v
```

Recorded runs are in [`certificates/`](certificates/).  The legacy command
reproduces the preceding 67.313763% construction; `gate` reproduces the ainta
seven-point certificate.

## Trust boundary

- The finite gap inequality, window inequalities, exact capacities, and final
  arithmetic are checked by this repository.  Floating-point optimization was
  used only to discover the rational candidate.
- The verifier uses Arb through pinned `python-flint==0.9.0`, fails closed on
  unresolved terminal cells, and explicitly outward-rounds every conversion
  used by the sinc-series tails and binary64 tables.
- The analytic interface for arbitrary admissible windows comes from the
  Anthropic paper and generic `AdmWindow` development; the stability
  refinement and shifted-block argument come from `ainta/zeta-simple-zeros`.
- Unlike Anthropic's original headline theorems, this strengthened result is
  not yet end-to-end formalized in Lean.  A Lean `AdmWindow` instance for the
  new trigonometric profile, the square-root block lemma, and the stability
  assembly remain to be ported.

## Status

Follow-up submitted by **Vivaswat Ojha**, August 11, 2026.  It was developed
in a ChatGPT Work conversation with OpenAI Codex and builds directly on the
three credited predecessor projects; the detailed division of labor is in
[`docs/provenance.md`](docs/provenance.md).  The finite certificate has been
replayed after verifier hardening, but the theorem claim should be treated as
a record candidate pending expert review and an end-to-end formalization.
Project-level citation and any future manuscript authorship are intentionally
left for discussion with the upstream maintainer.

A second campaign the same day ([docs/campaign-2.md](docs/campaign-2.md))
proved this bound is near-optimal within its method family (gap-horizon
transfer-operator certificates cap at ≈0.6734; pure pair-energy methods at
0.674826; unconditional sieve input cannot open bandwidth λ>1), and reduced
the route to 0.675+ to a single open lemma — the off-line pair bridge
composition — with strong certified evidence and exact counterexamples
delimiting its proof.

## License

MIT
