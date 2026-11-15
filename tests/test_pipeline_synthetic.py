"""LOGIC TEST ONLY. Every number here is SYNTHETIC and must never be shown as a result.
Checks that the code follows config/terramatch_config.json (project doc v2.0).
Run: py tests/test_pipeline_synthetic.py
"""
import sys, pathlib, json, tempfile, copy
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np, pandas as pd
from scipy import ndimage
from config import CFG, VARS
from features import terrain as tr
from grid.make_grid import build_grid
import analysis as an, comparison as cp
from run_pipeline import run

rng = np.random.default_rng(1)

# 1) configuration = doc v2.0
assert VARS == ("slope_p90_deg", "relief_m", "rough_sd_deg")
assert all(abs(CFG["variables"][v]["weight"] - 1/3) < 1e-6 for v in VARS)
assert round(CFG["common_resolution_m"]) == 463 and CFG["window_km"] == 5
assert CFG["grid"]["crs"] == "EPSG:4326" and CFG["grid"]["resolution_deg"] == 0.05
assert CFG["monte_carlo"]["iterations"] == 500
print("config matches doc v2.0: OK")

# 2) relief variables
x = np.arange(60) * tr.BASE_RES_M
assert abs(np.nanmedian(tr.slope_deg(np.tile(x * np.tan(np.radians(10)), (60, 1)))) - 10) < 0.01
fine = np.tile(np.arange(500) * 59.2 * np.tan(np.radians(5)), (500, 1))
assert abs(np.nanmedian(tr.slope_deg(tr.resample(fine, 59.2, 59.2))[2:-2, 2:-2]) - 5) < 0.2
print("slope and resampling: OK")

# 3) pending targets are refused, never invented
real_targets = an.load_targets(pathlib.Path(__file__).resolve().parents[1] / "data" / "targets.json")
for t in real_targets.values():
    if t["body"] == "moon":                                   # still waiting for SLDEM2015
        assert an.pending_variables(t) == list(VARS)
        try:
            an.target_ranges(t); raise SystemExit("FAIL: pending profile accepted")
        except an.TargetPending:
            pass
    else:                                                     # Mars computed from MOLA: every value sourced
        assert an.pending_variables(t) == [] and all(v["source"] and v["kind"] == "derived_from_dem" for v in t["variables"].values())
print("real targets: Mars computed and sourced, Moon pending and refused: OK")

# 4) SYNTHETIC profiles from synthetic DEMs
plain = lambda n: ndimage.gaussian_filter(rng.normal(0, 1, (n, n)), 3) * 10
meas = np.ones((65, 65)); meas[:, :15] = 0
t_mars = tr.build_target_from_dem(plain(65), tr.BASE_RES_M, tr.BASE_RES_M, target_id="mars_elysium", body="mars",
                                  name="SYNTHETIC", source="SYNTHETIC-TEST", product="SYNTHETIC", measured=meas)
t_moon = tr.build_target_from_dem(plain(510), 59.2, 59.2, target_id="moon_tranquillitatis", body="moon",
                                  name="SYNTHETIC", source="SYNTHETIC-TEST", product="SYNTHETIC")
assert 10 <= t_mars["n_windows"] < 25 and t_moon["n_windows"] == 25
t_mars["filter"] = CFG["filters"]["mars"]; t_moon["filter"] = CFG["filters"]["moon"]
print("profiles from DEM windows (mars, moon):", t_mars["n_windows"], t_moon["n_windows"])

# 5) SYNTHETIC Chile
grid, _ = build_grid(); n = len(grid); lat, lon = grid.lat_c.values, grid.lon_c.values
steep = (lon > -69.0) | (np.hypot(lat + 24.72, lon + 68.537) < 0.08)
master = pd.DataFrame({"cell_id": grid.cell_id,
    "slope_p90_deg": np.where(steep, rng.normal(25, 5, n), rng.normal(2, .8, n)).clip(0),
    "relief_m": np.where(steep, 900, 40) * rng.uniform(.7, 1.3, n),
    "rough_sd_deg": np.where(steep, 8, .8) * rng.uniform(.7, 1.3, n),
    "precip_mm_yr": np.where(lat > -30, rng.uniform(0, 60, n), rng.uniform(400, 3000, n)),
    "volcanic_unit": (np.hypot(lat + 38.692, lon + 71.729) < 0.2).astype(float)})
master.loc[np.hypot(lat + 38.692, lon + 71.729) < 0.025, list(VARS)] = [30, 1500, 9]
for la, lo in [(-24.064, -69.881), (-25.144, -68.820)]:
    near = np.hypot(lat - la, lon - lo) < 0.12
    for v in VARS:
        master.loc[near, v] = t_mars["variables"][v]["value"]
master.loc[rng.random(n) < 0.03, "relief_m"] = np.nan

# 6) per-cell outputs
prof = an.profile(master, t_mars)
assert {"d_slope_p90_deg", "s_relief_m", "coverage", "S", "status"} <= set(prof.columns)
assert (prof.loc[prof.status == "outside_filter", "S"].isna()).all()
two = prof[(prof.n_vars == 2) & prof.passes_filter]
assert two.S.notna().all(), "2 of 3 variables must still be scored"
m1 = master.copy(); m1.loc[:100, ["relief_m", "rough_sd_deg"]] = np.nan
p1 = an.profile(m1, t_mars)
assert (p1.loc[:100][p1.loc[:100].passes_filter].status == "insufficient_data").all()
assert cp.confidence(3, .7) == "Alta" and cp.confidence(2, .3) == "Media" and cp.confidence(3, .29) == "Baja"
print("distance, similarity, coverage, confidence: OK")

# 7) full run
targets = {"mars_elysium": t_mars, "moon_tranquillitatis": t_moon}
with tempfile.TemporaryDirectory() as d:
    # Synthetic polygons exclusively for unit testing, never a project geometry.
    import geopandas as gpd
    from shapely.geometry import Point
    from sites import SITES
    for site in SITES:
        origin = Point(site["lon"], site["lat"])
        poly = (origin.buffer(0.15).difference(origin.buffer(0.055))
                if site["id"] == "llaima_flows" else
                origin.buffer(0.04 if site["id"] == "llaima_cone" else 0.09))
        gpd.GeoDataFrame([{"site_id": site["id"]}], geometry=[poly], crs="EPSG:4326").to_file(
            pathlib.Path(d) / f'{site["id"]}.geojson', driver="GeoJSON")
    rep = run(grid, master, targets, d, iterations=40, sites_dir=d)
    names = sorted(p.name for p in pathlib.Path(d).iterdir() if p.suffix != ".geojson")
assert names == ["mars_montecarlo.csv", "mars_profile.csv", "moon_montecarlo.csv", "moon_profile.csv",
                 "sites_summary.csv", "validation.json"], names
print(json.dumps({b: rep[b]["checks"] for b in ("mars", "moon")}, indent=1))
assert all(c["passed"] for c in rep["mars"]["checks"].values())
assert rep["moon"]["checks"]["llaima_flows_S>llaima_cone_S"]["passed"]

# 8) real targets still pending -> run reports it and writes no profile
with tempfile.TemporaryDirectory() as d:
    rep2 = run(grid, master, real_targets, d, iterations=5, sites_dir=d)
    assert rep2["moon"]["status"] == "pending_targets" and not (pathlib.Path(d) / "moon_profile.csv").exists()
print("pending profiles are reported, not computed: OK")
print("ALL CHECKS PASSED (synthetic logic test, not a result)")
