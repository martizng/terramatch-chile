"""End-to-end run (owner: Rojas). Writes results/{mars,moon}_profile.csv, {mars,moon}_montecarlo.csv,
sites_summary.csv and validation.json (project doc v2.0, section 10.5).

  python src/run_pipeline.py            # uses data/processed/grid.csv, master.csv and data/targets.json

A profile whose values are still pending verification is skipped and reported as such.
A profile whose filter layer is missing is NOT ranked (status "pending_filter_data"): the filter is never
switched off. Complementary filters (config "sensitivity_filters") are run as sensitivity analyses only.
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


def web_table(grid, master, prof, mc):
    """One row per cell for the web page: id, coordinates, variables, distances, scores, coverage,
    stability, confidence, status and rank among scored cells (1 = most similar)."""
    from config import VARS
    cols = ["cell_id", "lat_c", "lon_c"]
    t = grid[cols].merge(master[["cell_id"] + [v for v in VARS if v in master] +
                                [c for c in ("valid_frac", "precip_mm_yr", "volcanic_unit") if c in master]],
                         on="cell_id", how="left").merge(prof, on="cell_id", how="left").merge(mc, on="cell_id", how="left")
    t["confidence"] = [cp.confidence(n, p) if st == "scored" else None
                       for n, p, st in zip(t.n_vars, t.p_top, t.status)]
    sc = t.status == "scored"
    t["rank"] = np.nan
    t.loc[sc, "rank"] = t.loc[sc, "S"].rank(ascending=False, method="min")
    return t


def run(grid, master, targets, out="results", iterations=None, sites_dir=None):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    master = grid[["cell_id"]].merge(master, on="cell_id", how="left")
    scale_report = {}
    scales = an.robust_scales(master, scale_report)
    summaries, report = [], {"run_at": datetime.now().isoformat(timespec="seconds"),
                             "config_version": CFG["version"], "rule": CFG["validation"]["rule"],
                             "scales": scale_report,
                             "excluded_variables": [v for v in CFG["variables"] if v not in scales]}
    for tid, t in targets.items():
        body = t["body"]
        try:
            an.target_ranges(t)
        except an.TargetPending as e:
            report[body] = {"status": "pending_targets", "detail": str(e)}
            continue
        try:
            prof = an.profile(master, t, scales)
        except an.FilterDataMissing as e:
            report[body] = {"status": "pending_filter_data", "detail": str(e)}
            continue
        mc = cp.monte_carlo(master, t, scales, iterations)
        prof.to_csv(out / f"{body}_profile.csv", index=False)
        mc.to_csv(out / f"{body}_montecarlo.csv", index=False)
        web_table(grid, master, prof, mc).to_csv(out / f"{body}_scores_web.csv", index=False)
        sdf = cp.site_summaries(grid, master, prof, mc, tid, True, sites_dir)
        summaries.append(sdf)
        r = {"status": "computed", "filter": t["filter"]["label"] if t.get("filter") else None,
             "counts": prof.status.value_counts().to_dict()}
        r.update(vl.validate_mars(prof, master, sdf) if body == "mars" else vl.validate_moon(sdf))
        sens = {}
        for f in CFG.get("sensitivity_filters", {}).get(body, []):
            t2 = {**t, "filter": f}
            try:
                p2 = an.profile(master, t2, scales)
            except an.FilterDataMissing as e:
                sens[f["id"]] = {"status": "pending_filter_data", "detail": str(e)}
                continue
            m2 = cp.monte_carlo(master, t2, scales, iterations)
            s2 = cp.site_summaries(grid, master, p2, m2, tid, True, sites_dir)
            p2.to_csv(out / f"{body}_profile_{f['id']}.csv", index=False)
            v2 = vl.validate_mars(p2, master, s2) if body == "mars" else vl.validate_moon(s2)
            sens[f["id"]] = {"status": "computed", "label": f["label"], "counts": p2.status.value_counts().to_dict(),
                             "checks": v2["checks"], "role": "sensitivity only, not the main result"}
        if sens:
            r["sensitivity"] = sens
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
    ap.add_argument("--sites-dir", default=CFG["paths"]["sites_dir"])
    ap.add_argument("--out", default="results")
    ap.add_argument("--iterations", type=int, default=None)
    a = ap.parse_args()
    rep = run(pd.read_csv(a.grid), pd.read_csv(a.master), an.load_targets(a.targets), a.out, a.iterations, a.sites_dir)
    print(json.dumps(rep, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
