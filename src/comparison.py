"""Comparison (owner: Rojas): ranking stability (Monte Carlo), confidence level and site summaries.
Rules from config/terramatch_config.json (project doc v2.0, Fase 3 and section 8.1).

AI-Assisted: Claude (draft of this module; logic reviewed and tested by the team).
"""
import warnings
import numpy as np
import pandas as pd
from config import CFG, VARS
import analysis as an
from sites import SITES, site_cells


def monte_carlo(master, target, scales=None, iterations=None, seed=None):
    """Monte Carlo stability for scored cells only; 100 = highest similarity.

    Excludes constant/non-informative variables as in analysis.profile.
    Ties receive average ranks, not a row-order advantage.
    """
    from scipy.stats import rankdata

    mc = CFG["monte_carlo"]
    n = mc["iterations"] if iterations is None else int(iterations)
    if n < 1:
        raise ValueError("iterations must be >= 1")
    rs = np.random.default_rng(mc["seed"] if seed is None else seed)
    scales = an.robust_scales(master) if scales is None else scales
    rng = an.target_ranges(target)
    active = [v for v in VARS if v in scales and np.isfinite(scales[v]) and scales[v] > 0]
    out = pd.DataFrame({"cell_id": master["cell_id"].values})
    out["p_top"] = np.nan
    for key in ("pct_p05", "pct_p50", "pct_p95"):
        out[key] = np.nan
    if not active:
        return out

    X = np.column_stack([an._tf(master[v].astype(float), v).to_numpy() for v in active])
    w0 = np.array([CFG["variables"][v]["weight"] for v in active], dtype=float)
    lo = np.array([rng[v][0] for v in active]); hi = np.array([rng[v][1] for v in active])
    sc = np.array([scales[v] for v in active])
    valid = np.isfinite(X)
    cov = (valid * w0).sum(1) / w0.sum()
    enough = (cov >= CFG["coverage_min"] - 1e-9) & (valid.sum(1) >= 2)
    idx = np.flatnonzero(an.apply_filter(master, target).to_numpy() & enough)
    if len(idx) == 0:
        return out
    Xz = np.where(valid[idx], X[idx], 0.0)
    mask = valid[idx]
    pct = np.empty((len(idx), n), dtype=np.float32)
    hits = np.zeros(len(idx), dtype=float)
    top_count = max(1, int(np.ceil(mc["top_fraction"] * len(idx))))
    for k in range(n):
        point = rs.uniform(lo, hi)
        w = rs.dirichlet(mc["dirichlet_concentration"] * w0 / w0.sum())
        wm = mask * w
        d = np.abs(Xz - point) / sc
        D = (d * wm).sum(1) / wm.sum(1)
        ranks = rankdata(D, method="average")   # smallest D is best (rank 1)
        pct[:, k] = 100.0 * (len(idx) - ranks) / max(len(idx) - 1, 1)
        hits += (ranks <= top_count)
    out.loc[idx, "p_top"] = hits / n
    vals = np.percentile(pct, mc["percentiles"], axis=1).T
    for i, key in enumerate(("pct_p05", "pct_p50", "pct_p95")):
        out.loc[idx, key] = vals[:, i]
    return out


def confidence(n_vars, p_top):
    p = 0.0 if p_top is None or np.isnan(p_top) else p_top
    for rule in CFG["confidence"]:
        if n_vars >= rule["min_vars"] and p >= rule["min_p_top"]:
            return rule["level"]
    return "Baja"


def site_summaries(grid, master, prof, mc, target_id, national=True, sites_dir="data/chile/sites"):
    both = prof.merge(mc, on="cell_id")
    scored = prof.loc[prof.status == "scored", "S"].values
    rows = []
    for s in [s for s in SITES if s["profile"] == target_id]:
        ids, method = site_cells(s, grid, master, sites_dir)
        sub = both[both.cell_id.isin(ids)]
        sc = sub[sub.status == "scored"]
        S = float(sc.S.median()) if len(sc) else np.nan
        ptop = float(sc.p_top.median()) if len(sc) else np.nan
        nv = int(sc.n_vars.median()) if len(sc) else 0
        row = dict(site=s["id"], name=s["name"], profile=target_id, role=s["role"], method=method,
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
