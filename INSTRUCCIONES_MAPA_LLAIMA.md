# TerraMatch Chile — Corrección de mapa del Llaima (v0.10.3)

## Problema identificado
El menú permitía escoger **Marte + Sur: Llaima**. Con esa combinación se cargaban los sitios marcianos Yungay/Pajonales/Llullaillaco. Además, el gráfico Plotly imponía una escala fija (`scaleanchor`) que podía ampliar la vista regional hasta toda la silueta de Chile.

## Cambios incluidos
- `app.py`: selector de región dependiente del planeta: Marte ofrece **Chile / Norte**; Luna ofrece **Chile / Sur: Llaima**. En Sur muestra dos visualizaciones ASTER rotuladas como tales (no fotografías) y una nota aclaratoria.
- `ui_data.py`: límites regionales de zoom aplicados de forma efectiva y filtrado de puntos fuera del área visible; eliminación de la restricción de escala problemática; trazado de ambos contornos provisionales `llaima_flows.geojson` y `llaima_cone.geojson` (solo líneas, no rellenos engañosos). No hay cálculos de puntajes nuevos ni cambios en resultados.

## Instalación en GitHub Desktop
1. Confirma que estás en la rama `integracion-motor-rojas-v07`.
2. Abre `Repository → Show in Explorer`.
3. Copia `app.py` y `ui_data.py` del ZIP a la raíz de la carpeta `terramatch-chile` y reemplaza los dos existentes.
4. En GitHub Desktop, revisa los cambios, marca ambos archivos y crea el commit: `Corregir zoom y sitios del mapa del Llaima`.
5. Presiona **Push origin** para actualizar Streamlit Cloud.
6. En la página, abre **Explorar Chile / Explore Chile**, elige **Luna / Moon**, luego **Sur: Llaima / South: Llaima**, y deja activada **Mostrar sitios destacados / Show key sites**.

## Resultado esperado
El mapa se acerca a Llaima y muestra sus celdas válidas y los contornos **provisionales** de las coladas y del cono. El azul y naranja de los contornos son solo para distinguir los dos polígonos: **no indican una equivalencia lunar**. El puntaje de similitud sigue representado por la escala de colores de las celdas válidas.

Se probaron ambas vistas (puntaje y cobertura) y los dos perfiles contra los CSV reales del motor v0.7. No cambiamos ningún dato científico. Las delimitaciones todavía requieren la revisión geológica de Pancho.
