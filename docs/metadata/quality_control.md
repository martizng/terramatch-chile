# Control de calidad — estado real (sáb 14-nov-2026)

Solo se declara "verificado" lo que se comprobó sobre archivos existentes.

## Capa BCN (Regional.shp) — requiere validación
- Verificado: abre; 17 entidades (16 regiones + "Zona sin demarcar"); campos `objectid, cir_sena, codregion, area_km, st_area_sh, st_length_, Region`; título de metadatos `siit2017.sde.regiones2017`.
- Verificado: CRS declarado en el `.prj` = Web Mercator (EPSG:3857). Extensión (WGS84): lon −109.45 a −66.42, lat −55.98 a −17.50 (incluye Isla de Pascua; la grilla de Rojas la excluye por su caja lon −76..−66).
- **Problema: 8 de 17 geometrías inválidas (autointersecciones de anillo).** La unión espacial de Rojas funcionó (31 660 de 31 660 centros de celda caen dentro), pero no está garantizado con geometrías inválidas; si se calcula área o se hace overlay, aplicar `make_valid()`/`buffer(0)` y documentarlo. No se modificó el original.
- 80 celdas de la grilla caen en "Zona sin demarcar" (se consideran "Chile" en la máscara); no afecta a los sitios del MVP.
- Cobertura por región (celdas): Magallanes 7020, Aysén 4998, Antofagasta 4459, Atacama 2769, … (ver `qc_bcn_regional.json`).
- No verificado: fecha de descarga (no registrada); el ZIP completo con comunas del doc 6.3 no está.
- Puntos de referencia: Yungay, Pajonales y Llullaillaco caen en la Región de Antofagasta; Llaima en La Araucanía.

## sites_chile.gpkg — hecho (3/5)
- Geometrías válidas; áreas UTM vs geodésica: Yungay 25.000/25.015 km², cono 28.271/28.255 km², Llullaillaco 201.042/201.192 km² (diferencias ≤0.08 %).
- Son reglas geométricas del documento técnico (no delimitación geológica). Pajonales y coladas Llaima NO tienen geometría (ver `sites_pending.csv`); `aoi_search` NO es el polígono de coladas.

## SERNAGEOMIN 1:1M → volcanic_units.tif / volcanic_units_broad.tif — hecho (15-nov-2026)
- **Fuente:** Mapa Geológico de Chile 1:1.000.000 de SERNAGEOMIN. Es una **copia de terceros** en ArcGIS Online, con créditos "Autor: CIGIDEN. Fuente: SERNAGEOMIN". URL: `https://services7.arcgis.com/UeyripQFTg6pfUe5/arcgis/rest/services/Mapa_Geol%C3%B3gico_de_Chile/FeatureServer/0`. Descargada el 2026-11-15. Los canales oficiales no estaban accesibles (ver README).
- **Verificado:**
  - 18.935 polígonos, con 1 geometría nula ("mar") omitida.
  - Bounds lon −75,69..−66,415 y lat −55,72..−17,50, dentro de la caja de la grilla. Área total de 734.283 km².
  - 149 códigos `geo`. Todo código con el dígito 3 es "Secuencias volcanicas", salvo EM3 (9 polígonos sin atributos).
  - Los rasters son uint8, EPSG:4326, caja −76..−66 / −56..−17, 0,01° y nodata 255.
- **Regex sobre `geo`:**
  - Estricta: `^(Q3|Pl3|PPl3|P3)[a-z]*$`. 899 polígonos: Q3av, Q3i, Q3t, Pl3, Pl3t, PPl3, P3i y P3t.
  - Amplia: `^[A-Za-z]+3[a-z]*$`. 3.514 polígonos.
- **Control de cordura (OK en las dos):** Llaima (−38,69, −71,73) = 1 (Q3i); Llullaillaco (−24,72, −68,54) = 1 (Q3i); Yungay (−24,10, −70,10) = 0 (Qa); Santiago (−33,45, −70,67) = 0 (Q1).
- **Grilla de 31.660 celdas:**
  - Estricta: 2.395 celdas con 1 (**7,56 %**).
  - Amplia: 6.123 celdas con 1 (**19,34 %**).
  - Nodata: 1.404 (4,4 %). Son centros que caen en mar o canales: 823 al sur de 50° S, 500 entre 45° y 50° S, y 31 al sur del límite del vector (−55,72).
- **Limitaciones:**
  - Escala 1:1M con unidades generalizadas: una celda de 5 km puede mezclar unidades.
  - "S I" (30.331 km², sobre todo hielo y lagos) se cuenta como 0.
  - `composicio` es una clase generalizada.
  - La copia no declara licencia.
  - La leyenda en PDF no se pudo extraer de forma automática.
- **Pendientes que no son de este paso:** el polígono de Pajonales y las coladas del Llaima (digitalización propia).

## ASTER GDEM V3 / GPM IMERG V07 — sin datos
No hay archivos descargados; no se realizó ningún control sobre datos reales. Los scripts tienen controles integrados (CRS, nodata, % vacíos, % mar, unidades, meses completos) que quedan en `aster_tile_qc.csv` y en los JSON de metadatos al ejecutarse.
