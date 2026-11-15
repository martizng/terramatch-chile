# MOLA MEGDR — Elysium Planitia (TerraMatch Chile)

## Estado
**Validado estructuralmente; pendiente evaluación de cobertura por ventana y aprobación final para perfil.**

## Procedencia
- Instrumento: Mars Orbiter Laser Altimeter (MOLA), Mars Global Surveyor.
- Dataset PDS: `MGS-M-MOLA-5-MEGDR-L3-V1.0`.
- Versión de producto declarada en etiquetas PDS3: `2.0`.
- Archivo original de topografía: `MEGT44N090HB.IMG` + etiqueta `.LBL`.
- Archivo original de conteo de observaciones: `MEGC44N090HB.IMG` + etiqueta `.LBL`.
- Resolución de la fuente: 128 píxeles/grado (0,0078125°/píxel); escala informada por PDS ≈0,463 km/píxel.
- Coordenadas de referencia del proyecto: 4,50° N; 135,90° E (Marte).
- Fuente oficial de consulta: https://pds-geosciences.wustl.edu/missions/mgs/megdr.html
- **URL exacta de descarga: pendiente de confirmar con integrante 2.**
- **Fecha efectiva de descarga: pendiente de confirmar con integrante 2.**
- **Procedimiento/comando de recorte y conversión a GeoTIFF: pendiente de recibir.**
- Derechos/condiciones de redistribución: verificar según la fuente oficial antes de publicación definitiva.

## Datos derivados recibidos
- `data/mars/processed/elysium_mola_dem.tif`: GeoTIFF 64 × 64 píxeles, elevación en metros respecto al areoide, 100 % de píxeles con valor en el recorte.
- `data/mars/processed/elysium_mola_counts.tif`: GeoTIFF 64 × 64 píxeles; conteo de observaciones directas por píxel.
- Ambos GeoTIFF están en coordenadas planetocéntricas marcianas con radio esférico 3.396.000 m; **no** son EPSG:4326 terrestre.
- Extensión de GeoTIFF: longitud 135.648437500° a 136.148437500° E; latitud 4.250000000° a 4.750000000° N.
- Tamaño angular: 0,5° × 0,5° (aproximadamente 30 km × 30 km en Marte).
- Resolución angular de los GeoTIFF: 0.007812500° × 0.007812500°.

## Control de calidad y advertencia
- Píxeles con al menos una observación directa: **1,253 / 4,096 (30.59 %)**.
- En el archivo de conteo, `NoData` está codificado como `4294967295` (uint32) y aparece en 2,843 píxeles. **Nunca contarlo como observaciones directas.**
- Conteos válidos observados entre 1 y 6; el DEM puede contener valores interpolados en zonas sin medición directa.
- La metodología exige excluir las ventanas del perfil con menos del 50 % de píxeles medidos; **no** aplicar el 50 % al recorte total como sustituto de esa verificación por ventana.
- Para calcular pendiente se debe usar una proyección métrica apropiada para Marte, no directamente grados geográficos.
- Mantener los originales `.IMG` fuera de Git normal por tamaño; registrar su ubicación respaldada y hash.
- Si no se dispone de suficientes ventanas válidas, declarar el problema y revaluar ubicación/tamaño del perfil solo mediante un cambio metodológico documentado y aprobado.

## Huellas SHA-256 de los originales recibidos
- `megt44n090hb.img`: `a65eb54042e579dbb6274aad8256e30fbb752dd70b93b6a3ad748909f1a9f687`
- `megc44n090hb.img`: `4513ad6d3c03b308d344907ff0b3b91e7b324d0248e7ad37e46302338f1fd531`
