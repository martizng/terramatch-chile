# results/

Estos archivos son **plantillas sin datos**: solo tienen los encabezados que leerá la interfaz.
Se sobrescriben al correr `python src/run_pipeline.py` con los datos reales. No contienen resultados.

| Archivo | Columnas principales |
|---|---|
| `{mars,moon}_profile.csv` | `d_*` distancia por variable, `s_*` similitud por variable (0-100), `coverage`, `S` similitud global, `status` (`scored`, `outside_filter`, `insufficient_data`) |
| `{mars,moon}_montecarlo.csv` | `p_top`, percentiles de ranking `pct_p05`, `pct_p50`, `pct_p95` |
| `sites_summary.csv` | Un resumen por sitio de la sección 5.2, con `confidence` (Alta, Media, Baja) |
| `validation.json` | Resultado real de cada prueba de la Fase 5 (`passed`: true, false o null si falta el dato) |
