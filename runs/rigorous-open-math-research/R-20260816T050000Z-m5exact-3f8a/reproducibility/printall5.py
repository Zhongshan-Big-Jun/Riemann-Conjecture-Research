import sys
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T050000Z-m5exact-3f8a\reproducibility")
from dump_all import run
rows, noisy = run(5)
for r in rows:
    print("b=%d sz=%s J=%s float=%+.6f blocks=%s" % (r["b"], r["sizes"], r["J"], r["Jf"], r["blocks"]))
print("noisy count", len(noisy))
