
import streamlit as st

st.set_page_config(
    page_title="TerraMatch Chile",
    page_icon="🌎",
    layout="wide"
)

# Encabezado
st.title("🌎 TerraMatch Chile")
st.subheader(
    "Explorando ambientes terrestres chilenos como análogos "
    "parciales de la Luna y Marte"
)

st.markdown("""
TerraMatch Chile es una plataforma de exploración y comparación
geoespacial que busca identificar ambientes de Chile con características
comparables a determinados entornos lunares y marcianos.
""")

st.divider()

# Navegación
st.sidebar.title("Exploración")
modulo = st.sidebar.selectbox(
    "Selecciona un módulo:",
    [
        "Inicio",
        "Explorador territorial",
        "Selector planetario",
        "Motor de descubrimiento",
        "Comparador de ambientes",
        "Ficha de analogía"
    ]
)

# Contenido de los módulos
if modulo == "Inicio":
    st.header("Bienvenido a TerraMatch Chile")
    st.write(
        "Explora las características de distintos ambientes "
        "terrestres y sus posibles analogías planetarias."
    )
    st.info("Plataforma en desarrollo. Los datos se incorporarán progresivamente.")

elif modulo == "Explorador territorial":
    st.header("Explorador territorial")
    st.write("Visualización geográfica de ambientes seleccionados de Chile.")
    st.warning("Pendiente: integrar datos geoespaciales y mapas.")

elif modulo == "Selector planetario":
    st.header("Selector planetario")
    planeta = st.radio("Selecciona un cuerpo celeste:", ["Luna", "Marte"])
    st.write(f"Entorno seleccionado: {planeta}")
    st.warning("Pendiente: incorporar características de referencia.")

elif modulo == "Motor de descubrimiento":
    st.header("Motor de descubrimiento")
    st.write("Identificación de posibles ambientes análogos.")
    st.warning("Pendiente: integrar resultados del análisis.")

elif modulo == "Comparador de ambientes":
    st.header("Comparador de ambientes")
    st.write("Comparación de características entre ambientes terrestres y planetarios.")
    st.warning("Pendiente: integrar variables y resultados comparativos.")

elif modulo == "Ficha de analogía":
    st.header("Ficha de analogía")
    st.write("Resumen de las características y diferencias de cada analogía.")
    st.warning("Pendiente: integrar fichas con información validada.")

st.divider()
st.caption("TerraMatch Chile | NASA Space Apps Challenge")
