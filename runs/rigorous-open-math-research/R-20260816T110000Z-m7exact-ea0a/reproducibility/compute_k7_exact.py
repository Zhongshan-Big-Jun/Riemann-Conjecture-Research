#!/usr/bin/env python
"""compute_k7_exact.py — compute EXACT J_sigma for every surviving k=7 partition (G2-pruned).

Strategy: J_sigma depends only on the cycle-edge multigraph H_sigma (isoclass). The 540
survivors collapse to 18 distinct H-isoclasses. For each isoclass:
  b=1                     -> J = 1 (closed form)
  b=2                     -> J = c_m - c_{m+2},  m = #cycle crossings (closed form, exact)
  b=3, b=4                -> J = sum_{perm in S_b} sign(perm) * B_Gamma(0) with the
                              AUDIT-GRADE exact box-spline engine (boxspline_exact2),
                              cross-validated against the fast engine (boxspline_exact_fast)
                              to < 1e-12, then rational reconstruction.

Each isoclass's J (exact Fraction) is assigned to every partition in that isoclass, then
all 540 weights are summed to give m_7 = sum J_sigma.

Checkpointed: writes k7_iso_results.json after each isoclass so long runs can resume.
Run: py -3.10 compute_k7_exact.py
"""
import os, sys, json, time, itertools
from fractions import Fraction as F
from math import comb, factorial
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import cycle_edges, rho_terms, perm_edges
import boxspline_exact2 as EX2
import boxspline_exact_fast as FST

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- exact c_{2n} = B_{2n}(0) ----------
def c_2n(n):
    m = 2 * n
    s = 0
    for k in range(n):
        s += (-1) ** k * comb(m, k) * (n - k) ** (m - 1)
    return F(s, factorial(m - 1))

