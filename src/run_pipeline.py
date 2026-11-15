"""End-to-end run (owner: Rojas). Writes results/{mars,moon}_profile.csv, {mars,moon}_montecarlo.csv,
sites_summary.csv and validation.json (project doc v2.0, section 10.5).

  python src/run_pipeline.py            # uses data/processed/grid.csv, master.csv and data/targets.json

A profile whose values are still pending verification is skipped and reported as such.
AI-Assisted: Claude (draft of this script; reviewed and run by the team).
"""
import argparse, json, sys
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CFG
import analysis as an
import comparison as cp
import validation as vl


def run(grid, master, targets, out="results", iterations=None, sites_dir="data/chile/sites"):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    if grid.cell_id.duplicated().any() or master.cell_id.duplicated().any():
        raise ValueError("Duplicate cell_id in grid or master")
    master = grid[["cell_id"]].merge(master, on="cell_id", how="left", validate="one_to_one")
    scales = an.robust_scales(master)
    if len(scales) < 2:
        raise ValueError("At least two informative topographic variables are required")
    summaries, report = [], {"run_at": datetime.now().isoformat(timespec="seconds"),
                             "config_version": CFG["version"], "rule": CFG["validation"]["rule"]}
    for tid, t in targets.items():
        body = t["body"]
        try:
            an.target_ranges(t)
        except an.TargetPending as e:
            report[body] = {"status": "pending_targets", "detail": str(e)}
            continue
        f = t.get("filter")
        if f and (f["column"] not in master or master[f["column"]].isna().all()):
            report[body] = {"status": "missing_filter_data", "detail":
                            f"Required filter '{f['column']}' unavailable; no ranking was computed"}
            continue
        national = True
        prof = an.profile(master, t, scales)
        mc = cp.monte_carlo(master, t, scales, iterations)
        prof.to_csv(out / f"{body}_profile.csv", index=False)
        mc.to_csv(out / f"{body}_montecarlo.csv", index=False)
        sdf = cp.site_summaries(grid, master, prof, mc, tid, national, sites_dir)
        summaries.append(sdf)
        r = {"status": "computed", "mode": "national" if national else "sites_only",
             "n_scored": int((prof.status == "scored").sum()),
             "n_outside_filter": int((prof.status == "outside_filter").sum()),
             "n_insufficient_data": int((prof.status == "insufficient_data").sum())}
        r.update(vl.validate_mars(prof, master, sdf) if body == "mars" else vl.validate_moon(sdf))
        report[body] = r
    if summaries:
        pd.concat(summaries).to_csv(out / "sites_summary.csv", index=False)
    (out / "validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", default="data/processed/grid.csv")
    ap.add_argument("--master", default="data/processed/master.csv")
    ap.add_argument("--targets", default="data/targets.json")
    ap.add_argument("--sites-dir", default="data/chile/sites")
    ap.add_argument("--out", default="results")
    ap.add_argument("--iterations", type=int, default=None)
    a = ap.parse_args()
    rep = run(pd.read_csv(a.grid), pd.read_csv(a.master), an.load_targets(a.targets), a.out, a.iterations, a.sites_dir)
    print(json.dumps(rep, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
