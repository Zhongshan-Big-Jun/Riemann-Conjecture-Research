"""The preceding 67.313763% construction, retained as a reproduction gate."""

from __future__ import annotations

from flint import arb, fmpq

from .design import KERNEL
from .verify_general import CertificateSpec


WEIGHT_DENOMINATOR = 1_000_000
WEIGHT_NUMERATORS = {
    (0, 1): 239_252,
    (0, 2): 528_172,
    (0, 3): 965_879,
    (0, 4): 1_000_000,
    (0, 5): 1_000_000,
    (0, 6): 2_000_000,
    (1, 2): 381_335,
    (1, 3): 465_776,
    (1, 4): 34_121,
    (1, 5): 0,
    (1, 6): 1_000_000,
    (2, 3): 379_413,
    (2, 4): 12_104,
    (2, 5): 34_121,
    (2, 6): 1_000_000,
    (3, 4): 379_413,
    (3, 5): 465_776,
    (3, 6): 965_879,
    (4, 5): 381_335,
    (4, 6): 528_172,
    (5, 6): 239_252,
}

PRESSURE = fmpq(1, 2300)
TARGET = fmpq(1, 200)
BLOCK_LENGTH = 257
H_CERT = fmpq(672_457, 1_000_000)
FINAL_BOUND_RATIONAL = fmpq(420_711, 625_000)


def certificate_spec(grid: int = 4000) -> CertificateSpec:
    weights = {
        pair: fmpq(numerator, WEIGHT_DENOMINATOR)
        for pair, numerator in WEIGHT_NUMERATORS.items()
        if numerator
    }
    return CertificateSpec(
        kernel=KERNEL,
        q=6,
        pressure=PRESSURE,
        target=TARGET,
        weights=weights,
        grid=grid,
    )


def final_bound() -> tuple[arb, arb, arb, arb]:
    m = BLOCK_LENGTH
    a_value = arb(TARGET) * (m - 6)
    r_value = 2 * a_value.sqrt() - 1
    eta = r_value / a_value
    bound = (
        m * arb(H_CERT) - eta * 6 * arb(PRESSURE) * (m - 1)
    ) / (m - r_value)
    return bound, a_value, r_value, eta
