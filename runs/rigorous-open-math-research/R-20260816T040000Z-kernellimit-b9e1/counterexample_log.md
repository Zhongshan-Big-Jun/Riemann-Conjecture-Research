# Counterexample / edge-case log — kernel-limit lemma

Run: `R-20260816T040000Z-kernellimit-b9e1`

## Tested cases

1. **λ boundary λ→0.** `K_λ(0)=√2 sin(λ/√2)→0`. The lemma's ratio `F_L(x)/F_L(0)` is not
   meaningful for fixed small λ without an additional lower-bound assumption (F_L(0)→0). For
   the C₉ application λ=1 fixed; and for any fixed λ₀>0 the ratio is well-conditioned. Not a
   counterexample, but a stated-conditions note (contract §3 requires λ∈(0,1] with lower
   bound when stating the ratio uniformly).
2. **x unbounded.** The absolute bound (Eq. 2) `|F_L−K_λ|≤2w/L` holds for **all** x (no
   x-dependence), but `K_λ(x)→0` as |x|→∞ (Riemann–Lebesgue), so the *ratio*
   `F_L(x)/F_L(0)` is bounded only for bounded x — consistent with OpenAI §1 "bounded
   normalized separations". The uniformity statement is therefore for x bounded.
3. **Cfun identification.** Testing `Cfun(λ,L,y)` (autocorrelation) as the kernel overlap
   FAILS to match kMT (Cfun/L=0.6145 vs kMT(0.3)=0.8681). This is a *misframing*, not a
   counterexample to the lemma; it documents that the kernel overlap is the Fourier object,
   and is recorded so a future Lean bridge does not bind the wrong integral.
4. **Numerical integrator bug** (ramp domain split). First ramp script double-counted/omitted
   the bulk band, producing non-converging ratios (err~O(1)). Corrected the domain split;
   with the fix the O(w/L) rate appears cleanly. Ledgered as a failed route / tooling bug,
   not a mathematical obstruction.

## Smallest failing claim encountered

There is **no** failing claim against the lemma as stated (Fourier overlap). The only
"failure" is the side claim that `Cfun` limits to `kMT`, which is false — bounded by (3).
