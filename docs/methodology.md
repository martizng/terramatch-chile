
# Metodología — TerraMatch Chile

## 1. Enfoque general

TerraMatch Chile propone una metodología híbrida que combina análisis geoespacial, evaluación multicriterio y técnicas exploratorias de aprendizaje automático para identificar ambientes chilenos potencialmente útiles como análogos parciales de determinados entornos de la Luna y Marte.

La plataforma no busca establecer equivalencias perfectas entre ambientes terrestres y planetarios, sino identificar similitudes, diferencias y posibles aplicaciones científicas.

## 2. Fases metodológicas

### Fase 1. Selección de perfiles planetarios

- Seleccionar regiones de referencia de Marte y la Luna.
- Identificar sus características geológicas, térmicas y geomorfológicas.
- Registrar los instrumentos y productos científicos utilizados.

### Fase 2. Preparación de datos

- Recopilar información geoespacial de Chile.
- Integrar datos de topografía, reflectancia, temperatura y geología.
- Revisar unidades, resolución espacial y calidad.
- Organizar los datos para permitir comparaciones.

### Fase 3. Evaluación multicriterio

- Representar cada ambiente mediante variables seleccionadas.
- Normalizar las variables cuantitativas.
- Definir ponderaciones según el perfil planetario.
- Calcular diferencias y similitudes entre ambientes.

### Fase 4. Aprendizaje automático exploratorio

Se consideran técnicas como:

- PCA: análisis de componentes principales.
- K-means o clustering jerárquico: identificación de agrupaciones.
- DBSCAN: exploración de agrupaciones y observaciones atípicas.

Estas técnicas complementan el análisis, pero no demuestran por sí solas que un ambiente sea un análogo planetario.

### Fase 5. Validación y priorización

- Contrastar los resultados con antecedentes científicos.
- Revisar la calidad y cobertura de los datos.
- Analizar similitudes y diferencias.
- Documentar las limitaciones de cada candidato.

## 3. Variables de análisis

Las principales dimensiones consideradas son:

- Geología y características superficiales.
- Topografía y geomorfología.
- Condiciones térmicas.
- Agua y humedad.
- Procesos superficiales.
- Entorno biológico y subsuperficial.

Para el MVP se priorizan elevación, pendiente, rugosidad, reflectancia, temperatura superficial diurna y nocturna, amplitud térmica y contexto geológico.

## 4. Alcance y limitaciones

Las analogías identificadas serán parciales y dependerán de la pregunta científica u operacional.

La plataforma no certifica lugares como análogos perfectos, no identifica sitios seguros de aterrizaje y no reemplaza la interpretación geológica experta.

Las variables con diferentes resoluciones, unidades o instrumentos deberán tratarse cuidadosamente para evitar comparaciones incorrectas.

## 5. Estado de implementación

Documento metodológico inicial. Los perfiles planetarios, productos de datos, variables definitivas, ponderaciones y parámetros del modelo serán especificados y actualizados durante el desarrollo del proyecto.
