#!/usr/bin/env python
"""prune_k8.py — enumerate all Bell(8)=4140 set partitions of {0..7}, compute b, H_sigma,
apply the G2 vanishing rule: J_sigma != 0 iff H_sigma CONNECTED AND m >= 2b-2.
Saves survivors to k8_survivors.json. b=5 survives here (m>=8 for b=5 possible since k=8).
Run: py -3.10 prune_k8.py
"""
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dataset import partitions_of, crossing_count, cycle_multigraph, profile

K = 8

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
    return len({f(i) for i in vs}) if vs else 0

def canon_H(H_edges, b):
    best = None
    for perm in itertools.permutations(range(b)):
        edges = []
        for u, v, mult in H_edges:
            pu, pv = perm[u], perm[v]
            a, bb = (pu, pv) if pu < pv else (pv, pu)
            edges.append((a, bb, mult))
        edges.sort()
        key = tuple(edges)
        if best is None or key < best:
            best = key
    return best

def rule_predict(b, m, H):
    if b == 1:
        return True
    if components(H, b) != 1:
        return False
    return m >= 2 * b - 2

def main():
    all_parts = partitions_of(K)
    print("Bell(8) =", len(all_parts), flush=True)
    assert len(all_parts) == 4140, f"expected Bell(8)=4140, got {len(all_parts)}"
    surv = []
    counts = {"total": len(all_parts), "kept": 0, "pruned_disconnected": 0, "pruned_low_surplus": 0}
    for blocks in all_parts:
        b = len(blocks)
        m = crossing_count(K, blocks)
        H = cycle_multigraph(K, blocks)
        pred = rule_predict(b, m, H)
        rec = {"k": K, "blocks": [sorted(x) for x in blocks], "b": b, "m": m,
               "profile": list(profile(blocks)),
               "H_edges": [[int(u), int(v), c] for (u, v), c in H.items()],
               "connected": components(H, b) == 1, "surplus_ok": m >= 2 * b - 2,
               "pred_nonzero": bool(pred)}
        if pred:
            surv.append(rec)
            counts["kept"] += 1
        else:
            if components(H, b) != 1:
                counts["pruned_disconnected"] += 1
            else:
                counts["pruned_low_surplus"] += 1
    by_b = {}
    for r in surv:
        by_b.setdefault(r["b"], []).append(r)
    # isoclass count
    iso = {}
    for r in surv:
        ch = canon_H(r["H_edges"], r["b"])
        iso.setdefault(ch, []).append(r)
    print("kept =", counts["kept"], "  pruned =", len(all_parts) - counts["kept"],
          "(disc", counts["pruned_disconnected"], "+ low_surplus", counts["pruned_low_surplus"], ")")
    print("survivors by b:", {b: len(v) for b, v in sorted(by_b.items())})
    print("distinct H-isoclasses:", len(iso), " by b:",
          {b: len([ch for ch in iso if iso[ch][0]['b'] == b]) for b in sorted({r['b'] for r in surv})})
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "k8_survivors.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"k": K, "counts": counts, "survivors_by_b": {
                     str(b): sorted(by_b[b], key=lambda r: (r["profile"], r["m"])) for b in sorted(by_b)},
                   "survivors": surv}, f, ensure_ascii=False, indent=1)
    print("wrote", out)

if __name__ == "__main__":
    main()
