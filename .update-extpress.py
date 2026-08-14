import io, json
p = r"F:\LaTeX\Riemann Conjecture"
path = p + r"\index\runs.json"
with io.open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)
for it in data["items"]:
    if it["run_id"] == "R-20260814T045000Z-extpress-2f36ae":
        it["upstream_status_verbatim"] = "RIGOROUS_PARTIAL_RESULT"
        it["summary"] = "NEW UNCONDITIONAL RECORD: liminf N0^s(T,2T)/N(T,2T) >= C_9 = (6875*H_MT - 1315/96)/6849 = 0.673053645952589925209110000745... (improves C_7 = 0.6730085279 by 4.51e-5). New k=9 pressure certificate F_8 >= 39/10000 (8-variable exhaustive Arb branch-and-bound, grid 4000, 53,137,290 nodes, kernel hash 7029ac0f...). General-k chain derived symbolically (reproduces k=7 exactly); block-energy/block-defect (m_9=264, A_0=624/625<1)/pinching verified; manager independently verified all final arithmetic. Honest caveats: f_9=0.00395 attempt uncertified within budget; true min ~0.00398 numerical only; k=11 infeasible; class limit 0.673126 formal only; N0/N->1 remains OPEN."
        it["audit_status"] = "PENDING (independent audit agent 907ba7d9 running; first attempt 278cfecf crashed without artifacts)"
        it["key_artifacts"] = [
            "candidate_proof.md 43214E4B95567EFC... (NEW RECORD C9 = 0.6730536459...)",
            "candidate_proof.general-k-derivation.md 9930B309CD6CE8D0...",
            "repro_manifest.md EADC6C319FA180C6...",
            "reproducibility/verify_kpoint_parallel.py 4B028360...",
            "reproducibility/certificates/nine-point-f8-gt-39over10000.txt D8FB68246BB90BEC...",
            "reproducibility/certificates/nine-point-f8-gt-19over5000-grid2000.txt 27D67F76F1CFC489...",
            "audit_report.md D0E1E115CD401D36... (solver self-audit; independent audit pending)"
        ]
        it["updated_at"] = "2026-08-14T17:20:00Z"
with io.open(path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
print("updated")
