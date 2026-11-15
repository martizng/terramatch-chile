# Resultados del MVP — TerraMatch Chile (motor Rojas v0.7)

**Estos son resultados reales del procesamiento piloto**, no plantillas vacías. Se generaron a partir de cuatro teselas ASTER GDEM v3, perfiles planetarios MOLA MEGDR y SLDEM2015 y filtros de datos terrestres. **No representan un ranking de todo Chile**.

## Cobertura y estados

- Grilla de referencia: **31.660** celdas de Chile.
- Celdas con las tres variables topográficas ASTER: **1.262**.
- **Marte**: **895** celdas con similitud calculada (`scored`).
- **Luna**: **256** celdas con similitud calculada (`scored`).
- Una celda con `outside_filter` está **excluida por el filtro** (no significa similitud baja).
- Una celda con `insufficient_data` **no posee información suficiente** (por ejemplo, ausencia de ASTER).
- `no_filter_data` significa que faltan los datos para aplicar el filtro.
- El puntaje `S` debe interpretarse **solo cuando `status=scored`**.

## Archivos

| Archivo | Contenido |
|---|---|
| `mars_scores_web.csv` | Tabla para mapa y ranking piloto de Marte: `cell_id`, coordenadas, variables, `S`, cobertura, confianza y estados. |
| `moon_scores_web.csv` | Tabla equivalente para la Luna. |
| `sites_summary.csv` | Resumen de los cinco sectores piloto y sus comparaciones. |
| `validation.json` | Pruebas de coherencia de Marte y Luna, y experimentos complementarios de sensibilidad. |
| `mars_profile.csv` y `moon_profile.csv` | Resultados por celda y variable del motor de similitud. |
| `mars_montecarlo.csv` y `moon_montecarlo.csv` | Estabilidad de ranking por 500 simulaciones Monte Carlo. |
| `mars_profile_precip_cr2met_imerg.csv` | Análisis complementario de sensibilidad; no es la fuente principal de lluvia. |
| `moon_profile_volcanic_broad.csv` | Análisis complementario del filtro volcánico amplio; no es el resultado principal. |

## Interpretación preliminar autorizada

- Yungay: **percentil 47,43** y Salar de Pajonales: **percentil 63,13** frente a Elysium Planitia. **No cumplen** el benchmark esperado (percentil ≥75).
- Llullaillaco: **percentil 8,27**, consistente con el control negativo esperado.
- Llaima, sector aproximado de coladas: **S=38,99**; cono: **S=17,16**. Es una comparación **relativa**, no evidencia de equivalencia geológica lunar.
- Los **cinco sitios evaluados** tienen confianza **Baja**. Algunas **celdas individuales** pueden tener confianza Alta; no confundir ambos niveles.
- La celda de mayor puntaje marciano del piloto está aproximadamente en **24,525° S, 68,925° O** (S=100), pero la geoforma local **no ha sido identificada ni validada**.

## Fuentes, validación y límites

Consultar el documento íntegro del equipo en `docs/validation/AFIRMACIONES_Y_EVIDENCIA.md`, así como `docs/methodology.md` y `docs/reviews/motor_v07_integracion.md`.

La cobertura es parcial; los polígonos de Pajonales y coladas del Llaima son proxies geológicos; el filtro lunar depende de una cartografía 1:1.000.000 de terceros. El perfil MOLA marciano proviene de solo cinco ventanas que cumplen el umbral de observación directa. La calidad de pixeles ASTER basada en NUM ha sido reportada por el equipo, pero requiere archivar su informe independiente.

**Los datos y puntajes no fueron generados por IA.** Se utilizó asistencia de IA para código y documentación, que debe declararse en la postulación.
