# Metodología — TerraMatch Chile

**Versión:** 2.0  
**Fecha:** 14 de noviembre de 2026  
**Estado:** Metodología definida para el MVP de NASA Space Apps Challenge.

## 1. Enfoque general

TerraMatch Chile es una plataforma geoespacial para identificar, caracterizar y comparar ambientes de Chile que puedan ser útiles como **análogos terrestres parciales** de determinados entornos de la Luna y Marte.

La metodología combina datos topográficos terrestres y planetarios, filtros ambientales o litológicos, evaluación multicriterio, análisis de sensibilidad y validación científica. El objetivo es explicar en qué dimensiones se parecen los ambientes, cuáles son sus diferencias y qué usos de investigación podrían explorarse.

Una analogía depende de la pregunta científica u operacional. Ningún sitio terrestre reproduce por completo las condiciones de otro cuerpo planetario. Por eso, TerraMatch informa similitud topográfica, evidencia geológica y utilidad potencial como aspectos distintos.

### 1.1 Alcance del MVP

El MVP considera:

- Un perfil marciano: Elysium Planitia, sector occidental.
- Un perfil lunar: Mare Tranquillitatis.
- Una grilla nacional de cribado para Chile y sitios de detalle.
- Tres variables topográficas comparables: pendiente P90, relieve local P95–P5 y rugosidad.
- Filtros previos específicos para cada perfil.
- Un puntaje reproducible, cobertura de datos, estabilidad Monte Carlo y nivel de confianza.
- Mapas, ranking de candidatos, comparaciones y fichas explicables.

Las cinco familias ambientales se mantienen como estructura del explorador: desiertos hiperáridos, salares y evaporitas, terrenos volcánicos, alta montaña/periglaciares y ambientes glaciares. No todas se procesarán en el MVP.

## 2. Perfiles planetarios de referencia

Los perfiles se construyen a partir de áreas piloto de aproximadamente 30 × 30 km. Para cada variable se registra el producto, instrumento, identificador exacto, versión, resolución, fecha de descarga y fuente. Un valor sin fuente documentada no se utiliza.

| Cuerpo | Región | Centro de referencia | Producto topográfico |
|---|---|---|---|
| Marte | Elysium Planitia, sector occidental | 4,50° N; 135,90° E | MOLA MEGDR, 128 píxeles por grado |
| Luna | Mare Tranquillitatis | 0,67416° N; 23,47314° E | SLDEM2015 (LOLA + Kaguya) |

Las coordenadas delimitan áreas de referencia para comparación científica; no son recomendaciones de emplazamiento de futuras bases ni certificaciones de seguridad.

### 2.1 Construcción de los perfiles

Cada área piloto contiene ventanas de análisis de 5 km. Para cada variable:

- El valor central del perfil corresponde a la mediana de las ventanas del área piloto.
- El rango de referencia [bajo, alto] corresponde a los percentiles 10 y 90.
- Se conserva el tipo de valor (medido, derivado o bibliográfico) y su fuente.

En el área piloto de Marte se debe considerar la cobertura de medición directa de MOLA. Se calcula la fracción de píxeles con observación directa mediante el producto de conteo de observaciones y se excluyen del perfil las ventanas con menos del 50 % de píxeles medidos.

## 3. Ambientes chilenos y sitios del MVP

Los sitios se utilizan para comprobar la coherencia del método y explorar candidatos. Sus roles no deben confundirse:

| Sitio | Perfil | Rol | Delimitación de referencia |
|---|---|---|---|
| Yungay | Marte | Benchmark de aridez | Ventana de 5 km centrada en 24,064° S; 69,881° W |
| Salar de Pajonales | Marte | Benchmark de depósitos salinos y evaporíticos | Contorno del salar digitalizado sobre imagen satelital; referencia 25,144° S; 68,820° W |
| Llaima, sector de coladas | Luna | Candidato exploratorio | Coladas del mapa geológico de SERNAGEOMIN dentro de 15 km de la cumbre; excluir píxeles con pendiente >15° |
| Llaima, cono | Luna | Contraste interno | Círculo de 3 km de radio alrededor de 38,692° S; 71,729° W |
| Llullaillaco | Marte | Control negativo: sector central de alta montaña | Círculo de 8 km de radio alrededor de 24,720° S; 68,537° W |

