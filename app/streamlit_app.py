import json
from pathlib import Path

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_GEOJSON = ROOT_DIR / "data" / "processed" / "patches.geojson"
DEMO_GEOJSON = ROOT_DIR / "data" / "demo" / "patches_demo.geojson"

RISK_COLORS = {
    "alto": "#d73027",
    "moderado": "#fc8d59",
    "bajo": "#1a9850",
    "sin_datos": "#999999",
}

st.set_page_config(
    page_title="BioConecta QRoo — Cancún",
    page_icon="🌿",
    layout="wide",
)

st.title("BioConecta QRoo — Cancún: interfaz urbano–forestal")
st.caption(
    "Especie focal (MVP): Jaguar (Panthera onca) | Cobertura base: ESA WorldCover 2021 v200 | "
    "Herramienta exploratoria — no confirma presencia ni rutas reales."
)

if PROCESSED_GEOJSON.exists():
    data_path = PROCESSED_GEOJSON
    is_demo = False
else:
    data_path = DEMO_GEOJSON
    is_demo = True

if is_demo:
    st.warning(
        "Mostrando **datos de demostración (`simulated`)** del contrato inicial (`data/demo/patches_demo.geojson`). "
        "Cuando el Integrante A exporte `data/processed/patches.geojson`, el dashboard los cargará automáticamente."
    )

with data_path.open("r", encoding="utf-8") as f:
    geojson_data = json.load(f)

rows = [feat["properties"] for feat in geojson_data.get("features", [])]
df = pd.DataFrame(rows)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Parches cargados", len(df))
col2.metric("Área total (ha)", f"{df['area_ha'].sum():.1f}" if not df.empty else "0.0")
col3.metric(
    "Alertas riesgo alto",
    int((df["risk_level"] == "alto").sum()) if "risk_level" in df else 0,
)
col4.metric(
    "Tipo de escenario",
    ", ".join(sorted(df["scenario_type"].dropna().unique())) if "scenario_type" in df else "sin_datos",
)

m = folium.Map(location=[21.145, -86.912], zoom_start=13, tiles="CartoDB positron")

def style_patch(feature):
    risk = feature["properties"].get("risk_level", "sin_datos")
    color = RISK_COLORS.get(risk, "#999999")
    return {
        "fillColor": color,
        "color": "#222222",
        "weight": 1.5,
        "fillOpacity": 0.55,
    }

folium.GeoJson(
    geojson_data,
    name="Parches de cobertura",
    style_function=style_patch,
    tooltip=folium.GeoJsonTooltip(
        fields=["patch_id", "area_ha", "suitability_score", "risk_level", "scenario_type"],
        aliases=["Parche:", "Área (ha):", "Idoneidad H:", "Riesgo:", "Escenario:"],
        localize=True,
    ),
).add_to(m)

folium.LayerControl().add_to(m)
st_folium(m, width=None, height=480, returned_objects=[])

st.subheader("Tabla de parches (contrato de datos)")
st.dataframe(df, use_container_width=True)
