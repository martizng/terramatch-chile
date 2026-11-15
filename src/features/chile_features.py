"""Chilean variables per grid cell (owners: Pancho delivers rasters, Rojas runs this script).

Inputs (GeoTIFF, EPSG:4326 or any CRS readable by rasterio):
  --dem          ASTER GDEM v3 of continental Chile: one mosaic or several tiles (all are read)
  --precip       PRIMARY aridity source: mean annual precipitation 2001-2024 (mm/yr), GPM IMERG Final V07
  --precip-alt   optional COMPLEMENTARY source (CR2MET-IMERG); used only as a sensitivity analysis
  --volcanic     optional 0/1 raster of volcanic units, strict criterion (main lunar filter)
  --volcanic-broad optional 0/1 raster, broad criterion (sensitivity only)
Output: data/processed/master.csv with cell_id, slope_p90_deg, relief_m, rough_sd_deg, valid_frac,
        utm_epsg, scale_error, precip_mm_yr, precip_alt_mm_yr, volcanic_unit, volcanic_broad
        (+ .metadata.json with a quality report).

Projection. Slopes are computed in metres, in the UTM zone of each cell (18S west of 72 W, 19S east of it,
doc v2.0 section 8 Fase 2). The point scale error |k - 1| is computed for every cell with pyproj and
written to master.csv; the run stops if any cell exceeds config chile_dem.max_scale_error.
No data. DEM pixels <= 0 m (ocean in the ASTER mosaic) and nodata pixels are NaN. A 5 km window with
less than chile_dem.window_min_valid_fraction valid pixels gives NaN: no coverage is never a value.

AI-Assisted: Claude (draft of this script; reviewed and run by the team).
"""
import argparse, glob, json, math
from pathlib import Path
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import CFG
from features.terrain import BASE_RES_M, slope_deg, window_px, _window_stats

DEMCFG = CFG["chile_dem"]


def zone_of(lon):
    for z in DEMCFG["utm_zones"]:
        if z["lon_min"] <= lon < z["lon_max"]:
            return z["epsg"]
    raise ValueError(f"longitude {lon} outside the configured UTM zones")


def dem_to_zone(paths, epsg, lon_min, lon_max, lat_min, lat_max):
    """Average-resample every DEM file into one metric grid of the given UTM zone at 463 m."""
    import rasterio
    from rasterio.transform import from_origin
    from rasterio.warp import reproject, transform_bounds, Resampling
    b = DEMCFG["zone_buffer_deg"]
    l, bt, r, t = transform_bounds("EPSG:4326", epsg, lon_min - b, lat_min - b, lon_max + b, lat_max + b,
                                   densify_pts=101)
    w, h = int(math.ceil((r - l) / BASE_RES_M)), int(math.ceil((t - bt) / BASE_RES_M))
    tr = from_origin(l, t, BASE_RES_M, BASE_RES_M)
    out = np.full((h, w), np.nan, dtype="float32")
    for p in paths:
        with rasterio.open(p) as src:
            tile = np.full((h, w), np.nan, dtype="float32")
            reproject(rasterio.band(src, 1), tile, src_transform=src.transform, src_crs=src.crs,
                      src_nodata=src.nodata, dst_transform=tr, dst_crs=epsg,
                      resampling=Resampling.average, dst_nodata=np.nan)
            out = np.where(np.isnan(out), tile, out)
    out[out <= DEMCFG["min_valid_elevation_m"]] = np.nan
    return out, tr


def window_features(dem, rows, cols):
    n = window_px(); h = n // 2
    s = slope_deg(dem)
    need = DEMCFG["window_min_valid_fraction"]
    nan = dict(slope_p90_deg=np.nan, relief_m=np.nan, rough_sd_deg=np.nan)
    out = []
    for r, c in zip(rows, cols):
        if r - h < 0 or c - h < 0 or r + h >= dem.shape[0] or c + h >= dem.shape[1]:
            out.append({**nan, "valid_frac": 0.0}); continue
        z = dem[r-h:r+h+1, c-h:c+h+1]; sl = s[r-h:r+h+1, c-h:c+h+1]
        vf = float(np.isfinite(sl).mean())
        out.append({**(_window_stats(z, sl) if vf >= need else nan), "valid_frac": vf})
    return out


