"""The certified design: window, weights, and deduction constants.

Every constant here is an exact rational. The design was found by numerical
optimization (see docs/provenance.md) but plays no role in the proof: the
proof is (i) the interval certificates over these exact rationals, and
(ii) the exact deduction of Section 5 of the paper.
"""

from __future__ import annotations

from flint import arb, fmpq

from .kernel import KernelSpec
from .verify_general import CertificateSpec

# Window v(s) = sum_j c_j cos(omega_j s), omega = (sqrt2, 2pi, ..., 12pi).
WINDOW_DENOMINATOR = 10**9
WINDOW_NUMERATORS = (
    1_000_000_000,
    3_322_500,
    -7_609_135,
    1_190_194,
    -731_476,
    -1_680_572,
    1_141_360,
)

KERNEL = KernelSpec(
    coeffs=tuple(fmpq(n, WINDOW_DENOMINATOR) for n in WINDOW_NUMERATORS),
    omega_pi_multiples=(2, 4, 6, 8, 10, 12),
)

# Reflection-symmetric pair weights a_{ij} / 10^6 for the 7-point window
# (0 <= i < j <= 6).  Every span capacity sum_i a_{i,i+r} equals 2 exactly.
WEIGHT_DENOMINATOR = 10**6
WEIGHT_NUMERATORS = {
    (0, 1): 236_484,
    (0, 2): 535_224,
    (0, 3): 969_656,
    (0, 4): 1_000_000,
    (0, 5): 1_000_000,
    (0, 6): 2_000_000,
    (1, 2): 381_281,
    (1, 3): 464_776,
    (1, 4): 30_344,
    (1, 5): 0,
    (1, 6): 1_000_000,
    (2, 3): 382_235,
    (2, 4): 0,
    (2, 5): 30_344,
    (2, 6): 1_000_000,
    (3, 4): 382_235,
    (3, 5): 464_776,
    (3, 6): 969_656,
    (4, 5): 381_281,
    (4, 6): 535_224,
    (5, 6): 236_484,
}

PRESSURE = fmpq(1, 2736)
TARGET = fmpq(891, 200_000)

# Deduction constants.
BLOCK_LENGTH = 272
H_CERT = fmpq(3_362_285_207, 5_000_000_000)
WINDOW_MIN = fmpq(3, 4)
FINAL_BOUND_RATIONAL = fmpq(1683, 2500)

# Prior records.
AINTA_BOUND = "0.673008527927..."
ANTHROPIC_H0 = "0.672500703679..."
PREVIOUS_BOUND = "0.673137630699..."


def certificate_spec(
    grid: int = 4000, use_tangent: bool = True
) -> CertificateSpec:
    """The main finite inequality F >= 891/200000."""

    weights = {
        key: fmpq(value, WEIGHT_DENOMINATOR)
        for key, value in WEIGHT_NUMERATORS.items()
        if value
    }
    return CertificateSpec(
        kernel=KERNEL,
        q=6,
        pressure=PRESSURE,
        target=TARGET,
        weights=weights,
        grid=grid,
        use_tangent=use_tangent,
    )


def final_bound() -> tuple[arb, arb, arb, arb]:
    """Return Arb enclosures of ``(bound, A, R, eta)``."""

    m = BLOCK_LENGTH
    a_value = arb(TARGET) * (m - 6)
    r_value = 2 * a_value.sqrt() - 1
    eta = r_value / a_value
    b_pressure = 6 * arb(PRESSURE)
    bound = (
        m * arb(H_CERT) - eta * b_pressure * (m - 1)
    ) / (m - r_value)
    return bound, a_value, r_value, eta


# Refined deduction (Phi_m envelope + window-in-frame counting; see
# docs/refined-deduction.md — attribution: tawanerguo-cn/zeta-simple-zeros).
REFINED_BLOCK_LENGTH = 235
REFINED_BOUND_RATIONAL = fmpq(6_732_425_893, 10**10)


def refined_final_bound() -> tuple[arb, arb, arb]:
    """Arb enclosures of ``(bound, A, Phi_m(A))`` for the refined assembly."""

    m = REFINED_BLOCK_LENGTH
    q = 6
    a_value = arb(TARGET) * (m - q)
    inner = arb(fmpq(m - 1, m)) * a_value
    phi = 2 * inner.sqrt() - 1 + a_value / m
    bound = (m * arb(H_CERT) - (m - q) * q * arb(PRESSURE)) / (m - phi)
    return bound, a_value, phi
