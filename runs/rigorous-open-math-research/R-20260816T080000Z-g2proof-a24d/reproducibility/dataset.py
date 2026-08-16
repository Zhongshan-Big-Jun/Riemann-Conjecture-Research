#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dataset.py — assemble the exact per-partition J_sigma dataset for k=3..6 and the
cycle-edge multigraph H_sigma for each partition.

Partitions of {0,...,k-1}: standard (restricted growth / block canonical) enumeration.
J_sigma for k=6 comes from the m6exact run CSVs (b=3,4,5,6) plus the analytic b=2 reduction
J = c_m - c_{m+2} (m = #cycle block-crossings), b=1 -> 1. This module is data-only; rule
testing lives in graph_rule.py.
"""
from fractions import Fraction
from math import comb, factorial
from collections import defaultdict
import csv, io, re

# ---------------- c-values exactly ----------------
def c_2n(n):
    m = 2*n
    s = 0
    for k in range(n):
        s += (-1)**k * comb(m,k) * (n-k)**(m-1)
    return Fraction(s, factorial(m-1))

C = {2: c_2n(1), 4: c_2n(2), 6: c_2n(3), 8: c_2n(4),
     10: c_2n(5), 12: c_2n(6)}

# ---------------- partition enumeration ----------------
def partitions_of(n):
    """All b.c. set-partitions of {0..n-1}. Blocks as frozensets."""
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
            yield from rec(i+1, b2)
        yield from rec(i+1, blocks + [frozenset([i])])
    return list(rec(1, [frozenset([0])]))

BlockKey = tuple  # frozenset of element labels is itself the canonical form

def block_of(blocks, el):
    for i, b in enumerate(blocks):
        if el in b:
            return i
    raise KeyError(el)

def cycle_multigraph(k, blocks):
    """Return H_sigma: counter (u,v) with u<v for each cycle edge crossing blocks.
    Self-loops (on-block cycle edges) dropped (they contribute K(0)=1)."""
    idx = [block_of(blocks, a) for a in range(k)]
    H = defaultdict(int)
    for a in range(k):
        bl, br = idx[a], idx[(a+1) % k]
        if bl != br:
            u, v = (bl, br) if bl < br else (br, bl)
            H[(u, v)] += 1
    return dict(H)

def crossing_count(k, blocks):
    idx = [block_of(blocks, a) for a in range(k)]
    return sum(1 for a in range(k) if idx[a] != idx[(a+1) % k])

def profile(blocks):
    return tuple(sorted((len(b) for b in blocks), reverse=True))

# ---------------- load k=6 exact per-partition J from CSVs ----------------
_parse_blocks = re.compile(r"\d+")

def _blocks_from_str(s):
    # string like [[0, 1, 2, 3], [4], [5]]  (canonical blocks given in m6 data)
    # Robust parse: strip outer list brackets, split on '], ['-style boundaries.
    s = s.strip()
    if s.startswith("[[") and s.endswith("]]"):
        s = s[1:-1]  # drop outermost [ ]
    # now s = "[0, 1, 2, 3], [4], [5]"
    blocks = []
    for grp in re.findall(r"\[([^\]]*)\]", s):
        items = [int(t.strip()) for t in grp.split(",") if t.strip()]
        blocks.append(frozenset(items))
    return tuple(blocks)

def _parse_fraction(s):
    s = s.strip()
    if s.startswith("np.float64"):
        s = re.sub(r"np\.float64\(([^)]*)\)", r"\1", s)
    return Fraction(s)

def load_m6():
    """Return dict mapping canonical block-tuple -> Fraction J, for k=6."""
    base = __file__ and None
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    data = {}

    # b=3 from clean table (idx blocks profile J)
    with open(os.path.join(here, "b3_clean_table.tsv"), encoding="utf-8") as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("idx\tblocks"):
                continue
            parts = ln.split("\t")
            if len(parts) < 4:
                continue
            blocks = _blocks_from_str(parts[1])
            J = _parse_fraction(parts[3])
            data[blocks] = J
    # b=4,5,6 from CSVs
    for fn in ["b4_fast_c0.csv","b4_fast_c1.csv","b4_fast_c2.csv","b4_fast_c3.csv","b4_fast_c4.csv",
               "b5_fast.csv","b6_fast.csv"]:
        with open(os.path.join(here,fn), encoding="utf-8") as f:
            rd = csv.DictReader(f)
            for row in rd:
                blocks = _blocks_from_str(row["blocks"])
                data[blocks] = _parse_fraction(row["J_recon"])

    k6 = partitions_of(6)
    # b=1 and b=2 are not in the CSVs; fill analytically:
    #   b=1 -> J=1 ;  b=2 -> J = c_m - c_{m+2}, m = #cycle block-crossings
    for blocks in k6:
        if blocks in data:
            continue
        b = len(blocks)
        if b == 1:
            data[blocks] = Fraction(1, 1)
        elif b == 2:
            m = crossing_count(6, blocks)
            data[blocks] = C[m] - C[m + 2]
        else:
            raise RuntimeError(f"k=6 blocks b={b} missing from both CSV and analytic: {blocks}")
    # sanity: every k=6 partition should have an entry
    missing = [b for b in k6 if b not in data]
    if missing:
        raise RuntimeError(f"{len(missing)} k=6 blocks missing, e.g. {missing[0]}")
    return data

def load_all():
    """Return dict: k -> {(canonical blocks): Fraction J}. k=2 b=2 analytic; k=6 from CSVs.
    k=3,4,5: exact per-partition structure filled from known runs where available; else None."""
    from fractions import Fraction as F
    out = {}

    # ---- k=3 (Bell=5): derive exactly from the boxespline engine is heavy here; we instead
    # note the reduced structure. For the vanishing-rule checker we still need J per partition.
    # k=3 partitions:
    #   (3) all-equal: J=1 (unit)
    # blocks of size 2+1 and 1+1+1: need exact values. Compute directly via the c-reduction
    # for b=2 and via an exact box-spline evaluation for b=3.  We defer exact I_pi computation
    # to exact_volumes.py which reproduces the D3/D4/D5 box-spline machinery and integrates.
    # ---- placeholder: computed in exact_volumes.py and merged back.
    out["k6"] = load_m6()
    return out
