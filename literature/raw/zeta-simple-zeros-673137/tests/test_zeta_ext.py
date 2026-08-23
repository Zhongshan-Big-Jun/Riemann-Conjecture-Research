"""Self-contained tests: kernel enclosures, design consistency, deduction."""

import math
import unittest

from flint import arb, ctx, fmpq

from zeta_ext import design, legacy_design
from zeta_ext.h0_cert import window_functional, window_min_enclosure
from zeta_ext.kernel import (
    MT_SPEC,
    KernelSpec,
    build_w_lower_table,
    build_w_second_lower_table,
    kernel_derivatives,
    kernel_k0,
    sinc_derivatives,
)
from zeta_ext.verify_general import CertificateSpec, uniform_weights


class SincTests(unittest.TestCase):
    def test_exact_zero(self):
        value, first, second = sinc_derivatives(arb(0))
        self.assertEqual(value, arb(1))
        self.assertEqual(first, arb(0))
        self.assertTrue(second.overlaps(-arb(1) / 3))

    def test_series_matches_closed_form(self):
        ctx.prec = 128
        for z0 in [0.05, 0.3, 0.6, 0.74, 0.76, 0.9, 1.5, 3.0]:
            z = arb(z0)
            v_closed = z.sin() / z
            d1_closed = (z * z.cos() - z.sin()) / (z * z)
            d2_closed = ((2 - z * z) * z.sin() - 2 * z * z.cos()) / (z * z * z)
            for mine, closed in zip(sinc_derivatives(z),
                                    (v_closed, d1_closed, d2_closed)):
                self.assertTrue(mine.overlaps(closed), z0)

    def test_series_at_zero_ball(self):
        ctx.prec = 128
        v, d1, d2 = sinc_derivatives(arb(0, 1e-3))
        self.assertTrue(v.contains(arb(1)))
        self.assertTrue(d1.contains(arb(0)))
        self.assertTrue(d2.contains(arb(-1) / 3))


class MontgomeryTaylorTests(unittest.TestCase):
    def test_k0_closed_form(self):
        ctx.prec = 128
        expected = arb(2).sqrt() * (1 / arb(2).sqrt()).sin()
        self.assertTrue(kernel_k0(MT_SPEC).overlaps(expected))

    def test_h_functional_reproduces_montgomery_taylor(self):
        ctx.prec = 192
        c_val, h_val = window_functional(MT_SPEC)
        c_closed = 2 * math.tan(1 / math.sqrt(2)) / (
            math.sqrt(2) + math.tan(1 / math.sqrt(2))
        )
        h_closed = 1.5 - (1 / math.sqrt(2)) / math.tan(1 / math.sqrt(2))
        self.assertLess(abs(float(c_val.mid()) - c_closed), 1e-14)
        self.assertLess(abs(float(h_val.mid()) - h_closed), 1e-14)

    def test_min_window_is_cos_inv_sqrt2(self):
        ctx.prec = 128
        low = window_min_enclosure(MT_SPEC, subdivisions=512)
        self.assertLess(abs(float(low) - math.cos(1 / math.sqrt(2))), 1e-3)


class DesignTests(unittest.TestCase):
    def test_span_capacities_are_exactly_two(self):
        for r in range(1, 7):
            total = fmpq(0)
            for i in range(0, 7 - r):
                total += fmpq(
                    design.WEIGHT_NUMERATORS[(i, i + r)],
                    design.WEIGHT_DENOMINATOR,
                )
            self.assertEqual(total, fmpq(2), r)

    def test_weights_reflection_symmetric(self):
        for (i, j), value in design.WEIGHT_NUMERATORS.items():
            self.assertEqual(value, design.WEIGHT_NUMERATORS[(6 - j, 6 - i)])

    def test_certificate_spec_capacity_ok(self):
        self.assertTrue(design.certificate_spec().capacity_ok())

    def test_window_tables_finite_at_integer_singularities(self):
        # The design kernel has sinc arguments vanishing at integer x.
        grid = 200
        table = build_w_lower_table(grid, 3 * grid, design.KERNEL)
        second = build_w_second_lower_table(grid, 3 * grid, design.KERNEL)
        self.assertTrue(all(v >= 0.0 for v in table))
        self.assertTrue(all(math.isfinite(v) for v in second))

    def test_design_h_value(self):
        ctx.prec = 192
        _, h_val = window_functional(design.KERNEL)
        self.assertTrue(h_val >= arb(design.H_CERT))
        self.assertLess(abs(float(h_val.mid()) - 0.6724570414145443), 1e-12)


