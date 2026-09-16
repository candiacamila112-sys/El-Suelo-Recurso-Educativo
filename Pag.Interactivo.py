import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from pathlib import Path
from folium.plugins import Search
import json
import html
# =========================================================
# EL SUELO - RECURSO EDUCATIVO INTERACTIVO
# Primera versión
# =========================================================

st.set_page_config(
    page_title="El Suelo | Recurso Educativo",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)
BASE_DIR = Path(__file__).resolve().parent
IMAGENES_DIR = BASE_DIR / "imagenes"
CACHE_SUELOS = BASE_DIR / "suelos_argentina.geojson"

# =========================================================
# ESTILOS
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Patrick+Hand&display=swap');

    :root {
        --verde: #23966f;
        --verde-claro: #e7f6ed;
        --azul: #4ca7d8;
        --azul-claro: #e7f5fc;
        --amarillo: #f4c95d;
        --amarillo-claro: #fff7d9;
        --lila: #8f78d8;
        --lila-claro: #f1edff;
        --rosa: #e989ad;
        --rosa-claro: #fff0f5;
        --texto: #17324d;
        --gris: #617384;
        --borde: #dce8ee;
    }

    .stApp {
        background: linear-gradient(180deg, #36804d 0%, #944b4b 100%);
        color: var(--texto);
        font-family: 'Nunito', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f5f2ff 0%, #178733 100%);
        border-right: 1px solid #dce7ec;
    }

    [data-testid="stSidebar"] * {
        font-family: 'Nunito', sans-serif;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        color: var(--texto);
        font-weight: 900;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: clamp(2.2rem, 5vw, 4.2rem) !important;
        line-height: 0.95 !important;
    }

    h2 {
        font-size: clamp(1.6rem, 3vw, 2.5rem) !important;
    }

    .hand {
        font-family: 'Patrick Hand', cursive;
    }

    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---------- Tarjetas ---------- */

    .card {
        border-radius: 22px;
        padding: 22px 24px;
        margin: 8px 0 18px 0;
        border: 1px solid var(--borde);
        box-shadow: 0 8px 22px rgba(32, 67, 84, 0.06);
    }

    .card h3 {
        margin-top: 0;
        margin-bottom: 8px;
        font-size: 1.35rem;
    }

    .card p {
        color: #40576a;
        line-height: 1.55;
        margin-bottom: 0;
    }

    .green { background: var(--verde-claro); border-left: 7px solid #63bf91; }
    .blue { background: var(--azul-claro); border-left: 7px solid #73bee8; }
    .yellow { background: var(--amarillo-claro); border-left: 7px solid #f0c14d; }
    .purple { background: var(--lila-claro); border-left: 7px solid #a18ce4; }
    .pink { background: var(--rosa-claro); border-left: 7px solid #e989ad; }

    .mini-card {
        background: white;
        border: 1px solid var(--borde);
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        height: 100%;
        box-shadow: 0 5px 16px rgba(32, 67, 84, 0.05);
    }

    .mini-icon {
        font-size: 2.1rem;
        margin-bottom: 6px;
    }

    .mini-title {
        font-size: 1.05rem;
        font-weight: 900;
        color: var(--texto);
    }

    .mini-text {
        color: var(--gris);
        font-size: 0.92rem;
        line-height: 1.4;
        margin-top: 5px;
    }


    /* ---------- Imagen de portada ---------- */

    .hero-image-wrap {
        position: relative;
        overflow: hidden;
        border-radius: 30px;
        border: 1px solid #d5e4e7;
        box-shadow: 0 12px 30px rgba(45, 92, 111, 0.10);
        background: #ffffff;
    }

    .hero-image-caption {
        position: absolute;
        left: 28px;
        bottom: 24px;
        padding: 13px 18px;
        border-radius: 16px;
        background: rgba(255,255,255,.90);
        backdrop-filter: blur(7px);
        color: #17324d;
        font-weight: 800;
        box-shadow: 0 5px 18px rgba(25,55,70,.12);
    }

    /* ---------- Videos ---------- */
    .video-card {
        background: #ffffff;
        border: 1px solid #dce8ee;
        border-radius: 22px;
        padding: 16px;
        margin-bottom: 22px;
        box-shadow: 0 8px 22px rgba(32, 67, 84, 0.06);
    }
    .video-title {
        color: #17324d;
        font-size: 1.15rem;
        font-weight: 900;
        margin-bottom: 4px;
    }
    .video-description {
        color: #71828f;
        font-size: .92rem;
        margin-bottom: 13px;
    }
    .video-frame {
        position: relative;
        width: 100%;
        padding-top: 56.25%;
        overflow: hidden;
        border-radius: 16px;
        background: #eef4f6;
    }
    .video-frame iframe {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        border: 0;
    }

    /* ---------- Portada ---------- */

    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 30px;
        padding: 50px 55px;
        min-height: 430px;
        background:
            radial-gradient(circle at 80% 15%, rgba(255,255,255,.85) 0 65px, transparent 66px),
            radial-gradient(circle at 87% 27%, rgba(255,255,255,.65) 0 90px, transparent 91px),
            linear-gradient(135deg, #dff4ff 0%, #effaf4 58%, #fff8dc 100%);
        border: 1px solid #cfe5ec;
        box-shadow: 0 12px 30px rgba(45, 92, 111, 0.08);
    }

    .hero:after {
        content: "🌿";
        position: absolute;
        right: 7%;
        bottom: 9%;
        font-size: 10rem;
        transform: rotate(-7deg);
        opacity: .9;
    }

    .hero-kicker {
        color: #226d55;
        font-weight: 900;
        font-size: 1rem;
        letter-spacing: .5px;
        margin-bottom: 12px;
    }

    .hero-title {
        font-family: 'Patrick Hand', cursive;
        color: #153c59;
        font-size: clamp(4.5rem, 10vw, 8.5rem);
        font-weight: 700;
        line-height: .78;
        margin: 0;
        position: relative;
        z-index: 2;
    }

    .hero-subtitle {
        font-family: 'Patrick Hand', cursive;
        font-size: clamp(2rem, 4vw, 3.3rem);
        color: #214b66;
        margin: 18px 0;
        position: relative;
        z-index: 2;
    }

    .hero-text {
        max-width: 560px;
        color: #35586c;
        font-size: 1.05rem;
        line-height: 1.55;
        position: relative;
        z-index: 2;
    }


    /* ---------- Cabecera de sección ---------- */

    .section-header {
        padding: 25px 30px;
        border-radius: 24px;
        margin-bottom: 22px;
        border: 1px solid var(--borde);
        background: linear-gradient(135deg, #ffffff, #f6fbfc);
    }

    .section-number {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: #e9f4ef;
        color: #27785c;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .section-header h1,
    .section-header h2 {
        margin-top: 0;
        margin-bottom: 7px;
    }

    .section-header p {
        color: var(--gris);
        margin-bottom: 0;
        font-size: 1.03rem;
    }

    /* ---------- Barra de progreso ---------- */

    .progress-wrap {
        background: #eaf0f3;
        height: 11px;
        border-radius: 99px;
        overflow: hidden;
        margin: 10px 0 18px 0;
    }

    .progress-bar {
        height: 100%;
        border-radius: 99px;
        background: linear-gradient(90deg, #55b58d, #6bb8dc);
    }

    /* ---------- Cajas de datos ---------- */

    .fact {
        padding: 18px;
        border-radius: 18px;
        background: #ffffff;
        border: 1px dashed #cbdde4;
        margin: 8px 0;
    }

    .fact strong {
        color: var(--texto);
    }

    .big-number {
        font-size: 2.5rem;
        font-weight: 900;
        color: #267a5e;
        line-height: 1;
    }

    /* ---------- Pie ---------- */

    .footer-card {
        text-align: center;
        background: linear-gradient(135deg, #eef9f3, #f4f0ff);
        border: 1px solid #dfe9e9;
        border-radius: 24px;
        padding: 28px;
        margin-top: 30px;
    }

    /* Botones */
    .stButton > button {
        border-radius: 999px;
        font-weight: 900;
        border: 1px solid #cfe0e5;
        min-height: 44px;
    }

    @media (max-width: 800px) {
        .hero {
            padding: 35px 25px;
            min-height: 500px;
        }

        .hero:after {
            right: 2%;
            bottom: 4%;
            font-size: 7rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATOS
# ============================================================

INFO_SUELOS = {
    "Alfisoles": ("#8E44AD", "🟣", "Suelos relativamente fértiles, frecuentes en regiones con suficiente humedad."),
    "Andisoles": ("#E67E22", "🟠", "Suelos desarrollados a partir de materiales volcánicos."),
    "Aridisoles": ("#F1C40F", "🟡", "Suelos propios de regiones áridas y con poca disponibilidad de agua."),
    "Entisoles": ("#27AE60", "🟢", "Suelos jóvenes, con poco desarrollo."),
    "Gelisoles": ("#3498DB", "🔵", "Suelos asociados a ambientes muy fríos."),
    "Histosoles": ("#16A085", "🟢", "Suelos ricos en materia orgánica."),
    "Inceptisoles": ("#2ECC71", "🟢", "Suelos con desarrollo mayor que los Entisoles."),
    "Molisoles": ("#795548", "🟤", "Suelos oscuros, generalmente ricos en materia orgánica."),
    "Oxisoles": ("#E74C3C", "🔴", "Suelos muy evolucionados de ambientes cálidos y húmedos."),
    "Spodosoles": ("#9B59B6", "🟣", "Suelos con acumulación de materia orgánica y minerales."),
    "Ultisoles": ("#C0392B", "🔴", "Suelos muy evolucionados de regiones cálidas y húmedas."),
    "Vertisoles": ("#34495E", "⚫", "Suelos con arcillas expansivas que pueden formar grietas."),
    "Complejo indiferenciado": ("#95A5A6", "⚪", "Áreas donde no se diferencia un único tipo."),
    "Médanos": ("#F5B041", "🏜️", "Acumulaciones de arena asociadas a la acción del viento."),
    "Salinas": ("#D5DBDB", "🧂", "Ambientes con alta concentración de sales."),
    "Cuerpos de agua": ("#2980B9", "💧", "Ríos, lagos y lagunas."),
    "Misceláneas": ("#7F8C8D", "⬜", "Áreas con características particulares."),
}

URL_IGN = (
    "https://ide.ign.gob.ar/geoservicios/rest/services/"
    "ANIDA/fisiconat/MapServer/35/query"
)
CAMPO_SUELO = "NEW_OR_07"


# =========================================================
# DATOS EDUCATIVOS
# =========================================================



COMPONENTES = [
    {
        "nombre": "Minerales",
        "icono": "🪨",
        "porcentaje": "45%",
        "color": "yellow",
        "texto": "Aportan estructura al suelo y contienen muchos de los nutrientes que necesitan las plantas.",
    },
    {
        "nombre": "Agua",
        "icono": "💧",
        "porcentaje": "25%",
        "color": "blue",
        "texto": "Se encuentra en los poros del suelo y permite transportar sustancias y nutrientes.",
    },
    {
        "nombre": "Aire",
        "icono": "💨",
        "porcentaje": "25%",
        "color": "purple",
        "texto": "Ocupa parte de los poros y es fundamental para las raíces y los organismos del suelo.",
    },
    {
        "nombre": "Materia orgánica",
        "icono": "🍂",
        "porcentaje": "5%",
        "color": "green",
        "texto": "Proviene de restos de seres vivos en descomposición y contribuye a la fertilidad.",
    },
]

REGIONES = {
    "Región Pampeana": {
        "icono": "🌾",
        "suelo": "Suelos oscuros y generalmente muy fértiles",
        "descripcion": "Predominan suelos ricos en materia orgánica, importantes para la producción agrícola.",
        "color": "#66b58b",
    },
    "NOA": {
        "icono": "🏜️",
        "suelo": "Suelos condicionados por ambientes áridos y montañosos",
        "descripcion": "El clima, el relieve y la disponibilidad de agua influyen fuertemente en sus características.",
        "color": "#f0bd4f",
    },
    "NEA": {
        "icono": "🌳",
        "suelo": "Suelos asociados a ambientes cálidos y húmedos",
        "descripcion": "La temperatura y las precipitaciones favorecen procesos intensos de meteorización y descomposición.",
        "color": "#69b99a",
    },
    "Cuyo": {
        "icono": "🍇",
        "suelo": "Suelos de ambientes predominantemente áridos",
        "descripcion": "El agua disponible es un factor fundamental y la actividad agrícola suele requerir riego.",
        "color": "#d99a62",
    },
    "Patagonia": {
        "icono": "🏔️",
        "suelo": "Suelos diversos, condicionados por el clima y el relieve",
        "descripcion": "Los fuertes vientos, las bajas temperaturas y la aridez influyen en su desarrollo.",
        "color": "#899fca",
    },
}

GLOSARIO = {
    "Suelo": "Capa superficial de la Tierra donde interactúan minerales, materia orgánica, agua, aire y organismos vivos.",
    "Materia orgánica": "Material procedente de restos de plantas, animales y microorganismos que se encuentran en distintos estados de descomposición.",
    "Minerales": "Partículas provenientes principalmente de la alteración de las rocas y que forman gran parte de la estructura del suelo.",
    "Textura": "Proporción relativa de arena, limo y arcilla presente en un suelo.",
    "Erosión": "Proceso mediante el cual partículas del suelo son desprendidas y transportadas por agua, viento u otros agentes.",
    "Fertilidad": "Capacidad del suelo para aportar condiciones y nutrientes adecuados para el crecimiento de las plantas.",
    "Permeabilidad": "Facilidad con la que el agua puede atravesar los espacios del suelo.",
    "Horizonte": "Capa del suelo que presenta características particulares y forma parte del perfil del suelo.",
}

# =========================================================
# FUNCIONES
# =========================================================

def cabecera(numero, titulo, descripcion, emoji="🌱"):
    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-number">{emoji} {numero}</div>
            <h1>{titulo}</h1>
            <p>{descripcion}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
def buscar_imagen(nombre):
    """Busca la imagen en /imagenes, tolerando mayúsculas y extensiones comunes."""
    ruta = IMAGENES_DIR / nombre
    if ruta.is_file():
        return ruta

    # Búsqueda tolerante: nombre y extensión sin distinguir mayúsculas/minúsculas.
    objetivo = Path(nombre).stem.lower()
    if IMAGENES_DIR.exists():
        for archivo in IMAGENES_DIR.iterdir():
            if archivo.is_file() and archivo.stem.lower() == objetivo and archivo.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                return archivo
    return None

def imagen(nombre, caption=None):
    ruta = buscar_imagen(nombre)
    if ruta is not None:
        st.image(str(ruta), use_container_width=True)
        if caption:
            st.caption(caption)
    else:
        disponibles = []
        if IMAGENES_DIR.exists():
            disponibles = [p.name for p in IMAGENES_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
        st.error(f"No se encontró la imagen '{nombre}' en la carpeta imagenes.")
        if disponibles:
            st.info("Imágenes detectadas: " + ", ".join(disponibles))
        else:
            st.info(f"Creá la carpeta '{IMAGENES_DIR}' y colocá allí tus archivos PNG.")

def tarjeta(titulo, texto, icono="", color="green"):
    st.markdown(
        f"""
        <div class="card {color}">
            <h3>{icono} {titulo}</h3>
            <p>{texto}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
@st.cache_data(show_spinner=False)
def descargar_suelos():
    if CACHE_SUELOS.exists():
        try:
            return json.loads(CACHE_SUELOS.read_text(encoding="utf-8"))
        except Exception:
            pass

    features = []
    offset = 0
    cantidad = 1000

    while True:
        params = {
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "true",
            "f": "geojson",
            "resultOffset": offset,
            "resultRecordCount": cantidad,
        }

        respuesta = requests.get(URL_IGN, params=params, timeout=60)
        respuesta.raise_for_status()

        nuevos = respuesta.json().get("features", [])
        if not nuevos:
            break

        features.extend(nuevos)

        if len(nuevos) < cantidad:
            break

        offset += cantidad

    datos = {"type": "FeatureCollection", "features": features}

    if features:
        try:
            CACHE_SUELOS.write_text(
                json.dumps(datos, ensure_ascii=False),
                encoding="utf-8"
            )
        except Exception:
            pass

    return datos

def obtener_suelo(feature):
    valor = feature.get("properties", {}).get(CAMPO_SUELO, "")
    return str(valor).strip() if valor else "Sin clasificar"

def color_suelo(nombre):
    if nombre in INFO_SUELOS:
        return INFO_SUELOS[nombre][0]

    nombre_l = nombre.lower()

    for clave, info in INFO_SUELOS.items():
        if clave.lower() in nombre_l or nombre_l in clave.lower():
            return info[0]

    return "#BDC3C7"

def estilo_suelo(feature):
    return {
        "fillColor": color_suelo(obtener_suelo(feature)),
        "color": "#555555",
        "weight": 0.5,
        "fillOpacity": 0.72,
    }

def estilo_hover(feature):
    return {
        "fillOpacity": 0.95,
        "weight": 2,
        "color": "#17324D",
    }

def crear_mapa(datos):
    mapa = folium.Map(
        location=[-38.4, -63.6],
        zoom_start=4,
        tiles=None,
        control_scale=True,
    )

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="&copy; OpenStreetMap &copy; CARTO",
        name="Mapa claro",
    ).add_to(mapa)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satélite",
    ).add_to(mapa)

    # Los campos pueden variar según la versión del servicio del IGN.
    # Usamos solamente los que realmente existen para evitar que Folium falle.
    features = datos.get("features", [])
    campos_disponibles = set()
    if features:
        campos_disponibles = set(features[0].get("properties", {}).keys())

    campos = []
    aliases = []
    for campo, alias in [
        (CAMPO_SUELO, "Tipo de suelo:"),
        ("PROV", "Provincia:"),
        ("NEW_SUB_07", "Suborden:"),
        ("NEW_GGR_07", "Gran grupo:"),
    ]:
        if campo in campos_disponibles:
            campos.append(campo)
            aliases.append(alias)

    tooltip = None
    if campos:
        tooltip = folium.GeoJsonTooltip(
            fields=campos,
            aliases=aliases,
            sticky=False,
            labels=True,
            style=(
                "background-color:white;color:#222;"
                "font-family:Arial;font-size:13px;padding:10px;"
                "border-radius:8px;"
            ),
        )

    capa = folium.GeoJson(
        datos,
        name="🌱 Suelos",
        style_function=estilo_suelo,
        highlight_function=estilo_hover,
        tooltip=tooltip,
    )

    capa.add_to(mapa)

    try:
        Search(
            layer=capa,
            search_label=CAMPO_SUELO,
            placeholder="🔎 Buscar tipo de suelo...",
            collapsed=False,
            search_zoom=6,
        ).add_to(mapa)
    except Exception:
        pass

    items = ""

    for nombre, (color, emoji, _) in INFO_SUELOS.items():
        items += f"""
        <div style="margin-bottom:6px;display:flex;align-items:center;">
            <span style="
                width:14px;height:14px;background:{color};
                display:inline-block;margin-right:7px;
                border:1px solid #555;border-radius:3px;">
            </span>
            <span style="color:#17324D;">{emoji} {html.escape(nombre)}</span>
        </div>
        """

    leyenda = f"""
    <div style="
        position:fixed;top:75px;right:18px;z-index:9999;
        width:230px;max-height:420px;overflow-y:auto;
        background:rgba(255,255,255,.96);
        border-radius:14px;padding:14px;
        box-shadow:0 3px 12px rgba(0,0,0,.18);
        font-family:Arial;font-size:12px;">
        <div style="
            font-size:16px;font-weight:bold;
            margin-bottom:9px;color:#145A32;">
            🌱 Referencias
        </div>
        {items}
    </div>
    """

    mapa.get_root().html.add_child(folium.Element(leyenda))
    folium.LayerControl(collapsed=False).add_to(mapa)

    return mapa

def video(video_id, titulo, descripcion):
    st.markdown(
        f"""
        <div class="video-card">
            <h3 style="margin-top:0;color:#17324D;">🎬 {titulo}</h3>
            <p class="small-note">{descripcion}</p>
        """,
        unsafe_allow_html=True,
    )

    st.video(f"https://www.youtube.com/watch?v={video_id}")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ESTADO DE LA APLICACIÓN
# =========================================================

if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0

if "quiz_respondido" not in st.session_state:
    st.session_state.quiz_respondido = False

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding:8px 0 18px 0;">
            <div style="font-size:3rem;">🌱</div>
            <div style="font-size:1.35rem; font-weight:900; color:#24435b;">
                Planeta Suelo
            </div>
            <div style="font-size:.9rem; color:#71828f;">
                Recurso educativo interactivo
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    opcion = st.radio(
        "Navegación",
        [
            "🏠 Inicio",
            "📖 1. ¿Qué es el suelo?",
            "🧪 2. Componentes",
            "🗺️ 3. Tipos de suelos en Argentina",
            "🌱 4. Importancia del suelo",
            "🧠 5. Encuestas",
            "🔗 6. Recursos adicionales",
            "📚 7. Glosario",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            background:#ffffff;
            border:1px solid #dbe8ed;
            border-radius:18px;
            padding:15px;
            text-align:center;
        ">
            <div style="font-size:1.7rem;">💡</div>
            <b>Tip</b>
            <p style="font-size:.85rem;color:#6b7d89;margin:5px 0 0 0;">
            Explorá las distintas secciones y resolvé el desafío final.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.markdown("---")
st.sidebar.caption("Ambiente · Suelo · Educación ambiental")

# =========================================================
# 0. INICIO
# =========================================================

if opcion == "🏠 Inicio":
    imagen(
        "portada_suelo.png",
        "El suelo sostiene gran parte de la vida que conocemos."
    )
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">🌿 RECURSO EDUCATIVO INTERACTIVO</div>
            <div class="hero-title">El Suelo</div>
            <div class="hero-subtitle">un mundo bajo nuestros pies</div>
            <div class="hero-text">
                Explorá, descubrí y aprendé sobre el suelo, sus componentes,
                su diversidad, su importancia y la relación que mantiene
                con la vida y el ambiente.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🌱 ¿Qué vamos a descubrir?")

    c1, c2, c3 = st.columns(3)

    with c1:
        tarjeta(
            "Conocer",
            "Qué es el suelo, cómo se forma y cuáles son sus principales componentes.",
            "📖",
        )

    with c2:
        tarjeta(
            "Explorar",
            "La diversidad de suelos de Argentina mediante un mapa geográfico interactivo.",
            "🗺️",
        )

    with c3:
        tarjeta(
            "Reflexionar",
            "Por qué cuidar el suelo es también cuidar la vida y nuestro ambiente.",
            "🌎",
        )

    st.markdown("---")
    st.info("💡 Usá el menú de la izquierda para recorrer el recurso.")
# =========================================================
# 1. ¿QUÉ ES EL SUELO?
# =========================================================

elif opcion == "📖 1. ¿Qué es el suelo?":

    cabecera(
        "1",
        "¿Qué es el suelo?",
        "Una mirada sencilla al recurso que sostiene gran parte de la vida terrestre.",
        "📖",
    )

    c1, c2 = st.columns(2)

    with c1:
        tarjeta(
            "Una capa viva",
            "El suelo es la capa superficial de la Tierra en la que interactúan "
            "minerales, materia orgánica, agua, aire y una enorme diversidad de organismos.",
            "🌱",
            "green",
        )

        tarjeta(
            "¿Cómo se forma?",
            "Su formación depende de factores como la roca de origen, el clima, "
            "el relieve, los organismos y el paso del tiempo. Es un proceso lento.",
            "⏳",
            "yellow",
        )

    with c2:
        tarjeta(
            "No es solamente tierra",
            "Cuando hablamos de suelo no nos referimos únicamente a partículas minerales. "
            "También hay agua, aire, raíces, hongos, bacterias, pequeños animales y materia orgánica.",
            "🪱",
            "pink",
        )

        tarjeta(
            "Arena, limo y arcilla",
            "La textura del suelo depende, entre otras cosas, de la proporción de partículas "
            "de distinto tamaño. La arena es más gruesa; el limo es intermedio; la arcilla es muy fina.",
            "🪨",
            "blue",
        )

    st.markdown("### 🔎 Tres ideas para recordar")

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            '<div class="mini-card"><div class="mini-icon">🌍</div>'
            '<div class="mini-title">Es dinámico</div>'
            '<div class="mini-text">Cambia con el agua, el clima, los organismos y las actividades humanas.</div></div>',
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            '<div class="mini-card"><div class="mini-icon">🦠</div>'
            '<div class="mini-title">Tiene vida</div>'
            '<div class="mini-text">Contiene microorganismos y pequeños organismos que participan en muchos procesos.</div></div>',
            unsafe_allow_html=True,
        )

    with c:
        st.markdown(
            '<div class="mini-card"><div class="mini-icon">🌾</div>'
            '<div class="mini-title">Es fundamental</div>'
            '<div class="mini-text">Interviene en la producción de alimentos y en el funcionamiento de los ecosistemas.</div></div>',
            unsafe_allow_html=True,
        )

    st.info("💡 **Para pensar:** ¿Qué pasaría con una planta si el suelo no pudiera almacenar agua ni contener aire?")

# =========================================================
# 2. COMPONENTES
# =========================================================

elif opcion == "🧪 2. Componentes":

    cabecera(
        "2",
        "Componentes del suelo",
        "El suelo está formado por una combinación de materiales sólidos, agua y aire.",
        "🧪",
    )

    st.markdown("### 🧩 Una composición que puede variar")

    cols = st.columns(4)

    for col, componente in zip(cols, COMPONENTES):
        with col:
            st.markdown(
                f"""
                <div class="mini-card">
                    <div class="mini-icon">{componente['icono']}</div>
                    <div class="big-number">{componente['porcentaje']}</div>
                    <div class="mini-title">{componente['nombre']}</div>
                    <div class="mini-text">{componente['texto']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    col1, col2 = st.columns([1.05, 1])

    with col1:
        tarjeta(
            "¿La proporción siempre es exactamente igual?",
            "No. Los porcentajes son una representación educativa de un suelo mineral "
            "idealizado. En la naturaleza las proporciones cambian según el tipo de suelo, "
            "el clima, la vegetación, el uso del territorio y otras condiciones.",
            "🔬",
            "blue",
        )

    with col2:
        tarjeta(
            "Materia orgánica",
            "La materia orgánica puede mejorar la estructura del suelo, favorecer la retención "
            "de agua y aportar nutrientes a medida que se descompone.",
            "🍂",
            "green",
        )

    st.markdown("### 🧱 ¿Qué ocurre con la textura?")

    textura = st.select_slider(
        "Deslizá para explorar",
        options=["Arena", "Limo", "Arcilla"],
        value="Limo",
    )

    if textura == "Arena":
        tarjeta(
            "Arena",
            "Sus partículas son relativamente grandes. Los suelos arenosos suelen permitir "
            "un drenaje rápido del agua.",
            "🏖️",
            "yellow",
        )
    elif textura == "Limo":
        tarjeta(
            "Limo",
            "Sus partículas tienen un tamaño intermedio. Presenta características entre la arena y la arcilla.",
            "🌫️",
            "blue",
        )
    else:
        tarjeta(
            "Arcilla",
            "Sus partículas son muy pequeñas. Los suelos con mucha arcilla pueden retener bastante agua, "
            "aunque también pueden tener problemas de drenaje si la estructura es desfavorable.",
            "🧱",
            "pink",
        )


# ============================================================
# 4. TIPOS DE SUELO + MAPA
# ============================================================

elif opcion == "🗺️ 3. Tipos de suelos en Argentina":

    cabecera(
        "3",
        "Tipos de suelos en Argentina",
        "Explorá la distribución de distintos tipos de suelo mediante un mapa interactivo basado en datos del IGN.",
        "🗺️",
    )

    st.markdown(
        """
        <div class="map-note">
        🗺️ <b>Mapa interactivo:</b> pasá el cursor sobre las áreas,
        utilizá el buscador o cambiá entre mapa claro y vista satelital.
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        with st.spinner("Cargando información geográfica de los suelos..."):
            datos = descargar_suelos()

        if datos.get("features"):
            st.success(f"Mapa cargado correctamente: {len(datos['features']):,} zonas.")
            mapa = crear_mapa(datos)
            st_folium(mapa, width="100%", height=650, returned_objects=[])
            st.caption(
                "Fuente: Instituto Geográfico Nacional (IGN), servicio geográfico ANIDA."
            )
        else:
            st.warning("No se encontraron datos geográficos.")

    except Exception as error:
        st.error("No fue posible cargar el mapa en este momento.")
        st.caption(f"Detalle técnico: {error}")

# =========================================================
# 4. IMPORTANCIA
# =========================================================

elif opcion == "🌱 4. Importancia del suelo":

    cabecera(
        "4",
        "Importancia del suelo",
        "Cuidar el suelo es cuidar procesos esenciales para la vida y para las sociedades.",
        "🌱",
    )

    funciones = [
        ("🌾", "Permite el crecimiento", "Las plantas encuentran en el suelo soporte, agua y nutrientes."),
        ("🪱", "Es hábitat", "Muchos organismos viven en el suelo y participan en su funcionamiento."),
        ("💧", "Regula el agua", "El suelo puede almacenar, infiltrar y transportar agua."),
        ("🌎", "Participa en ciclos", "Interviene en ciclos de nutrientes y en procesos relacionados con el carbono."),
        ("♻️", "Recicla materia", "Los organismos descomponedores transforman restos orgánicos."),
        ("🍎", "Sostiene la producción", "Una gran parte de nuestros alimentos depende directa o indirectamente del suelo."),
    ]

    cols = st.columns(3)

    for i, (icono, titulo, texto) in enumerate(funciones):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="mini-card" style="margin-bottom:18px;">
                    <div class="mini-icon">{icono}</div>
                    <div class="mini-title">{titulo}</div>
                    <div class="mini-text">{texto}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    tarjeta(
        "🌍 El suelo es un recurso que debemos cuidar",
        "La erosión, la pérdida de materia orgánica, la contaminación, la compactación y otros procesos "
        "pueden afectar sus funciones. El manejo responsable busca mantener o recuperar su calidad.",
        "💚",
        "green",
    )

    st.markdown("### 🤔 ¿Qué acciones ayudan a cuidarlo?")

    acciones = [
        "Evitar dejar el suelo desnudo durante largos períodos cuando sea posible.",
        "Mantener cobertura vegetal para reducir el impacto de la lluvia y el viento.",
        "Utilizar prácticas que reduzcan la erosión.",
        "Evitar la contaminación por residuos y sustancias peligrosas.",
        "Favorecer la conservación de materia orgánica.",
    ]

    for accion in acciones:
        st.markdown(f"✅ {accion}")

# =========================================================
# 5. ACTIVIDADES
# =========================================================

elif opcion == "🧠 5. Encuestas":

    cabecera(
        "5",
        "Encuestas",
        "Poné a prueba lo que aprendiste. Leé con atención y elegí la respuesta correcta.",
        "🧠",
    )

    preguntas = [
        {
            "pregunta": "¿Cuál de estos elementos NO forma parte del suelo?",
            "opciones": ["Minerales", "Agua", "Aire", "Luz solar"],
            "correcta": "Luz solar",
            "explicacion": "La luz solar es fundamental para los ecosistemas, pero no es un componente material del suelo.",
        },
        {
            "pregunta": "¿Cuál de estas partículas es la más fina?",
            "opciones": ["Arena", "Limo", "Arcilla", "Grava"],
            "correcta": "Arcilla",
            "explicacion": "La arcilla está formada por partículas muy pequeñas y puede retener bastante agua.",
        },
        {
            "pregunta": "¿Qué región argentina se caracteriza por una importante actividad agrícola sobre suelos fértiles?",
            "opciones": ["Región Pampeana", "Patagonia", "Cuyo", "NOA"],
            "correcta": "Región Pampeana",
            "explicacion": "La Región Pampeana posee condiciones ambientales y suelos que favorecen una intensa actividad agropecuaria.",
        },
        {
            "pregunta": "¿Cuál es una función del suelo?",
            "opciones": ["Ser hábitat de organismos", "Producir luz", "Crear el viento", "Eliminar toda el agua"],
            "correcta": "Ser hábitat de organismos",
            "explicacion": "El suelo constituye un hábitat para una gran diversidad de organismos.",
        },
        {
            "pregunta": "¿Cuál de estas acciones puede ayudar a reducir la erosión?",
            "opciones": ["Mantener cobertura vegetal", "Dejar el suelo desnudo", "Eliminar toda la vegetación", "Aumentar el pisoteo"],
            "correcta": "Mantener cobertura vegetal",
            "explicacion": "La cobertura vegetal protege la superficie del suelo frente al impacto de la lluvia y el viento.",
        },
    ]

    respuestas = []

    for i, pregunta in enumerate(preguntas):
        st.markdown(
            f"""
            <div class="card purple">
                <h3>Pregunta {i + 1}</h3>
                <p><b>{pregunta['pregunta']}</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        respuesta = st.radio(
            "Elegí una opción:",
            pregunta["opciones"],
            key=f"pregunta_{i}",
            label_visibility="collapsed",
        )
        respuestas.append(respuesta)

    if st.button("📝 Corregir actividad", use_container_width=True):

        puntaje = sum(
            respuestas[i] == preguntas[i]["correcta"]
            for i in range(len(preguntas))
        )

        st.session_state.puntaje = puntaje
        st.session_state.quiz_respondido = True

    if st.session_state.quiz_respondido:

        puntaje = st.session_state.puntaje
        total = len(preguntas)
        porcentaje = int((puntaje / total) * 100)

        st.markdown("---")
        st.markdown("## 🏆 Resultado")

        st.progress(porcentaje / 100)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Puntaje", f"{puntaje}/{total}")

        with c2:
            st.metric("Porcentaje", f"{porcentaje}%")

        with c3:
            if porcentaje == 100:
                mensaje = "¡Excelente! 🌟"
            elif porcentaje >= 60:
                mensaje = "¡Muy bien! 🌱"
            else:
                mensaje = "¡A seguir explorando! 🔎"
            st.metric("Resultado", mensaje)

        if porcentaje == 100:
            st.balloons()
            st.success("¡Excelente! Completaste correctamente toda la actividad.")
        elif porcentaje >= 60:
            st.success("¡Muy buen trabajo! Revisá las preguntas que te costaron.")
        else:
            st.info("No pasa nada. Volvé a las secciones anteriores y probá nuevamente.")

        with st.expander("🔎 Ver explicaciones"):
            for i, pregunta in enumerate(preguntas):
                correcta = respuestas[i] == pregunta["correcta"]
                simbolo = "✅" if correcta else "❌"

                st.markdown(
                    f"**{simbolo} {i + 1}. {pregunta['pregunta']}**"
                )

                st.write(
                    f"Respuesta correcta: **{pregunta['correcta']}**"
                )
                st.caption(pregunta["explicacion"])

# ============================================================
# 7. RECURSOS
# ============================================================

elif opcion == "🔗 6. Recursos adicionales":

    st.header("6. 🔗 Recursos adicionales")

    st.markdown("### 🖼️ Infografías para analizar")

    c1, c2 = st.columns(2)

    with c1:
        imagen(
            "educacion_ambiental.png",
            "Educación ambiental: naturaleza, sociedad y cultura."
        )

    with c2:
        imagen(
            "que_es_el_ambiente.png",
            "Ambiente y vínculo sociedad-naturaleza."
        )

    st.markdown(
        """
        <div class="caja violeta">
            <h3>💬 Para pensar</h3>
            <p>
            ¿Cómo se relacionan las ideas de estas infografías con el suelo?
            ¿Por qué podemos decir que el suelo no es solamente un recurso
            natural, sino también parte de las relaciones entre sociedad
            y ambiente?
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎬 Videos")

    video(
        "VS0vakZiWnU",
        "Video 1",
        "Recurso audiovisual para introducir o reforzar el tema."
    )

    video(
        "LRv3k2tT_cc",
        "Video 2",
        "Material complementario para continuar explorando."
    )

    video(
        "4Q4u-jP53VU",
        "Video 3",
        "Recurso audiovisual para ampliar y relacionar conceptos."
    )


# =========================================================
# 7. GLOSARIO
# =========================================================

elif opcion == "📚 7. Glosario":

    cabecera(
        "7",
        "Glosario",
        "Buscá y explorá conceptos importantes relacionados con el suelo.",
        "📚",
    )

    busqueda = st.text_input(
        "🔎 Buscar término",
        placeholder="Por ejemplo: erosión, arcilla, materia orgánica...",
    )

    termino_busqueda = busqueda.lower().strip()

    encontrados = {
        termino: definicion
        for termino, definicion in GLOSARIO.items()
        if not termino_busqueda
        or termino_busqueda in termino.lower()
        or termino_busqueda in definicion.lower()
    }

    if encontrados:
        for termino, definicion in encontrados.items():
            with st.expander(f"📖 {termino}"):
                st.write(definicion)
    else:
        st.warning("No encontramos ese término. Probá con otra palabra.")

    st.markdown("---")

    tarjeta(
        "🌱 Para recordar",
        "Aprender vocabulario científico ayuda a comprender mejor los procesos ambientales "
        "y a explicar nuestras observaciones con mayor precisión.",
        "💡",
        "green",
    )

# =========================================================
# PIE DE APLICACIÓN
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#78909c;
        padding:30px 10px 5px 10px;
        font-size:.85rem;
    ">
        🌱 El Suelo · Recurso Educativo Interactivo<br>
        <span style="opacity:.75;">Primera versión · Ambiente</span>
    </div>
    """,
    unsafe_allow_html=True,
)

