"""Command-line entry points for the certificates.

  zeta-673200-verify gate   -- reproduce the ainta 7-point certificate
                               (correctness gate for this verifier)
  zeta-673200-verify fast   -- window bounds, H(v), and exact deduction
  zeta-673200-verify main   -- prove F >= 891/200000 (parallel)
  zeta-673200-verify all    -- fast + main
  zeta-673200-verify legacy-main -- reproduce the preceding 67.313763% design
"""

from __future__ import annotations

import argparse
import sys
import time

from flint import arb, ctx, fmpq

from . import design, legacy_design
from .h0_cert import (
    window_functional,
    window_min_enclosure,
    window_monotone_factor_upper,
)
from .kernel import MT_SPEC
from .parallel import verify_parallel
from .verify_general import CertificateSpec, uniform_weights, verify_general


def run_gate(args: argparse.Namespace) -> int:
    spec = CertificateSpec(
        kernel=MT_SPEC,
        q=6,
        pressure=fmpq(1, 3000),
        target=fmpq(19, 5000),
        weights=uniform_weights(6),
        grid=4000,
    )
    if args.workers > 1:
        report = verify_parallel(spec, workers=args.workers)
    else:
        report = verify_general(spec, progress_every=200_000)
    print("\n".join(report.lines()))
    print("expected_nodes=707797 (matches ainta's committed run up to table "
          "tightness; their run records 707901)")
    return 0 if report.verified else 1


def run_fast(_: argparse.Namespace) -> int:
    ctx.prec = 256
    ok = True

    low = window_min_enclosure(design.KERNEL, subdivisions=8192)
    good = bool(low >= arb(design.WINDOW_MIN))
    ok &= good
    print(f"min v >= {low.str(15)}  [>= 3/4: {good}]")

    # max v <= 1 via the same subdivision on the reflected bound.
    from .h0_cert import _omegas  # noqa: PLC2701

    omegas = _omegas(design.KERNEL)
    coeffs = [arb(c) for c in design.KERNEL.coeffs]
    hi = None
    n = 8192
    for i in range(n):
        cell = arb(fmpq(2 * i + 1, 4 * n), fmpq(1, 4 * n))
        value = arb(0)
        for c, om in zip(coeffs, omegas):
            value += c * (om * cell).cos()
        upper = value.upper()
        hi = upper if hi is None or upper > hi else hi
    good = bool(arb(hi) <= arb(1))
    ok &= good
    print(f"max v <= {arb(hi).str(15)}  [<= 1: {good}]")

    derivative_factor = window_monotone_factor_upper(
        design.KERNEL, subdivisions=8192
    )
    good = bool(derivative_factor <= 0)
    ok &= good
    print(
        f"max v'(s)/s <= {derivative_factor.str(15)}  "
        f"[monotone: {good}]"
    )

    c_val, h_val = window_functional(design.KERNEL)
    good = bool(h_val >= arb(design.H_CERT))
    ok &= good
    print(f"c1(v) = {c_val.str(20)}")
    print(f"H(v)  = {h_val.str(20)}  [>= {design.H_CERT}: {good}]")

    bound, a_val, r_val, eta = design.final_bound()
    good = bool(bound >= arb(design.FINAL_BOUND_RATIONAL))
    ok &= good
    print(
        f"m = {design.BLOCK_LENGTH}  A = {a_val.str(12)}  "
        f"R = {r_val.str(20)}  eta = {eta.str(18)}"
    )
    print(f"final bound = {bound.str(22)}  "
          f"[>= {design.FINAL_BOUND_RATIONAL}: {good}]")
    print(f"fast_parts_verified={ok}")
    return 0 if ok else 1


def run_main(args: argparse.Namespace) -> int:
    spec = design.certificate_spec(grid=args.grid)
    started = time.time()
    if args.workers > 1:
        report = verify_parallel(spec, workers=args.workers)
    else:
        report = verify_general(spec, progress_every=200_000)
    print("\n".join(report.lines()))
    print(f"wall_seconds={time.time() - started:.1f}")
    return 0 if report.verified else 1


def run_legacy_fast(_: argparse.Namespace) -> int:
    ctx.prec = 256
    bound, a_value, r_value, eta = legacy_design.final_bound()
    good = bool(bound >= arb(legacy_design.FINAL_BOUND_RATIONAL))
    print(f"m={legacy_design.BLOCK_LENGTH}")
    print(f"A={a_value.str(40)}")
    print(f"R={r_value.str(40)}")
    print(f"eta={eta.str(40)}")
    print(f"final bound={bound.str(50)}")
    print(
        f"rational bound={legacy_design.FINAL_BOUND_RATIONAL} "
        f"[verified: {good}]"
    )
    return 0 if good else 1


def run_legacy_main(args: argparse.Namespace) -> int:
    spec = legacy_design.certificate_spec(grid=args.grid)
    report = (
        verify_parallel(spec, workers=args.workers)
        if args.workers > 1
        else verify_general(spec, progress_every=200_000)
    )
    print("\n".join(report.lines()))
    return 0 if report.verified else 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="zeta-673200-verify")
    parser.add_argument(
        "command",
        choices=[
            "gate",
            "fast",
            "main",
            "all",
            "legacy-fast",
            "legacy-main",
        ],
    )
    parser.add_argument("--grid", type=int, default=4000)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if args.command == "gate":
        return run_gate(args)
    if args.command == "fast":
        return run_fast(args)
    if args.command == "main":
        return run_main(args)
    if args.command == "legacy-fast":
        return run_legacy_fast(args)
    if args.command == "legacy-main":
        return run_legacy_main(args)
    status = run_fast(args)
    return status or run_main(args)


if __name__ == "__main__":
    sys.exit(main())
