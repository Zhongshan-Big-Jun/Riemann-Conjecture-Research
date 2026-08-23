import sys
from fractions import Fraction as F
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260817T030000Z-shiGeneralize-4f2a\reproducibility")
import multi_cert_scan as mc

def run(label, certs):
    best = None
    for m in range(9, 1001):
        sol = mc.solve_lp(m, certs)
        if sol is None:
            continue
        status, tau, r, tax, bound, nodes, rows = sol
        if best is None or bound > best[0]:
            best = (bound, m, tau, tax, r)
    if best is None:
        print(f"{label}: none")
    else:
        bound, m, tau, tax, r = best
        print(f"{label}: m={m} B={bound} tau={tau}")

run("baseline", mc.CERTIFICATES)

# Add all known q=8 canonical points as extra same-q certificates.
extra = [
    ("f9=0.00392 canonical", 8, F(1,4000), F(392,100000)),
    ("f9=0.0039 canonical", 8, F(1,4000), F(39,10000)),
    ("f9=0.0038 canonical", 8, F(1,4000), F(19,5000)),
]
certs = list(mc.CERTIFICATES) + [{"name": n, "q": q, "p": p, "eps": e} for n,q,p,e in extra]
run("baseline + all q8 canonicals", certs)
