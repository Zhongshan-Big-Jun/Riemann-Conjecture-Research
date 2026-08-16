#!/usr/bin/env python
"""Batched exact shape-integrals for k=6 using the exact-volume box-spline engine.
Usage:
    py batch_exact6.py <start_idx> <end_idx> <b> <outcsv> [<k>]
Computes shape_integral_exact2 for partitions of k (default 6) with exactly b blocks whose
index (in partitions_of(k) filtering by b) lies in [start_idx, end_idx). Writes progress to
stdout (flush) and appends a CSV row per partition.
"""
import sys, os, time, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from enumerate_moments import partitions_of, blocksizes
from shape_exact2 import shape_integral_exact2, reconstruct

def main():
    start = int(sys.argv[1]); end = int(sys.argv[2]); b = int(sys.argv[3])
    outcsv = sys.argv[4]
    k = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    parts = [list(bl) for bl in partitions_of(k) if len(bl) == b]
    sel = parts[start:end]
    hdr = not os.path.exists(outcsv)
    f = open(outcsv, 'a', newline='')
    w = csv.writer(f)
    if hdr:
        w.writerow(["idx","blocks","b","sizes","J_float","J_recon","wall_s","count_perm"])
    for i, bl in enumerate(sel):
        t0 = time.time()
        val = shape_integral_exact2(bl, k)
        try:
            fr = reconstruct(val)
            tag = "ok"
        except ValueError as e:
            fr, tag = F(0), f"noise:{e}"
        wall = time.time() - t0
        if fr == 0 and abs(val) > 1e-4:
            tag = tag + "|zero-nonzero-check"
        w.writerow([start+i, repr(sorted(sorted(x) for x in bl)), b,
                    repr(sorted(len(x) for x in bl)), repr(val), str(fr),
                    round(wall,2), tag])
        f.flush()
        print(f"[{start+i}] b={b} blocks={[sorted(sorted(x) for x in bl)]} J={val:+.9f} recon={fr} tag={tag} wall={wall:.1f}s", flush=True)
    f.close()
    print(f"DONE batch [{start},{end}) b={b}: {len(sel)} partitions in {time.time() - t0:.0f}s", flush=True)

main()
