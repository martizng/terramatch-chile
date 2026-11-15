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


def synthetic_site_polygons(d):
    """SYNTHETIC test polygons (circles/annulus in degrees) written to d; never used as real sites."""
    from shapely.geometry import Point, mapping
    shapes = {"yungay": Point(-69.881, -24.064).buffer(0.05), "pajonales": Point(-68.820, -25.144).buffer(0.06),
              "llullaillaco": Point(-68.537, -24.720).buffer(0.08), "llaima_cone": Point(-71.729, -38.692).buffer(0.03),
              "llaima_flows": Point(-71.729, -38.692).buffer(0.15).difference(Point(-71.729, -38.692).buffer(0.035))}
    for k, g in shapes.items():
        (pathlib.Path(d) / f"{k}.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": [
            {"type": "Feature", "properties": {"site_id": k, "note": "synthetic test geometry"}, "geometry": mapping(g)}]}))


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
for t in real_targets.values():                               # both profiles computed from real crops
    assert an.pending_variables(t) == [] and all(v["source"] and v["kind"] == "measured" for v in t["variables"].values())
pend = json.loads(json.dumps(real_targets["moon_tranquillitatis"]))
for v in pend["variables"].values():
    v.update(value=None, low=None, high=None, status="pending_verification")
assert an.pending_variables(pend) == list(VARS)
try:
    an.target_ranges(pend); raise SystemExit("FAIL: pending profile accepted")
except an.TargetPending:
    pass
print("real targets: Mars and Moon computed and sourced; a pending profile is refused: OK")

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
    synthetic_site_polygons(d)
    rep = run(grid, master, targets, d, iterations=40, sites_dir=d)
    names = sorted(p.name for p in pathlib.Path(d).iterdir() if p.suffix != ".geojson")
assert names == ["mars_montecarlo.csv", "mars_profile.csv", "mars_scores_web.csv", "moon_montecarlo.csv",
                 "moon_profile.csv", "moon_scores_web.csv", "sites_summary.csv", "validation.json"], names
print(json.dumps({b: rep[b]["checks"] for b in ("mars", "moon")}, indent=1))
assert all(c["passed"] for c in rep["mars"]["checks"].values())
assert rep["moon"]["checks"]["llaima_flows_S>llaima_cone_S"]["passed"]

# 8) a pending profile -> run reports it and writes no profile
with tempfile.TemporaryDirectory() as d:
    rep2 = run(grid, master, {"mars_elysium": real_targets["mars_elysium"], "moon_tranquillitatis": pend}, d, iterations=5, sites_dir=d)
    assert rep2["moon"]["status"] == "pending_targets" and not (pathlib.Path(d) / "moon_profile.csv").exists()
print("pending profiles are reported, not computed: OK")

# 9) a variable with IQR = 0 and SD = 0 is excluded, never given an artificial scale
m0 = master.copy(); m0["rough_sd_deg"] = 1.0
rep0 = {}; sc0 = an.robust_scales(m0, rep0)
assert "rough_sd_deg" not in sc0 and rep0["rough_sd_deg"].startswith("excluded")
p0 = an.profile(m0, t_mars, sc0)
assert p0.d_rough_sd_deg.isna().all() and (p0.n_vars <= 2).all() and (p0.coverage <= 2/3 + 1e-9).all()
mc0 = cp.monte_carlo(m0, t_mars, sc0, 5)
assert mc0.p_top.notna().any()
m0b = master.copy(); m0b["slope_p90_deg"] = np.where(np.arange(n) % 2, 1.0, 1.0); m0b.loc[::2, "slope_p90_deg"] = 1.0
assert "slope_p90_deg" not in an.robust_scales(m0b)
print("IQR = SD = 0 -> variable excluded and reported: OK")

# 10) missing filter layer -> profile NOT ranked (filter never switched off)
with tempfile.TemporaryDirectory() as d:
    rep3 = run(grid, master.drop(columns=["volcanic_unit"]), targets, d, iterations=5, sites_dir=d)
    assert rep3["moon"]["status"] == "pending_filter_data" and not (pathlib.Path(d) / "moon_profile.csv").exists()
    assert rep3["mars"]["status"] == "computed"
print("missing lunar filter layer -> pending_filter_data, no ranking: OK")

