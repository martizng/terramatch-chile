# Actualización final TerraMatch Chile — web v0.10.2

**IMPORTANTE:** subir a la rama `integracion-motor-rojas-v07`, NO a `main`.

## Qué subir

- `app.py`: el código completo v0.10, con colores corregidos, 8 limitaciones científicas explícitas y comparación relativa del Llaima.
- `docs/validation/AFIRMACIONES_Y_EVIDENCIA.md`: documento ORIGINAL de Rojas, sin modificar.
- `results/README.md`: documentación corregida, que ya reconoce los CSV reales v0.7 (el README anterior decía incorrectamente que eran plantillas vacías).

## Cómo subir con GitHub Desktop

1. Descargar y extraer el ZIP.
2. Abrir GitHub Desktop, elegir la rama `integracion-motor-rojas-v07`.
3. Abrir `Repository > Show in Explorer`.
4. Copiar y pegar `app.py`, `docs/` y `results/` dentro de la **raíz del repositorio**. Aceptar combinar las carpetas y reemplazar SOLO los archivos del paquete; no eliminar otros.
5. En Changes deben aparecer como máximo: `app.py` modificado, `results/README.md` modificado y `docs/validation/AFIRMACIONES_Y_EVIDENCIA.md` nuevo.
6. Escribir Commit `Alinear web y documentacion con evidencia del motor v0.7`; pulsar **Commit** y luego **Push origin**.
7. Confirmar que Streamlit Cloud cargue la web en español e inglés; en Datos y limitaciones deben aparecer los apartados de MOLA, IMERG y control ASTER NUM.

## Comprobaciones y advertencias

- Ambos CSV tienen 31.660 filas, con 895 y 256 puntuadas para Marte y Luna, respectivamente.
- Se conservan sin alteraciones los datos científicos, puntajes, filtros, Monte Carlo y polígonos.
- Solo cuatro teselas ASTER piloto: no hay ranking nacional.
- Los cinco sitios tienen confianza Baja; algunas celdas individuales tienen confianza Alta.
- La geoforma de 24,5° S, 68,9° O sigue pendiente de verificación geográfica; no asignarle nombre ni tipo.
- Las comparaciones del Llaima son relativas, no prueba de terreno lunar.
- El dato NUM del 100% de píxeles ASTER estéreo, 11–29 escenas, viene del mensaje posterior del equipo, **no figura en AFIRMACIONES_Y_EVIDENCIA.md**; la web lo identifica como dato comunicado, con evidencia pendiente de archivo. Para presentarlo como plenamente validado, subir reporte NUM de Pancho.
- Pruebas: sintaxis Python, simetría de 196 claves de idioma, esquema y conteos CSV. La experiencia visual publicada aún debe revisarse en el navegador.
