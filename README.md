# BioConecta QRoo

**Zona piloto:** Periferia de Cancún, municipio de Benito Juárez, Quintana Roo  
**Especie focal (MVP):** Jaguar (*Panthera onca*)  
**Enfoque:** Prototipo geoespacial exploratorio de idoneidad potencial de hábitat, fragmentación de parches y alertas explicables.

> **Aviso científico:** Este prototipo es una herramienta exploratoria basada en datos públicos y reglas documentadas. **No** mide abundancia de jaguares, **no** confirma rutas ni ocupación actual y **no** predice extinciones. Todos los datos simulados se etiquetan explícitamente como `simulated`.

## Estructura del repositorio

```text
.
├── app/
│   └── streamlit_app.py     # Dashboard interactivo (Streamlit + Folium)
├── data/
│   ├── raw/                 # Datos fuente y AOI (GeoTIFFs ignorados en Git)
│   ├── processed/           # Salidas reales del ETL (patches.geojson / patches.csv)
│   └── demo/                # Datos de ejemplo válidos con el contrato de datos
├── src/
│   └── alerts.py            # Motor de alertas explicables (y módulos del ETL)
├── docs/                    # Investigación, metodología y validación
├── tests/                   # Pruebas unitarias de reglas y contrato
├── requirements.txt
└── README.md
```

## Instalación y ejecución

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Contrato de datos (Integrante A → Integrante B)

Archivo esperado en `data/processed/patches.geojson` (en `EPSG:4326` para visualización web, con métricas calculadas en `EPSG:32616`) y/o `data/processed/patches.csv`:

| Columna | Tipo | Descripción |
|---|---|---|
| `patch_id` | string | Identificador estable del parche (ej. `QR-001`). |
| `area_ha` | float | Superficie de cobertura arbórea en hectáreas (CRS métrico). |
| `suitability_score` | float \| null | Media espacial del índice exploratorio `H(x)` en `[0, 1]`. |
| `distance_road_m` | float \| null | Distancia a red vial en metros (`null` si no hay capa vial). |
| `connectivity_score` | float \| null | Conectividad potencial (`null` si no aplica). |
| `vegetation_loss_pct` | float \| null | Pérdida temporal (`null` si solo existe un año de datos). |
| `risk_level` | string | `bajo`, `moderado`, `alto` o `sin_datos`. |
| `alert_reason` | string | Explicación legible de la regla aplicada. |
| `data_year` | integer | Año de la capa base (ej. `2021`). |
| `scenario_type` | string | `observed`, `modeled` o `simulated`. |
