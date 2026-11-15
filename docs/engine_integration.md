# Integración del motor analítico — TerraMatch Chile

**Estado:** código integrado en rama de revisión; el motor aún no ha generado resultados científicos con ASTER de Chile.  
**Procedencia:** módulo de análisis entregado por Rojas, corregido y comprobado con pruebas sintéticas.  
**Fuente metodológica:** `docs/methodology.md` (v2.0).

## Qué incluye

- `src/analysis.py`: distancia al rango, IQR/desviación estándar, cobertura y filtros.
- `src/comparison.py`: Monte Carlo 500 repeticiones, estabilidad, confianza y sitios.
- `src/validation.py`: benchmarks y controles; informa fallos sin alterar resultados.
- `src/run_pipeline.py`: calcula salidas solo cuando el perfil y filtro requerido están disponibles.
- `src/features/`: derivación de topografía, creación de perfiles desde DEM y elaboración de `master.csv`.
- `src/grid/`: regeneración de grilla por límites.
- `src/sites.py`: utiliza polígonos explícitos de `data/chile/sites/`; no inventa contornos faltantes.
- `config/terramatch_config.json`: parámetros reproducibles y criterios de aceptación.
- `data/targets.json`: perfil de Marte **preliminar**, basado en cinco ventanas MOLA con cobertura directa suficiente; perfil lunar marcado como pendiente.
- `tests/`: pruebas **sintéticas**. Sus resultados nunca deben mostrarse como descubrimientos reales.

## Correcciones de seguridad metodológica

1. Si IQR = 0 y desviación estándar = 0, la variable se excluye de las distancias y de la cobertura. Se requieren al menos dos variables informativas.
2. Si falta la columna del filtro de aridez/volcanismo o no tiene valores, el perfil queda con estado `missing_filter_data`; **no se calcula un ranking sin filtro**.
3. Un sitio sin polígono validado se marca `pending_geometry`; no se sustituyen los contornos de Pajonales/coladas Llaima por círculos o anillos inventados.
4. Monte Carlo trata empates sin favorecer el orden de las filas y evita calcular percentiles de celdas no elegibles.
5. El script de topografía terrestre utiliza UTM 19S como aproximación continental **solo** dentro de la caja [−76°, −66°] de longitud y [−56°, −17°] de latitud. La distorsión de escala se comprobó por muestreo en ese dominio; fuera de él la suposición no aplica.

## Instalación y pruebas

Desde la raíz del repositorio:

```bash
python -m pip install -r requirements-analysis.txt
python tests/test_engine_safeguards.py
python tests/test_pipeline_synthetic.py
```

Las pruebas no requieren ASTER. Deben completarse con `ALL SAFEGUARD CHECKS PASSED` y `ALL CHECKS PASSED`. El repositorio de la interfaz `app.py` se mantiene sin cambios.

## Reproducción del perfil planetario

Los recortes MOLA ya están en GitHub:

```bash
python src/features/build_targets.py --mars data/mars/processed/elysium_mola_dem.tif --mars-count data/mars/processed/elysium_mola_counts.tif --out data/targets.json
```

Revisar `data/targets.json` y sus limitaciones antes de presentar resultados. **Solo cinco ventanas MOLA** pasan el umbral de 50 % de medición directa; representatividad pendiente de validar. No eliminar el control de conteos. La Luna sigue pendiente de SLDEM2015.

## Cuando llegue ASTER GDEM v3

Primero verificar teselas y disponibilidad, y construir un DEM derivado que cubra los sitios que se evaluarán. Reemplazar el siguiente ejemplo de ruta por el nombre real:

```bash
python src/features/chile_features.py --grid data/processed/grid.csv --dem data/chile/processed/aster_dem_validado.tif --precip data/chile/processed/imerg_precip_2001_2024.tif --out data/processed/master.csv
python src/run_pipeline.py --grid data/processed/grid.csv --master data/processed/master.csv --targets data/targets.json --sites-dir data/chile/sites --out results
```

El mosaico ASTER aún **no está en GitHub**, por tanto estos dos comandos de producción no pueden ejecutarse con datos terrestres auténticos todavía. Si se dispone de cobertura ASTER parcial, no se debe presentar como ranking nacional completo. No usar el ráster combinado CR2MET–IMERG para el filtro principal sin modificar y justificar la metodología.

## Pendientes de validación

- Adquirir ASTER GDEM v3 en la cobertura necesaria y revisar unidades, CRS, NoData y resolución efectiva.
- Completar polígonos de Salar de Pajonales y coladas del Llaima.
- Validar clasificación de unidades volcánicas SERNAGEOMIN antes del filtro lunar.
- Obtener SLDEM2015/LOLA y validar el perfil lunar.
- Evaluar representatividad de las cinco ventanas válidas del perfil MOLA.
- Ejecutar pruebas con datos reales y revisar puntajes/percentiles; los tests sintéticos no reemplazan la validación científica.

**Estados internos del motor:** `outside_filter` = fuera del filtro; `insufficient_data` = información insuficiente; `scored` = calculado; `missing_filter_data` = falta el insumo del filtro; `pending_geometry` = sitio pendiente de delimitar.