def sample_raster(path, lon, lat):
    import rasterio
    with rasterio.open(path) as ds:
        vals = np.array([v[0] for v in ds.sample(zip(lon, lat))], float)
        if ds.nodata is not None:
            vals[vals == ds.nodata] = np.nan
    return vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", default="data/processed/grid.csv")
    ap.add_argument("--dem", required=True, nargs="+", help="mosaic or tiles (glob patterns accepted)")
    ap.add_argument("--precip", required=True, help="GPM IMERG Final V07, mean 2001-2024, mm/yr (primary)")
    ap.add_argument("--precip-alt", default=None, help="CR2MET-IMERG (complementary, sensitivity only)")
    ap.add_argument("--volcanic", default=None)
    ap.add_argument("--volcanic-broad", default=None)
    ap.add_argument("--out", default="data/processed/master.csv")
    a = ap.parse_args()
    from pyproj import Proj, Transformer
    import rasterio
    paths = sorted({p for pat in a.dem for p in (glob.glob(pat) or [pat])})
    grid = pd.read_csv(a.grid)
    zones = grid.lon_c.map(zone_of)
    parts = []
    for epsg in zones.unique():
        g = grid[zones == epsg]
        dem, tr = dem_to_zone(paths, epsg, g.lon_c.min(), g.lon_c.max(), g.lat_c.min(), g.lat_c.max())
        x, y = Transformer.from_crs("EPSG:4326", epsg, always_xy=True).transform(g.lon_c.values, g.lat_c.values)
        rows, cols = rasterio.transform.rowcol(tr, x, y)
        f = pd.DataFrame(window_features(dem, np.array(rows), np.array(cols)), index=g.index)
        fac = Proj(epsg).get_factors(g.lon_c.values, g.lat_c.values)
        f["utm_epsg"] = epsg
        f["scale_error"] = np.maximum(np.abs(np.asarray(fac.meridional_scale) - 1),
                                      np.abs(np.asarray(fac.parallel_scale) - 1))
        parts.append(f)
        print(f"{epsg}: {len(g)} cells, DEM grid {dem.shape}, valid pixels {np.isfinite(dem).mean():.1%}")
    feats = pd.concat(parts).loc[grid.index]
    master = pd.concat([grid[["cell_id"]], feats], axis=1)
    worst = float(master.scale_error.max())
    if worst > DEMCFG["max_scale_error"]:
        raise SystemExit(f"UTM scale error {worst:.4%} exceeds {DEMCFG['max_scale_error']:.2%}")
    lon, lat = grid.lon_c.values, grid.lat_c.values
    master["precip_mm_yr"] = sample_raster(a.precip, lon, lat)
    master["precip_alt_mm_yr"] = sample_raster(a.precip_alt, lon, lat) if a.precip_alt else np.nan
    master["volcanic_unit"] = sample_raster(a.volcanic, lon, lat) if a.volcanic else np.nan
    master["volcanic_broad"] = sample_raster(a.volcanic_broad, lon, lat) if a.volcanic_broad else np.nan
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(a.out, index=False)
    terrain_ok = master[["slope_p90_deg", "relief_m", "rough_sd_deg"]].notna().all(axis=1)
    meta = {"dem_files": [Path(p).name for p in paths], "precip_primary": a.precip, "precip_complementary": a.precip_alt,
            "volcanic": a.volcanic, "volcanic_broad": a.volcanic_broad, "base_res_m": BASE_RES_M,
            "projection_for_slope": "UTM 18S (EPSG:32718) west of 72 W, UTM 19S (EPSG:32719) east of it",
            "scale_error_max": worst, "scale_error_median": float(master.scale_error.median()),
            "window_km": CFG["window_km"], "window_min_valid_fraction": DEMCFG["window_min_valid_fraction"],
            "n_cells": int(len(master)), "n_cells_terrain_complete": int(terrain_ok.sum()),
            "n_cells_no_terrain_coverage": int(master.slope_p90_deg.isna().sum()),
            "n_cells_no_precip": int(master.precip_mm_yr.isna().sum()),
            "ai": "script drafted with AI assistance; no data values generated by AI"}
    Path(a.out).with_suffix(".metadata.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))
    print(master.describe().T)


if __name__ == "__main__":
    main()
