import sys
from fractions import Fraction as F
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260817T030000Z-shiGeneralize-4f2a\reproducibility")
import multi_cert_scan as mc

def add(q, p, eps, name):
    certs = list(mc.CERTIFICATES)
    certs.append({"name": name, "q": q, "p": p, "eps": eps})
    return certs

def run(label, certs):
    best = None
    feasible = 0
    for m in range(9, 1001):
        sol = mc.solve_lp(m, certs)
        if sol is None:
            continue
        feasible += 1
        status, tau, r, tax, bound, nodes, rows = sol
        if best is None or bound > best[0]:
            best = (bound, m, tau, tax, r)
    if best is None:
        print(label, "none")
        return
    bound, m, tau, tax, r = best
    print(f"{label}: feasible={feasible} m={m} B={bound} R={r} tau={tau} tax={tax}")

run("baseline", mc.CERTIFICATES)
run("baseline+synthetic q9 canonical 0.00395", add(9, F(1,4500), F(395,100000), "q9-synth-canon"))
run("baseline+synthetic q9 strong 0.0042", add(9, F(1,4500), F(42,10000), "q9-synth-strong"))
