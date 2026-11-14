
import streamlit as st
import folium
from streamlit_folium import st_folium

# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------

st.set_page_config(
    page_title="TerraMatch Chile | Planetary Research",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# IDENTIDAD VISUAL
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #172B36;
    --terracotta: #D47B55;
    --sand: #EAE6DA;
    --green: #718477;
    --ink: #26343B;
    --muted: #758087;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #F4F2EC;
    color: var(--ink);
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background-color: var(--navy);
}

[data-testid="stSidebar"] * {
    color: #F4F2EC !important;
}

[data-testid="stSidebar"] .stRadio label {
    padding: 7px 4px;
}

[data-testid="stSidebar"] hr {
    border-color: #52616A;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: var(--navy);
    letter-spacing: -0.7px;
}

.hero {
    background: var(--navy);
    padding: 48px 46px;
    border-radius: 17px;
    color: #F4F2EC;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}

.hero-label {
    color: #DCA082;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 18px;
}

.hero h1 {
    color: #F4F2EC;
    font-size: 43px;
    line-height: 1.15;
    font-weight: 800;
    margin-bottom: 15px;
}

.hero p {
    color: #D3DAD8;
    font-size: 16px;
    max-width: 700px;
    line-height: 1.7;
}

.hero-note {
    color: #DCA082;
    font-size: 12px;
    letter-spacing: 1px;
    margin-top: 26px;
    font-weight: 600;
}

.section-label {
    color: var(--terracotta);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 8px;
}

.info-card {
    background: #FFFFFF;
    padding: 23px;
    border: 1px solid #E5E1D7;
    border-radius: 12px;
    min-height: 155px;
}

.info-card h3 {
    font-size: 18px;
    margin-bottom: 9px;
}

.info-card p {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.6;
}

.card-number {
    color: var(--terracotta);
    font-family: 'Manrope', sans-serif;
    font-size: 27px;
    font-weight: 800;
    margin-bottom: 10px;
}

.ambient-card {
    background: #EAE6DA;
    border-radius: 11px;
    padding: 18px;
    min-height: 125px;
    border-bottom: 3px solid var(--green);
}

.ambient-card h4 {
    color: var(--navy);
    font-size: 15px;
    margin-bottom: 7px;
}

.ambient-card p {
    color: #68716E;
    font-size: 12px;
    line-height: 1.5;
}

.terra-divider {
    border: none;
    border-top: 1px solid #DDD9CF;
    margin: 30px 0;
}

.small-note {
    color: #758087;
    font-size: 12px;
}

.stButton > button {
    background: var(--terracotta);
    color: white;
    border: none;
    border-radius: 7px;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #B96543;
    color: white;
    border: none;
}

[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #E5E1D7;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# NAVEGACIÓN
# --------------------------------------------------

st.sidebar.markdown("""
<div style="padding: 12px 0 22px 0;">
    <div style="font-size: 25px; font-weight: 800;
                font-family: Manrope, sans-serif;">
        TERRA<span style="color:#D47B55;">MATCH</span>
    </div>
    <div style="font-size: 10px; letter-spacing: 2px;
                color:#BAC5C4;">
        CHILE · PLANETARY RESEARCH
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("PLATAFORMA DE EXPLORACIÓN")

modulo = st.sidebar.radio(
    "NAVEGACIÓN",
    [
        "Inicio",
        "Explorador territorial",
        "Selector planetario",
        "Motor de descubrimiento",
        "Comparador de ambientes",
        "Ficha de analogía"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:11px; color:#BAC5C4; line-height:1.7;">
<strong>PROYECTO</strong><br>
NASA Space Apps Challenge<br><br>
<strong>ENFOQUE</strong><br>
Chile como laboratorio natural
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# ENCABEZADO DE SECCIONES
# --------------------------------------------------

def section_header(label, title, description):
    st.markdown(
        f'<div class="section-label">{label}</div>',
        unsafe_allow_html=True
    )
    st.title(title)
    st.write(description)
    st.markdown('<hr class="terra-divider">', unsafe_allow_html=True)


# --------------------------------------------------
# INICIO
# --------------------------------------------------

if modulo == "Inicio":

    st.markdown("""
    <div class="hero">
        <div class="hero-label">CHILE AS A NATURAL LABORATORY</div>
        <h1>Exploring Earth.<br>Understanding other worlds.</h1>
        <p>
        Una plataforma de exploración geoespacial que busca identificar
        y caracterizar ambientes chilenos con características comparables
        a determinados entornos de la Luna y Marte.
        </p>
        <div class="hero-note">
        TIERRA &nbsp; / &nbsp; LUNA &nbsp; / &nbsp; MARTE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">EL PROYECTO</div>',
        unsafe_allow_html=True
    )
    st.header("Una nueva perspectiva sobre nuestros territorios")

    st.write("""
    Chile reúne una extraordinaria diversidad geológica y ambiental.
    TerraMatch propone utilizar esa diversidad como punto de partida
    para investigar posibles analogías terrestres y planetarias.

    Integramos información geoespacial, satelital y científica para
    explorar similitudes, diferencias y oportunidades de investigación.
    """)

    st.markdown('<hr class="terra-divider">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">EXPLORACIÓN</div>',
        unsafe_allow_html=True
    )
    st.header("Tres dimensiones de análisis")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="info-card">
            <div class="card-number">01</div>
            <h3>Territorio</h3>
            <p>Exploración de ambientes geológicos y geomorfológicos
            a lo largo de Chile.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <div class="card-number">02</div>
            <h3>Otros mundos</h3>
            <p>Perfiles ambientales de referencia de la Luna
            y Marte.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="info-card">
            <div class="card-number">03</div>
            <h3>Análisis</h3>
            <p>Comparación multidimensional de características
            y procesos superficiales.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="terra-divider">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">BIBLIOTECA TERRITORIAL</div>',
        unsafe_allow_html=True
    )
    st.header("Ambientes que queremos investigar")

    ambientes = [
        ("Desiertos hiperáridos", "Aridez, suelos y procesos superficiales."),
        ("Salares y evaporitas", "Sales, sulfatos y depósitos evaporíticos."),
        ("Terrenos volcánicos", "Basaltos, flujos de lava y morfología."),
        ("Alta montaña", "Hielo, congelamiento y procesos periglaciares."),
        ("Ambientes glaciares", "Morfología y procesos relacionados con hielo.")
    ]

    columnas = st.columns(3)

    for i, (nombre, descripcion) in enumerate(ambientes):
        with columnas[i % 3]:
            st.markdown(f"""
            <div class="ambient-card">
                <h4>{nombre}</h4>
                <p>{descripcion}</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")

    st.markdown('<hr class="terra-divider">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">PROPÓSITO</div>',
        unsafe_allow_html=True
    )
    st.header("¿Por qué TerraMatch?")

    st.write("""
    La utilidad de un análogo depende de la pregunta científica u
    operacional. Un ambiente puede ser relevante para estudiar materiales,
    otro para analizar procesos térmicos y otro para ensayar movilidad
    o estrategias de muestreo.

    TerraMatch busca hacer visibles esas diferencias y explicar
    por qué cada ambiente podría ser útil.
    """)


# --------------------------------------------------
# EXPLORADOR TERRITORIAL
# --------------------------------------------------

elif modulo == "Explorador territorial":

    section_header(
        "01 / CHILE",
        "Explorador territorial",
        "Una primera aproximación geográfica a los ambientes de interés."
    )

    st.info(
        "Este mapa muestra una base cartográfica general. "
        "Las capas científicas y los sitios de análisis se incorporarán "
        "cuando estén disponibles los datos validados del equipo."
    )

    mapa = folium.Map(
        location=[-33.5, -70.7],
        zoom_start=4,
        tiles="CartoDB positron"
    )

    st_folium(
        mapa,
        width=None,
        height=520,
        returned_objects=[]
    )

    st.markdown('<hr class="terra-divider">', unsafe_allow_html=True)

    st.subheader("Familias ambientales")

    filtro = st.selectbox(
        "Selecciona una familia para explorar:",
        [
            "Todas",
            "Desiertos hiperáridos",
            "Salares y evaporitas",
            "Terrenos volcánicos",
            "Alta montaña y ambientes periglaciares",
            "Ambientes glaciares"
        ]
    )

    st.write(
        "Familia seleccionada: **" + filtro + "**"
    )

    st.caption(
        "Los sitios específicos, sus coordenadas y atributos "
        "se mostrarán una vez incorporados los datos."
    )


# --------------------------------------------------
# SELECTOR PLANETARIO
# --------------------------------------------------

elif modulo == "Selector planetario":

    section_header(
        "02 / CUERPOS PLANETARIOS",
        "Selector planetario",
        "Selecciona un cuerpo celeste para explorar sus perfiles de referencia."
    )

    planeta = st.selectbox(
        "Cuerpo celeste",
        ["Marte", "Luna"]
    )

    if planeta == "Marte":
        st.markdown("### Marte")
        st.write("""
        Se investigarán ambientes áridos, volcánicos y criogénicos,
        según la disponibilidad de productos científicos comparables.
        """)
        st.markdown("**Instrumentos de referencia considerados**")
        st.write("MOLA · THEMIS · TES · HiRISE · CRISM")

    else:
        st.markdown("### Luna")
        st.write("""
        Se investigarán terrenos basálticos, cráteres, pendientes,
        bloques y rugosidad superficial.
        """)
        st.markdown("**Instrumentos de referencia considerados**")
        st.write("LOLA · Diviner · LROC")

    st.warning(
        "Los perfiles específicos y sus variables se encuentran "
        "pendientes de selección y procesamiento."
    )


# --------------------------------------------------
# MOTOR DE DESCUBRIMIENTO
# --------------------------------------------------

elif modulo == "Motor de descubrimiento":

    section_header(
        "03 / ANÁLISIS",
        "Motor de descubrimiento",
        "Exploración de combinaciones de variables para identificar "
        "posibles candidatos a análogos terrestres."
    )

    st.write("Dimensiones consideradas:")

    dimensiones = [
        "Geología y características superficiales",
        "Topografía y geomorfología",
        "Condiciones térmicas",
        "Agua y humedad",
        "Procesos superficiales"
    ]

    for dimension in dimensiones:
        st.markdown(f"- {dimension}")

    st.info(
        "El modelo multicriterio y las técnicas de aprendizaje automático "
        "se integrarán una vez que el equipo disponga de variables "
        "procesadas y perfiles planetarios compatibles."
    )


# --------------------------------------------------
# COMPARADOR
# --------------------------------------------------

elif modulo == "Comparador de ambientes":

    section_header(
        "04 / COMPARACIÓN",
        "Comparador de ambientes",
        "Una herramienta para analizar similitudes y diferencias "
        "entre ambientes terrestres y planetarios."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Ambiente terrestre")
        st.selectbox(
            "Selecciona un ambiente",
            [
                "Pendiente de integración",
                "Desierto hiperárido",
                "Salar",
                "Terreno volcánico",
                "Alta montaña",
                "Ambiente glaciar"
            ]
        )

    with col2:
        st.markdown("### Perfil planetario")
        st.selectbox(
            "Selecciona un perfil",
            ["Marte", "Luna"]
        )

    st.warning(
        "La comparación se habilitará cuando estén integrados "
        "los datos y las variables compatibles. No se muestran "
        "puntajes ficticios."
    )


# --------------------------------------------------
# FICHA DE ANALOGÍA
# --------------------------------------------------

elif modulo == "Ficha de analogía":

    section_header(
        "05 / RESULTADOS",
        "Ficha de analogía",
        "Un resumen explicable de cada candidato y su posible utilidad científica."
    )

    st.markdown("### Contenido de cada ficha")

    campos = [
        "Ubicación y descripción del ambiente",
        "Perfil planetario de referencia",
        "Variables y fuentes utilizadas",
        "Similitudes observadas",
        "Diferencias identificadas",
        "Cobertura y calidad de los datos",
        "Utilidad potencial para investigación",
        "Limitaciones y antecedentes científicos"
    ]

    for campo in campos:
        st.markdown(f"- {campo}")

    st.info(
        "Las fichas se generarán una vez que existan resultados "
        "validados para los sitios seleccionados."
    )


# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------

st.markdown('<hr class="terra-divider">', unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; justify-content:space-between;
            flex-wrap:wrap; gap:10px;">
    <div style="font-size:12px; color:#758087;">
        <strong style="color:#172B36;">TERRAMATCH CHILE</strong><br>
        NASA Space Apps Challenge
    </div>
    <div style="font-size:11px; color:#758087; text-align:right;">
        Explorando la Tierra para comprender otros mundos.
    </div>
</div>
""", unsafe_allow_html=True)
