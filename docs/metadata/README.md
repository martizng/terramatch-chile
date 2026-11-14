# Guía de entrega y metadatos de datos geoespaciales

## 1. Objetivo

Este documento establece los requisitos para entregar, identificar y documentar los conjuntos de datos utilizados en TerraMatch Chile.

Su objetivo es asegurar que los archivos recibidos sean trazables, verificables y utilizables para el procesamiento geoespacial y el análisis de similitud entre ambientes terrestres, lunares y marcianos.

Todos los integrantes responsables de recopilar datos deben acompañar sus archivos con la información solicitada en esta guía.

## 2. Requisitos generales de entrega

Cada conjunto de datos debe entregarse con:

- Archivo original descargado u obtenido desde la fuente.
- Nombre del producto o conjunto de datos.
- Institución o plataforma de origen.
- Enlace de descarga o acceso.
- Versión del producto, cuando corresponda.
- Fecha de descarga o consulta.
- Formato original.
- Resolución espacial o escala, cuando corresponda.
- Cobertura geográfica y extensión del área.
- Sistema de coordenadas y datum, cuando corresponda.
- Unidades de medida de las variables.
- Descripción de la información contenida.
- Restricciones de uso o licencia, si están disponibles.

No se deben reemplazar los archivos originales por capturas de pantalla, imágenes de visualización o versiones modificadas sin conservar el original.

## 3. Información específica según el tipo de dato

### 3.1. Modelos digitales de elevación (DEM)

Para los modelos de elevación de Chile, Marte y la Luna se debe registrar:

- Nombre del producto.
- Misión, instrumento o institución responsable.
- Resolución espacial o resolución nativa.
- Sistema de coordenadas.
- Datum horizontal y referencia vertical, si están documentados.
- Unidades de elevación.
- Extensión geográfica.
- Valores NoData o píxeles sin información.
- Fecha y versión del producto.
- Procesamientos realizados, si corresponde.

Productos considerados:

- ASTER GDEM v3: modelo de elevación terrestre de Chile.
- MOLA MEGDR: modelo de elevación de Marte, con referencia de 128 píxeles por grado.
- SLDEM2015: modelo lunar que integra información de LOLA y Kaguya.

### 3.2. Datos de precipitación

Para GPM IMERG Final V07 se debe registrar:

- Nombre y versión del producto.
- Institución de origen.
- Periodo temporal utilizado.
- Frecuencia temporal de los datos.
- Resolución espacial.
- Unidades de precipitación.
- Cobertura geográfica.
- Fecha de descarga.
- Variables o bandas utilizadas.

Para el proyecto se considera GPM IMERG Final V07, producto mensual, con climatología 2001–2024 y resolución aproximada de 0,1°.

### 3.3. Información geológica

Para los datos de SERNAGEOMIN se debe registrar:

- Nombre del mapa o servicio geológico.
- Institución responsable.
- Escala cartográfica.
- Fecha o versión disponible.
- Tipo de unidad geológica.
- Cobertura territorial.
- Método de obtención (descarga, servicio WMS u otro).
- Procesamiento o digitalización adicional realizada.

**Importante:** el servicio WMS de SERNAGEOMIN entrega imágenes y no polígonos geológicos directamente. Si se digitalizan unidades volcánicas o sectores de coladas, se debe documentar que se trata de una interpretación o digitalización realizada por el equipo.

### 3.4. Límites territoriales y sitios piloto

Para los límites de Chile y las áreas de estudio se debe registrar:

- Institución o fuente.
- Nombre de la capa.
- Tipo de geometría (punto, línea o polígono).
- Sistema de coordenadas.
- Escala o precisión conocida.
- Fecha de obtención.
- Método de delimitación, cuando corresponda.

Los sitios piloto considerados son:

- Yungay.
- Salar de Pajonales.
- Llaima: sector de coladas.
- Llaima: cono.
- Llullaillaco.

## 4. Formatos de entrega

Se recomienda utilizar los siguientes formatos:

