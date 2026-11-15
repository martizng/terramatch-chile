"""Common grid generator (owner: Rojas).

Creates the one and only grid every teammate joins on.

cell_id = iy * nx + ix, where iy counts rows from the SOUTH edge and ix counts
columns from the WEST edge of the full bounding box. Because the id depends only on
(bbox, resolution), it never changes if the land mask is updated later.

Usage:
    python src/grid/make_grid.py --out data/processed/grid.csv
    python src/grid/make_grid.py --land-mask data/raw/chile_boundary.geojson   # needs geopandas

AI-Assisted: Claude (first draft of this script; reviewed and run by the team).
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

# Contract section 4 (proposal, still TODO(decide) there)
LAT_MIN, LAT_MAX = -56.0, -17.0
LON_MIN, LON_MAX = -76.0, -66.0
RES = 0.05


def build_grid(res=RES, lat_min=LAT_MIN, lat_max=LAT_MAX, lon_min=LON_MIN, lon_max=LON_MAX):
    ny = int(round((lat_max - lat_min) / res))
    nx = int(round((lon_max - lon_min) / res))
    iy, ix = np.meshgrid(np.arange(ny), np.arange(nx), indexing="ij")
    iy, ix = iy.ravel(), ix.ravel()
    df = pd.DataFrame({
        "cell_id": iy * nx + ix,
        "iy": iy,
        "ix": ix,
        "lat_c": lat_min + (iy + 0.5) * res,
        "lon_c": lon_min + (ix + 0.5) * res,
    })
    meta = dict(res=res, lat_min=lat_min, lat_max=lat_max, lon_min=lon_min,
                lon_max=lon_max, ny=ny, nx=nx, n_cells_total=int(ny * nx))
    return df, meta


def cell_id_of(lat, lon, meta):
    """cell_id containing a point (used to locate validation sites)."""
    iy = int(np.floor((lat - meta["lat_min"]) / meta["res"]))
    ix = int(np.floor((lon - meta["lon_min"]) / meta["res"]))
    if not (0 <= iy < meta["ny"] and 0 <= ix < meta["nx"]):
        raise ValueError(f"point ({lat},{lon}) outside the grid")
    return iy * meta["nx"] + ix


def apply_land_mask(df, mask_path):
    """Keep only cells whose centre falls inside the polygon file (Chile boundary)."""
    import geopandas as gpd  # optional dependency
    poly = gpd.read_file(mask_path).to_crs(4326)
    pts = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon_c, df.lat_c), crs=4326)
    keep = gpd.sjoin(pts, poly[["geometry"]], predicate="within", how="inner")
    return df[df.cell_id.isin(keep.cell_id)].reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/processed/grid.csv")
    ap.add_argument("--res", type=float, default=RES)
    ap.add_argument("--land-mask", default=None,
                    help="vector file with the Chile boundary (decision pending in the contract)")
    a = ap.parse_args()

    df, meta = build_grid(res=a.res)
    if a.land_mask:
        df = apply_land_mask(df, a.land_mask)
        meta["land_mask"] = a.land_mask
    else:
        meta["land_mask"] = None
        print("WARNING: no land mask. The grid still contains ocean and Argentina cells.")
    meta["n_cells_kept"] = int(len(df))

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    out.with_suffix(".metadata.json").write_text(json.dumps(meta, indent=2))
    print(meta)


if __name__ == "__main__":
    main()
