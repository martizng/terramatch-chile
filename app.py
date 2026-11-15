"""TerraMatch Chile — piloto web v0.7.

Lee exclusivamente resultados reales del motor Rojas v0.7. Las cifras y
percentiles representan los sectores cubiertos por cuatro teselas ASTER;
no se extrapolan a todo Chile. Ejecutar con: streamlit run app.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium

BASE = Path(__file__).resolve().parent

st.set_page_config(page_title="TerraMatch Chile | Planetary Analogues", page_icon="🌎", layout="wide")

st.markdown(
    """
<style>
.block-container {padding-top: 1.65rem; max-width: 1360px;}
.tm-hero {background: linear-gradient(125deg,#112a43 0%,#12596a 100%); color:white;
  padding: 29px 34px; border-radius: 17px; margin-bottom: 19px;}
.tm-hero h1 {color:white; margin:0 0 6px; font-size:2.25rem;}
.tm-hero p {color:#e7f2f5; margin:0; font-size:1.01rem;}
.tm-pill {display:inline-block; padding:5px 10px; border-radius:20px;
  background:#e4f4ef; color:#154f45; font-size:.8rem; font-weight:650;}
small {opacity:.88;}
</style>
""",
    unsafe_allow_html=True,
)

LABELS = {
    "es": {
        "subtitle": "Explorando la Tierra para comprender otros mundos",
        "intro": "Análisis exploratorio y explicable de similitud **topográfica**, no certificación de análogos planetarios.",
        "language": "Idioma / Language", "planet": "Perfil planetario", "view": "Sección",
        "home": "Resumen", "map": "Mapa de similitud", "sites": "Comparador de sitios", "validation": "Validación y datos",
        "pilot": "RESULTADOS PILOTO · MOTOR v0.7 · 4 TESELAS ASTER",
        "coverage": "Celdas con topografía ASTER", "scored": "Celdas puntuadas para este perfil",
        "cells": "Celdas de la grilla de referencia", "sites_count": "Sitios de evaluación",
        "map_title": "Dónde hay resultados calculados", "map_help": "El mapa muestra solamente celdas con similitud calculada. Las celdas excluidas por filtros o sin datos no reciben color de similitud.",
        "min_score": "Puntaje mínimo para mostrar", "show_sites": "Mostrar sitios piloto",
        "top": "Celdas mejor puntuadas dentro del área piloto", "top_note": "Estas posiciones describen solo las celdas puntuadas del piloto; no son un ranking nacional.",
        "status": "Estados del conjunto de datos", "all_cells_note": "Un filtro puede excluir una celda incluso si no tiene DEM ASTER; consulta también 'valid_frac' para identificar la cobertura topográfica.",
        "select_site": "Elige un sitio", "site_details": "Ficha del sitio", "site_metric": "Valor del sitio", "target_metric": "Referencia planetaria (mediana)",
        "site_score": "Similitud topográfica", "site_percentile": "Percentil dentro del piloto", "confidence": "Confianza", "coverage_data": "Cobertura de variables",
        "site_note": "Los polígonos de Pajonales y las coladas del Llaima son aproximaciones geológicas de escala 1:1.000.000; requieren verificación adicional.",
        "site_no_data": "No existen resultados de sitio para este perfil.", "vars": "Variables y comparación", "download": "Descargar celdas puntuadas (CSV)",
        "source": "Fuentes y método", "data_quality": "Revisión de calidad y limitaciones", "checks": "Pruebas de coherencia del modelo",
        "passed": "Cumple", "failed": "No cumple", "unavailable": "Sin verificar", "status_def": "Cómo interpretar los estados",
        "scored_label": "Calculado", "outside": "Fuera del filtro", "insufficient": "Datos insuficientes", "no_filter": "Sin datos del filtro",
        "warn": "Resultados preliminares: cobertura limitada a cuatro teselas ASTER, filtro volcánico pendiente de auditoría, máscaras NUM aún sin integración formal y calibración/validación en revisión.",
        "missing": "No se encontraron los archivos necesarios. Confirma que estás en la rama integracion-motor-rojas-v07 y que los CSV están en results/.",
        "repo": "Repositorio y metodología", "download_label": "Descargar CSV", "no_scored": "No hay celdas que cumplan este puntaje mínimo.",
        "method": "Tres indicadores calculados en ventanas de 5 km a escala común ~463 m: pendiente P90, relieve P95–P5 y rugosidad. Se aplica un filtro de aridez para Marte (IMERG ≤250 mm/año) o un filtro geológico volcánico para la Luna. La puntuación 0–100 representa únicamente similitud topográfica.",
        "validation_note": "Las pruebas fallidas se muestran expresamente; no modificamos los resultados para cumplir los criterios.",
    },
    "en": {
        "subtitle": "Explore Earth. Understand Other Worlds.",
        "intro": "Exploratory, explainable **topographic similarity** screening—not certification of planetary analogues.",
        "language": "Language / Idioma", "planet": "Planetary reference", "view": "View",
        "home": "Overview", "map": "Similarity map", "sites": "Site comparison", "validation": "Validation & data",
        "pilot": "PILOT RESULTS · ENGINE v0.7 · 4 ASTER TILES",
        "coverage": "Cells with ASTER terrain data", "scored": "Scored cells for this profile",
        "cells": "Cells in reference grid", "sites_count": "Evaluation sites",
        "map_title": "Where scores were actually calculated", "map_help": "Only cells with computed similarity scores are colored. Filtered-out and data-deficient cells are not assigned low scores.",
        "min_score": "Minimum similarity to display", "show_sites": "Show pilot sites",
        "top": "Top-scoring cells within pilot coverage", "top_note": "Ranks represent scored pilot cells only, not a national ranking.",
        "status": "Dataset status counts", "all_cells_note": "A filter may exclude a cell that also lacks ASTER coverage; consult 'valid_frac' for terrain-data availability.",
        "select_site": "Select a site", "site_details": "Site profile", "site_metric": "Site value", "target_metric": "Planetary reference (median)",
        "site_score": "Terrain similarity", "site_percentile": "Percentile within pilot", "confidence": "Confidence", "coverage_data": "Variable coverage",
        "site_note": "Pajonales and Llaima lava-flow polygons are geological proxies at 1:1,000,000 scale; additional verification is required.",
        "site_no_data": "No site-level results are available for this profile.", "vars": "Terrain metrics", "download": "Download scored cells (CSV)",
        "source": "Sources and methods", "data_quality": "Quality review and limitations", "checks": "Model coherence checks",
        "passed": "Passed", "failed": "Failed", "unavailable": "Not verified", "status_def": "How to interpret status flags",
        "scored_label": "Scored", "outside": "Outside filter", "insufficient": "Insufficient data", "no_filter": "Missing filter data",
        "warn": "Preliminary results: limited coverage from four ASTER tiles; volcanic filter awaits source review, ASTER NUM provenance masks are not yet integrated, and model validation is ongoing.",
        "missing": "Required files were not found. Check branch integracion-motor-rojas-v07 and the results/ CSV files.",
        "repo": "Repository and methodology", "download_label": "Download CSV", "no_scored": "No scored cells meet this threshold.",
        "method": "Three terrain indicators calculated in 5 km windows at a common ~463 m resolution: 90th-percentile slope, P95–P5 local relief, and slope roughness. An aridity filter applies to Mars (IMERG ≤250 mm/year) and a volcanic-unit filter applies to the Moon. The 0–100 score represents topographic similarity only.",
        "validation_note": "Failed checks are shown explicitly. Scores have not been adjusted to force the desired outcome.",
    },
}

@st.cache_data(show_spinner=False)
def read_results(profile_key: str) -> pd.DataFrame:
    paths = {"mars": "mars_scores_web.csv", "moon": "moon_scores_web.csv"}
    df = pd.read_csv(BASE / "results" / paths[profile_key])
    # Distinguish absence of a score from a genuine zero score.
    df["S"] = pd.to_numeric(df["S"], errors="coerce")
    return df


@st.cache_data(show_spinner=False)
def read_sites() -> pd.DataFrame:
    return pd.read_csv(BASE / "results" / "sites_summary.csv")


@st.cache_data(show_spinner=False)
def read_targets() -> list[dict]:
    with open(BASE / "data" / "targets.json", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def read_validation() -> dict:
    with open(BASE / "results" / "validation.json", encoding="utf-8") as f:
        return json.load(f)


def fnum(value, digits=1) -> str:
    if pd.isna(value):
        return "—"
    return f"{float(value):,.{digits}f}"


def status_name(key: str, tr: dict) -> str:
    return {
        "scored": tr["scored_label"],
        "outside_filter": tr["outside"],
        "insufficient_data": tr["insufficient"],
        "no_filter_data": tr["no_filter"],
    }.get(str(key), str(key))


def value_colour(score: float) -> str:
    if score >= 75:
        return "#1cb8a1"
    if score >= 50:
        return "#42a6cf"
    if score >= 25:
        return "#ecae4e"
    return "#d97b72"


def make_map(rows: pd.DataFrame, sites: pd.DataFrame, include_sites: bool, tr: dict):
    # The map only visualizes rows with actual scores; excluded cells never get a score color.
    m = folium.Map(location=[-31.0, -70.4], zoom_start=5, tiles="CartoDB positron", control_scale=True)
    for r in rows.itertuples(index=False):
        score = float(r.S)
        color = value_colour(score)
        folium.CircleMarker(
            [float(r.lat_c), float(r.lon_c)],
            radius=5,
            color=color,
            weight=1,
            fill=True,
            fill_color=color,
            fill_opacity=.76,
            tooltip=(f"Cell {int(r.cell_id)} | Score {score:.1f}/100"),
            popup=(f"<b>Cell {int(r.cell_id)}</b><br>Score: {score:.2f}/100"
                   f"<br>Coverage: {float(r.coverage):.0%}"
                   f"<br>Confidence: {escape(str(r.confidence))}"),
        ).add_to(m)
    if include_sites:
        for r in sites.itertuples(index=False):
            folium.Marker(
                location=[float(r.ref_lat), float(r.ref_lon)],
                tooltip=str(r.name),
                popup=(f"<b>{escape(str(r.name))}</b><br>Score: {fnum(r.S)}"
                       f"<br>Percentile: {fnum(r.percentile)}"
                       f"<br>Confidence: {escape(str(r.confidence))}"),
                icon=folium.Icon(color="darkblue", icon="info-sign"),
            ).add_to(m)
    return m


language = st.sidebar.selectbox("Language / Idioma", ["Español", "English"], index=0)
lang = "es" if language == "Español" else "en"
tr = LABELS[lang]
planet = st.sidebar.radio(tr["planet"], ["Marte" if lang == "es" else "Mars", "Luna" if lang == "es" else "Moon"])
profile = "mars" if planet in {"Marte", "Mars"} else "moon"
view = st.sidebar.radio(tr["view"], [tr["home"], tr["map"], tr["sites"], tr["validation"]])
st.sidebar.caption(tr["pilot"])
st.sidebar.markdown("[GitHub](https://github.com/martizng/terramatch-chile) · [Methodology](https://github.com/martizng/terramatch-chile/blob/main/docs/methodology.md)")

try:
    df = read_results(profile)
    site_data = read_sites()
    targets = read_targets()
    validation = read_validation()
except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as err:
    st.error(f"{tr['missing']}\n\n{err}")
    st.stop()

profile_id = "mars_elysium" if profile == "mars" else "moon_tranquillitatis"
planetary_target = next((p for p in targets if p.get("id") == profile_id), None)
selected_sites = site_data.loc[site_data["profile"] == profile_id].copy()
scored = df.loc[df["status"].eq("scored") & df["S"].notna()].copy()
with_aster = int(df[["slope_p90_deg", "relief_m", "rough_sd_deg"]].notna().all(axis=1).sum())

st.markdown(
    f'<div class="tm-hero"><h1>🌎 TerraMatch Chile</h1>'
    f'<p>{escape(tr["subtitle"])}</p></div>', unsafe_allow_html=True
)
st.caption(tr["pilot"])
st.warning(tr["warn"])

if view == tr["home"]:
    st.markdown(tr["intro"])
    c1,c2,c3,c4 = st.columns(4)
    c1.metric(tr["coverage"], f"{with_aster:,}")
    c2.metric(tr["scored"], f"{len(scored):,}")
    c3.metric(tr["cells"], f"{len(df):,}")
    c4.metric(tr["sites_count"], str(len(selected_sites)))
    st.subheader(tr["source"])
    st.write(tr["method"])
    c1,c2 = st.columns([1,1])
    with c1:
        st.subheader(tr["status"])
        counts = df["status"].value_counts()
        status_df = pd.DataFrame({"status": [status_name(s,tr) for s in counts.index], "cells":counts.values})
        st.dataframe(status_df, use_container_width=True, hide_index=True)
        st.caption(tr["all_cells_note"])
    with c2:
        st.subheader(tr["top"])
        st.dataframe(
            scored.nsmallest(min(len(scored),10), "rank")[["cell_id","lat_c","lon_c","S","coverage","confidence"]].rename(columns={"S":"score"}).round(2),
            use_container_width=True, hide_index=True
        )
        st.caption(tr["top_note"])

elif view == tr["map"]:
    st.subheader(tr["map_title"])
    st.info(tr["map_help"])
    c1,c2 = st.columns([3,1])
    with c1:
        score_threshold = st.slider(tr["min_score"], min_value=0, max_value=100, value=0, step=5)
    with c2:
        show_sites = st.checkbox(tr["show_sites"], value=True)
    shown = scored.loc[scored["S"] >= score_threshold]
    if shown.empty and not (show_sites and not selected_sites.empty):
        st.info(tr["no_scored"])
    else:
        st_folium(make_map(shown,selected_sites,show_sites,tr), height=515, width=None, returned_objects=[])
    st.caption(tr["top_note"])
    st.markdown("**0–24** 🟥 · **25–49** 🟨 · **50–74** 🟦 · **75–100** 🟩")
    st.dataframe(
        shown.sort_values("S",ascending=False)[["cell_id","lat_c","lon_c","S","coverage","confidence","rank"]].head(40).round(2),
        use_container_width=True,hide_index=True
    )
    st.download_button(tr["download_label"], data=shown.to_csv(index=False).encode("utf-8-sig"),
                       file_name=f"terramatch_{profile}_scored_pilot.csv", mime="text/csv")

elif view == tr["sites"]:
    st.subheader(tr["site_details"])
    if selected_sites.empty:
        st.info(tr["site_no_data"])
    else:
        names = selected_sites["name"].tolist()
        site_name = st.selectbox(tr["select_site"],names)
        site = selected_sites.loc[selected_sites["name"] == site_name].iloc[0]
        c1,c2,c3,c4 = st.columns(4)
        c1.metric(tr["site_score"], f"{fnum(site['S'])}/100")
        c2.metric(tr["site_percentile"], f"{fnum(site['percentile'])}")
        c3.metric(tr["confidence"], str(site["confidence"]))
        c4.metric(tr["coverage_data"], f"{float(site['coverage']):.0%}")
        values = [
            ("Slope P90 (°)", "slope_p90_deg"),
            ("Local relief P95–P5 (m)", "relief_m"),
            ("Roughness (°)", "rough_sd_deg"),
        ]
        table = []
        for title,key in values:
            tgt = (planetary_target or {}).get("variables",{}).get(key,{})
            table.append({
                "Metric":title,
                tr["site_metric"]:fnum(site[f"{key}_value"],2),
                tr["target_metric"]:fnum(tgt.get("value"),2),
                "Target interval":f"{fnum(tgt.get('low'),2)} – {fnum(tgt.get('high'),2)}",
            })
        st.subheader(tr["vars"])
        st.dataframe(pd.DataFrame(table),hide_index=True,use_container_width=True)
        st.caption(f"{site['name']} · {site['role']} · {int(site['n_scored'])} scored grid cell(s)")
        st.warning(tr["site_note"])
        st.dataframe(selected_sites[["name","role","S","percentile","coverage","confidence"]].round(2),
                     use_container_width=True,hide_index=True)

else:
    st.subheader(tr["data_quality"])
    st.write(tr["method"])
    st.warning(tr["warn"])
    st.subheader(tr["checks"])
    checks = validation.get(profile,{}).get("checks",{})
    validation_rows = []
    for name, result in checks.items():
        ok = result.get("passed")
        status = tr["passed"] if ok is True else tr["failed"] if ok is False else tr["unavailable"]
        validation_rows.append({"Check":name,"Value":result.get("value"),"Result":status})
    st.dataframe(pd.DataFrame(validation_rows),hide_index=True,use_container_width=True)
    st.caption(tr["validation_note"])
    st.subheader(tr["status_def"])
    st.write(f"**scored:** {tr['scored_label']}; **outside_filter:** {tr['outside']}; "
             f"**insufficient_data:** {tr['insufficient']}; **no_filter_data:** {tr['no_filter']}.")
    st.caption(tr["all_cells_note"])
    st.json({"profile":profile_id,"valid_aster_cells":with_aster,"scored_cells":len(scored),
             "all_grid_cells":len(df),"filter":validation.get(profile,{}).get("filter"),
             "methodology_version":"2.0","motor_version":"0.7"})

st.divider()
st.caption("TerraMatch Chile · NASA Space Apps Challenge 2026 · Pilot outputs only · Data and model limitations apply")
