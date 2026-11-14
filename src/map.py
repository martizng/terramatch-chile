
"""
map.py

Módulo de visualización geográfica de TerraMatch Chile.

Su objetivo es generar mapas interactivos para explorar
los ambientes y sitios de estudio seleccionados en Chile.

Pendiente:
- Integrar datos geoespaciales del equipo.
- Incorporar capas de ambientes y unidades de análisis.
- Agregar filtros geográficos.
- Visualizar variables ambientales disponibles.
"""

import folium


def create_base_map():
    """
    Crea un mapa base centrado en Chile.

    Returns
    -------
    folium.Map
        Mapa interactivo inicial.
    """

    mapa = folium.Map(
        location=[-30.0, -71.0],
        zoom_start=4,
        tiles="OpenStreetMap"
    )

    return mapa
