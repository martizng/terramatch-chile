"""Comparison (owner: Rojas): ranking stability (Monte Carlo), confidence level and site summaries.
Rules from config/terramatch_config.json (project doc v2.0, Fase 3 and section 8.1).

AI-Assisted: Claude (draft of this module; logic reviewed and tested by the team).
"""
import warnings
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from config import CFG, VARS
import analysis as an
from sites import SITES, site_cells


def monte_carlo(master, target, scales=None, iterations=None, seed=None):
    """p_top and rank-percentile p05/p50/p95 per cell (100 = most similar)."""
    mc = CFG["monte_carlo"]
    n = iterations or mc["iterations"]
    rs = np.random.default_rng(mc["seed"] if seed is None else seed)
    scales = an.robust_scales(master) if scales is None else scales
    rng = an.target_ranges(target)
    # a variable excluded from the scaling (IQR = SD = 0) counts as missing in every cell
    X = np.column_stack([an._tf(master[v].astype(float), v).to_numpy() if v in scales and v in master
                         else np.full(len(master), np.nan) for v in VARS])
    base = np.array([CFG["variables"][v]["weight"] for v in VARS])
    lo = np.array([rng[v][0] for v in VARS]); hi = np.array([rng[v][1] for v in VARS])
    sc = np.array([scales.get(v, 1.0) for v in VARS])   # placeholder never used: column is all NaN
    valid = ~np.isnan(X); Xz = np.nan_to_num(X)
    cov = (valid * base).sum(1) / base.sum()
    idx = np.where(an.apply_filter(master, target).to_numpy() & (cov >= CFG["coverage_min"] - 1e-9))[0]
    pct = np.full((len(X), n), np.nan, dtype=np.float32)
    for k in range(n):
        point = rs.uniform(lo, hi)
        w = rs.dirichlet(mc["dirichlet_concentration"] * base / base.sum())
        wm = valid[idx] * w
        D = (np.abs(Xz[idx] - point) / sc * wm).sum(1) / wm.sum(1)
        # average ranks: cells with identical D get identical percentiles (100 = most similar)
        pct[idx, k] = 100.0 * (rankdata(-D, method="average") - 1) / max(len(idx) - 1, 1)
    out = pd.DataFrame({"cell_id": master["cell_id"].values})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        hit = np.where(np.isnan(pct), np.nan, (pct >= 100 * (1 - mc["top_fraction"])).astype(float))
        out["p_top"] = np.nanmean(hit, axis=1)
        q = np.full((len(X), 3), np.nan)
        if len(idx):
            q[idx] = np.nanpercentile(pct[idx], mc["percentiles"], axis=1).T
    out["pct_p05"], out["pct_p50"], out["pct_p95"] = q[:, 0], q[:, 1], q[:, 2]
    return out


def confidence(n_vars, p_top):
    p = 0.0 if p_top is None or np.isnan(p_top) else p_top
    for rule in CFG["confidence"]:
        if n_vars >= rule["min_vars"] and p >= rule["min_p_top"]:
            return rule["level"]
    return "Baja"


def site_summaries(grid, master, prof, mc, target_id, national=True, sites_dir=None):
    both = prof.merge(mc, on="cell_id")
    scored = prof.loc[prof.status == "scored", "S"].values
    rows = []
    for s in [s for s in SITES if s["profile"] == target_id]:
        ids, method = site_cells(s, grid, master, sites_dir)
        sub = both[both.cell_id.isin(ids)]
        sc = sub[sub.status == "scored"]
        S = float(sc.S.median()) if len(sc) else np.nan
        ptop = float(sc.p_top.median()) if len(sc) else np.nan
        nv = int(sub.n_vars.median()) if len(sub) else 0
        row = dict(site=s["id"], name=s["name"], profile=target_id, role=s["role"], method=method,
                   ref_lat=s["lat"], ref_lon=s["lon"],
                   geometry="polygon" if method == "polygon" else "pending",
                   n_cells=len(ids), n_scored=len(sc), S=S,
                   percentile=an.percentile_of(S, scored) if national else np.nan,
                   p_top=ptop, pct_p05=float(sc.pct_p05.median()) if len(sc) else np.nan,
                   pct_p95=float(sc.pct_p95.median()) if len(sc) else np.nan,
                   n_vars=nv, coverage=float(sub.coverage.median()) if len(sub) else 0.0,
                   confidence=confidence(nv, ptop),
                   status="scored" if len(sc) else (sub.status.mode().iat[0] if len(sub) else method))
        for v in VARS:
            row[f"{v}_value"] = float(master.loc[master.cell_id.isin(ids), v].median()) if v in master else np.nan
            row[f"d_{v}"] = float(sub[f"d_{v}"].median()) if len(sub) else np.nan
            row[f"s_{v}"] = float(sub[f"s_{v}"].median()) if len(sub) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)