| Tipo de información | Formato recomendado |
|---|---|
| Modelos de elevación | GeoTIFF (.tif) |
| Información geográfica vectorial | GeoJSON (.geojson) o GeoPackage (.gpkg) |
| Datos tabulares | CSV (.csv) |
| Datos científicos originales | Conservar formato original |
| Metadatos | JSON (.json) |
| Código y procesamiento | Python (.py) o Jupyter Notebook (.ipynb) |
| Documentación | Markdown (.md) o PDF (.pdf) |

Si el producto original se encuentra en NetCDF, HDF u otro formato científico, se debe conservar ese archivo y documentarlo. Las conversiones a GeoTIFF u otros formatos deben entregarse como copias procesadas, sin eliminar el original.

## 5. Organización de archivos

Los archivos deben separarse según su origen y estado de procesamiento:

- `data/chile/raw/`: datos originales de Chile.
- `data/chile/processed/`: datos terrestres procesados.
- `data/chile/sites/`: polígonos y geometrías de los sitios piloto.
- `data/mars/raw/`: datos originales de Marte.
- `data/mars/processed/`: datos marcianos procesados.
- `data/mars/metadata/`: metadatos de los productos marcianos.
- `data/moon/raw/`: datos originales de la Luna.
- `data/moon/processed/`: datos lunares procesados.
- `data/moon/metadata/`: metadatos de los productos lunares.

Los archivos originales no deben sobrescribirse ni modificarse directamente.

## 6. Convención para nombrar archivos

Se utilizará el siguiente formato:

`PLANETA_O_ZONA_PRODUCTO_VARIABLE_VERSION.ext`

Ejemplos:

- `CHILE_ASTER_GDEM_V3_ELEVACION.tif`
- `CHILE_GPM_IMERG_FINAL_V07_PRECIPITACION.nc`
- `MARS_MOLA_MEGDR_ELEVACION.tif`
- `MOON_SLDEM2015_ELEVACION.tif`
- `CHILE_LLAIMA_COLADAS_GEOLOGIA.geojson`

Los nombres deben ser descriptivos, sin espacios ni caracteres especiales.

## 7. Plantilla de metadatos

Cada conjunto de datos debe acompañarse de un archivo JSON con la información disponible.

Ejemplo de estructura:

```json
{
  "dataset_id": "MA001",
  "dataset_name": "MOLA MEGDR",
  "planet_or_zone": "Mars - Elysium Planitia",
  "variable": "Elevation",
  "source_institution": "NASA",
  "source_url": "",
  "product_version": "",
  "download_date": "",
  "original_filename": "",
  "original_format": "",
  "spatial_resolution": "128 pixels per degree",
  "coordinate_reference_system": "",
  "vertical_datum": "",
  "units": "",
  "geographic_extent": "",
  "temporal_coverage": "",
  "nodata_value": "",
  "license_or_usage_restrictions": "",
  "processing_applied": "None",
  "responsible_member": "",
  "additional_notes": ""
}
```

Los campos que no correspondan o cuya información no esté disponible deben quedar vacíos o indicarse como "No documentado". No se deben inventar valores.

## 8. Control de calidad y recepción

Antes de incorporar un archivo al repositorio, se debe comprobar:

1. Que provenga de una fuente identificable.
2. Que el archivo pueda abrirse y leerse.
3. Que su formato sea compatible con el uso previsto.
4. Que tenga resolución, unidades y sistema de referencia documentados cuando corresponda.
5. Que su cobertura espacial sea adecuada para el área de estudio.
6. Que se acompañe de sus metadatos.
7. Que cualquier procesamiento adicional esté documentado.

La recepción de un archivo no significa que esté aprobado para el análisis.

El estado de cada conjunto de datos se actualizará en `docs/data_inventory.csv`.

## 9. Responsabilidad de entrega

Cada integrante debe entregar los archivos originales y sus respectivos metadatos en la carpeta compartida de Google Drive asignada a su área de trabajo.

La persona responsable de la integración del repositorio revisará los archivos, verificará su documentación, actualizará el inventario y determinará su incorporación a GitHub.

**TerraMatch Chile — NASA Space Apps Challenge**
