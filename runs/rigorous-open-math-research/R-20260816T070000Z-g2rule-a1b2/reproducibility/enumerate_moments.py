#!/usr/bin/env python
"""Enumerate set partitions of {0..k-1}, compute each shape integral J_sigma exactly, and
sum to m_k = sum_sigma J_sigma.  Anchor on m_2=4/3, m_3=2, m_4=13/4 before trusting m_5.

Formula (derived in whiteboard):
  m_k = (1/N) E[tr G^k] = sum_{sigma in Part(k)} J_sigma,  (limit N->inf, density 1)
  J_sigma = int_{R^{b-1}} [prod_{a} K(x_{sigma(a)}-x_{sigma(a+1)})] * rho_b dx,
  b = #blocks, x_b pinned (translation), rho_b = det[K(x_i-x_j)]_{i,j=1..b}.
"""
import os, sys, itertools, time, json
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxspline_exact import shape_integral_exact


def partitions_of(n):
    def rec(i, blocks):
        if i == n:
            yield tuple(frozenset(b) for b in blocks)
            return
        seen = set()
        for j, bb in enumerate(blocks):
            key = frozenset(bb)
            if key in seen:
                continue
            seen.add(key)
            b2 = [x for x in blocks]
            b2[j] = bb | {i}
            yield from rec(i + 1, b2)
        yield from rec(i + 1, blocks + [frozenset([i])])
    return list(rec(1, [frozenset([0])]))


def blocksizes(blocks):
    return sorted(len(b) for b in blocks)


def run(k):
    allparts = partitions_of(k)
    total = F(0)
    per_b = {}
    detail = []
    t0 = time.time()
    for blocks in allparts:
        J = shape_integral_exact(list(blocks), k)
        total += J
        b = len(blocks)
        per_b.setdefault(b, F(0))
        per_b[b] += J
        detail.append({"blocks": sorted(sorted(x) for x in blocks), "b": b,
                       "sizes": blocksizes(blocks), "J": str(J)})
    dt = time.time() - t0
    return total, per_b, detail, dt


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    results = {}
    for k in range(2, kmax + 1):
        total, per_b, detail, dt = run(k)
        results[k] = {"m_k": str(total), "float": float(total),
                      "per_b": {str(b): str(v) for b, v in per_b.items()},
                      "num_partitions": len(detail), "wall_s": round(dt, 3)}
        print(f"k={k}: m_k = {total} = {float(total):.10f}  (wall {dt:.1f}s)")
        print(f"      per #blocks: " + ", ".join(f"b={b}:{v}" for b, v in sorted(per_b.items())))
    want = {2: F(4, 3), 3: F(2), 4: F(13, 4)}
    for k, expected in want.items():
        got = F(results[k]["m_k"])
        print(f"CHECK k={k}: got {got} expected {expected} -> {'PASS' if got == expected else 'FAIL'}")
