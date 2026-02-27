# Challenge Técnico — Ingeniería de Datos (World/Country Data)

Este repositorio contiene la resolución de una **prueba técnica para una empresa de datos**.  
Incluye una solución end-to-end: **ingesta desde APIs públicas**, **ETL con validaciones**, **staging en CSV**, **carga a una base SQLite** y **dashboard en Power BI**.

🎥 **Video (walkthrough de la solución):**  
https://drive.google.com/file/d/1vY66Qq0FBI696hyjYAXo_N2uwsLU44jt/view

---

## Contenido
- [Objetivo / Consigna](#objetivo--consigna)
- [Fuentes de datos](#fuentes-de-datos)
- [Solución implementada](#solución-implementada)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Cómo ejecutar](#cómo-ejecutar)
- [Resultados](#resultados)
- [Decisiones de diseño](#decisiones-de-diseño)
- [Limitaciones y próximos pasos](#limitaciones-y-próximos-pasos)

---

## Objetivo / Consigna

Construir una solución de ingeniería de datos que:

1. **Extraiga información de países y métricas asociadas** desde **APIs públicas**.
2. **Transforme y normalice** datos semiestructurados (arrays / diccionarios JSON) a estructuras tabulares.
3. Aplique **controles de calidad** (tipos, rangos, nulos, integridad referencial).
4. Persista resultados en un **área de staging** (archivos) y luego en una **base de datos**.
5. Presente un **dashboard** consumiendo el dataset final.
6. (Plus) Dejar lista una **orquestación** repetible del pipeline.

---

## Fuentes de datos

La solución integra dos fuentes principales:

- **REST Countries (v3.1)**: información “maestra” del país (códigos, región/subregión, área, status ONU, fronteras, idiomas, monedas, husos horarios, etc.).
- **World Bank API**: series de tiempo de indicadores demográficos (población total y porcentajes urbano/rural) por país y año.

---

## Solución implementada

### 1) Orquestación (Prefect + Papermill)
- El pipeline se ejecuta como un **flow maestro** que corre todos los notebooks `etl_*.ipynb` en orden.
- Se usa **Papermill** para ejecutar notebooks como unidades de ETL repetibles.
- Hay configuración de **deployment/schedule** para correr diariamente (cron).

### 2) Patrón ETL (por dominio)
Cada notebook sigue un patrón consistente:

**Extract → Transform → Validate → Load**
- **Extract**: requests a API(s), paginado cuando aplica.
- **Transform**: normalización a `pandas.DataFrame`, *explode* de listas, flatten de diccionarios, renames, casts.
- **Validate**: reglas con **Pandera** (schema, rangos, longitud de códigos ISO, etc.) + checks de **integridad referencial** contra `countries.csv`.
- **Load**: escritura de un CSV en `stage/`.

Ejemplos de salidas (staging):
- `stage/countries.csv` (tabla base)
- `stage/country_languages.csv`, `stage/country_currencies.csv`, `stage/country_borders.csv`, etc.
- `stage/country_population.csv`, `stage/country_urban_population.csv`, `stage/country_rural_population.csv`

### 3) Integridad referencial
- La tabla base `countries.csv` actúa como **catálogo de países** (clave `cca3`).
- Los ETLs dependientes validan que `id_country ∈ countries(cca3)` antes de persistir.

### 4) Carga a base de datos (SQLite)
- Un ETL final construye/actualiza una base **SQLite** (`stage/world_data.db`).
- Se cargan **todos los CSV** de `stage/` como tablas, permitiendo un dataset final fácil de consumir por BI.

### 5) Dashboard (Power BI)
- En `Dashboard/` se incluye el archivo `.pbix` y capturas.
- El dashboard está pensado para consumir el modelo en SQLite (o los CSV) y mostrar vistas por país/región/continente, además de tendencias de población.

---

## Estructura del repositorio

.
├── Dashboard/
│ ├── Paises.pbix
│ └── Screenshots/
│ ├── Argentina.png
│ ├── Andorra.png
│ ├── Continentes.png
│ └── Regiones.png
├── doc/
│ ├── Desafio_Data_Engineer_Generic.pdf
│ ├── Diseño de Solución Cloud – ETL World Data.pdf
│ └── Informe de Proceso ETL – World Data.pdf
├── etl/
│ ├── master_flow.ipynb
│ ├── master_entry.py
│ ├── prefect.yaml
│ ├── deployment.yaml
│ ├── etl_Country.ipynb
│ ├── etl_*.ipynb
│ └── common/
│ ├── loaders.py
│ └── utils.py
└── stage/
├── *.csv
└── world_data.db

## Ejecutar ETLs individuales

Podés abrir y correr cualquier notebook `etl_*.ipynb` de forma independiente, pero en general:

1. Corré primero **`etl_Country.ipynb`** (catálogo base).
2. Luego el resto de los notebooks `etl_*.ipynb`.
3. Por último **`etl_database.ipynb`** para construir `world_data.db`.

---

## Resultados

Capturas rápidas del dashboard (Power BI):

- `Dashboard/Screenshots/Regiones.png`
- `Dashboard/Screenshots/Continentes.png`
- `Dashboard/Screenshots/Argentina.png`
- `Dashboard/Screenshots/Andorra.png`

---

## Decisiones de diseño

- **Staging en CSV:** simple, auditable y fácil de versionar/inspeccionar.
- **SQLite como “data mart” local:** habilita consumo directo desde Power BI y simplifica la portabilidad.
- **Notebooks como unidades ETL:** buen trade-off para una prueba técnica (rápido para iterar, claro para explicar).
- **Pandera para data quality:** contratos explícitos de datos (tipos, rangos, claves).
- **Prefect + schedule:** deja lista la ejecución repetible y orquestada.

---

## Limitaciones y próximos pasos

- **Empaquetado:** migrar notebooks a módulos `.py` para ejecución headless más robusta (CI/CD).
- **Observabilidad:** logs estructurados, métricas por etapa, retries/backoff y alertas.
- **Modelado:** definir un modelo dimensional explícito (star/snowflake) en vez de “1 CSV = 1 tabla”.
- **Testing:** tests unitarios + contract tests (schemas) + data tests sobre muestras.
- **Configuración:** parametrizar rangos de años, paths y endpoints por config/env vars.

---

## Documentación adicional

En `doc/` se adjunta:

- Consigna genérica del desafío  
- Diseño de solución (cloud/arquitectura)  
- Informe de proceso ETL  

---

## Extras (si querés mejorar el repo)

Si querés, también puedo:

- Generarte un `requirements.txt` y/o `pyproject.toml`
- Armar un diagrama de arquitectura (Mermaid) más detallado
- Redactar una versión del README en inglés para recruiters
