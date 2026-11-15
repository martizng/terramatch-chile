"""Pure data and offline cartographic helpers for TerraMatch Chile's Streamlit UI.

All scientific values come from Rojas v0.7 CSV/JSON files. This module does NOT
recompute planetary scores, infer missing values, or substitute excluded cells.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'results'
VISUALS = ROOT / 'assets' / 'visuals'

FILES = {
    'mars': RESULTS / 'mars_scores_web.csv',
    'moon': RESULTS / 'moon_scores_web.csv',
}

REQUIRED_COLUMNS = {
    'cell_id', 'lat_c', 'lon_c', 'status', 'S', 'valid_frac',
    'slope_p90_deg', 'relief_m', 'rough_sd_deg', 'confidence', 'coverage',
}

SITE_IMAGES = {
    'yungay': 'yungay_aster.jpg',
    'pajonales': 'pajonales_aster.jpg',
    'llullaillaco': 'llullaillaco_aster.jpg',
    'llaima_flows': 'llaima_flows_aster.jpg',
    'llaima_cone': 'llaima_cone_aster.jpg',
}
SITE_EXPLANATIONS = {
    'yungay': {
        'es': 'Referencia de aridez para el perfil marciano. Su percentil topográfico no alcanzó el umbral previsto; la aridez y el relieve no son lo mismo.',
        'en': 'Aridity reference for the Martian profile. Its terrain percentile missed the predefined threshold: aridity and relief are not equivalent.',
    },
    'pajonales': {
        'es': 'Referencia de depósitos salinos/evaporíticos. El contorno de estudio es un proxy geológico regional, no la delimitación precisa del salar.',
        'en': 'Salt/evaporite reference. The study footprint is a regional geological proxy, not a precise salt-flat boundary.',
    },
    'llullaillaco': {
        'es': 'Sector montañoso de contraste: su baja similitud topográfica es consistente con el comportamiento esperado de un control negativo.',
        'en': 'High-mountain contrast area: its low terrain similarity is consistent with the expected negative-control behavior.',
    },
    'llaima_flows': {
        'es': 'Candidato exploratorio lunar: la zona representada como coladas supera al cono, pero su polígono es un proxy geológico, pendiente de corroboración.',
        'en': 'Exploratory lunar candidate: the mapped flow area scores above the cone, but its polygon is a geological proxy awaiting confirmation.',
    },
    'llaima_cone': {
        'es': 'Contraste interno del perfil lunar. Su topografía más abrupta ayuda a interpretar diferencias con los sectores de coladas.',
        'en': 'Internal lunar-profile contrast area. Its steeper terrain helps explain differences with the mapped lava-flow sectors.',
    },
}


def read_data(base: Path = ROOT) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, list[dict], dict]:
    scores: dict[str, pd.DataFrame] = {}
    for profile, path in FILES.items():
        location = base / path.relative_to(ROOT)
        df = pd.read_csv(location)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f'{location.name} missing columns: {sorted(missing)}')
        if df['cell_id'].duplicated().any():
            raise ValueError(f'Duplicated cell_id in {location.name}')
        for col in ['S', 'coverage', 'valid_frac', 'lat_c', 'lon_c']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        invalid_scored = df['status'].eq('scored') & df['S'].isna()
        invalid_unscored = ~df['status'].eq('scored') & df['S'].notna()
        if invalid_scored.any() or invalid_unscored.any():
            raise ValueError(f'Invalid score/status combinations in {location.name}')
        scores[profile] = df
    sites = pd.read_csv(base / 'results' / 'sites_summary.csv')
    with open(base / 'data' / 'targets.json', encoding='utf-8') as handle:
        targets = json.load(handle)
    with open(base / 'results' / 'validation.json', encoding='utf-8') as handle:
        validation = json.load(handle)
    return scores, sites, targets, validation


def scored_cells(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['status'].eq('scored') & df['S'].notna()].copy()


def astercells(df: pd.DataFrame) -> pd.DataFrame:
    return df[df[['slope_p90_deg', 'relief_m', 'rough_sd_deg']].notna().all(axis=1)].copy()


def status_summary(df: pd.DataFrame) -> dict[str, int]:
    return {key: int(value) for key, value in df['status'].value_counts().items()}


def site_image(site_id: str) -> Path:
    return VISUALS / SITE_IMAGES.get(site_id, 'yungay_aster.jpg')


def iter_rings(geometry: dict) -> Iterable[list[list[float]]]:
    if geometry.get('type') == 'Polygon':
        for ring in geometry.get('coordinates', [])[:1]:
            yield ring
    elif geometry.get('type') == 'MultiPolygon':
        for polygon in geometry.get('coordinates', []):
            for ring in polygon[:1]:
                yield ring


def make_terrain_map(df: pd.DataFrame, sites: pd.DataFrame, *, mode='score', region='all',
                     min_score=0.0, show_sites=True, locale='es') -> go.Figure:
    """Responsive, interactive lat/lon plot with a local (no tile server) Chile outline.

    `score` mode: only real scored cells receive a numeric color.
    `coverage` mode: only cells with ASTER terrain metrics are shown, categorized by status.
    """
    path = VISUALS / 'chile_outline.geojson'
    with open(path, encoding='utf-8') as handle:
        boundary = json.load(handle)['features'][0]['geometry']
    fig = go.Figure()
    xs, ys = [], []
    for ring in iter_rings(boundary):
        xs.extend([xy[0] for xy in ring] + [None])
        ys.extend([xy[1] for xy in ring] + [None])
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', fill='toself', fillcolor='#E5EFF1',
                             line={'color': '#90ADB5', 'width': 1.05}, hoverinfo='skip',
                             name='Chile', showlegend=False))
    if mode == 'score':
        rows = scored_cells(df)
        rows = rows[rows['S'] >= min_score]
        if len(rows):
            fig.add_trace(go.Scatter(
                x=rows['lon_c'], y=rows['lat_c'], mode='markers',
                marker={'size': 8, 'opacity': .85, 'color': rows['S'],
                        'colorscale': [[0, '#E89A5B'], [.35, '#E7CF80'], [.65, '#67BFC4'], [1, '#19566F']],
                        'cmin': 0, 'cmax': 100, 'colorbar': {'title': 'Score /100', 'thickness': 12, 'len': .58}},
                customdata=rows[['cell_id', 'coverage', 'confidence']].astype(str).to_numpy(),
                hovertemplate=('<b>Celda %{customdata[0]}</b><br>' if locale=='es' else '<b>Cell %{customdata[0]}</b><br>')
                + 'Score: %{marker.color:.1f}/100<br>'
                + ('Cobertura: ' if locale=='es' else 'Coverage: ') + '%{customdata[1]}<br>'
                + ('Confianza: ' if locale=='es' else 'Confidence: ') + '%{customdata[2]}<extra></extra>',
                showlegend=False, name='Score'))
    else:
        # Important: 30k grid positions without ASTER are deliberately NOT plotted.
        rows = astercells(df)
        palette = [('scored', '#147E8C'), ('outside_filter','#C89A56'),
                   ('insufficient_data','#8A94A6'), ('no_filter_data','#9F74AE')]
        labels_es={'scored':'Con puntaje','outside_filter':'Fuera del filtro','insufficient_data':'Datos insuficientes','no_filter_data':'Falta filtro'}
        labels_en={'scored':'Scored','outside_filter':'Outside filter','insufficient_data':'Insufficient data','no_filter_data':'Missing filter data'}
        labels=labels_es if locale=='es' else labels_en
        for key,color in palette:
            sub=rows[rows['status'].eq(key)]
            if not sub.empty:
                fig.add_trace(go.Scatter(x=sub['lon_c'], y=sub['lat_c'], mode='markers',
                    marker={'size':8,'color':color,'opacity':.85}, name=f'{labels[key]} ({len(sub):,})',
                    customdata=sub[['cell_id','valid_frac']].astype(str).to_numpy(),
                    hovertemplate='<b>%{customdata[0]}</b><br>ASTER valid_frac=%{customdata[1]}<extra></extra>'))
    if show_sites:
        fig.add_trace(go.Scatter(x=sites['ref_lon'], y=sites['ref_lat'], mode='markers+text',
            text=sites['name'],textposition='top right',textfont={'size':10,'color':'#17354F'},
            marker={'size':14,'symbol':'diamond','color':'#E86B4D','line':{'width':2,'color':'#FFFFFF'}},
            customdata=sites[['S','percentile','confidence']].astype(str).to_numpy(),
            hovertemplate='<b>%{text}</b><br>Score: %{customdata[0]}<br>Percentile: %{customdata[1]}<br>Confidence: %{customdata[2]}<extra></extra>',
            showlegend=True,name='Sitios piloto' if locale=='es' else 'Pilot sites'))
    bounds={'all':((-76.5,-65.5),(-56.2,-17)),
            'north':((-71.2,-67.1),(-26.8,-22.4)),
            'south':((-73.4,-70.3),(-40.2,-37.3))}
    xb,yb=bounds.get(region,bounds['all'])
    fig.update_xaxes(range=xb,visible=False,showgrid=False,zeroline=False)
    fig.update_yaxes(range=yb,visible=False,showgrid=False,zeroline=False,scaleanchor='x',scaleratio=1)
    fig.update_layout(height=590 if region=='all' else 520, margin={'l':5,'r':5,'t':6,'b':5},
        paper_bgcolor='#F6FAFB',plot_bgcolor='#F6FAFB',
        legend={'orientation':'h','yanchor':'top','y':-0.03,'x':0},
        hoverlabel={'bgcolor':'#123A4B','font':{'color':'white','size':12}},
        dragmode='zoom',font={'family':'Arial,sans-serif','color':'#183849'})
    return fig
