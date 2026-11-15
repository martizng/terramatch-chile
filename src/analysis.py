"""Analysis (owner: Rojas): distance, per-variable similarity, global similarity and coverage.
Rules come from config/terramatch_config.json (project doc v2.0, section 8, Fase 3).

  d_i = max(low_i - x_i, 0, x_i - high_i) / IQR_i        IQR over all Chilean cells
  s_i = 100 exp(-d_i)                                     per-variable similarity
  D   = sum(w_i m_i d_i) / sum(w_i m_i),  S = 100 exp(-D) global similarity
  coverage = sum(w_i m_i) / sum(w_i); below coverage_min -> "insufficient_data"
  cells failing the profile filter -> "outside_filter" (never ranked)
  cells without data for the filter -> "no_filter_data" (never ranked, never read as low similarity)
  scale: IQR; if IQR = 0, standard deviation; if both are 0 the variable is EXCLUDED (no artificial scale)

AI-Assisted: Claude (draft of this module; logic reviewed and tested by the team).
"""
import json
import numpy as np
import pandas as pd
from config import CFG, VARS


class TargetPending(Exception):
    """A planetary profile still has variables without a verified value."""


class FilterDataMissing(Exception):
    """The layer needed by a profile filter is not available; the profile is not ranked."""


def _tf(x, var):
    return np.log1p(np.clip(x, 0, None)) if CFG["variables"][var]["transform"] == "log1p" else x


def load_targets(path):
    raw = json.loads(open(path, encoding="utf-8").read())
    raw = raw["targets"] if isinstance(raw, dict) and "targets" in raw else raw
    return {t["id"]: t for t in raw}


def pending_variables(target):
    """Variables of a profile that still lack value/range or source."""
    out = []
    for v in VARS:
        spec = target.get("variables", {}).get(v, {})
        if spec.get("low") is None or spec.get("high") is None or not spec.get("source") \
                or spec.get("status") == "pending_verification":
            out.append(v)
    return out


def target_ranges(target):
    pend = pending_variables(target)
    if pend:
        raise TargetPending(f"{target['id']}: pending verification for {pend}")
    return {v: (float(_tf(target["variables"][v]["low"], v)), float(_tf(target["variables"][v]["high"], v)))
            for v in VARS}


def filter_state(master, f):
    """Per cell: 1 = passes, 0 = fails, NaN = no data for the filter column.
    Raises FilterDataMissing if the column is absent or empty (the filter is never switched off)."""
    if not f:
        return pd.Series(1.0, index=master.index)
    col = master.get(f["column"])
    if col is None or col.isna().all():
        raise FilterDataMissing(f"no data for filter column '{f['column']}' ({f.get('label', '')})")
    col = col.astype(float)
    if f["type"] == "max":
        ok = col <= f["max"]
    elif f["type"] == "flag":
        ok = col == 1
    else:
        raise ValueError(f"unknown filter type {f['type']}")
    return ok.astype(float).where(col.notna())


def apply_filter(master, target):
    """Boolean: True only where the filter is passed with data."""
    return (filter_state(master, target.get("filter")) == 1).fillna(False)


def robust_scales(master, report=None):
    """IQR per variable over all Chilean cells; SD if IQR = 0; excluded if both are 0 (doc v2.0, Fase 3)."""
    sc = {}
    for v in VARS:
        if v not in master:
            if report is not None: report[v] = "excluded: column absent"
            continue
        x = _tf(master[v].astype(float), v).dropna()
        if len(x) < 10:
            if report is not None: report[v] = f"excluded: only {len(x)} cells with data"
            continue
        iqr = float(x.quantile(0.75) - x.quantile(0.25)); sd = float(x.std())
        if iqr > 0:
            sc[v] = iqr
            if report is not None: report[v] = f"IQR = {iqr:.6g}"
        elif sd > 0:
            sc[v] = sd
            if report is not None: report[v] = f"IQR = 0, SD used = {sd:.6g}"
        elif report is not None:
            report[v] = "excluded: IQR = 0 and SD = 0"
    return sc


def distances(master, target, scales):
    """Per-variable normalised distance to the profile range (NaN stays NaN)."""
    rng = target_ranges(target)
    out = {}
    for v in VARS:
        if v in master and v in scales:
            lo, hi = rng[v]
            x = _tf(master[v].astype(float), v).to_numpy()
            out[v] = np.maximum.reduce([lo - x, np.zeros_like(x), x - hi]) / scales[v]
        else:
            out[v] = np.full(len(master), np.nan)
    return out


def profile(master, target, scales=None):
    """One row per cell: d_*, s_*, n_vars, coverage, D, S, passes_filter, status."""
    scales = robust_scales(master) if scales is None else scales
    d = distances(master, target, scales)
    w = {v: CFG["variables"][v]["weight"] for v in VARS}
    fstate = filter_state(master, target.get("filter")).to_numpy()
    passes = fstate == 1
    res = pd.DataFrame({"cell_id": master["cell_id"].values, "passes_filter": passes})
    num = np.zeros(len(res)); den = np.zeros(len(res)); n_av = np.zeros(len(res), int)
    for v in VARS:
        res[f"d_{v}"] = d[v]
        res[f"s_{v}"] = 100 * np.exp(-d[v])
        ok = ~np.isnan(d[v])
        num += np.where(ok, w[v] * np.nan_to_num(d[v]), 0); den += np.where(ok, w[v], 0); n_av += ok
    res["n_vars"] = n_av
    res["coverage"] = den / sum(w.values())
    enough = res["coverage"].to_numpy() >= CFG["coverage_min"] - 1e-9
    with np.errstate(invalid="ignore", divide="ignore"):
        D = np.where(enough & passes, num / np.where(den > 0, den, 1), np.nan)
    res["D"] = D
    res["S"] = 100 * np.exp(-D)
    res["status"] = np.select([np.isnan(fstate), fstate == 0, ~enough],
                              ["no_filter_data", "outside_filter", "insufficient_data"], "scored")
    return res


def percentile_of(value, scored_values):
    """Percentile (0-100, 100 = most similar) of a value among scored cells."""
    s = np.asarray(scored_values, float); s = s[~np.isnan(s)]
    if value is None or np.isnan(value) or s.size == 0:
        return np.nan
    return float(100.0 * (s < value).mean() + 50.0 * (s == value).mean())
