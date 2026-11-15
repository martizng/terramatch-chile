# Revisión de integración — Motor v0.7 (15 nov 2026)

**Estado:** revisión; no fusionar todavía a `main`. Entrega de Rojas `terramatch_v07.zip` y BJOR `MARTI-20261115T171305Z-1-001.zip`.

## Comprobaciones realizadas
- Los CSV `master.csv`, `mars_scores_web.csv` y `moon_scores_web.csv` contienen 31.660 `cell_id` únicos.
- Topografía ASTER piloto: 1.262 celdas; Marte: 895 puntuadas; Luna: 256 puntuadas. Cobertura **no nacional**.
- Los resultados excluidos tienen `S` nulo, y los conteos de `validation.json` coinciden con las tablas.
- Cinco GeoJSON bien formados y con geometrías válidas; dos delimitaciones usan proxies geológicos 1:1.000.000.
- Los recortes MOLA de BJOR y Rojas son idénticos. Los recortes SLDEM2015 contienen los mismos píxeles, CRS y extensión, aunque su compresión difiere.
- Se ejecutaron con éxito los controles iniciales sintéticos; la suite completa excedió el tiempo de esta revisión. Validación de integración completa pendiente.

## Hallazgos que debemos resolver
1. `src/features/chile_features.py` utiliza `*_dem.tif` pero **no aplica explícitamente las máscaras de procedencia de `*_num.tif`**. Incorporar evaluación de calidad ASTER o declarar formalmente la limitación antes de publicar.
2. `pajonales.geojson` representa la unidad sedimentaria MQs, **no el contorno específico del salar**. `llaima_flows.geojson` representa unidad volcánica Q3i excluyendo el cono; **no equivale a un levantamiento preciso de coladas**. Presentar ambos como proxies.
3. Los percentiles e IQR corresponden exclusivamente a celdas cubiertas por las cuatro teselas; **no describen un ranking nacional**.
4. La capa volcánica procede de una copia de terceros de SERNAGEOMIN. Confirmar fuente, leyenda, criterios y condiciones de reutilización; el análisis lunar es preliminar.
5. El campo `kind: measured` de `data/targets.json` se utiliza para pendientes, relieve y rugosidad **derivados de DEM**; cambiar a `derived_from_dem` para evitar una atribución incorrecta.
6. Aclarar en el mapa: `status=insufficient_data` con `coverage=0` significa sin cobertura topográfica; `outside_filter` = filtro no cumplido; `no_filter_data` = sin información del filtro. Si concurren falta de DEM y exclusión por filtro, el estado prioriza el filtro: mostrar también `valid_frac`.
7. Reproducir recortes BJOR desde los originales y ejecutar la suite completa; mantener MOLA `counts` y el filtro de observación directa >=50%.

## Resultados de coherencia informados
- Yungay p47,4 y Pajonales p63,1: **no cumplen** benchmark p>=75 (esto debe verse en web/documentación).
- Llullaillaco p8,3 y terreno empinado p2,5: cumplen controles.
- Llaima, proxy de coladas S39,0 > cono S17,2: cumple comparación interna; interpretación sujeta a calidad geológica.
- Confianza de los cinco sitios: Baja.

## Próximo paso técnico
Importar archivos de v0.7 **a esta rama**, no a `main`; ejecutar controles completos, corregir hallazgos y vincular la web a los CSV reales. Conservar la rama/PR anterior sin fusionarla hasta cerrar la revisión.
