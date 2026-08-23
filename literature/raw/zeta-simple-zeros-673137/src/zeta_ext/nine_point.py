"""The certified nine-point (q=8) record candidate; see docs/nine-point.md.

Same window as design.KERNEL. Certificate: certificates/nine-point-final-grid4000.txt (F >= 15211/2500000,
cross-host split, 116,272,426 nodes, verified; the earlier 60817/10^7
certificate is retained in certificates/nine-point-p2500-grid4000.txt).
Assembly uses the refined deduction (docs/refined-deduction.md) at m = 177.
"""

from __future__ import annotations

from flint import arb, fmpq

from .design import H_CERT, KERNEL
from .verify_general import CertificateSpec

WEIGHT_DENOMINATOR = 10_000_000
WEIGHT_NUMERATORS = {
    (0, 1): 1_802_576,
    (0, 2): 4_832_031,
    (0, 3): 5_411_933,
    (0, 4): 10_000_000,
    (0, 5): 10_000_000,
    (0, 6): 10_000_000,
    (0, 7): 10_000_000,
    (0, 8): 20_000_000,
    (1, 2): 2_694_869,
    (1, 3): 2_295_599,
    (1, 4): 1_780_844,
    (1, 5): 0,
    (1, 6): 0,
    (1, 7): 0,
    (1, 8): 10_000_000,
    (2, 3): 2_714_860,
    (2, 4): 0,
    (2, 5): 2_807_223,
    (2, 6): 0,
    (2, 7): 0,
    (2, 8): 10_000_000,
    (3, 4): 2_787_695,
    (3, 5): 5_744_740,
    (3, 6): 2_807_223,
    (3, 7): 0,
    (3, 8): 10_000_000,
    (4, 5): 2_787_695,
    (4, 6): 0,
    (4, 7): 1_780_844,
    (4, 8): 10_000_000,
    (5, 6): 2_714_860,
    (5, 7): 2_295_599,
    (5, 8): 5_411_933,
    (6, 7): 2_694_869,
    (6, 8): 4_832_031,
    (7, 8): 1_802_576,
}

PRESSURE = fmpq(1, 2500)
TARGET = fmpq(15_211, 2_500_000)
BLOCK_LENGTH = 177
Q = 8
FINAL_BOUND_RATIONAL = fmpq(6_733_127_422, 10**10)


def certificate_spec(grid: int = 4000, use_tangent: bool = True) -> CertificateSpec:
    weights = {
        key: fmpq(value, WEIGHT_DENOMINATOR)
        for key, value in WEIGHT_NUMERATORS.items()
        if value
    }
    return CertificateSpec(
        kernel=KERNEL, q=Q, pressure=PRESSURE, target=TARGET,
        weights=weights, grid=grid, use_tangent=use_tangent,
    )


def final_bound() -> tuple[arb, arb, arb]:
    """Arb enclosures of (bound, A, Phi_m(A)) under the refined deduction."""

    m = BLOCK_LENGTH
    a_value = arb(TARGET) * (m - Q)
    phi = 2 * (arb(fmpq(m - 1, m)) * a_value).sqrt() - 1 + a_value / m
    bound = (m * arb(H_CERT) - (m - Q) * Q * arb(PRESSURE)) / (m - phi)
    return bound, a_value, phi
