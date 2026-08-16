#!/usr/bin/env python
"""prune_k7.py — enumerate all Bell(7)=877 set partitions of {0..6}, compute b, H_sigma,
and apply the G2 vanishing rule: J_sigma != 0  iff  H_sigma CONNECTED  AND  m >= 2b-2.
Saves the surviving (predicted nonzero) partitions to k7_survivors.json with all metadata.
Run: py -3.10 prune_k7.py
"""
import os, sys, json
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dataset import partitions_of, crossing_count, cycle_multigraph, profile

K = 7

def components(H, b):
    par = list(range(b))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    deg = [0] * b
    for (u, v) in H:
        ru, rv = f(u), f(v)
        if ru != rv:
            par[ru] = rv
        deg[u] += 1
        deg[v] += 1
    vs = [i for i in range(b) if deg[i] > 0]
    if not vs:
        return 0
    return len({f(i) for i in vs})

def rule_predict(b, m, H):
    """True -> predicted nonzero (G2 rule)."""
    if b == 1:
        return True
    if components(H, b) != 1:
        return False
    return m >= 2 * b - 2

def main():
    all_parts = partitions_of(K)
    assert len(all_parts) == 877, f"expected Bell(7)=877, got {len(all_parts)}"
    surv = []
    pruned = []
    counts = {"total": len(all_parts), "kept": 0, "pruned_disconnected": 0, "pruned_low_surplus": 0}
    for blocks in all_parts:
        b = len(blocks)
        m = crossing_count(K, blocks)
        H = cycle_multigraph(K, blocks)
        rec = {
            "k": K,
            "blocks": [sorted(x) for x in blocks],
            "b": b,
            "m": m,
            "profile": list(profile(blocks)),
            "H_edges": [[int(u), int(v), c] for (u, v), c in H.items()],
            "connected": components(H, b) == 1,
            "surplus_ok": m >= 2 * b - 2,
        }
        pred = rule_predict(b, m, H)
        rec["pred_nonzero"] = bool(pred)
        if pred:
            surv.append(rec)
            counts["kept"] += 1
        else:
            pruned.append(rec)
            if components(H, b) != 1:
                counts["pruned_disconnected"] += 1
            else:
                counts["pruned_low_surplus"] += 1
    # group survivors by b
    by_b = {}
    for r in surv:
        by_b.setdefault(r["b"], []).append(r)
    print("Bell(7) =", len(all_parts))
    print("kept (predicted nonzero) =", counts["kept"])
    print("pruned_total =", len(pruned), "= disconnected", counts["pruned_disconnected"],
          "+ low_surplus", counts["pruned_low_surplus"])
    print("survivors by b:", {b: len(v) for b, v in sorted(by_b.items())})
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "k7_survivors.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"k": K, "counts": counts,
                   "survivors_by_b": {str(b): [x for x in sorted(by_b[b], key=lambda r: (r["profile"], r["m"]))]
                                      for b in sorted(by_b)},
                   "survivors": surv}, f, ensure_ascii=False, indent=1)
    print("wrote", out)

if __name__ == "__main__":
    main()
