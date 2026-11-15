"""Build or update data/targets.json from the planetary crops delivered by BJOR (doc section 12).
Each body is optional: a body that is not given keeps its current entry (e.g. pending_verification).

  py src/features/build_targets.py --mars data/raw/elysium_mola_dem.tif --mars-count data/raw/elysium_mola_counts.tif
  py src/features/build_targets.py --moon data/raw/sldem2015_tranquillitatis_crop.tif

AI-Assisted: Claude (draft of this script; reviewed and run by the team).
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from features.terrain import read_planetary_crop, build_target_from_dem
from config import CFG

SPEC = {
    "mars": dict(target_id="mars_elysium", name="Elysium Planitia, sector occidental",
                 product="MGS MOLA MEGDR 128 ppd (MEGT44N090HB.IMG, v2.0)",
                 source="https://astrogeology.usgs.gov/search/map/mars_mgs_mola_dem_463m",
                 center={"lat": 4.50, "lon": 135.90}, pilot_area="30 x 30 km; lat 4.25-4.75 N, lon 135.65-136.15 E"),
    "moon": dict(target_id="moon_tranquillitatis", name="Mare Tranquillitatis",
                 product="SLDEM2015 (LOLA + Kaguya TC) 512 ppd",
                 source="https://pgda.gsfc.nasa.gov/products/54",
                 center={"lat": 0.67416, "lon": 23.47314}, pilot_area="30 x 30 km; lat 0.18-1.17 N, lon 22.98-23.97 E"),
}


def build(body, dem_path, count_path=None):
    s = SPEC[body]
    dem, px, py = read_planetary_crop(dem_path, body)
    measured = None
    if count_path:
        cnt, _, _ = read_planetary_crop(count_path, body)
        measured = (np.nan_to_num(cnt) > 0).astype(float)
    t = build_target_from_dem(dem, px, py, target_id=s["target_id"], body=body, name=s["name"],
                              product=s["product"], source=s["source"], measured=measured)
    t.update(center=s["center"], pilot_area=s["pilot_area"], product=s["product"], filter=CFG["filters"][body],
             input_files=[Path(dem_path).name] + ([Path(count_path).name] if count_path else []),
             pixel_m=[round(px, 1), round(py, 1)],
             measured_fraction=None if measured is None else round(float(measured.mean()), 3),
             elevation_median_m=float(np.nanmedian(dem)))
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mars"); ap.add_argument("--mars-count")
    ap.add_argument("--moon")
    ap.add_argument("--out", default="data/targets.json")
    a = ap.parse_args()
    out = Path(a.out)
    current = {t["body"]: t for t in json.loads(out.read_text(encoding="utf-8"))} if out.exists() else {}
    if a.mars:
        current["mars"] = build("mars", a.mars, a.mars_count)
    if a.moon:
        current["moon"] = build("moon", a.moon)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps([current[b] for b in ("mars", "moon") if b in current], indent=2, ensure_ascii=False),
                   encoding="utf-8")
    for b, t in current.items():
        vals = {k: v.get("value") for k, v in t["variables"].items()}
        print(b, t.get("n_windows", "pending"), vals)


if __name__ == "__main__":
    main()
