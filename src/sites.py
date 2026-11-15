"""Pilot site selection using supplied, explicit geometries. No inferred polygons.

Provided in data/chile/sites/: sites_chile.gpkg or per-site GeoJSON.
Pajonales and Llaima flows remain pending until a verified polygon is supplied.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SITES = [
    dict(id="yungay", name="Yungay", role="benchmark", profile="mars_elysium",
         lat=-24.064, lon=-69.881),
    dict(id="pajonales", name="Salar de Pajonales", role="benchmark", profile="mars_elysium",
         lat=-25.144, lon=-68.820),
    dict(id="llullaillaco", name="Llullaillaco", role="control", profile="mars_elysium",
         lat=-24.720, lon=-68.537),
    dict(id="llaima_flows", name="Llaima, sector de coladas", role="candidate", profile="moon_tranquillitatis",
         lat=-38.692, lon=-71.729),
    dict(id="llaima_cone", name="Llaima, cono", role="contrast", profile="moon_tranquillitatis",
         lat=-38.692, lon=-71.729),
]


def _load_polygon(site, sites_dir):
    import geopandas as gpd
    folder = Path(sites_dir)
    geojson = folder / f"{site['id']}.geojson"
    if geojson.exists():
        g = gpd.read_file(geojson)
    elif (folder / "sites_chile.gpkg").exists():
        g = gpd.read_file(folder / "sites_chile.gpkg", layer="sites")
        if "site_id" not in g:
            raise ValueError("sites_chile.gpkg needs site_id field")
        g = g.loc[g.site_id == site["id"]]
    else:
        return None
    if g.empty:
        return None
    if "site_id" in g and not (g.site_id.astype(str) == site["id"]).all():
        raise ValueError(f"Incorrect site_id for {site['id']} polygon")
    if g.crs is None:
        raise ValueError(f"Missing CRS for {site['id']} polygon")
    if not g.geometry.is_valid.all() or g.geometry.is_empty.any():
        raise ValueError(f"Invalid/empty geometry for {site['id']}")
    return g.to_crs(4326).geometry.union_all()


def site_cells(site, grid, master=None, sites_dir="data/chile/sites"):
    """Return (cell_ids, method). No fallback to invented circles/annuli."""
    poly = _load_polygon(site, sites_dir)
    if poly is None:
        return [], "pending_geometry"
    import geopandas as gpd
    pts = gpd.GeoSeries(gpd.points_from_xy(grid.lon_c, grid.lat_c), crs=4326)
    ids = grid.loc[pts.intersects(poly).values, "cell_id"].tolist()
    if not ids:
        return [], "polygon_without_grid_centers"
    return ids, "polygon"
