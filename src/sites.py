"""Sites of the MVP (doc section 5.2) and how each is turned into a set of grid cells.

Only verified polygons are used: <sites_dir>/<site_id>.geojson (default data/chile/sites, config "paths").
A site without a polygon is "pending_geometry": it gets no cells and no score, and every validation check
that needs it is reported as pending. No approximate circles or annuli are generated (doc v2.0, section 8).

AI-Assisted: Claude (draft of this module; reviewed by the team).
"""
from pathlib import Path
from config import CFG, CONFIG_PATH

ROOT = CONFIG_PATH.parents[1]          # project root: relative site paths are resolved from here
import numpy as np
import pandas as pd

SITES = [
    dict(id="yungay", name="Yungay", role="benchmark", profile="mars_elysium", lat=-24.064, lon=-69.881),
    dict(id="pajonales", name="Salar de Pajonales", role="benchmark", profile="mars_elysium", lat=-25.144, lon=-68.820),
    dict(id="llullaillaco", name="Llullaillaco", role="control", profile="mars_elysium", lat=-24.720, lon=-68.537),
    dict(id="llaima_flows", name="Llaima, sector de coladas", role="candidate", profile="moon_tranquillitatis",
         lat=-38.692, lon=-71.729),
    dict(id="llaima_cone", name="Llaima, cono", role="contrast", profile="moon_tranquillitatis", lat=-38.692, lon=-71.729),
]


def _dist_km(lat0, lon0, lat, lon):
    p = np.pi / 180
    a = (np.sin((lat - lat0) * p / 2) ** 2 + np.cos(lat0 * p) * np.cos(lat * p) * np.sin((lon - lon0) * p / 2) ** 2)
    return 2 * 6371.0 * np.arcsin(np.sqrt(a))


def site_cells(site, grid, master=None, sites_dir=None):
    """-> (list of cell_ids, method): method is "polygon" or "pending_geometry"."""
    base = Path(sites_dir or CFG["paths"]["sites_dir"])
    gj = (base if base.is_absolute() else ROOT / base) / f"{site['id']}.geojson"
    if not gj.exists():
        return [], "pending_geometry"
    import geopandas as gpd
    g = gpd.read_file(gj).to_crs(4326)
    poly = g.union_all() if hasattr(g, "union_all") else g.unary_union
    pts = gpd.GeoSeries(gpd.points_from_xy(grid.lon_c, grid.lat_c), crs=4326)
    ids = grid.cell_id[pts.within(poly).values].tolist()
    if not ids:                       # polygon smaller than a 0.05 deg cell: the cell containing its centroid
        c = poly.centroid
        ids = [grid.cell_id.iloc[int(np.argmin(_dist_km(c.y, c.x, grid.lat_c.values, grid.lon_c.values)))]]
    return ids, "polygon"
