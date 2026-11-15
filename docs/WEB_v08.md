# TerraMatch Chile — Web guiada v0.8

## Qué cambia
- Menú con siete secciones: Inicio, Sobre el proyecto, Cómo funciona, Explorar Chile, Fichas de sitios, Resultados y validación, Datos y limitaciones.
- Interfaz en español e inglés; navegación con páginas internas y botones de acceso rápido.
- Mapa interactivo hecho con Plotly que NO depende de mapas-base OSM ni proveedores externos para dibujar celdas/silueta. Tiene regiones, selección Marte/Luna, filtro de puntaje y visualización de estados para la cobertura ASTER.
- Relieves ilustrativos de Chile (ASTER), Marte (MOLA) y Luna (SLDEM2015), generados a partir de los datos reales del equipo y acompañados de créditos. Son **visualizaciones de relieve**, no fotografías de paisaje.
- Comparador en fichas, interpretación accesible, resultados de validación y limitaciones.

## Archivos nuevos/modificados

```
app.py
ui_data.py
requirements.txt
assets/visuals/*.jpg
assets/visuals/chile_outline.geojson
assets/visuals/ATTRIBUTION.md
docs/WEB_v08.md
```

NO sustituir los archivos `results/*.csv`, `results/validation.json` ni `data/targets.json`: continúan siendo los valores calculados por Rojas v0.7.

## Cómo desplegar sin Python

1. En GitHub Desktop cambiar a `integracion-motor-rojas-v07`.
2. Abrir `Repository > Show in Explorer`.
3. Copiar las carpetas y archivos de este ZIP a la raíz del repositorio **fusionando** `assets/` y `docs/` y reemplazando `app.py` y `requirements.txt`; añadir `ui_data.py`.
4. Revisar cambios, crear commit `Rediseñar interfaz TerraMatch v0.8 con mapa y fichas` y hacer `Push origin`.
5. Streamlit Community Cloud despliega automáticamente desde la rama. Si no se actualiza, seleccionar **Reboot** o **Reboot app** desde la administración de la aplicación.
6. Visitar la URL habitual `https://terramatch-chile-v07.streamlit.app/` y recorrer las siete secciones.

## Validación efectuada
- Compilación Python de `app.py` y `ui_data.py`: correcta.
- Ingesta de `mars_scores_web.csv` (31.660 celdas; 895 con puntaje), `moon_scores_web.csv` (31.660 celdas; 256 con puntaje), `sites_summary.csv` (5 sitios), `targets.json` y `validation.json`: correcta.
- Generación local de figuras Plotly para Marte/Luna y modo de puntuación/estado: correcta.
- Comprobación lógica de las siete rutas tanto en español como en inglés con una interfaz simulada: correcta.
- **No se ha realizado un test visual real en navegador/Streamlit Cloud** en este entorno. Se necesita revisar la URL tras desplegar.

## Riesgos científicos conservados
- Solo cuatro teselas ASTER, por tanto 1.262 celdas con relieve procesado; no hay un ranking nacional.
- La capa NUM de ASTER requiere integración explícita a la máscara de calidad del motor.
- Las geometrías de Pajonales y coladas del Llaima son proxies a escala geológica regional.
- Filtro volcánico lunar pendiente de auditoría de fuente/licencia/leyenda.
- Las cinco fichas mantienen confianza baja. Las pruebas fallidas de Marte se reportan, no se ocultan.
- Las puntuaciones nulas y estados excluidos nunca se interpretan como similitud igual a cero.

## Pendientes para siguientes versiones
- Fotografías locales de sitios con autorización de uso y atribución, además de imágenes oficiales de NASA para portada; las imágenes científicas actuales tienen valor explicativo, pero no reemplazan fotografías de campo.
- Mejorar metadatos de procedencia y licencias de capas geológicas.
- Realizar pruebas de accesibilidad, carga y comportamiento en pantallas pequeñas en Streamlit real.
- Completar los controles de la suite analítica y sus máscaras de calidad.
