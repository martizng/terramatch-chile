"""Relief variables (owner: Rojas). Implements sections 6.1, 6.2 and Fase 1 of the project doc v2.0.

All three bodies are processed the same way:
  1. resample the DEM to the common base resolution BASE_RES_M (463 m, MOLA MEGDR 128 ppd);
  2. compute slope (degrees) on a metric grid;
  3. per 5 km window: slope_p90_deg, relief_m (P95 - P5 of elevation), rough_sd_deg (std of slope).

Planetary profiles (build_target_from_dem): non-overlapping 5 km windows inside the 30 x 30 km pilot
area; windows with < 50 % directly measured pixels are dropped (MOLA interpolation near the equator);
reference value = median, range = P10-P90.

AI-Assisted: Claude (draft of this module; reviewed and tested by the team).
"""
import sys
from pathlib import Path
import numpy as np
from scipy import ndimage
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import CFG, VARS

BASE_RES_M = CFG["common_resolution_m"]          # MOLA MEGDR 128 ppd at the equator (USGS Astrogeology)
WINDOW_KM = CFG["window_km"]
MIN_MEASURED = CFG["profile_windows"]["min_measured_fraction"]
MIN_WINDOWS = CFG["profile_windows"]["min_valid_windows"]
P_LO, P_HI = CFG["profile_windows"]["range_percentiles"]
RADIUS_KM = {"mars": 3396.19, "moon": 1737.4}


def resample(dem, px_x_m, px_y_m, out_m=BASE_RES_M):
    """Area-average resampling of a regular grid to out_m (NaN-aware)."""
    dem = np.asarray(dem, float)
    fy, fx = px_y_m / out_m, px_x_m / out_m
    valid = np.isfinite(dem).astype(float)
    filled = np.where(valid > 0, dem, 0.0)
    if fx < 1 or fy < 1:                      # downsampling: box-average first
        sy, sx = max(1, int(round(1 / fy))), max(1, int(round(1 / fx)))
        filled = ndimage.uniform_filter(filled, size=(sy, sx), mode="nearest")
        valid = ndimage.uniform_filter(valid, size=(sy, sx), mode="nearest")
    z = ndimage.zoom(filled, (fy, fx), order=1)
    v = ndimage.zoom(valid, (fy, fx), order=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = np.where(v > 0.5, z / np.where(v > 0, v, 1), np.nan)
    return out


def slope_deg(dem, px_m=BASE_RES_M):
    dzdy, dzdx = np.gradient(np.asarray(dem, float), px_m, px_m)
    return np.degrees(np.arctan(np.hypot(dzdx, dzdy)))


def _window_stats(z, s):
    z = z[np.isfinite(z)]; s = s[np.isfinite(s)]
    if z.size < 4 or s.size < 4:
        return dict(slope_p90_deg=np.nan, relief_m=np.nan, rough_sd_deg=np.nan)
    return dict(slope_p90_deg=float(np.percentile(s, 90)),
                relief_m=float(np.percentile(z, 95) - np.percentile(z, 5)),
                rough_sd_deg=float(np.std(s)))


def window_px(px_m=BASE_RES_M, window_km=WINDOW_KM):
    return max(3, int(round(window_km * 1000 / px_m)))


def tiled_windows(dem, measured=None, px_m=BASE_RES_M, window_km=WINDOW_KM):
    """Non-overlapping windows over a DEM already at px_m. Returns list of dicts."""
    n = window_px(px_m, window_km)
    s = slope_deg(dem, px_m)
    rows = []
    for i in range(0, dem.shape[0] - n + 1, n):
        for j in range(0, dem.shape[1] - n + 1, n):
            d = _window_stats(dem[i:i+n, j:j+n], s[i:i+n, j:j+n])
            d["measured_frac"] = float(np.mean(measured[i:i+n, j:j+n])) if measured is not None else 1.0
            d["row"], d["col"] = i, j
            rows.append(d)
    return rows


def centered_windows(dem, rows, cols, px_m=BASE_RES_M, window_km=WINDOW_KM):
    """Window centered on each (row, col) pixel of a DEM already at px_m (used for Chilean cells)."""
    n = window_px(px_m, window_km); h = n // 2
    s = slope_deg(dem, px_m)
    out = []
    for r, c in zip(rows, cols):
        if r < 0 or c < 0 or r >= dem.shape[0] or c >= dem.shape[1]:
            out.append(dict(slope_p90_deg=np.nan, relief_m=np.nan, rough_sd_deg=np.nan)); continue
        sl = (slice(max(0, r-h), r+h+1), slice(max(0, c-h), c+h+1))
        out.append(_window_stats(dem[sl], s[sl]))
    return out


def planetary_pixel_m(body, res_deg_lon, res_deg_lat, center_lat):
    """Pixel size in metres of a lat/lon (simple cylindrical) planetary grid."""
    k = np.pi * RADIUS_KM[body] * 1000 / 180
    return res_deg_lon * k * np.cos(np.radians(center_lat)), res_deg_lat * k


def build_target_from_dem(dem, px_x_m, px_y_m, *, target_id, body, name, source, product,
                          test_purpose="morphology", measured=None, min_measured=MIN_MEASURED):
    """Profile entry for data/targets.json from a planetary DEM crop (doc section 6.2, Fase 1)."""
    z = resample(dem, px_x_m, px_y_m)
    m = None
    if measured is not None:
        m = resample(np.asarray(measured, float), px_x_m, px_y_m)
        m = np.nan_to_num(m)
    wins = [w for w in tiled_windows(z, m) if w["measured_frac"] >= min_measured]
    if len(wins) < MIN_WINDOWS:
        raise ValueError(f"only {len(wins)} usable windows: profile not reliable")
    variables = {}
    for v in VARS:
        x = np.array([w[v] for w in wins]); x = x[np.isfinite(x)]
        variables[v] = {"value": float(np.median(x)), "low": float(np.percentile(x, P_LO)),
                        "high": float(np.percentile(x, P_HI)), "kind": "measured",
                        "status": "computed",
                        "source": f"{product}; derived at {BASE_RES_M:.0f} m, {WINDOW_KM:g} km windows",
                        "notes": f"{len(wins)} windows used"}
    return {"id": target_id, "body": body, "name": name, "test_purpose": test_purpose,
            "source": source, "n_windows": len(wins), "variables": variables}


def read_planetary_crop(path, body):
    """Read a lat/lon GeoTIFF crop (MOLA MEGDR or SLDEM2015) -> (dem, px_x_m, px_y_m). Needs rasterio."""
    import rasterio
    with rasterio.open(path) as ds:
        dem = ds.read(1, masked=True).astype(float).filled(np.nan)   # works for integer rasters too
        t = ds.transform
        center_lat = (ds.bounds.top + ds.bounds.bottom) / 2
        radius_km = RADIUS_KM[body]
        try:
            a = ds.crs.to_dict().get("a") or ds.crs.ellipsoid.semi_major_metre
            if a and 1e6 < a < 1e7:
                radius_km = a / 1000
        except Exception:
            pass
    k = np.pi * radius_km * 1000 / 180
    px_x, px_y = abs(t.a) * k * np.cos(np.radians(center_lat)), abs(t.e) * k
    return dem, px_x, px_y