Los polígonos y geometrías definitivas se guardan en el repositorio con identificadores estables para que el análisis sea reproducible. Las coordenadas son referencias iniciales y deben contrastarse con las fuentes cartográficas utilizadas al delimitar cada polígono.

En el caso de Llullaillaco, la delimitación de 8 km de radio representa un sector central del entorno volcánico y de alta montaña, no necesariamente la totalidad del edificio volcánico. Por ello, los resultados deben interpretarse como correspondientes al área de control delimitada y no extrapolarse a todo el volcán.

### 3.1 Benchmarks y candidatos exploratorios

Para evitar atribuir una condición de análogo sin respaldo suficiente, TerraMatch distingue entre sitios de referencia utilizados para evaluar el comportamiento del método y sitios cuya posible utilidad como análogos todavía debe investigarse.

- **Sitio de referencia:** lugar seleccionado por presentar características ambientales o superficiales relevantes para evaluar la coherencia del método. Su selección no implica que exista una validación científica previa como análogo planetario.
- **Candidato exploratorio:** sitio cuya combinación de características resulta de interés para la comparación, pero que requiere validación científica adicional.
- **Análogo terrestre documentado:** sitio cuya pertinencia como análogo para investigación planetaria se encuentra respaldada por un inventario especializado o literatura científica revisada por pares.

Yungay y Salar de Pajonales se utilizan en el MVP como sitios de referencia para evaluar la respuesta del modelo frente a ambientes áridos y depósitos salinos o evaporíticos, respectivamente. Su condición de análogos terrestres documentados deberá comprobarse mediante fuentes específicas para cada sitio antes de atribuirles esa categoría.

