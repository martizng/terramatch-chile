# TerraMatch Chile - Integrante 2 (BJOR)
# Reproduccion de recortes planetarios desde productos originales.
# Requiere el paquete 'terra' y la estructura data/mars/raw, data/moon/raw.
# No sobrescribe los GeoTIFF definitivos en data/*/processed.

library(terra)

proyecto <- file.path(path.expand('~'), 'TerraMatch_BJOR')
if (!dir.exists(proyecto)) stop('No se encuentra la carpeta TerraMatch_BJOR en Documentos.')
setwd(proyecto)

dir.create('data/verificacion', recursive = TRUE, showWarnings = FALSE)

raw_marte_dem <- 'data/mars/raw/megt44n090hb.lbl'
raw_marte_counts <- 'data/mars/raw/megc44n090hb.lbl'
raw_luna <- 'data/moon/raw/SLDEM2015_512_00N_30N_000_045.JP2'
stopifnot(file.exists(raw_marte_dem), file.exists(raw_marte_counts), file.exists(raw_luna))

# Marte - MOLA MEGDR, mosaico 90-180 E y 0-44 N.
# Ajustar la georreferenciacion de la grilla PDS a coordenadas marcianas en grados
# (radio cartografico 3396000 m), como en el procedimiento original.
mola_dem <- rast(raw_marte_dem)
mola_counts <- rast(raw_marte_counts)
stopifnot(compareGeom(mola_dem, mola_counts, stopOnError = FALSE))

crs_marte <- '+proj=longlat +a=3396000 +b=3396000 +no_defs +type=crs'
ext(mola_dem) <- ext(90, 180, 0, 44)
ext(mola_counts) <- ext(90, 180, 0, 44)
crs(mola_dem) <- crs_marte
crs(mola_counts) <- crs_marte

zona_marte <- ext(135.65, 136.15, 4.25, 4.75)
elysium_dem <- crop(mola_dem, zona_marte)
elysium_counts <- crop(mola_counts, zona_marte)

writeRaster(elysium_dem, 'data/verificacion/elysium_mola_dem.tif', overwrite = TRUE)
writeRaster(elysium_counts, 'data/verificacion/elysium_mola_counts.tif', overwrite = TRUE)

# Luna - SLDEM2015, se conserva la referencia lunar original.
# La etiqueta PDS del producto respalda el factor 0.5 para elevaciones en metros.
sldem <- rast(raw_luna)
zona_luna <- ext(22.98, 23.97, 0.18, 1.17)
tranquillitatis <- crop(sldem, zona_luna, snap = 'out') * 0.5
names(tranquillitatis) <- 'elevacion_m'

writeRaster(
  tranquillitatis,
  'data/verificacion/tranquillitatis_sldem2015_dem.tif',
  datatype = 'FLT4S',
  gdal = 'COMPRESS=LZW',
  overwrite = TRUE
)

# Verificacion contra los archivos de entrega oficial.
archivos <- c(
  'elysium_mola_dem.tif',
  'elysium_mola_counts.tif',
  'tranquillitatis_sldem2015_dem.tif'
)
resultados <- logical(length(archivos))

for (i in seq_along(archivos)) {
  cuerpo <- if (i <= 2) 'mars' else 'moon'
  entregado <- rast(file.path('data', cuerpo, 'processed', archivos[i]))
  reproducido <- rast(file.path('data/verificacion', archivos[i]))

  geo_ok <- compareGeom(entregado, reproducido, stopOnError = FALSE)
  valores_ok <- isTRUE(all.equal(
    values(entregado), values(reproducido), check.attributes = FALSE
  ))
  resultados[i] <- geo_ok && valores_ok
  cat(archivos[i], '| Geometria:', geo_ok,
      '| Valores:', valores_ok, '\n')
}

if (!all(resultados)) stop('Hay diferencias: revisar los recortes antes de compartir.')
cat('\nVERIFICACION COMPLETA: los tres GeoTIFF son reproducibles.\n')
