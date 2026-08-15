import sys
sys.path.insert(0, r"F:\LaTeX\Riemann Conjecture\runs\rigorous-open-math-research\R-20260816T050000Z-m5exact-3f8a\reproducibility")
import hp_one
print("results:")
for pat in ["[{0,1},{2,4},{3}]", "[{0,3},{1,4},{2}]", "[{0},{1,4},{2,3}]",
            "[{0,2},{1},{3,4}]", "[{0,3},{1},{2,4}]",
            "[{0,1,3},{2},{4}]", "[{0},{1,3,4},{2}]"]:
    blocks = [frozenset(x) for x in eval(pat)]
    tot, wall = hp_one.J_hp_one(blocks, 5, 1000000)
    print(f"  {pat} -> {tot:+.6f}  (wall {wall:.0f}s)")