El inventario USGS Known Terrestrial Analog Sites for Planetary Science (Hunter, 2020; DOI [10.5066/P9J72921](https://doi.org/10.5066/P9J72921)) constituye una fuente de consulta para identificar antecedentes de análogos terrestres. También se deben revisar publicaciones científicas y antecedentes geológicos específicos de cada lugar.

La ausencia de un sitio en un inventario no demuestra que sea nuevo. Se debe utilizar la expresión “no documentado en las fuentes revisadas”, no “análogo nuevo”.

## 4. Variables y filtros

TerraMatch organiza las variables en seis dimensiones: geología y superficie; topografía; condiciones térmicas; agua y humedad; procesos superficiales; y entorno biológico/subsuperficial.

En el MVP, **solo las variables topográficas forman parte del puntaje de similitud**. Los filtros de aridez y litología se aplican antes del cálculo y no suman ni restan puntos.

### 4.1 Variables que entran al puntaje

| Variable | Definición | Unidad | Fuente terrestre y planetaria |
|---|---|---|---|
| Pendiente P90 | Percentil 90 de la pendiente dentro de la ventana | Grados (°) | ASTER GDEM v3 / MOLA MEGDR / SLDEM2015 |
| Relieve local P95–P5 | Diferencia entre los percentiles 95 y 5 de elevación dentro de la ventana | Metros (m) | ASTER GDEM v3 / MOLA MEGDR / SLDEM2015 |
| Rugosidad | Desviación estándar de la pendiente dentro de la ventana de 5 km | Grados (°) | ASTER GDEM v3 / MOLA MEGDR / SLDEM2015 |

La elevación absoluta se puede informar como contexto, pero no entra al puntaje: cada cuerpo utiliza una referencia vertical diferente.

### 4.2 Filtros previos por perfil

**Perfil Marte — aridez**

- Fuente: GPM IMERG Final V07 mensual (GPM_3IMERGM).
- Se utiliza el período 2001–2024 para construir una climatología de precipitación.
- Primero se calcula la precipitación media mensual de cada mes calendario considerando los años disponibles del período. Luego, se suman los doce valores medios mensuales para estimar la precipitación anual media climatológica.
- Solo se consideran para el ranking las celdas con precipitación anual media ≤250 mm.
- Las celdas que no cumplen se etiquetan como `fuera_del_filtro`, no como baja similitud.
- La resolución de IMERG es de 0,1° (aprox. 10 km); por tanto, el filtro es regional respecto de la grilla nacional de 0,05° y esa limitación debe informarse.

Se utiliza IMERG para este filtro porque su resolución es más adecuada que la de NASA POWER para representar el gradiente de precipitación andino. NASA POWER se conserva como contexto y no se utiliza en el puntaje ni en los filtros.

**Perfil Luna — litología volcánica**

- Fuente: Mapa Geológico de Chile 1:1.000.000 de SERNAGEOMIN.
- Solo se consideran unidades volcánicas para la comparación con Mare Tranquillitatis, una llanura basáltica.
- Las celdas excluidas se etiquetan como `fuera_del_filtro`.
- El servicio WMS de SERNAGEOMIN entrega imágenes, no polígonos vectoriales. Si no se dispone de cartografía vectorial, el análisis lunar del MVP se limita a los sitios de detalle delimitados y documentados, en particular las coladas del Llaima y su cono como contraste.

### 4.3 Variables complementarias y capas de contexto

No entran al puntaje del MVP:

- Reflectancia e índices espectrales (por ejemplo, Landsat; contexto).
- Temperatura superficial diurna/nocturna y amplitud térmica (fase posterior; MODIS en Chile, THEMIS/TES en Marte y Diviner en la Luna).
- Nieve, hielo, glaciares e indicadores periglaciares.
- Dunas, polvo, erosión, depósitos y cambios temporales.
- Cobertura vegetal, geomorfología detallada y otras capas geológicas.

No se deben equiparar automáticamente magnitudes de sensores diferentes. La temperatura superficial orbital no equivale a la temperatura del aire de una estación meteorológica, y las bandas espectrales de instrumentos distintos no son intercambiables sin una justificación específica.

## 5. Preparación y armonización espacial

### 5.1 Datos de entrada

| Dataset | Uso en el MVP |
|---|---|
| ASTER GDEM v3 | Modelo de elevación terrestre para derivar las tres variables topográficas |
| GPM IMERG Final V07 mensual | Filtro de aridez del perfil marciano |
| Mapa Geológico de Chile 1:1.000.000, SERNAGEOMIN | Filtro litológico lunar, delimitación de coladas y contexto |
| Límites regionales BCN | Delimitación referencial de la cobertura nacional |
| MOLA MEGDR | Perfil topográfico de Elysium Planitia |
| SLDEM2015 | Perfil topográfico de Mare Tranquillitatis |

Al descargar cada producto se registra el identificador exacto del archivo/producto, versión, fecha de descarga, resolución, licencia o condiciones de uso y fuente de acceso. Los identificadores definitivos no se deben inventar ni completar antes de descargar y verificar los archivos.

### 5.2 Escala común

Para evitar comparar variables calculadas a escalas incompatibles:

- La grilla nacional de cribado utiliza EPSG:4326 con resolución angular de 0,05°. La capa de límites de BCN se utiliza como referencia de recorte, sin atribuirle precisión geodésica.
- Las variables topográficas se calculan en ventanas de 5 km centradas en cada celda; no directamente sobre celdas de 0,05°, cuyo tamaño físico cambia con la latitud.
- La resolución base común es aproximadamente 463 m por píxel, correspondiente a MOLA MEGDR de 128 píxeles por grado en el ecuador.
- ASTER GDEM v3 (aprox. 30 m) y SLDEM2015 (aprox. 59 m) se remuestrean a la resolución base común **antes** de calcular la pendiente, porque esta depende de la resolución.
- La pendiente y las variables derivadas se calculan en una proyección métrica adecuada para cada cuerpo (UTM en Chile y proyección equivalente en las áreas planetarias); luego se asignan a las unidades de análisis correspondientes.
- Se aplican máscaras de calidad y se conservan los valores NoData. No se rellenan datos faltantes con cero.
- Cada resultado informa su resolución efectiva y cobertura.

La resolución efectiva del MVP es aproximadamente 463 m, aunque la fuente terrestre ASTER tenga una resolución nativa más fina.

### 5.3 Estadísticas por ventana

Para cada ventana de 5 km y para cada sitio se calculan las estadísticas necesarias para obtener las tres variables del puntaje. También se conserva información de cobertura, calidad, resolución y fecha del producto. Los valores atípicos y los píxeles inválidos se tratan mediante las máscaras de calidad documentadas.

## 6. Cálculo de similitud

### 6.1 Rango del perfil y distancia por variable

Para cada variable $(i$), el perfil planetario tiene un rango de referencia \([bajo_i, alto_i]\). La distancia normalizada de un valor terrestre \(x_i\) se define como:

$$
d_i = \frac{\max(bajo_i-x_i,\ 0,\ x_i-alto_i)}{s_i}
$$

Donde \(s_i\) corresponde a la escala de normalización de la variable. Se define inicialmente como el rango intercuartílico (IQR) de esa variable en Chile:

\[
IQR_i = Q_{75,i} - Q_{25,i}
\]

La distancia es cero cuando el valor terrestre se encuentra dentro del rango del perfil. Si queda fuera, se mide la distancia al límite más cercano y se normaliza por la variabilidad de esa variable en Chile.

Para evitar divisiones por cero, se aplica el siguiente criterio:

1. Si el IQR es mayor que cero, se utiliza como escala de normalización.
2. Si el IQR es igual a cero y la desviación estándar es mayor que cero, se utiliza la desviación estándar.
3. Si tanto el IQR como la desviación estándar son cero, la variable se considera constante y no informativa para esa comparación. Se excluye del cálculo de distancia y de la cobertura correspondiente.

El relieve local se transforma mediante \(\log(1+x)\) antes del cálculo, debido a su distribución asimétrica. La misma transformación se aplica de forma consistente al perfil y a los valores terrestres.

### 6.2 Distancia y similitud agregadas

Para cada variable se define \(m_i=1\) si existe un dato válido y utilizable, y \(m_i=0\) si falta o no puede utilizarse. La distancia topográfica agregada se calcula como:

\[
D_{top} = \frac{\sum_i w_i m_i d_i}{\sum_i w_i m_i}
\]

La similitud topográfica se calcula como:

\[
S_{top} = 100\cdot e^{-D_{top}}
\]

En el MVP las tres variables tienen el mismo peso inicial:

\[
w_1=w_2=w_3=\frac{1}{3}
\]

Como el puntaje incluye solo la dimensión topográfica, la similitud global del MVP coincide con \(S_{top}\). La aplicación debe mostrar tanto el puntaje global como la distancia/similitud de cada variable para que el resultado sea explicable.

Esta transformación es una decisión metodológica del proyecto, no un estándar científico universal. Se debe documentar y evaluar su comportamiento con los sitios de referencia y controles definidos.

### 6.3 Datos faltantes y cobertura

Un dato faltante nunca se reemplaza por cero. La cobertura se calcula como:

\[
Cobertura = \frac{\sum_i w_i m_i}{\sum_i w_i}
\]

Las variables excluidas por presentar variabilidad nula tanto en el IQR como en la desviación estándar no se consideran disponibles para esa comparación. Por lo tanto, tampoco aportan al numerador ni al denominador de la cobertura.

Si la cobertura es menor que 0,5 —es decir, si falta más de una de las tres variables originalmente consideradas—, la celda se etiqueta como `información insuficiente` y no se presenta como un candidato con puntaje comparable.

Los estados de una celda deben distinguir al menos:

- `fuera_del_filtro`: no cumple el filtro previo del perfil.
- `información insuficiente`: no alcanza la cobertura mínima.
- Resultado calculado: tiene datos suficientes y pasó el filtro.

## 7. Análisis de sensibilidad e incertidumbre

Se realizan 500 repeticiones Monte Carlo para evaluar la estabilidad del ranking.

En cada repetición:

1. El valor de referencia del perfil para cada variable se sortea uniformemente dentro de su rango ([bajo, alto]).
2. Los pesos de las tres variables se perturban mediante una distribución Dirichlet de concentración 20, centrada en los pesos base iguales.
3. Se recalcula la similitud y el ranking de las celdas o sitios elegibles.

Para cada candidato se informa:

- **p_top:** proporción de repeticiones en que el candidato queda dentro del 1 % más similar.
- **Rango de posición:** percentiles p05, p50 y p95 de su posición en el ranking.

Un candidato que aparece entre los primeros lugares solo bajo una configuración particular de valores o pesos no se considera robusto.

### 7.1 Nivel de confianza

| Nivel | Condición |
|---|---|
| Alta | Las tres variables disponibles y p_top ≥0,7 |
| Media | Al menos dos de las tres variables disponibles y p_top ≥0,3 |
| Baja | Cualquier otro caso |

El nivel de confianza resume cobertura y estabilidad del resultado; no equivale a certeza de analogía geológica ni a validación operacional.

## 8. Validación científica y priorización

La validación combina consistencia cuantitativa, revisión cartográfica y antecedentes científicos. Para cada candidato se revisan las fuentes, la resolución, la cobertura, las limitaciones y la pertinencia respecto de la pregunta de investigación.

### 8.1 Pruebas de coherencia del MVP

**Perfil marciano — Elysium Planitia**

- Yungay y Salar de Pajonales deben ubicarse en el percentil 75 o superior entre las celdas chilenas que pasan el filtro de aridez.
- El sector central delimitado de Llullaillaco, utilizado como control negativo, se espera que se ubique en el percentil 25 o inferior.
- También se utiliza como control sistemático el 5 % de las celdas con mayor pendiente P90 entre las que pasan el filtro.

Estas pruebas evalúan si el método distingue superficies áridas de bajo relieve frente a terrenos empinados. No demuestran por sí solas una analogía geológica.

**Perfil lunar — Mare Tranquillitatis**

- El sector de coladas del Llaima debe obtener una similitud mayor que el cono del mismo volcán.
- Si no se encuentra un análogo lunar documentado en Chile, la validación se limita a esta prueba de coherencia y se declara expresamente como limitación.

### 8.2 Métricas y lectura de resultados

La métrica principal de validación es el percentil de ranking de cada sitio entre todas las celdas chilenas que pasan el filtro correspondiente. El AUC puede informarse como métrica secundaria, considerando que con pocos puntos de referencia es inestable.

La interpretación de cada ficha debe separar:

1. **Similitud observada:** resultado del cálculo; en el MVP es similitud topográfica.
2. **Interpretación científica:** explicación sustentada en literatura, cartografía y evidencia geológica.
3. **Utilidad potencial:** hipótesis de aplicación en investigación, ensayos de instrumentos, movilidad robótica, muestreo o preparación de misiones.

Si un benchmark o control no cumple el comportamiento esperado, el resultado se informa igualmente y se investiga su causa; no se ajustan los datos para forzar el cumplimiento.

## 9. Flujo metodológico reproducible

1. Descargar y registrar los productos terrestres y planetarios.
2. Verificar integridad, sistema de referencia, unidades, resolución, cobertura y calidad.
3. Delimitar las áreas piloto planetarias y los sitios chilenos.
4. Construir la grilla nacional y las unidades de detalle.
5. Armonizar los modelos de elevación a la resolución base común.
6. Calcular pendiente P90, relieve local P95–P5 y rugosidad en ventanas de 5 km.
7. Construir los perfiles planetarios con la mediana y los percentiles 10–90 de sus ventanas.
8. Aplicar el filtro de aridez para Marte o el filtro litológico para la Luna.
9. Calcular cobertura, distancia por variable y similitud topográfica.
10. Ejecutar las 500 repeticiones Monte Carlo y calcular estabilidad/rangos.
11. Validar benchmarks, controles y candidatos con fuentes científicas y cartográficas.
12. Exportar resultados y conectarlos con los mapas, comparador y fichas de la aplicación.

## 10. Entregables del motor analítico

| Archivo | Contenido esperado |
|---|---|
| `data/processed/grid.csv` | `cell_id` y coordenadas del centro de cada celda |
| `data/targets.json` | Perfiles de Elysium Planitia y Mare Tranquillitatis: valor, rango, tipo, fuente y metadatos por variable |
| `results/<perfil>_profile.csv` | `cell_id`, distancia/similitud por variable, cobertura, similitud global y estado del filtro |
| `results/<perfil>_montecarlo.csv` | `cell_id`, p_top y percentiles p05, p50 y p95 del ranking |
| `results/sites_summary.csv` | Resultados de los sitios del MVP, nivel de confianza y diferencias por variable |
| `results/validation.json` | Percentiles de benchmarks y controles; AUC si se calcula |

Los nombres y esquemas definitivos deben mantenerse consistentes entre el motor analítico y la aplicación.

## 11. Alcance, limitaciones y trabajo futuro

TerraMatch Chile:

- No certifica lugares como análogos perfectos.
- No identifica sitios seguros de aterrizaje ni rutas transitables para vehículos específicos.
- No predice habitabilidad extraterrestre ni demuestra existencia de vida.
- No reemplaza la interpretación geológica experta.
- No equipara condiciones que no son físicamente comparables, como gravedad, atmósfera, vacío, radiación o polvo electrostático.
- No interpreta la similitud topográfica como similitud automática de materiales, composición, temperatura o procesos.

El MVP se concentra en dos perfiles y tres variables topográficas. La incorporación de variables térmicas, espectrales, mineralógicas, hídricas, glaciares, biológicas o subsuperficiales queda para fases posteriores, una vez que existan productos comparables y documentados.

PCA y clustering (por ejemplo, K-means) pueden utilizarse como exploración complementaria si el tiempo y la calidad de los datos lo permiten. No son requisito para el funcionamiento central y sus agrupaciones no constituyen evidencia de analogía planetaria.

## 12. Fuentes de datos principales

- ASTER GDEM v3: [NASA/USGS LP DAAC](https://lpdaac.usgs.gov/products/astgtmv003/)
- GPM IMERG Final V07 mensual: [NASA GES DISC](https://doi.org/10.5067/GPM/IMERG/3B-MONTH/07)
- SERNAGEOMIN, Mapa Geológico de Chile 1:1.000.000: [servicio WMS](http://ogc.sernageomin.cl/cgi-bin/SNGM_Bedrock_Geology/wms?request=GetCapabilities&service=WMS)
- Biblioteca del Congreso Nacional, mapas vectoriales: [BCN](https://www.bcn.cl/siit/mapas_vectoriales)
- SLDEM2015: [NASA PDS Geosciences Node / PGDA](https://pgda.gsfc.nasa.gov/products/54)
- MOLA MEGDR: [USGS Astrogeology](https://astrogeology.usgs.gov/search/map/mars_mgs_mola_dem_463m) y [PDS Geosciences Node](https://pds-geosciences.wustl.edu/missions/mgs/megdr.html)
- Inventario USGS de análogos terrestres: [Known Terrestrial Analog Sites for Planetary Science](https://doi.org/10.5066/P9J72921)

La documentación de fuentes no reemplaza el registro de los identificadores, versiones y fechas de los archivos efectivamente descargados. Esos metadatos deben mantenerse en el inventario de datos del repositorio.
