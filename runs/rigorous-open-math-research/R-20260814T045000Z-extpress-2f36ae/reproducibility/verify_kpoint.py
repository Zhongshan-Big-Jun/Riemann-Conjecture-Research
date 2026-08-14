"""Generalized k-point pressure certificate: certify F_{k-1}(g) >= f_k.

F_{k-1}(g_1..g_{k-1}) = 1/(500*(k-1)) * sum_i g_i
   + sum_{s=1}^{k-1} (2/(k-s)) * sum_{i=1}^{k-s} w(g_i+...+g_{i+s-1})

for all g_i >= 0, where w(x)=k(x)^2 is the normalized Montgomery-Taylor
overlap kernel.  Reuses the repo's Arb kernel/rounding/report infrastructure
(k-1 = d variables).  Generalizes verify_seven.py to arbitrary k.

Usage:
    python verify_kpoint.py k NUM/DEN [--grid G] [--precision B] [--cutoff-cells N]
                            [--progress-every N] [--target-scalar X]
Output:          a VerificationReport in the repo's text format, printed to stdout.

Grid/precision choices MUST be justified in the paper trail.  The reported
bool/nodes/splits/hashes are deterministic.

NOTE: the target certificate value f_k is chosen by the caller (typically the
numerical minimum); a too-high target FAILS loudly (terminal unresolved cell),
which is the correct behavior -- no silent partial certificate.
"""
from __future__ import annotations

import argparse
import itertools
import math
import time
from typing import List, Optional, Sequence, Tuple

from flint import arb, fmpq
import sys, os
# make the repo package importable if run from the run tree
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    *(['..']*5),
    'literature', 'raw', 'zeta-simple-zeros', 'src'))

