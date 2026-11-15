# TerraMatch Chile — Motor analítico v0.7 (Rojas)

Implementa las reglas del documento técnico v2.0. **Todas las reglas están en `config/terramatch_config.json`**; el código no tiene valores fijos.

| Parámetro (doc v2.0) | Valor en la configuración |
|---|---|
| Variables del puntaje | Pendiente P90, relieve local P95–P5, rugosidad |
| Pesos iniciales | 1/3 cada una |
| Resolución común | 463 m (MOLA MEGDR 128 ppd) |
| Ventana local | 5 km |
| Grilla nacional | EPSG:4326, 0,05° |
| Cobertura mínima | 2 de las 3 variables (0,5 del peso) |
| Escala | IQR; si vale 0, desviación estándar; si ambas valen 0, la variable se excluye |
| Proyección para la pendiente | UTM 18S / 19S según la celda; error de escala máximo 0,053% |
| Filtro de Marte | GPM IMERG Final V07 ≤ 250 mm/año (CR2MET-IMERG solo complementario) |
| Filtro de la Luna | Unidades volcánicas, criterio estricto (amplio solo complementario); nunca se desactiva |
| Monte Carlo | 500 iteraciones |
| Estabilidad | p_top y percentiles de ranking p05–p95 |
| Confianza | Alta: 3 variables y p_top ≥ 0,7 · Media: ≥ 2 variables y p_top ≥ 0,3 · Baja: el resto |

## Estructura

```
config/terramatch_config.json    reglas del doc v2.0
src/analysis.py                  distancia y similitud por variable, similitud global, cobertura, filtros
src/comparison.py                estabilidad del ranking (Monte Carlo), nivel de confianza, resumen por sitio
src/validation.py                pruebas de la Fase 5
src/run_pipeline.py              ejecuta todo y escribe results/
src/features/                    variables de relieve, perfiles planetarios (build_targets.py), variables de Chile
src/grid/make_grid.py            grilla nacional
src/sites.py                     sitios de la sección 5.2
notebooks/exploratory_analysis.ipynb
data/targets.json                perfiles de Marte y Luna (calculados)
data/processed/grid.csv          grilla oficial, 31.660 celdas
results/                         plantillas con encabezados, SIN resultados
tests/test_pipeline_synthetic.py prueba de lógica con datos sintéticos (nunca son resultados)
```

## Estado (domingo 15, 12:40)

- **Perfiles planetarios calculados:** Marte desde MOLA MEGDR (5 de 25 ventanas, solo 30,6% de medición directa) y la Luna desde SLDEM2015 (25 de 25 ventanas). Detalle en `data/targets.json`.
- **Correcciones:** ver `CAMBIOS_v0.5.md` y `CAMBIOS_v0.6.md`.
- **Sitios:** polígonos de los 5 sitios en `data/chile/sites/`. Un sitio sin polígono queda `pending_geometry` (sin círculos aproximados).
- **Primera comparación real hecha** con 4 teselas ASTER piloto: ver `RESULTADOS_v0.7.md`. `results/` contiene resultados reales.
- Si una prueba de validación no se cumple, `validation.json` lo informa tal cual. Si falta el polígono de un sitio, su prueba queda pendiente (`passed: null`). Los resultados no se ajustan.

## Uso

```
py -m pip install numpy pandas scipy rasterio geopandas pyproj matplotlib scikit-learn jupyter
py tests/test_pipeline_synthetic.py
py src/features/build_targets.py --mars data/raw/elysium_mola_dem.tif --mars-count data/raw/elysium_mola_counts.tif
py src/features/build_targets.py --moon data/raw/tranquillitatis_sldem2015_dem.tif
py src/features/chile_features.py --dem "data/raw/aster_gdem_v3/*_dem.tif" --precip data/chile/processed/imerg_precip_2001_2024.tif --precip-alt data/raw/precip_annual_cr2met_imerg.tif --volcanic data/raw/volcanic_units.tif --volcanic-broad data/raw/volcanic_units_broad.tif
py src/run_pipeline.py
```

AI-Assisted: código redactado con Claude; revisado, ejecutado y mantenido por el equipo. Ningún valor de datos fue generado por IA.