# 11) cells without filter data are "no_filter_data", never low similarity
m2 = master.copy(); m2.loc[:500, "precip_mm_yr"] = np.nan
p2 = an.profile(m2, t_mars)
assert (p2.loc[:500, "status"] == "no_filter_data").all() and p2.loc[:500, "S"].isna().all()
print("no filter data -> no_filter_data with S = NaN: OK")

# 12) sites without a verified polygon are pending: no cells, no score, check passed = null (no circles)
with tempfile.TemporaryDirectory() as d:
    rep4 = run(grid, master, targets, d, iterations=5, sites_dir=d)
    ss = pd.read_csv(pathlib.Path(d) / "sites_summary.csv")
assert set(ss.geometry) == {"pending"} and (ss.n_cells == 0).all() and ss.S.isna().all()
assert set(rep4["mars"]["pending_geometry_sites"]) == {"yungay", "pajonales", "llullaillaco"}
assert all(rep4["mars"]["checks"][k]["passed"] is None for k in rep4["mars"]["checks"] if not k.startswith("steep"))
assert rep4["moon"]["checks"]["llaima_flows_S>llaima_cone_S"]["passed"] is None
print("sites without polygon -> pending_geometry, no score, checks pending: OK")

# 12b) Monte Carlo: identical cells get identical rank percentiles (average ranks)
mt = master.copy(); mt.loc[:, list(VARS)] = mt.loc[:, list(VARS)].round(0)
mct = cp.monte_carlo(mt, t_mars, None, 3)
el = mt.join(mct.set_index(mct.index)[["pct_p50"]]).dropna(subset=["pct_p50"])
spread = el.groupby(list(VARS)).pct_p50.agg(lambda x: x.max() - x.min())
assert (spread.fillna(0) < 1e-3).all(), spread.max()
print("Monte Carlo ties -> identical percentiles (average ranks): OK")

# 13) Chilean DEM -> master.csv: UTM by zone, measured scale error, ocean and no coverage = NaN
import rasterio
from rasterio.transform import from_origin
from features import chile_features as chf
with tempfile.TemporaryDirectory() as d:
    d = pathlib.Path(d); res = 0.002
    lats = -38.0 - (np.arange(500) + 0.5) * res; lons = -73.0 + (np.arange(1000) + 0.5) * res
    LA, LO = np.meshgrid(lats, lons, indexing="ij")
    z = (LA + 40.0) * 110950.0 * np.tan(np.radians(5))            # ~5 deg plane, north-facing
    z[LO < -72.8] = 0.0                                             # "ocean"
    z[:, 700:] = -9999                                              # no data band
    prof_t = dict(driver="GTiff", height=500, width=1000, count=1, dtype="float32", crs="EPSG:4326",
                  transform=from_origin(-73.0, -38.0, res, res), nodata=-9999)
    with rasterio.open(d / "dem.tif", "w", **prof_t) as f: f.write(z.astype("float32"), 1)
    pr = np.full((500, 1000), 100.0, "float32")
    with rasterio.open(d / "pr.tif", "w", **prof_t) as f: f.write(pr, 1)
    g, meta = build_grid(res=0.05, lat_min=-39.0, lat_max=-38.0, lon_min=-73.0, lon_max=-71.0)
    g.to_csv(d / "grid.csv", index=False)
    sys.argv = ["x", "--grid", str(d / "grid.csv"), "--dem", str(d / "dem.tif"), "--precip", str(d / "pr.tif"),
                "--out", str(d / "master.csv")]
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()): chf.main()
    ms = pd.read_csv(d / "master.csv").merge(g, on="cell_id")
inner = ms[(ms.lon_c > -72.7) & (ms.lon_c < -71.7) & (ms.lat_c < -38.1) & (ms.lat_c > -38.9)]
assert set(ms.utm_epsg) == {"EPSG:32718", "EPSG:32719"}
assert inner.slope_p90_deg.notna().all() and (inner.slope_p90_deg.sub(5).abs() < 0.3).all(), inner.slope_p90_deg.describe()
assert ms[ms.lon_c < -72.85].slope_p90_deg.isna().all(), "ocean cells must be NaN"
assert ms[ms.lon_c > -71.5].slope_p90_deg.isna().all(), "cells without DEM coverage must be NaN"
assert ms.scale_error.max() < 0.01
print(f"chile_features: UTM 18S/19S, slope 5 deg recovered in both zones, ocean and no coverage = NaN, "
      f"max scale error {ms.scale_error.max():.3%}: OK")
print("ALL CHECKS PASSED (synthetic logic test, not a result)")
