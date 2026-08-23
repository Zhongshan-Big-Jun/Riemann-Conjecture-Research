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
        print(f"{label}: m={m} B={bound} tau_q9={tau[-1] if len(tau)>2 else 0}")

# Baseline
run("baseline", mc.CERTIFICATES)

# Synthetic q=9 scenarios (all evidence only)
scenarios = [
    ("q9 p=1/4500 eps=0.00395", F(1,4500), F(395,100000)),
    ("q9 p=1/4500 eps=0.00400", F(1,4500), F(400,100000)),
    ("q9 p=1/4500 eps=0.00420", F(1,4500), F(420,100000)),
    ("q9 p=1/4500 eps=0.00450", F(1,4500), F(450,100000)),
    ("q9 p=1/4000 eps=0.00420", F(1,4000), F(420,100000)),
    ("q9 p=1/3500 eps=0.00420", F(1,3500), F(420,100000)),
    ("q9 p=1/3000 eps=0.00450", F(1,3000), F(450,100000)),
]
for name, p, eps in scenarios:
    certs = list(mc.CERTIFICATES) + [{"name": name, "q": 9, "p": p, "eps": eps}]
    run(name, certs)
