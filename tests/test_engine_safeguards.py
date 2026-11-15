"""Regression tests for data quality, missing filters, constant variables and polygons.

These use tiny synthetic tables only; they never represent scientific results.
"""
import json
import sys
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import analysis as an
import comparison as cp
from sites import SITES, site_cells
from run_pipeline import run


def target(body="mars"):
    return {
        "id": "mars_elysium" if body == "mars" else "moon_tranquillitatis",
        "body": body,
        "variables": {v: {"low": 2, "high": 5, "value": 3, "source": "SYNTHETIC-TEST"} for v in an.VARS},
        "filter": {"column": "precip_mm_yr", "type": "max", "max": 250} if body == "mars" else
                  {"column": "volcanic_unit", "type": "flag"},
    }


def test_zero_variance_excluded_and_not_imputed():
    master = pd.DataFrame({"cell_id": np.arange(10),
        "slope_p90_deg": np.linspace(0, 9, 10),
        "relief_m": np.linspace(1, 10, 10),
        "rough_sd_deg": np.ones(10),
        "precip_mm_yr": np.zeros(10)})
    scales = an.robust_scales(master)
    assert "rough_sd_deg" not in scales
    prof = an.profile(master, target(), scales)
    assert prof["s_rough_sd_deg"].isna().all()
    assert (prof.n_vars == 2).all()
    assert (prof.coverage == 1.0).all()
    assert prof.status.eq("scored").all()
    mc = cp.monte_carlo(master, target(), scales, iterations=20)
    assert mc.p_top.notna().all()
    assert (mc.p_top.between(0,1)).all()


def test_missing_filter_refuses_ranking():
    grid = pd.DataFrame({"cell_id": range(12), "lat_c": [-24.1]*12, "lon_c": [-69.9]*12})
    master = pd.DataFrame({"cell_id": range(12), "slope_p90_deg": np.linspace(1,2,12),
                           "relief_m": np.linspace(3,10,12), "rough_sd_deg": np.linspace(2,3,12)})
    with tempfile.TemporaryDirectory() as tmp:
        report = run(grid, master, {"moon_tranquillitatis": target("moon")}, out=tmp, iterations=3)
        assert report["moon"]["status"] == "missing_filter_data"
        assert not list(Path(tmp).glob("*_profile.csv"))


def test_missing_polygons_are_pending_not_invented():
    grid = pd.DataFrame({"cell_id": [1], "lat_c": [-25.144], "lon_c": [-68.820]})
    with tempfile.TemporaryDirectory() as tmp:
        ids, method = site_cells(next(s for s in SITES if s["id"] == "pajonales"), grid, sites_dir=tmp)
        assert ids == [] and method == "pending_geometry"


def test_missing_data_never_treated_as_zero():
    master = pd.DataFrame({"cell_id": range(10),
                           "slope_p90_deg": np.linspace(1,4,10),
                           "relief_m": np.linspace(1,10,10),
                           "rough_sd_deg": np.linspace(3,6,10),
                           "precip_mm_yr": [100]*10})
    master.loc[0,["slope_p90_deg","relief_m"]] = np.nan
    prof=an.profile(master,target())
    assert prof.loc[0,"status"] == "insufficient_data"
    assert np.isnan(prof.loc[0,"S"])


if __name__ == "__main__":
    test_zero_variance_excluded_and_not_imputed()
    test_missing_filter_refuses_ranking()
    test_missing_polygons_are_pending_not_invented()
    test_missing_data_never_treated_as_zero()
    print("ALL SAFEGUARD CHECKS PASSED (synthetic-only)")
