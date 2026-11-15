# Motor TerraMatch v0.5: correcciones pedidas por Marti (domingo 15, 12:40)

## Correcciones

| # | Archivo | Antes | Ahora |
|---|---|---|---|
| 1 | `src/analysis.py` | Si el IQR y la desviación estándar valían 0, se usaba una escala artificial de 1. | Se usa el IQR; si vale 0, la desviación estándar (doc v2.0, Fase 3); si ambas valen 0, **la variable se excluye**: queda como faltante en todas las celdas (baja la cobertura y la confianza) y se informa en `validation.json` (`scales`, `excluded_variables`). |
| 2 | `src/run_pipeline.py`, `src/analysis.py` | Si faltaba la capa volcánica, el filtro lunar se desactivaba solo. | **El filtro nunca se desactiva.** Sin capa, el perfil queda `pending_filter_data` y no se rankea. Las celdas sin dato del filtro quedan `no_filter_data` (S vacío), distintas de `outside_filter`. |
| 3 | `src/features/chile_features.py` | Todo Chile en UTM 19S, con el error de escala supuesto. | Cada celda se procesa en su zona: **UTM 18S al oeste de 72° O y 19S al este**. El error de escala se calcula para cada celda con pyproj (columna `scale_error`) y la ejecución se detiene si supera el 1%. En la grilla real el máximo es **0,053%** (con una sola zona 19S habría sido 0,276%). |
| 4 | `src/features/chile_features.py` | Una ventana de 5 km con 4 píxeles válidos ya daba valores; el mar podía leerse como terreno plano. | Los píxeles ≤ 0 m (mar en ASTER) y los nodata quedan vacíos. Una ventana con menos del 50% de píxeles válidos da NaN (columna `valid_frac`). **Sin cobertura nunca se convierte en similitud baja ni alta.** Acepta el mosaico ASTER o varias teselas. |
| 5 | `src/sites.py`, `src/validation.py` | Las geometrías aproximadas (círculos) se usaban como si fueran los sitios. | Cada sitio indica `geometry = polygon` o `approximate`. Con geometría aproximada, la validación queda `provisional: true`. Solo es definitiva con los polígonos de `data/sites/<id>.geojson`. |
| 6 | `src/sites.py` | El sector de coladas del Llaima se elegía por pendiente ≤ 15° y luego se comparaba por pendiente: la prueba lunar se cumplía por construcción. | Anillo de 3 a 15 km **sin criterio de pendiente**, marcado como aproximado hasta tener el polígono de las coladas. |
| 7 | `config/terramatch_config.json`, `chile_features.py`, `run_pipeline.py` | Una sola columna de precipitación. | **GPM IMERG Final V07 es el filtro principal** (`--precip` → `precip_mm_yr`). CR2MET-IMERG entra solo como análisis complementario (`--precip-alt` → `precip_alt_mm_yr`), y el criterio volcánico amplio igual (`--volcanic-broad`). Los resultados complementarios van en `validation.json → sensitivity` y en `*_profile_<id>.csv`; nunca reemplazan al principal. |

Todas las reglas nuevas están en `config/terramatch_config.json` (`normalization`, `chile_dem`, `sensitivity_filters`, `sites_rule`).

## Pruebas ejecutadas

`py tests/test_pipeline_synthetic.py`, ejecutado y aprobado en el contenedor de trabajo y en la PC de Rojas. Las pruebas usan **datos sintéticos** y solo verifican la lógica; no son resultados.

1. La configuración coincide con el doc v2.0.
2. La pendiente y el remuestreo recuperan pendientes conocidas.
3. Los perfiles reales de Marte (MOLA) y la Luna (SLDEM2015) están calculados y con fuente; un perfil pendiente se rechaza.
4. Los perfiles se calculan desde ventanas del DEM.
5. Funcionan la distancia, la similitud, la cobertura (2 de 3 variables) y los niveles de confianza.
6. La ejecución completa genera todos los CSV y `validation.json`.
7. Un perfil pendiente se informa y no se calcula.
8. **Nueva:** una variable con IQR = 0 y SD = 0 se excluye y se informa.
9. **Nueva:** sin capa volcánica, la Luna queda `pending_filter_data`, sin ranking, y Marte se calcula igual.
10. **Nueva:** las celdas sin dato del filtro quedan `no_filter_data` con S vacío.
11. **Nueva:** los sitios aproximados se marcan y la validación queda provisional.
12. **Nueva:** un DEM sintético que cruza 72° O se procesa en 18S y 19S, la pendiente de 5° se recupera en ambas zonas, el mar y la franja sin DEM quedan NaN, y el error de escala máximo es 0,044%.

Adicional: los insumos reales de Pancho (precipitación y unidades volcánicas) se leen sin errores sobre la grilla real de 31.660 celdas.

## Pendiente para la primera prueba con datos reales

- `aster_chile.tif` (Pancho, en proceso).
- `imerg_precip_2001_2024.tif`: IMERG Final V07 solo, para todas las celdas (Pancho ya lo calculó para armar el raster combinado). Sin este archivo, Marte queda `pending_filter_data` a propósito.
- Polígonos de los sitios en `data/sites/` (opcional para la primera prueba; sin ellos, la validación es provisional).

Comando de la primera prueba:

```
py src/features/chile_features.py --dem data/raw/aster_chile.tif --precip data/raw/imerg_precip_2001_2024.tif --precip-alt data/raw/precip_annual_cr2met_imerg.tif --volcanic data/raw/volcanic_units.tif --volcanic-broad data/raw/volcanic_units_broad.tif
py src/run_pipeline.py
```

AI-Assisted: código y este resumen redactados con Claude; revisados y ejecutados por el equipo. Ningún valor de datos fue generado por IA.
