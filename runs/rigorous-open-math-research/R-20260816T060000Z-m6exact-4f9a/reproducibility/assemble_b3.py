#!/usr/bin/env python
"""Assemble the exact m_6^{b<=3} from the loaded batch results and print the full k=6 coefficient
structure (per block-size profile), then the exact m_6^(b<=3) and the b=1/b=2 contributions.
Also dumps per-partition J into a clean table for the candidate_proof."""
import csv, glob, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enumerate_moments import partitions_of

def load_b3():
    d = {}
    for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "b3_batch*.csv")):
        with open(f) as fh:
            for r in csv.DictReader(fh):
                idx = int(r["idx"]); recon = r["J_recon"].strip()
                d[idx] = F(0) if recon == "0" else F(recon)
    return d

def main():
    b3 = load_b3()
    print(f"b=3 rows loaded: {len(b3)}/90")
    # map idx -> profile (index in filtered b=3 list)
    parts3 = [list(bl) for bl in partitions_of(6) if len(bl) == 3]
    assert len(parts3) == 90
    from collections import defaultdict
    byprof = defaultdict(lambda: [0, F(0)])
    valbyprof = defaultdict(defaultdict)  # prof -> {value: count}
    tot = F(0)
    for idx in sorted(b3, key=int):
        bl = parts3[idx]
        prof = tuple(sorted(len(x) for x in bl))
        J = b3[idx]
        byprof[prof][0] += 1
        byprof[prof][1] += J
        key = J
        if J not in valbyprof[prof]:
            valbyprof[prof][J] = 0
        valbyprof[prof][J] += 1
        tot += J
    print("=== b=3 per-profile sums ===")
    for prof in sorted(byprof):
        cnt, s = byprof[prof]
        print(f"  profile {prof}: n={cnt} sum={s} = {float(s):+.8f}")
    print(f"m_6^(b=3) = {tot} = {float(tot):.12f}")
    print("=== b=3 per-profile distinct values (value -> count) ===")
    for prof in sorted(valbyprof):
        print(f"  profile {prof}: " + ", ".join(f"{v} x{c}" for v, c in sorted(valbyprof[prof].items(), key=lambda kv: float(kv[0]))))
    b1 = F(1)
    b2 = F(4297, 630)
    m6 = b1 + b2 + tot
    print(f"\nm_6^(b<=3) = b1({b1}) + b2({b2}) + b3({tot}) = {m6} = {float(m6):.12f}")
    # dump clean per-partition table for artifact
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "b3_clean_table.tsv"), "w") as fh:
        fh.write("idx\tblocks\tprofile\tJ\n")
        for idx in sorted(b3, key=int):
            bl = parts3[idx]
            fh.write(f"{idx}\t{sorted(sorted(x) for x in bl)}\t{tuple(sorted(len(x) for x in bl))}\t{b3[idx]}\n")
    return m6

if __name__ == "__main__":
    m = main()
    print(f"\nFINAL m_6^(b<=3) = {m}")