from zeta_simple_zeros.kernel import (
    RangeMinimum,
    build_kernel_table,
    build_second_derivative_lower_table,
    kernel_constants,
    squared_kernel_derivatives,
    table_sha256,
)
from zeta_simple_zeros.report import VerificationReport
from zeta_simple_zeros.rounding import down_add, down_mul, down_ratio, up_ratio


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('k', type=int, help='points per block (>=3)')
    ap.add_argument('target', help='target fraction, e.g. 19/5000')
    ap.add_argument('--grid', type=int, default=4000)
    ap.add_argument('--precision', type=int, default=128)
    ap.add_argument('--progress-every', type=int, default=0)
    ap.add_argument('--tail-start-frac', type=float, default=0.95,
                    help='fraction of grid where w\'\' table starts (>=0.95)')
    args = ap.parse_args()

    k = args.k
    assert k >= 3, "k must be >= 3"
    d = k - 1                       # number of variables (gaps)
    P_DEN = 500 * d                 # pressure denominator
    if '/' in args.target:
        tn, td = args.target.split('/')
        TARGET_N, TARGET_D = int(tn), int(td)
    else:
        raise ValueError("target must be NUM/DEN")
    TARGET = TARGET_N / TARGET_D
    GRID = args.grid
    PRECISION_BITS = args.precision

    # Pressure cutoff: linear term alone proves target once sum(g) >= target*P_DEN.
    cutoff_cells = int(math.floor(TARGET * P_DEN * GRID)) + 8
    # second-derivative table used for convex tangent bounds (w'' stable away
    # from the removable pole), start at 95% of grid.
    SECOND_START = int(args.tail_start_frac * (cutoff_cells))

    # c_r = 2/(k-r) for span r=1..d (rational, and binary64 down/up bounds)
    COEFF = {r: math.nextafter(2.0/(k-r), -math.inf) for r in range(1, d+1)}
    COEFF_UP = {r: math.nextafter(2.0/(k-r), math.inf) for r in range(1, d+1)}
    COEFF_RAT = {r: fmpq(2, k-r) for r in range(1, d+1)}
    ONE_BODY = {r: down_ratio(2, k-r) for r in range(1, d+1)}  # = 2/(k-1) only used for span 1

    started = time.perf_counter()
    table = build_kernel_table(GRID, cutoff_cells, PRECISION_BITS)
    ranges = RangeMinimum(table)
    second_table = build_second_derivative_lower_table(GRID, cutoff_cells,
                                                       start_index=SECOND_START,
                                                       precision=PRECISION_BITS)
    second_ranges = RangeMinimum(second_table)
    constants = kernel_constants()
    target_upper = up_ratio(TARGET_N, TARGET_D)

    def kernel_min(left: int, right: int) -> float:
        if right >= ranges.length:
            return 0.0
        return ranges.query(left, right)

    def second_derivative_min(left: int, right: int) -> float:
        if right >= second_ranges.length:
            return float("-inf")
        return second_ranges.query(left, right)

    # One-body pruning: U(g) = g/(500d) + (2/(k-1)) w(g)  (its own single-gap term).
    # A cell surviving the k-d box product must have U below target.
    surviving: List[int] = []
    for index in range(int(cutoff_cells)):
        one_body = down_ratio(index, GRID * P_DEN)                     # g/(500d)
        one_body = down_add(one_body, down_mul(ONE_BODY[1], table[index]))
        if one_body < target_upper:
            surviving.append(index)
    components: List[Tuple[int, int]] = []
    for index in surviving:
        if not components or index > components[-1][1] + 1:
            components.append([index, index])
        else:
            components[-1][1] = index
    components = [(c[0], c[1]) for c in components]

    stack = [(tuple(parts), 0) for parts in itertools.product(components, repeat=d)]
    initial_boxes = len(stack)
    nodes = pruned = splits = max_depth = 0
    pressure_pruned = interval_pruned = tangent_pruned = 0

    CellRange = Tuple[int, int]
    Box = Tuple[CellRange, ...]

    def box_lower(box: Box) -> float:
        lows = [p[0] for p in box]; highs = [p[1] for p in box]
        low_prefix = [0]; high_prefix = [0]
        for lo, hi in zip(lows, highs):
            low_prefix.append(low_prefix[-1] + lo)
            high_prefix.append(high_prefix[-1] + hi)
        result = down_ratio(low_prefix[-1], GRID * P_DEN)
        for span in range(1, d+1):
            coeff = COEFF[span]
            for start in range(d - span + 1):
                left = low_prefix[start+span] - low_prefix[start]
                right = high_prefix[start+span] - high_prefix[start] + span - 1
                result = down_add(result, down_mul(coeff, kernel_min(left, right)))
        return result

    def coeff_times_signed_lower(span: int, lower: float) -> float:
        if lower == float("-inf"):
            return lower
        coeff = COEFF[span] if lower >= 0.0 else COEFF_UP[span]
        return math.nextafter(coeff * lower, -math.inf)

    def float_ldl_is_positive(matrix: List[List[float]]) -> bool:
        n = d
        lower = [[0.0]*n for _ in range(n)]
        diag = [0.0]*n
        for col in range(n):
            pivot = matrix[col][col]
            for prev in range(col):
                pivot -= lower[col][prev]*lower[col][prev]*diag[prev]
            if pivot <= 1e-12:
                return False
            diag[col] = pivot
            lower[col][col] = 1.0
            for row in range(col+1, n):
                value = matrix[row][col]
                for prev in range(col):
                    value -= lower[row][prev]*lower[col][prev]*diag[prev]
                lower[row][col] = value/pivot
        return True

    def arb_ldl_is_positive(terms: Sequence[Tuple[int,int,float]]) -> bool:
        n = d
        matrix = [[arb(0) for _ in range(n)] for _ in range(n)]
        for start, span, coefficient in terms:
            exact = _exact_float(coefficient)
            for row in range(start, start+span):
                for col in range(start, start+span):
                    matrix[row][col] += exact
        lower = [[arb(0) for _ in range(n)] for _ in range(n)]
        diag = [arb(0) for _ in range(n)]
        for col in range(n):
            lower[col][col] = arb(1)
            pivot = matrix[col][col]
            for prev in range(col):
                pivot -= lower[col][prev]*lower[col][prev]*diag[prev]
            if not (pivot > 0):
                return False
            diag[col] = pivot
            for row in range(col+1, n):
                value = matrix[row][col]
                for prev in range(col):
                    value -= lower[row][prev]*lower[col][prev]*diag[prev]
                lower[row][col] = value/pivot
        return True

    def _exact_float(value: float) -> arb:
        num, den = value.as_integer_ratio()
        return arb(fmpq(num, den))

    def convex_tangent_lower(box: Box) -> Optional[arb]:
        lows = [p[0] for p in box]; highs = [p[1] for p in box]
        low_prefix = [0]; high_prefix = [0]
        for lo, hi in zip(lows, highs):
            low_prefix.append(low_prefix[-1]+lo)
            high_prefix.append(high_prefix[-1]+hi)
        terms: List[Tuple[int,int,float]] = []
        heuristic = [[0.0]*d for _ in range(d)]
        for span in range(1, d+1):
            for start in range(d-span+1):
                left = low_prefix[start+span]-low_prefix[start]
                right = high_prefix[start+span]-high_prefix[start]+span-1
                second_lower = second_derivative_min(left, right)
                scalar = coeff_times_signed_lower(span, second_lower)
                if scalar == float("-inf"):
                    return None
                terms.append((start, span, scalar))
                for row in range(start, start+span):
                    for col in range(start, start+span):
                        heuristic[row][col] += scalar
        if not float_ldl_is_positive(heuristic):
            return None
        if not arb_ldl_is_positive(terms):
            return None
        midpoints = [fmpq(lo+hi+1, 2*GRID) for lo, hi in box]
        radii = [fmpq(hi-lo+1, 2*GRID) for lo, hi in box]
        value = sum((arb(p) for p in midpoints), arb(0)) / P_DEN
        gradient = [arb(fmpq(1, P_DEN)) for _ in range(d)]
        for span in range(1, d+1):
            coeff = arb(COEFF_RAT[span])
            for start in range(d-span+1):
                point = sum(midpoints[start:start+span], fmpq(0))
                pot, der, _ = squared_kernel_derivatives(arb(point), constants)
                value += coeff*pot
                for coord in range(start, start+span):
                    gradient[coord] += coeff*der
        lower = value
        for der, radius in zip(gradient, radii):
            lower -= der.abs_upper() * arb(radius)
        return lower

    while stack:
        box, depth = stack.pop()
        nodes += 1
        max_depth = max(max_depth, depth)
        if sum(p[0] for p in box) >= cutoff_cells:
            pruned += 1; pressure_pruned += 1
            continue
        lower = box_lower(box)
        if lower >= target_upper:
            pruned += 1; interval_pruned += 1
            continue
        tangent_lower = convex_tangent_lower(box)
        if tangent_lower is not None and tangent_lower >= arb(fmpq(TARGET_N, TARGET_D)):
            pruned += 1; tangent_pruned += 1
            continue
        widths = [r-l for l, r in box]
        if max(widths) == 0:
            print(f"kpoint certificate FAILED at terminal cell box={box} lower={lower.hex()}")
            sys.exit(2)
        splits += 1
        coord = max(range(d), key=widths.__getitem__)
        L, R = box[coord]
        mid = (L+R)//2
        lo_half = list(box); hi_half = list(box)
        lo_half[coord] = (L, mid); hi_half[coord] = (mid+1, R)
        stack.append((tuple(lo_half), depth+1))
        stack.append((tuple(hi_half), depth+1))
        if args.progress_every and nodes % args.progress_every == 0:
            print(f"kpoint k={k}: nodes={nodes} pending={len(stack)} depth={max_depth}")

    elapsed = time.perf_counter() - started
    component_text = ";".join(f"[{a},{b}]" for a, b in components)
    rep = VerificationReport(
        certificate=f"{k}-point",
        verified=True,
        target=f"F{d} >= {TARGET_N}/{TARGET_D}",
        grid=GRID,
        precision_bits=PRECISION_BITS,
        kernel_table_sha256=table_sha256(table),
        nodes=nodes,
        pruned=pruned,
        splits=splits,
        maximum_depth=max_depth,
        initial_boxes=initial_boxes,
        elapsed_seconds=elapsed,
        details={
            "k": k,
            "pressure_pruned": pressure_pruned,
            "interval_pruned": interval_pruned,
            "tangent_pruned": tangent_pruned,
            "second_derivative_table_sha256": table_sha256(second_table),
            "surviving_gap_components_cells": component_text,
            "surviving_gap_components_count": len(components),
        },
    )
    print(rep.to_text())


if __name__ == '__main__':
    main()
