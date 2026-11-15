# TerraMatch Chile: primera comparación con datos reales (motor v0.7, domingo 15, 14:05)

Resultados reales y reproducibles con la cobertura ASTER disponible. **No es un ranking nacional**: solo se puntúan las celdas cubiertas por las 4 teselas piloto. Los resultados se informan tal cual; nada se ajustó para cumplir las pruebas.

## Datos usados

| Insumo | Archivo | Cobertura |
|---|---|---|
| Relieve de Chile | ASTER GDEM v3, teselas S25W070, S25W069, S26W069, S39W072 (`ASTER_GDEM_V3_Originales.zip`, carpeta ASTER_MARTI) | 1.262 celdas de 31.660 (895 en el norte, 367 en el Llaima) |
| Perfil de Marte | MOLA MEGDR 128 ppd, Elysium Planitia (`data/targets.json`) | 5 de 25 ventanas (30,6% de medición directa) |
| Perfil de la Luna | SLDEM2015 512 ppd, Mare Tranquillitatis (`data/targets.json`) | 25 de 25 ventanas |
| Filtro de Marte | GPM IMERG Final V07, ≤ 250 mm/año (`data/chile/processed/`) | todas las celdas |
| Filtro de la Luna | Unidades volcánicas, criterio estricto (`data/raw/volcanic_units.tif`) | 1.404 celdas sin dato |
| Sitios | 5 polígonos en `data/chile/sites/` | ningún sitio pendiente |

Procesamiento: remuestreo a 463 m en UTM 18S/19S (error de escala máximo 0,053%), ventanas de 5 km con al menos 50% de píxeles válidos, 500 iteraciones de Monte Carlo con rangos promedio.

## Resultados

| Perfil | Celdas puntuadas | Fuera del filtro | Sin datos suficientes (incluye sin ASTER) | Sin dato del filtro |
|---|---|---|---|---|
| Marte | 895 | 21.196 | 9.569 | 0 |
| Luna | 256 | 27.861 | 2.139 | 1.404 |

### Validación (`results/validation.json`)

| Prueba | Valor | Criterio | Resultado |
|---|---|---|---|
| Yungay (referencia de Marte) | percentil 47,4 | ≥ 75 | **No se cumple** |
| Salar de Pajonales (referencia de Marte) | percentil 63,1 | ≥ 75 | **No se cumple** |
| Llullaillaco (control) | percentil 8,3 | ≤ 25 | Se cumple |
| 5% de celdas más empinadas (control) | percentil mediano 2,5 | ≤ 25 | Se cumple |
| AUC secundario (referencias vs control) | 1,0 | — | — |
| Coladas del Llaima > cono (Luna) | S 39,0 vs 17,2 (diferencia 21,8) | coladas > cono | Se cumple |

El análisis complementario da lo mismo: con CR2MET-IMERG, Yungay queda en el percentil 47,3 y Pajonales en el 63,0; con el criterio volcánico amplio, las coladas también superan al cono.

### Por qué fallan Yungay y Pajonales (lectura de los datos, no corrección)

Elysium Planitia es extremadamente lisa a 463 m: pendiente P90 de 0,45° y relieve local de 15 m en 5 km. Yungay tiene pendiente P90 de 8,2° y relieve de 173 m; Pajonales, 7,4° y 155 m. Las dos quedan fuera del rango del perfil en las tres variables. Ambos son análogos de Marte por aridez y química del suelo, no por topografía a 5 km. El modelo sí distingue bien el terreno empinado (los controles quedan en los percentiles 8 y 2,5). Las celdas más parecidas a Elysium son planicies del norte, alrededor de 24,5° S y 68,9° O (S = 100, p_top = 1,0, confianza Alta); hay que identificar en imagen satelital qué geoforma es.

### Confianza

Marte: 9 celdas Alta, 1 Media y 885 Baja. Luna: 2 Alta, 2 Media y 252 Baja. Los 5 sitios quedan en confianza Baja (p_top = 0).

## Limitaciones

- Cobertura piloto: el IQR que normaliza las distancias se calcula sobre las 1.262 celdas con ASTER, no sobre todo Chile. Con más teselas, los percentiles van a cambiar.
- Perfil de Marte con 5 ventanas (MOLA interpolado en el 69% de los píxeles).
- IMERG sobrestima la lluvia en el desierto; los sitios quedan bajo 250 mm igual.
- Pajonales y las coladas del Llaima vienen del mapa geológico 1:1.000.000 (copia de terceros).
- Yungay y el cono ocupan 1 celda cada uno (sitios más chicos que una celda de 0,05°).

## Archivos para la página (`results/`)

| Archivo | Contenido |
|---|---|
| `mars_scores_web.csv`, `moon_scores_web.csv` | Una fila por celda: `cell_id`, `lat_c`, `lon_c`, variables, distancia y similitud por variable, `coverage`, `S`, `status`, `p_top`, `pct_p05/p50/p95`, `confidence`, `rank` (1 = más similar entre las puntuadas) |
| `mars_profile.csv`, `moon_profile.csv` | Distancias y puntajes por celda |
| `mars_montecarlo.csv`, `moon_montecarlo.csv` | Estabilidad del ranking |
| `sites_summary.csv` | Los 5 sitios: coordenadas de referencia, celdas, S, percentil, confianza, valores y distancias por variable |
| `validation.json` | Pruebas, conteos, escalas y análisis complementarios |
| `*_profile_precip_cr2met_imerg.csv`, `*_profile_volcanic_broad.csv` | Solo análisis complementario |
| `data/processed/master.csv` | Variables de Chile por celda (`valid_frac`, `utm_epsg`, `scale_error`, precipitación y unidades volcánicas) |

Para el mapa: `status = scored` lleva color por `S`; `outside_filter` se pinta como "fuera del filtro"; `insufficient_data` con `coverage = 0` es "sin cobertura ASTER"; `no_filter_data` es "sin dato del filtro". Nunca se deben mostrar como similitud baja.

## Cómo reproducir

```
py tests/test_pipeline_synthetic.py
py src/features/chile_features.py --dem "data/raw/aster_gdem_v3/*_dem.tif" --precip data/chile/processed/imerg_precip_2001_2024.tif --precip-alt data/raw/precip_annual_cr2met_imerg.tif --volcanic data/raw/volcanic_units.tif --volcanic-broad data/raw/volcanic_units_broad.tif
py src/run_pipeline.py
```
Las teselas ASTER no van en el ZIP (100 MB): se descomprimen desde `ASTER_GDEM_V3_Originales.zip` en `data/raw/aster_gdem_v3/`.

AI-Assisted: código y resumen redactados con Claude; ejecutado en el computador de Rojas con datos reales. Ningún valor de datos fue generado por IA.
