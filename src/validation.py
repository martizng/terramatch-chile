"""Validation (owner: Rojas): checks of project doc v2.0, Fase 5. Reports the real outcome;
results are never changed to match expectations.

AI-Assisted: Claude (draft of this module; logic reviewed and tested by the team).
"""
import numpy as np
from config import CFG
import analysis as an

VAL = CFG["validation"]


def _auc(pos, neg):
    p = np.asarray(pos, float); q = np.asarray(neg, float)
    p = p[~np.isnan(p)]; q = q[~np.isnan(q)]
    if not len(p) or not len(q):
        return None
    return float(((p[:, None] > q[None, :]).sum() + 0.5 * (p[:, None] == q[None, :]).sum()) / (len(p) * len(q)))


def _check(value, ok):
    return {"value": None if value is None or np.isnan(value) else round(float(value), 2),
            "passed": None if value is None or np.isnan(value) else bool(ok)}


def validate_mars(prof, master, sites_df):
    s = sites_df.set_index("site")
    scored = prof.loc[prof.status == "scored", "S"].values
    out = {}
    for k in VAL["mars_benchmarks"]:
        p = s.loc[k, "percentile"] if k in s.index else np.nan
        out[f"{k}_percentile>={VAL['benchmark_min_percentile']}"] = _check(p, p >= VAL["benchmark_min_percentile"])
    for k in VAL["mars_controls"]:
        p = s.loc[k, "percentile"] if k in s.index else np.nan
        out[f"{k}_percentile<={VAL['control_max_percentile']}"] = _check(p, p <= VAL["control_max_percentile"])
    el = prof[prof.status == "scored"].merge(master[["cell_id", "slope_p90_deg"]], on="cell_id")
    p = np.nan
    if len(el) >= 20:
        steep = el[el.slope_p90_deg >= el.slope_p90_deg.quantile(1 - VAL["steep_top_fraction"])]
        p = float(np.median([an.percentile_of(x, scored) for x in steep.S]))
    out[f"steep_top5_median_percentile<={VAL['control_max_percentile']}"] = _check(p, p <= VAL["control_max_percentile"])
    pos = [s.loc[k, "S"] for k in VAL["mars_benchmarks"] if k in s.index]
    neg = [s.loc[k, "S"] for k in VAL["mars_controls"] if k in s.index]
    return {"checks": out, "auc_secondary": _auc(pos, neg)}


def validate_moon(sites_df):
    s = sites_df.set_index("site")
    a = s.loc[VAL["moon_pair"]["higher"], "S"] if VAL["moon_pair"]["higher"] in s.index else np.nan
    b = s.loc[VAL["moon_pair"]["lower"], "S"] if VAL["moon_pair"]["lower"] in s.index else np.nan
    diff = a - b
    return {"checks": {"llaima_flows_S>llaima_cone_S": {
        "value": None if np.isnan(diff) else round(float(diff), 2),
        "passed": None if np.isnan(diff) else bool(diff > 0)}}}