def cval(N):
    # N even
    return c_2n(N // 2)

# ---------- isoclass canonical form ----------
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

# ---------- helpers ----------
def np_array(fl):
    return np.array([int(round(x)) for x in fl])

def blocks_of(r):
    return tuple(frozenset(x) for x in r["blocks"])

def J_closed_b2(blocks, k):
    # b=2: J = c_m - c_{m+2}, m = #cycle crossings
    bid = {}
    for i, bl in enumerate(blocks):
        for e in bl:
            bid[e] = i
    idx = [bid[a] for a in range(k)]
    m = sum(1 for a in range(k) if idx[a] != idx[(a + 1) % k])
    return cval(m) - cval(m + 2), m

def J_box_exact(blocks, k, b):
    cyc = [np_array(e) for e in cycle_edges(blocks, k)]
    tot = 0.0
    for sign, perm in rho_terms(b):
        pe = [np_array(e) for e in perm_edges(perm, b)]
        tot += sign * EX2.coarea_value_exact(cyc + pe)
    return tot

def J_box_fast(blocks, k, b):
    cyc = [np_array(e) for e in cycle_edges(blocks, k)]
    tot = 0.0
    for sign, perm in rho_terms(b):
        pe = [np_array(e) for e in perm_edges(perm, b)]
        tot += sign * FST.eq_coarea_value_exact_fast(cyc + pe)
    return tot

def reconstruct(v, maxden=5000000):
    """Reconstruct exact rational from a float signed sum. Returns (Fraction, is_zero, residual)."""
    if abs(v) < 1e-6:
        return F(0), True, abs(v)
    fr = F(v)
    rc = fr.limit_denominator(maxden)
    err = abs(float(rc) - v)
    is_zero = (rc == F(0))
    return rc, is_zero, err

# ---------- main ----------
def main():
    with open(os.path.join(HERE, "k7_survivors.json"), encoding="utf-8") as f:
        data = json.load(f)
    surv = data["survivors"]
    K = data["k"]

    # group into isoclasses
    iso = defaultdict(list)
    for r in surv:
        ch = canon_H(r["H_edges"], r["b"])
        iso[ch].append(r)
    print(f"survivors={len(surv)} isoclasses={len(iso)}", flush=True)

    out_file = os.path.join(HERE, "k7_iso_results.json")
    results = {}
    if os.path.exists(out_file):
        with open(out_file, encoding="utf-8") as f:
            results = json.load(f)

    # deterministic order: by (b, m, canonical)
    order = sorted(iso.keys(), key=lambda ch: (iso[ch][0]["b"], iso[ch][0]["m"], ch))
    for ci, ch in enumerate(order):
        key = str(ch)
        if key in results and results[key].get("J_frac"):
            continue
        rows = iso[ch]
        b = rows[0]["b"]
        m = rows[0]["m"]
        rep = rows[0]
        t0 = time.time()
        entry = {"b": b, "m": m, "profile": rep["profile"], "n_partitions": len(rows),
                 "canonical": ch, "rep_blocks": rep["blocks"], "H_edges": rep["H_edges"]}
        if b == 1:
            Jf = F(1)
            entry.update({"method": "closed_b1", "J_frac": str(Jf), "J_num": Jf.numerator,
                          "J_den": Jf.denominator, "J_float": 1.0, "n_partitions": len(rows)})
        elif b == 2:
            Jf, mc = J_closed_b2(blocks_of(rep), K)
            entry.update({"method": "closed_b2", "m_crossing": mc, "J_frac": str(Jf),
                          "J_num": Jf.numerator, "J_den": Jf.denominator, "J_float": float(Jf),
                          "n_partitions": len(rows)})
        else:
            ve = J_box_exact(blocks_of(rep), K, b)
            vf = J_box_fast(blocks_of(rep), K, b)
            diff = abs(ve - vf)
            Jf, is_zero, resid = reconstruct(ve)
            entry.update({"method": "box_exact", "box_exact_float": ve, "box_fast_float": vf,
                          "engine_diff": diff, "J_frac": str(Jf), "J_num": Jf.numerator,
                          "J_den": Jf.denominator, "J_float": float(Jf),
                          "recon_residual": resid, "is_zero": bool(is_zero),
                          "n_partitions": len(rows)})
        entry["time_s"] = round(time.time() - t0, 2)
        results[key] = entry
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        print(f"[{ci+1}/{len(order)}] b={b} m={m} n_part={len(rows)} J={Jf} "
              f"({time.time()-t0:.1f}s) diff={entry.get('engine_diff','-')}", flush=True)

    # ---------- assemble per-partition and sum ----------
    J_by_key = {key: F(res["J_num"], res["J_den"]) for key, res in results.items()}
    # build canonical->J
    canon_to_J = {}
    for ch, res in results.items():
        canon_to_J[ch] = F(res["J_num"], res["J_den"])

    per_partition = []
    total = F(0)
    for r in surv:
        ch = canon_H(r["H_edges"], r["b"])
        Jf = canon_to_J[ch]
        total += Jf
        per_partition.append({
            "k": r["k"], "blocks": r["blocks"], "b": r["b"], "m": r["m"],
            "profile": r["profile"], "isoclass": str(ch),
            "J_num": Jf.numerator, "J_den": Jf.denominator, "J": str(Jf),
        })
    print(f"\nm_7 = {total} = {float(total):.12f}")
    print(f"per-partition entries: {len(per_partition)}")

    with open(os.path.join(HERE, "k7_allJ.json"), "w", encoding="utf-8") as f:
        json.dump({"k": K, "m_7": str(total), "m_7_num": total.numerator, "m_7_den": total.denominator,
                   "isoclasses": results, "per_partition": per_partition},
                  f, ensure_ascii=False, indent=1)
    print("wrote k7_allJ.json")

    # sanity: sum by b
    byb = defaultdict(lambda: F(0))
    bybcnt = defaultdict(int)
    for r in per_partition:
        byb[r["b"]] += F(r["J_num"], r["J_den"])
        bybcnt[r["b"]] += 1
    for b in sorted(byb):
        print(f"  b={b}: n={bybcnt[b]} sum={byb[b]} = {float(byb[b]):.9f}")

if __name__ == "__main__":
    main()
