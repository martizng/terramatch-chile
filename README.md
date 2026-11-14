# 🌎 TerraMatch Chile

### Chile como laboratorio natural para explorar análogos terrestres de la Luna y Marte

## 1. Sobre el proyecto

**TerraMatch Chile** es una propuesta de plataforma geoespacial que busca identificar, caracterizar y comparar ambientes del territorio chileno que puedan ser útiles como análogos parciales de determinados entornos de la Luna y Marte.

El proyecto integra información satelital, geoespacial, geológica y ambiental de Chile con productos científicos de misiones planetarias. Mediante análisis multicriterio y técnicas exploratorias de aprendizaje automático, busca reconocer similitudes, diferencias y combinaciones de características que permitan identificar nuevos candidatos para investigación.

Chile ofrece una diversidad de ambientes naturales —desiertos hiperáridos, salares, sistemas volcánicos, alta montaña y ambientes glaciares— que permite explorar distintas condiciones y procesos relevantes para la investigación planetaria.

## 2. Pregunta de investigación

¿Qué ambientes de Chile presentan características o procesos comparables con determinados entornos lunares y marcianos, en qué dimensiones se parecen, cuáles son sus diferencias y para qué actividades de investigación o preparación de misiones podrían ser útiles?

## 3. Objetivo general

Desarrollar una plataforma geoespacial que integre datos abiertos de Chile, la Tierra, la Luna y Marte para identificar, caracterizar y priorizar ambientes chilenos potencialmente útiles como análogos parciales de entornos planetarios.

## 4. ¿Qué permitirá hacer la plataforma?

El prototipo considera cinco módulos principales:

- **Explorador territorial:** visualizar y explorar ambientes seleccionados de Chile mediante información geográfica.
- **Selector planetario:** seleccionar perfiles de referencia de la Luna y Marte.
- **Motor de descubrimiento:** identificar ambientes chilenos con combinaciones de características comparables.
- **Comparador de ambientes:** analizar similitudes y diferencias entre ambientes terrestres y perfiles planetarios.
- **Ficha de analogía:** presentar las características, resultados, posibles aplicaciones y limitaciones de cada candidato.

## 5. Ambientes chilenos de interés

El proyecto considera cinco familias ambientales iniciales:

| Ambiente | Características de interés |
|---|---|
| Desiertos hiperáridos | Aridez, suelos y procesos superficiales |
| Salares y evaporitas | Sales, sulfatos y procesos de evaporación |
| Terrenos volcánicos | Basaltos, flujos de lava y morfología |
| Alta montaña y ambientes periglaciares | Hielo, congelamiento y descongelamiento |
| Ambientes glaciares | Morfología glaciar y procesos asociados al hielo |

Estas familias constituyen líneas de exploración y no una clasificación de análogos ya validada.

## 6. Metodología

La metodología propuesta combina:

1. Selección de perfiles ambientales de referencia de Marte y la Luna.
2. Recopilación y preparación de datos geoespaciales terrestres y planetarios.
3. Armonización de variables y escalas de análisis.
4. Evaluación multicriterio para comparar características.
5. Técnicas exploratorias de aprendizaje automático para identificar agrupaciones.
6. Validación, interpretación y priorización de candidatos.

La comparación considera dimensiones como geología, topografía, condiciones térmicas, reflectancia, agua y procesos superficiales.

## 7. Tecnologías consideradas

| Tecnología | Aplicación |
|---|---|
| Python | Procesamiento y análisis de datos |
| Google Earth Engine | Acceso y procesamiento geoespacial |
| GeoPandas y Rasterio | Manejo de información geográfica |
| NumPy y Pandas | Procesamiento de datos |
| Scikit-learn | Análisis exploratorio y aprendizaje automático |
| Streamlit | Desarrollo de la plataforma web |
| Folium | Visualización de mapas interactivos |
| QGIS | Exploración y análisis cartográfico |

## 8. Estructura del repositorio

```text
terramatch-chile/
│
├── app.py
├── requirements.txt
│
├── data/
│   ├── chile/
│   ├── mars/
│   └── moon/
│
├── src/
│   ├── analysis.py
│   ├── map.py
│   └── comparison.py
│
├── docs/
│   ├── methodology.md
│   └── references.md
│
└── assets/
    └── images/
```

## 9. Estado del proyecto

El repositorio contiene la estructura inicial del prototipo, documentación metodológica y módulos de software preparados para integrar los datos y resultados del equipo.

La implementación del análisis, la incorporación de productos científicos y la validación de las comparaciones se desarrollarán progresivamente.

Los resultados deberán interpretarse como analogías parciales, dependientes de la pregunta científica u operacional y de la calidad y compatibilidad de los datos.

## 10. Alcances y limitaciones

TerraMatch Chile no busca establecer equivalencias perfectas entre ambientes terrestres y planetarios. Tampoco certifica sitios de aterrizaje, predice habitabilidad extraterrestre ni reemplaza la interpretación geológica experta.

Su propósito es ofrecer una herramienta exploratoria, reproducible y explicable para apoyar la identificación y caracterización de posibles análogos terrestres.

---

**NASA Space Apps Challenge | TerraMatch Chile**

*Explorando la Tierra para comprender otros mundos.*