class DeductionTests(unittest.TestCase):
    def test_final_bound_arithmetic(self):
        ctx.prec = 192
        m = design.BLOCK_LENGTH
        eps = arb(design.TARGET)
        p = arb(design.PRESSURE)
        h_low = arb(design.H_CERT)
        a_val = eps * (m - 6)
        r_val = 2 * a_val.sqrt() - 1
        eta = r_val / a_val
        bound = (m * h_low - eta * 6 * p * (m - 1)) / (m - r_val)
        self.assertTrue(bound >= arb(design.FINAL_BOUND_RATIONAL))
        self.assertLess(abs(float(bound.mid()) - 0.6732001170127619), 1e-14)

    def test_preceding_record_arithmetic(self):
        ctx.prec = 192
        bound, _, _, _ = legacy_design.final_bound()
        self.assertTrue(bound >= arb(legacy_design.FINAL_BOUND_RATIONAL))
        self.assertLess(abs(float(bound.mid()) - 0.6731376306993446), 1e-14)

    def test_reduces_to_ainta_formula_with_unit_cap(self):
        # eta = 1, R = A < 1 reproduces ainta's (4.7) exactly.
        ctx.prec = 192
        h0 = arb(3) / 2 - (1 / arb(2).sqrt()) / (1 / arb(2).sqrt()).tan()
        m = 269
        eps = arb(fmpq(19, 5000))
        p = arb(fmpq(1, 3000))
        a_val = eps * (m - 6)
        assert a_val < 1
        bound = (m * h0 - 6 * p * (m - 1)) / (m - a_val)
        expected = (1_345_000 * h0 - 2_680) / 1_340_003
        self.assertTrue(bound.overlaps(expected))


class GateSmokeTests(unittest.TestCase):
    def test_uniform_weights_capacity(self):
        spec = CertificateSpec(
            kernel=MT_SPEC,
            q=6,
            pressure=fmpq(1, 3000),
            target=fmpq(19, 5000),
            weights=uniform_weights(6),
            grid=400,
        )
        self.assertTrue(spec.capacity_ok())



class RefinedDeductionTests(unittest.TestCase):
    def test_refined_bound_arithmetic(self):
        ctx.prec = 256
        bound, a_value, phi = design.refined_final_bound()
        self.assertTrue(a_value >= arb(fmpq(design.REFINED_BLOCK_LENGTH,
                                            design.REFINED_BLOCK_LENGTH - 1)))
        self.assertTrue(phi <= a_value)
        self.assertTrue(bound >= arb(design.REFINED_BOUND_RATIONAL))
        self.assertLess(
            abs(float(bound.mid()) - 0.6732425893558967), 1e-15
        )

    def test_refined_m_scan_optimum(self):
        ctx.prec = 192
        q = 6

        def bound_at(m):
            a_value = arb(design.TARGET) * (m - q)
            inner = arb(fmpq(m - 1, m)) * a_value
            phi = 2 * inner.sqrt() - 1 + a_value / m
            return (m * arb(design.H_CERT)
                    - (m - q) * q * arb(design.PRESSURE)) / (m - phi)

        best = design.REFINED_BLOCK_LENGTH
        for m in range(best - 3, best + 4):
            if m != best:
                self.assertTrue(bound_at(m) <= bound_at(best), m)


if __name__ == "__main__":
    unittest.main(verbosity=2)
