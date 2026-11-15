# Motor TerraMatch v0.6: ajustes pedidos por Marti (domingo 15, 14:10)

Se suma a `CAMBIOS_v0.5.md`. Carpeta completa: incluye `src/features/` (con `chile_features.py`, UTM 18S/19S) y `src/grid/`.

| # | Archivo | Cambio |
|---|---|---|
| 1 | todo el paquete | ZIP completo `terramatch_v06.zip`, armado y probado desde una carpeta limpia (sin `__pycache__`). Incluye `src/features/`, `src/grid/` y `tests/`. |
| 2 | `src/comparison.py` | Monte Carlo con **rangos promedio** (`scipy.stats.rankdata(method="average")`): las celdas con D idéntico reciben el mismo percentil. Se eliminó `argsort().argsort()`. Nueva prueba 12b. |
| 3 | `src/sites.py`, `config` | Los sitios se leen de **`data/chile/sites/<id>.geojson`** (config `paths.sites_dir`; se puede cambiar con `--sites-dir`). |
| 4 | `src/sites.py`, `src/validation.py` | **Sin polígono verificado, el sitio queda `pending_geometry`**: sin celdas, sin puntaje y su prueba de validación con `passed: null`. Ya no se generan círculos ni anillos. `validation.json` lista los sitios pendientes en `pending_geometry_sites`. |
| 5 | `config`, README | IMERG se lee desde **`data/chile/processed/imerg_precip_2001_2024.tif`** (mismo archivo del repositorio). |

## Polígonos de los 5 sitios (`data/chile/sites/`)

| Sitio | Método | Celdas de la grilla |
|---|---|---|
| Yungay | Cuadrado de 5 km (regla del doc, sección 5.2) | 1 |
| Salar de Pajonales | Unidad MQs (FID 3617) del Mapa Geológico 1:1M que contiene el salar, 104,65 km² | 4 |
| Llullaillaco | Círculo de 8 km alrededor de la cumbre (regla del doc) | 4 |
| Coladas del Llaima | Unidad Q3i (FID 10388) menos el círculo de 3 km del cono, 262,73 km², sin criterio de pendiente | 11 |
| Cono del Llaima | Círculo de 3 km (regla del doc) | 1 |

Pajonales y las coladas vienen del mapa geológico 1:1.000.000 (copia CIGIDEN de SERNAGEOMIN), no de una digitalización sobre imagen satelital; se declara como limitación. Si el equipo no los acepta como verificados, basta con quitar esos dos archivos: el motor los deja `pending_geometry`.

## Pruebas ejecutadas (carpeta limpia)

`py tests/test_pipeline_synthetic.py` desde una copia limpia del ZIP: **todas las verificaciones aprobadas** (11 bloques más la ejecución completa del motor) (datos sintéticos; verifican la lógica, no son resultados). Nuevas en v0.6:
- 12: sin polígonos, los 5 sitios quedan `pending_geometry`, sin puntaje y con las pruebas en `passed: null`.
- 12b: en el Monte Carlo, celdas idénticas reciben percentiles idénticos.
- 7: la ejecución completa usa polígonos sintéticos generados por la propia prueba (no se usan círculos del motor).

AI-Assisted: código y resumen redactados con Claude; revisados y ejecutados por el equipo. Ningún valor de datos fue generado por IA.
