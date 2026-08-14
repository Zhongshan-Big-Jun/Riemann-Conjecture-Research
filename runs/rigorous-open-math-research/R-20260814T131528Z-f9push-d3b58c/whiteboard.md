# Whiteboard — f9push-d3b58c

- **Run ID:** R-20260814T131528Z-f9push-d3b58c
- **Task packet ID:** Q-20260814-criticalline-p1-507bb5

## Current plan

Certify f₉ = 0.00395 (F₈ ≥ 395/100000) and release the new records:
C₉(ζ) = 0.6730855621335040490732…, C₉(ξ′) = 0.8692247262341557806822…
(one window-determined kernel serves both families).

## Route history

- 22-worker spawn stall; 8-worker restart (grid-2000 and grid-4000, 128-bit) [SUCCEEDED]
- Verifier patched with --out atomic write (job-system stdout loss workaround) [SUCCEEDED]
- 0.00395 runs launched 2026-08-14T23:13Z (pwsh-1 grid-4000, pwsh-2 grid-2000), still running [PARTIAL]
- Final constants verified via exact rational forms (mpmath 70 digits) [SUCCEEDED]
- whiteboard + release-checklist + candidate_proof.draft prepared [SUCCEEDED]

## Ideas to return to

- 0.00396 run only if 0.00395 closes comfortably (cost gradient 5–10×).
- Fallback ladder 0.00394 / 0.00393 if 0.00395 times out.

## Open obligations

- Collect certificates (per-job ETA measured 2026-08-15 00:34 +08: each job ~19.0k core-s
  in 80.6 min wall, ~0.49 CPU-s/wall-s per worker: grid-2000 ~16h remaining, grid-4000
  ~44h; grid-2000 expected to land first — sufficient for release); run release-checklist.md.
- Independent audit of the 0.00395 certificate + record theorem (manager-level pattern).
- Update FRONTIER / index; validate_pipeline clean; git commit + push.

## Key artifacts

- reproducibility/verify_kpoint_parallel.py, release-checklist.md, candidate_proof.draft.md
- reproducibility/certificates/ (pending: nine-point-f8-gt-395over100000-grid{2000,4000}.txt)
