"""Consistency and exact-arithmetic tests for the 67.3200% design."""

import unittest

from flint import arb, ctx, fmpq

from zeta_ext import design
from zeta_ext.h0_cert import window_functional, window_monotone_factor_upper


class RecordDesignTests(unittest.TestCase):
    def test_span_capacities_are_exactly_two(self):
        for span in range(1, 7):
            total = sum(
                (
                    fmpq(
                        design.WEIGHT_NUMERATORS[(start, start + span)],
                        design.WEIGHT_DENOMINATOR,
                    )
                    for start in range(7 - span)
                ),
                fmpq(0),
            )
            self.assertEqual(total, fmpq(2), span)

    def test_weights_are_reflection_symmetric(self):
        for (left, right), numerator in design.WEIGHT_NUMERATORS.items():
            self.assertEqual(
                numerator,
                design.WEIGHT_NUMERATORS[(6 - right, 6 - left)],
            )

    def test_certificate_spec_capacity_ok(self):
        self.assertTrue(design.certificate_spec().capacity_ok())

    def test_window_is_certifiably_monotone(self):
        ctx.prec = 192
        upper = window_monotone_factor_upper(design.KERNEL, subdivisions=8192)
        self.assertTrue(upper <= 0)

    def test_tightened_window_functional_bound(self):
        ctx.prec = 256
        _, h_value = window_functional(design.KERNEL)
        self.assertTrue(h_value >= arb(design.H_CERT))


class RecordDeductionTests(unittest.TestCase):
    def test_final_bound_arithmetic(self):
        ctx.prec = 256
        bound, a_value, r_value, eta = design.final_bound()
        self.assertTrue(a_value > 1)
        self.assertTrue(r_value < a_value)
        self.assertTrue(eta < 1)
        self.assertTrue(bound >= arb(design.FINAL_BOUND_RATIONAL))
        self.assertLess(
            abs(float(bound.mid()) - 0.67320011701276185682),
            1e-15,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
