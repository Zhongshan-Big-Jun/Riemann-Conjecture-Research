#!/usr/bin/env python3
"""Independent re-verification of our canonical k=9 F8>=392/100000 certificate
using the upstream trmdy generalized verifier (MT kernel, uniform weights).
"""
import time
from flint import fmpq
from zeta_ext.kernel import MT_SPEC
from zeta_ext.verify_general import CertificateSpec, uniform_weights, verify_general
from zeta_ext.parallel import verify_parallel

SPEC = CertificateSpec(
    kernel=MT_SPEC,
    q=8,
    pressure=fmpq(1, 4000),
    target=fmpq(392, 100000),
    weights=uniform_weights(8),
    grid=2000,
    precision=128,
    use_tangent=True,
)

if __name__ == "__main__":
    print("verifying canonical k=9 F8 >= 392/100000 with upstream verifier")
    print(f"capacity_ok={SPEC.capacity_ok()}")
    start = time.time()
    report = verify_parallel(SPEC, workers=4)
    print("\n".join(report.lines()))
    print(f"wall_seconds={time.time()-start:.1f}")
