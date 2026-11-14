
import streamlit as st

st.set_page_config(
    page_title="TerraMatch Chile",
    page_icon="🌎",
    layout="wide"
)

# Identidad visual
st.markdown("""
<style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #102D46, #176B78);
        padding: 38px;
        border-radius: 18px;
        color: white;
        margin-bottom: 28px;
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #E4F1F3;
        font-size: 17px;
    }

    .module-card {
        background: #F2F6F8;
        border: 1px solid #DCE6EA;
        border-radius: 14px;
        padding: 20px;
        min-height: 155px;
        margin-bottom: 15px;
    }

    .module-card h3 {
        color: #164B60;
        font-size: 19px;
    }

    .module-card p {
        color: #354A55;
        font-size: 14px;
    }

    .section-label {
        color: #176B78;
        font-weight: 700;
        letter-spacing: 1px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Menú lateral
st.sidebar.title("🌎 TerraMatch Chile")
st.sidebar.caption("Plataforma de exploración geoespacial")
st.sidebar.divider()

modulo = st.sidebar.selectbox(
    "EXPLORACIÓN",
    [
        "Inicio",
        "Explorador territorial",
        "Selector planetario",
        "Motor de descubrimiento",
        "Comparador de ambientes",
        "Ficha de analogía"
    ]
)

st.sidebar.divider()
st.sidebar.caption("NASA Space Apps Challenge | 2026")

# Página de inicio
if modulo == "Inicio":

    st.markdown("""
    <div class="hero">
        <h1>🌎 TerraMatch Chile</h1>
        <p><b>Explorando la Tierra para comprender otros mundos.</b></p>
        <p>
        Identificación y comparación de ambientes terrestres chilenos
        como posibles análogos parciales de determinados entornos
        de la Luna y Marte.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<p class="section-label">SOBRE EL PROYECTO</p>',
        unsafe_allow_html=True
    )

    st.header("Chile como laboratorio natural")

    st.write("""
    Chile presenta una extraordinaria diversidad geológica y ambiental.
    Sus desiertos, salares, terrenos volcánicos y ambientes de alta montaña
    ofrecen oportunidades para estudiar procesos y características que
    pueden ser comparables con determinados entornos planetarios.

    TerraMatch Chile propone integrar información geoespacial, ambiental
    y científica para explorar estas relaciones, identificar similitudes
    y reconocer también sus diferencias.
    """)

    st.divider()

    st.markdown(
        '<p class="section-label">EXPLORA LA PLATAFORMA</p>',
        unsafe_allow_html=True
    )

    st.header("Módulos de TerraMatch")

    modulos = [
        ("🗺️ Explorador territorial",
         "Explora ambientes seleccionados de Chile mediante información geográfica."),
        ("🪐 Selector planetario",
         "Selecciona perfiles de referencia de la Luna y Marte."),
        ("🔎 Motor de descubrimiento",
         "Identifica posibles candidatos mediante variables ambientales y geoespaciales."),
        ("⚖️ Comparador de ambientes",
         "Examina similitudes y diferencias entre ambientes terrestres y planetarios."),
        ("📋 Ficha de analogía",
         "Consulta las características, aplicaciones y limitaciones de cada candidato.")
    ]

    columnas = st.columns(2)

    for i, (titulo, descripcion) in enumerate(modulos):
        with columnas[i % 2]:
            st.markdown(f"""
            <div class="module-card">
                <h3>{titulo}</h3>
                <p>{descripcion}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        '<p class="section-label">AMBIENTES TERRESTRES DE INTERÉS</p>',
        unsafe_allow_html=True
    )

    st.header("La diversidad de Chile")

    ambientes = st.columns(5)

    nombres = [
        ("🏜️", "Desiertos", "Aridez y suelos"),
        ("🧂", "Salares", "Sales y evaporitas"),
        ("🌋", "Volcánicos", "Rocas y flujos de lava"),
        ("🏔️", "Alta montaña", "Hielo y procesos periglaciares"),
        ("🧊", "Glaciares", "Morfología y procesos asociados al hielo")
    ]

    for columna, (icono, nombre, detalle) in zip(ambientes, nombres):
        with columna:
            st.markdown(f"### {icono}")
            st.markdown(f"**{nombre}**")
            st.caption(detalle)

    st.divider()

    st.info(
        "Estado del proyecto: prototipo en desarrollo. "
        "Los resultados científicos y las capas de datos se incorporarán "
        "a medida que avance el análisis y la validación."
    )

# Explorador territorial
elif modulo == "Explorador territorial":
    st.title("🗺️ Explorador territorial")
    st.write("Visualización geográfica de ambientes seleccionados de Chile.")
    st.warning("Pendiente: integrar capas geoespaciales y sitios de estudio.")

# Selector planetario
elif modulo == "Selector planetario":
    st.title("🪐 Selector planetario")
    planeta = st.radio("Selecciona un cuerpo celeste:", ["Luna", "Marte"])
    st.write(f"Perfil de referencia seleccionado: **{planeta}**")
    st.warning("Pendiente: incorporar perfiles y variables científicas.")

# Motor de descubrimiento
elif modulo == "Motor de descubrimiento":
    st.title("🔎 Motor de descubrimiento")
    st.write("Identificación de posibles ambientes análogos.")
    st.warning("Pendiente: integrar resultados del análisis del equipo.")

# Comparador
elif modulo == "Comparador de ambientes":
    st.title("⚖️ Comparador de ambientes")
    st.write("Comparación de características terrestres y planetarias.")
    st.warning("Pendiente: integrar variables y métricas validadas.")

# Ficha de analogía
elif modulo == "Ficha de analogía":
    st.title("📋 Ficha de analogía")
    st.write("Resumen de características, similitudes y diferencias.")
    st.warning("Pendiente: integrar fichas con información validada.")

st.divider()
st.caption("TerraMatch Chile | NASA Space Apps Challenge 2026")
