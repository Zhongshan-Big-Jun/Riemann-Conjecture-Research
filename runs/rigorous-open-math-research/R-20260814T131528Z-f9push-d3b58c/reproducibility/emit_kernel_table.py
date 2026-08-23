#!/usr/bin/env python3
"""Emit the k-point pressure verifier kernel table as exact rationals.

The existing `build_kernel_table` returns rigorous binary64 lower bounds for
min k^2 on each grid cell.  Converting each binary64 to an exact Fraction
preserves that value exactly.  This is data for the T2 reflection route: a
later Lean checker can treat these fractions as the exact rational table and
verify the interval/rounding proof separately.

Output: JSON list of [numerator, denominator] pairs, plus metadata/hash.
"""
from __future__ import annotations

import argparse, hashlib, json, os, sys, time
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
    *(['..']*5), 'literature', 'raw', 'zeta-simple-zeros', 'src'))

from zeta_simple_zeros.kernel import build_kernel_table, table_sha256

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--grid', type=int, default=2000)
    ap.add_argument('--cutoff', type=int, default=None)
    ap.add_argument('--precision', type=int, default=128)
    ap.add_argument('--out', type=str, required=True)
    args = ap.parse_args()

    # Default cutoff matches the verified k=9 f=392/100000 certificate:
    # cutoff = floor((392/100000) * (500*8) * grid) + 8
    if args.cutoff is None:
        args.cutoff = int((392 / 100000) * (500 * 8) * args.grid) + 8

    start = time.perf_counter()
    table = build_kernel_table(args.grid, args.cutoff, args.precision)
    elapsed = time.perf_counter() - start

    entries = []
    digest = hashlib.sha256()
    for v in table:
        f = Fraction(v)
        # JSON only has finite precision for numbers; emit exact numerator/denominator.
        entries.append([f.numerator, f.denominator])
        digest.update(str(f.numerator).encode() + b'/' + str(f.denominator).encode() + b'\n')

    data = {
        "format": "kernel-table-exact-rational-v1",
        "grid": args.grid,
        "cutoff": args.cutoff,
        "precision_bits": args.precision,
        "entry_count": len(entries),
        "entries": entries,
        "binary64_sha256": table_sha256(table),
        "rational_sha256": digest.hexdigest(),
        "build_seconds": elapsed,
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or '.', exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))
    print(f"wrote {args.out}: {len(entries)} entries, {round(elapsed,3)}s")
    print(f"binary64 sha256 {data['binary64_sha256']}")
    print(f"rational sha256 {data['rational_sha256']}")

if __name__ == '__main__':
    main()
