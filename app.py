import streamlit as st
import tensorflow as tf
import pandas as pd
import numpy as np
import json
import os
import html
import hashlib

from PIL import Image, UnidentifiedImageError
from io import BytesIO


# ============================================================
# CONFIGURACION GENERAL
# ============================================================

st.set_page_config(
    page_title="PlantIA",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
<style>

:root {
    --verde-profundo: #123D2E;
    --verde: #1F6B4F;
    --verde-medio: #2D7A5C;
    --verde-claro: #E8F2EC;
    --crema: #F5F4EF;
    --blanco: #FFFFFF;
    --texto: #1D2939;
    --gris: #667085;
    --borde: #DDE4DF;
    --dorado: #C3A25D;
}


/* =========================================================
   PAGINA
========================================================= */

html,
body,
[data-testid="stAppViewContainer"],
.stApp {
    background-color: var(--crema) !important;
    color: var(--texto) !important;
}

[data-testid="stHeader"] {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    max-width: 1320px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* =========================================================
   TEXTOS
========================================================= */

.stMarkdown,
.stMarkdown p,
.stMarkdown span,
label,
[data-testid="stWidgetLabel"],
[data-testid="stCaptionContainer"] {
    color: var(--texto) !important;
}

h1,
h2,
h3 {
    color: var(--texto) !important;
}


/* =========================================================
   MARCA
========================================================= */

.brand {
    color: var(--verde-profundo) !important;
    font-size: 1.78rem;
    font-weight: 850;
    line-height: 1;
    margin-top: 0.3rem;
}

.brand-subtitle {
    color: var(--gris) !important;
    font-size: 0.82rem;
    margin-top: 0.42rem;
}


/* =========================================================
   TITULOS
========================================================= */

.page-label {
    color: var(--verde) !important;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 1.15rem;
    margin-bottom: 0.4rem;
}

.page-title {
    color: var(--texto) !important;
    font-size: 2.5rem;
    font-weight: 850;
    line-height: 1.08;
    margin-bottom: 0.6rem;
}

.page-subtitle {
    color: var(--gris) !important;
    max-width: 850px;
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1.25rem;
}

.accent-line {
    width: 60px;
    height: 4px;
    border-radius: 20px;

    background:
        linear-gradient(
            90deg,
            var(--verde),
            var(--dorado)
        );

    margin-bottom: 1.25rem;
}


/* =========================================================
   BOTONES
========================================================= */

.stButton > button {
    min-height: 46px;
    border-radius: 11px;
    font-weight: 700;
    transition: all 0.15s ease;
}

.stButton > button[kind="primary"] {
    background: var(--verde) !important;
    border-color: var(--verde) !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    background: var(--verde-profundo) !important;
    border-color: var(--verde-profundo) !important;
}

.stButton > button[kind="secondary"] {
    background: white !important;
    border: 1px solid var(--borde) !important;
    color: var(--texto) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: var(--verde-claro) !important;
    color: var(--verde-profundo) !important;
}


/* =========================================================
   PANEL INSTRUCCIONES
========================================================= */

.upload-intro {
    background:
        linear-gradient(
            135deg,
            #123D2E,
            #1F6B4F
        );

    border-radius: 20px;
    padding: 2rem;
    min-height: 255px;

    box-shadow:
        0 14px 35px
        rgba(18, 61, 46, 0.10);
}

.upload-small {
    color: rgba(255,255,255,0.72) !important;
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.10em;
}

.upload-title {
    color: white !important;
    font-size: 1.72rem;
    font-weight: 800;
    line-height: 1.15;
    margin-top: 0.8rem;
    margin-bottom: 0.8rem;
}

.upload-text {
    color: rgba(255,255,255,0.86) !important;
    font-size: 0.93rem;
    line-height: 1.62;
}


/* =========================================================
   PANEL DE ENTRADA
========================================================= */

.input-panel {
    background: #FFFFFF;
    border: 1px solid var(--borde);
    border-radius: 20px;
    padding: 1.25rem;

    box-shadow:
        0 10px 30px
        rgba(32,50,42,0.04);
}

.input-title {
    color: var(--texto) !important;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}

.input-subtitle {
    color: var(--gris) !important;
    font-size: 0.84rem;
    line-height: 1.45;
    margin-bottom: 0.7rem;
}


/* =========================================================
   RADIO SUBIR / CAMARA
========================================================= */

div[role="radiogroup"] {
    background: #F2F5F2;
    padding: 5px;
    border-radius: 12px;
    gap: 5px;
}

div[role="radiogroup"] label {
    background: white;
    border: 1px solid var(--borde);
    border-radius: 9px;
    padding: 0.45rem 0.8rem;
}


/* =========================================================
   FILE UPLOADER
========================================================= */

[data-testid="stFileUploader"] {
    background: white !important;
    border: 1px solid var(--borde);
    border-radius: 16px;
    padding: 0.8rem;
}

[data-testid="stFileUploaderDropzone"] {
    background: #FAFCFA !important;
    border: 1.5px dashed #9CB5A8 !important;
    border-radius: 13px !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: var(--texto) !important;
}


/* =========================================================
   CAMARA
========================================================= */

[data-testid="stCameraInput"] {
    background: #FFFFFF;
    border: 1px solid var(--borde);
    border-radius: 16px;
    padding: 0.7rem;
}


/* =========================================================
   RESULTADO
========================================================= */

.result-box {
    background: var(--blanco);
    border: 1px solid var(--borde);
    border-radius: 18px;
    padding: 1.45rem;
    min-height: 250px;

    box-shadow:
        0 9px 26px
        rgba(32,50,42,0.05);
}

.result-label {
    color: var(--gris) !important;
    font-size: 0.70rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.result-name {
    color: var(--texto) !important;
    font-size: 1.55rem;
    font-weight: 850;
    line-height: 1.2;
    margin-top: 0.4rem;
}

.result-confidence {
    color: var(--verde) !important;
    font-size: 2.15rem;
    font-weight: 850;
    margin-top: 0.25rem;
}


/* =========================================================
   ENCABEZADO INFORMACION
========================================================= */

.compact-main {
    background:
        linear-gradient(
            135deg,
            #123D2E,
            #1F6B4F
        );

    border-radius: 17px;

    padding: 1.3rem 1.5rem;

    margin-top: 1rem;
    margin-bottom: 1rem;
}

.compact-main-title {
    color: white !important;
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 0.35rem;
}

.compact-main-text {
    color: rgba(255,255,255,0.86) !important;
    font-size: 0.87rem;
    line-height: 1.48;
}


/* =========================================================
   TARJETAS PEQUEÑAS
========================================================= */

.mini-card {
    background: #FFFFFF;
    border: 1px solid var(--borde);
    border-radius: 14px;
    padding: 1rem;
    min-height: 104px;
}

.mini-label {
    color: var(--gris) !important;
    font-size: 0.67rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.mini-value {
    color: var(--texto) !important;
    font-size: 0.92rem;
    font-weight: 750;
    line-height: 1.3;
    margin-top: 0.4rem;
}


/* =========================================================
   CUADROS DE INFORMACION
========================================================= */

.compact-card {
    background: #FFFFFF;
    border: 1px solid var(--borde);
    border-radius: 16px;

    padding: 1.15rem;

    min-height: 292px;

    box-shadow:
        0 6px 20px
        rgba(28,45,37,0.035);

    margin-bottom: 0.4rem;
}

.compact-category {
    color: var(--verde) !important;
    font-size: 0.70rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: 0.09em;

    padding-bottom: 0.65rem;
    margin-bottom: 0.75rem;

    border-bottom: 1px solid #E8ECE9;
}

.compact-item {
    margin-bottom: 0.78rem;
}

.compact-title {
    color: var(--texto) !important;
    font-size: 0.83rem;
    font-weight: 800;
    margin-bottom: 0.16rem;
}

.compact-text {
    color: #596675 !important;
    font-size: 0.79rem;
    line-height: 1.38;
}


/* =========================================================
   SELECT
========================================================= */

[data-baseweb="select"] > div {
    background: white !important;
    color: var(--texto) !important;
    border-color: var(--borde) !important;
}

[role="option"] {
    background: white !important;
    color: var(--texto) !important;
}

[role="option"]:hover {
    background: var(--verde-claro) !important;
}


/* =========================================================
   IMAGENES
========================================================= */

[data-testid="stImage"] img {
    border-radius: 17px;
}


/* =========================================================
   ALERTAS
========================================================= */

[data-testid="stAlert"] {
    border-radius: 13px;
}


/* =========================================================
   GUIA USO
========================================================= */

.step-number {
    width: 38px;
    height: 38px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background: var(--verde);
    color: white !important;

    font-weight: 850;
    margin-bottom: 0.75rem;
}

.help-card {
    background: white;
    border: 1px solid var(--borde);
    border-radius: 16px;
    padding: 1.25rem;
    min-height: 205px;
}

.help-title {
    color: var(--texto) !important;
    font-weight: 800;
    font-size: 1rem;
    margin-bottom: 0.4rem;
}

.help-text {
    color: var(--gris) !important;
    line-height: 1.5;
    font-size: 0.88rem;
}


/* =========================================================
   CELULAR
========================================================= */

@media (max-width: 800px) {

    .page-title {
        font-size: 2rem;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .compact-card {
        min-height: auto;
    }

    .result-box {
        min-height: auto;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# ARCHIVOS
# ============================================================

MODELO_PATH = "modelo_plantas_14_final.keras"
CLASES_PATH = "clases_plantas.json"
EXCEL_PATH = "informacion_14_plantas_puno.xlsx"

CARPETA_IMAGENES = "imagenes_referencia"


# ============================================================
# MODELO
# ============================================================

@tf.keras.utils.register_keras_serializable(
    package="PlantIA",
    name="preprocess_input"
)
def preprocess_input(x):

    return tf.keras.applications.mobilenet_v2.preprocess_input(x)


@st.cache_resource
def cargar_modelo():

    return tf.keras.models.load_model(
        MODELO_PATH,
        compile=False,
        safe_mode=False,
        custom_objects={
            "preprocess_input": preprocess_input
        }
    )


# ============================================================
# CLASES
# ============================================================

@st.cache_data
def cargar_clases():

    with open(
        CLASES_PATH,
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)


# ============================================================
# EXCEL
# ============================================================

@st.cache_data
def cargar_excel():

    datos = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Cuidados_14_plantas",
        header=3
    )

    datos.columns = (
        datos.columns
        .astype(str)
        .str.strip()
    )

    return datos


# ============================================================
# OBTENER CAMPO
# ============================================================

def obtener(
    info,
    campo,
    defecto="Información no disponible."
):

    if campo not in info.index:
        return defecto

    valor = info[campo]

    if pd.isna(valor):
        return defecto

    texto = str(valor).strip()

    if texto == "" or texto.lower() == "nan":
        return defecto

    return texto


# ============================================================
# NOMBRES COMUNES
# ============================================================

NOMBRES_COMUNES = {

    "Aloe Vera":
        "Sábila",

    "Chrysanthemum":
        "Crisantemo",

    "Daffodils (Narcissus spp.)":
        "Narciso",

    "Dracaena":
        "Drácena o palo de agua",

    "English Ivy (Hedera helix)":
        "Hiedra inglesa",

    "Jade plant (Crassula ovata)":
        "Árbol de jade",

    "Kalanchoe":
        "Kalanchoe o calanchoe",

    "Monstera Deliciosa (Monstera deliciosa)":
        "Costilla de Adán",

    "Orchid":
        "Orquídea",

    "Peace lily":
        "Cuna de Moisés o lirio de la paz",

    "Poinsettia (Euphorbia pulcherrima)":
        "Flor de Navidad o nochebuena",

    "Rubber Plant (Ficus elastica)":
        "Caucho o gomero",

    "Schefflera":
        "Cheflera o árbol paraguas",

    "Tulip":
        "Tulipán"
}


# ============================================================
# IMAGENES DE REFERENCIA
# ============================================================

NOMBRES_IMAGEN = {

    "Aloe Vera":
        "aloe_vera",

    "Chrysanthemum":
        "chrysanthemum",

    "Daffodils (Narcissus spp.)":
        "daffodils",

    "Dracaena":
        "dracaena",

    "English Ivy (Hedera helix)":
        "english_ivy",

    "Jade plant (Crassula ovata)":
        "jade_plant",

    "Kalanchoe":
        "kalanchoe",

    "Monstera Deliciosa (Monstera deliciosa)":
        "monstera",

    "Orchid":
        "orchid",

    "Peace lily":
        "peace_lily",

    "Poinsettia (Euphorbia pulcherrima)":
        "poinsettia",

    "Rubber Plant (Ficus elastica)":
        "rubber_plant",

    "Schefflera":
        "schefflera",

    "Tulip":
        "tulip"
}


# ============================================================
# NOMBRE PARA MOSTRAR
# ============================================================

def nombre_para_mostrar(clase_ia):

    clase_ia = str(
        clase_ia
    ).strip()

    comun = NOMBRES_COMUNES.get(
        clase_ia,
        clase_ia
    )

    base = clase_ia.split(
        " ("
    )[0].strip()

    if base.lower() == comun.lower():

        return base

    return f"{base} ({comun})"


# ============================================================
# BUSCAR IMAGEN REFERENCIAL
# ============================================================

def buscar_imagen_referencia(clase_ia):

    nombre = NOMBRES_IMAGEN.get(
        str(clase_ia).strip()
    )

    if not nombre:

        return None

    for extension in [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]:

        ruta = os.path.join(
            CARPETA_IMAGENES,
            nombre + extension
        )

        if os.path.exists(ruta):

            return ruta

    return None


# ============================================================
# HTML SEGURO
# ============================================================

def seguro(texto):

    return html.escape(
        str(texto)
    )


# ============================================================
# TARJETAS
# ============================================================

def mini_tarjeta(
    titulo,
    contenido
):

    st.markdown(
        f"""
<div class="mini-card">

<div class="mini-label">
{seguro(titulo)}
</div>

<div class="mini-value">
{seguro(contenido)}
</div>

</div>
""",
        unsafe_allow_html=True
    )


def bloque_compacto(
    titulo,
    elementos
):

    elementos_html = ""

    for subtitulo, texto in elementos:

        elementos_html += f"""
<div class="compact-item">

<div class="compact-title">
{seguro(subtitulo)}
</div>

<div class="compact-text">
{seguro(texto)}
</div>

</div>
"""

    st.markdown(
        f"""
<div class="compact-card">

<div class="compact-category">
{seguro(titulo)}
</div>

{elementos_html}

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# VALIDACION DE IMAGEN SUBIDA
# ============================================================

def validar_imagen_subida(archivo):

    extensiones_permitidas = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    formatos_permitidos = {
        "JPEG",
        "PNG",
        "WEBP"
    }

    nombre = str(
        archivo.name
    ).lower()

    extension = os.path.splitext(
        nombre
    )[1]


    if extension not in extensiones_permitidas:

        return (
            False,
            None,
            "Archivo rechazado. Solo se permiten "
            "JPG, JPEG, PNG o WEBP."
        )


    if archivo.size > 8 * 1024 * 1024:

        return (
            False,
            None,
            "La fotografía supera el límite de 8 MB."
        )


    try:

        contenido = archivo.getvalue()


        es_jpeg = contenido.startswith(
            b"\xff\xd8\xff"
        )


        es_png = contenido.startswith(
            b"\x89PNG\r\n\x1a\n"
        )


        es_webp = (
            len(contenido) >= 12
            and contenido[0:4] == b"RIFF"
            and contenido[8:12] == b"WEBP"
        )


        if not (
            es_jpeg
            or es_png
            or es_webp
        ):

            return (
                False,
                None,
                "Archivo rechazado. El contenido no "
                "corresponde a una fotografía válida."
            )


        prueba = Image.open(
            BytesIO(contenido)
        )


        formato = prueba.format


        prueba.verify()


        if formato not in formatos_permitidos:

            return (
                False,
                None,
                "Formato de imagen no admitido."
            )


        imagen = Image.open(
            BytesIO(contenido)
        ).convert(
            "RGB"
        )


        return (
            True,
            imagen,
            None
        )


    except UnidentifiedImageError:

        return (
            False,
            None,
            "El archivo no contiene una imagen válida."
        )


    except Exception:

        return (
            False,
            None,
            "No fue posible validar la fotografía."
        )


# ============================================================
# PROCESAR FOTO DE CAMARA
# ============================================================

def procesar_foto_camara(foto):

    try:

        contenido = foto.getvalue()


        if len(contenido) == 0:

            return (
                False,
                None,
                "No se recibió ninguna fotografía."
            )


        imagen = Image.open(
            BytesIO(contenido)
        ).convert(
            "RGB"
        )


        return (
            True,
            imagen,
            None
        )


    except Exception:

        return (
            False,
            None,
            "No fue posible procesar la fotografía "
            "capturada por la cámara."
        )


# ============================================================
# VERIFICAR ARCHIVOS
# ============================================================

faltantes = []

for ruta in [
    MODELO_PATH,
    CLASES_PATH,
    EXCEL_PATH
]:

    if not os.path.exists(ruta):

        faltantes.append(ruta)


if faltantes:

    st.error(
        "Faltan archivos necesarios para iniciar PlantIA."
    )

    for archivo in faltantes:

        st.write(archivo)

    st.stop()


# ============================================================
# CARGAR SISTEMA
# ============================================================

try:

    modelo = cargar_modelo()

    clases = cargar_clases()

    datos = cargar_excel()


except Exception as error:

    st.error(
        "No fue posible iniciar PlantIA."
    )

    st.code(
        str(error)
    )

    st.stop()


# ============================================================
# ESTADO
# ============================================================

if "pagina" not in st.session_state:

    st.session_state.pagina = "Inicio"


if "resultado_ia" not in st.session_state:

    st.session_state.resultado_ia = None


if "entrada_version" not in st.session_state:

    st.session_state.entrada_version = 0


if "upload_error" not in st.session_state:

    st.session_state.upload_error = None


# ============================================================
# CAMBIAR PAGINA
# ============================================================

def cambiar_pagina(pagina):

    st.session_state.pagina = pagina

    st.rerun()


# ============================================================
# CABECERA
# ============================================================

marca, nav1, nav2, nav3 = st.columns(
    [
        2.5,
        1,
        1.3,
        1.15
    ]
)


with marca:

    st.markdown(
        """
<div class="brand">
PlantIA
</div>

<div class="brand-subtitle">
Asistente inteligente para el cuidado vegetal
</div>
""",
        unsafe_allow_html=True
    )


with nav1:

    if st.button(
        "Inicio",
        width="stretch",
        type=(
            "primary"
            if st.session_state.pagina == "Inicio"
            else "secondary"
        )
    ):

        cambiar_pagina(
            "Inicio"
        )


with nav2:

    if st.button(
        "Guía de plantas",
        width="stretch",
        type=(
            "primary"
            if st.session_state.pagina == "Guia"
            else "secondary"
        )
    ):

        cambiar_pagina(
            "Guia"
        )


with nav3:

    if st.button(
        "Guía de uso",
        width="stretch",
        type=(
            "primary"
            if st.session_state.pagina == "Uso"
            else "secondary"
        )
    ):

        cambiar_pagina(
            "Uso"
        )


# ============================================================
# DASHBOARD DE INFORMACION
# ============================================================

def mostrar_ficha_completa(info):

    st.write("")


    st.markdown(
        f"""
<div class="compact-main">

<div class="compact-main-title">
Información y cuidados
</div>

<div class="compact-main-text">
{seguro(obtener(info, "Descripción corta"))}
</div>

</div>
""",
        unsafe_allow_html=True
    )


    d1, d2, d3, d4 = st.columns(
        4
    )


    with d1:

        mini_tarjeta(
            "Familia",
            obtener(
                info,
                "Familia"
            )
        )


    with d2:

        mini_tarjeta(
            "Dificultad",
            obtener(
                info,
                "Dificultad de cuidado"
            )
        )


    with d3:

        mini_tarjeta(
            "Riego",
            obtener(
                info,
                "Frecuencia de riego (orientativa)"
            )
        )


    with d4:

        mini_tarjeta(
            "Temperatura",
            obtener(
                info,
                "Temperatura recomendada"
            )
        )


    st.write("")


    c1, c2, c3 = st.columns(
        3,
        gap="medium"
    )


    with c1:

        bloque_compacto(
            "Cuidados esenciales",
            [
                (
                    "Forma de riego",
                    obtener(
                        info,
                        "Cómo regar / cantidad"
                    )
                ),
                (
                    "Iluminación",
                    obtener(
                        info,
                        "Luz"
                    )
                ),
                (
                    "Humedad",
                    obtener(
                        info,
                        "Humedad"
                    )
                ),
                (
                    "Tipo de cultivo",
                    obtener(
                        info,
                        "Tipo de cultivo recomendado"
                    )
                )
            ]
        )


    with c2:

        bloque_compacto(
            "Cultivo y mantenimiento",
            [
                (
                    "Sustrato",
                    obtener(
                        info,
                        "Sustrato"
                    )
                ),
                (
                    "Fertilización",
                    obtener(
                        info,
                        "Fertilización"
                    )
                ),
                (
                    "Poda",
                    obtener(
                        info,
                        "Poda"
                    )
                ),
                (
                    "Trasplante",
                    obtener(
                        info,
                        "Trasplante / cambio de maceta"
                    )
                )
            ]
        )


    with c3:

        bloque_compacto(
            "Propagación",
            [
                (
                    "Método",
                    obtener(
                        info,
                        "Método de propagación"
                    )
                ),
                (
                    "Cómo plantar",
                    obtener(
                        info,
                        "Cómo propagar / sembrar"
                    )
                ),
                (
                    "Momento recomendado",
                    obtener(
                        info,
                        "Momento recomendado"
                    )
                ),
                (
                    "Profundidad",
                    obtener(
                        info,
                        "Profundidad / colocación"
                    )
                )
            ]
        )


    st.write("")


    p1, p2, p3 = st.columns(
        3,
        gap="medium"
    )


    with p1:

        bloque_compacto(
            "Riego y señales",
            [
                (
                    "Falta de agua",
                    obtener(
                        info,
                        "Señales de falta de agua"
                    )
                ),
                (
                    "Exceso de agua",
                    obtener(
                        info,
                        "Señales de exceso de agua"
                    )
                )
            ]
        )


    with p2:

        bloque_compacto(
            "Problemas frecuentes",
            [
                (
                    "Plagas o problemas",
                    obtener(
                        info,
                        "Plagas / problemas frecuentes"
                    )
                ),
                (
                    "Acción correctiva",
                    obtener(
                        info,
                        "Acción correctiva inicial"
                    )
                )
            ]
        )


    with p3:

        bloque_compacto(
            "Seguridad y Puno",
            [
                (
                    "Recomendación para Puno",
                    obtener(
                        info,
                        "Recomendación para Puno"
                    )
                ),
                (
                    "Precauciones",
                    obtener(
                        info,
                        "Precauciones"
                    )
                )
            ]
        )


# ============================================================
# FUNCION DE ANALISIS
# ============================================================

def analizar_imagen(imagen):

    imagen_ia = imagen.resize(
        (
            224,
            224
        )
    )


    arreglo = np.array(
        imagen_ia,
        dtype=np.float32
    )


    arreglo = np.expand_dims(
        arreglo,
        axis=0
    )


    predicciones = modelo.predict(
        arreglo,
        verbose=0
    )[0]


    indice = int(
        np.argmax(
            predicciones
        )
    )


    planta = clases[
        indice
    ]


    confianza = float(
        predicciones[
            indice
        ] * 100
    )


    return (
        planta,
        confianza,
        predicciones
    )


# ============================================================
# PAGINA INICIO
# ============================================================

if st.session_state.pagina == "Inicio":

    st.markdown(
        """
<div class="page-label">
Reconocimiento vegetal
</div>

<div class="page-title">
Identifica una planta mediante una fotografía
</div>

<div class="accent-line"></div>

<div class="page-subtitle">
Puedes subir una fotografía que ya tengas guardada o utilizar
directamente la cámara del dispositivo para tomar una nueva imagen.
</div>
""",
        unsafe_allow_html=True
    )


    info_col, entrada_col = st.columns(
        [
            0.72,
            1.28
        ],
        gap="large"
    )


    # ========================================================
    # INSTRUCCIONES
    # ========================================================

    with info_col:

        st.markdown(
            """
<div class="upload-intro">

<div class="upload-small">
Antes de comenzar
</div>

<div class="upload-title">
Utiliza una fotografía clara y enfocada.
</div>

<div class="upload-text">
Puedes seleccionar una fotografía existente o tomar una nueva
con la cámara del dispositivo.

La planta debe ocupar una parte importante de la imagen y debe
tener buena iluminación.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    # ========================================================
    # SUBIR O TOMAR FOTO
    # ========================================================

    with entrada_col:

        st.markdown(
            """
<div class="input-title">
¿Cómo deseas obtener la fotografía?
</div>

<div class="input-subtitle">
Selecciona una de las dos opciones.
</div>
""",
            unsafe_allow_html=True
        )


        metodo = st.radio(
            "Método de entrada",
            [
                "Subir fotografía",
                "Tomar fotografía"
            ],
            horizontal=True,
            label_visibility="collapsed",
            key=(
                "metodo_"
                + str(
                    st.session_state.entrada_version
                )
            )
        )


        archivo_entrada = None
        imagen = None


        # ====================================================
        # OPCION 1 - SUBIR
        # ====================================================

        if metodo == "Subir fotografía":

            if st.session_state.upload_error:

                st.error(
                    st.session_state.upload_error
                )

                st.session_state.upload_error = None


            archivo_entrada = st.file_uploader(
                "Seleccionar fotografía",
                type=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp"
                ],
                accept_multiple_files=False,
                max_upload_size=8,
                key=(
                    "archivo_"
                    + str(
                        st.session_state.entrada_version
                    )
                ),
                help=(
                    "Solo JPG, JPEG, PNG y WEBP. "
                    "Máximo 8 MB."
                )
            )


            st.caption(
                "Formatos permitidos: JPG, JPEG, PNG y WEBP. "
                "Máximo 8 MB."
            )


            if archivo_entrada is not None:

                valido, imagen, error = validar_imagen_subida(
                    archivo_entrada
                )


                if not valido:

                    st.session_state.upload_error = error

                    st.session_state.resultado_ia = None

                    st.session_state.entrada_version += 1

                    st.rerun()


        # ====================================================
        # OPCION 2 - CAMARA
        # ====================================================

        else:

            archivo_entrada = st.camera_input(
                "Tomar fotografía",
                resolution="720p",
                width="stretch",
                key=(
                    "camara_"
                    + str(
                        st.session_state.entrada_version
                    )
                )
            )


            st.caption(
                "Permite el acceso a la cámara y toma "
                "una fotografía clara de la planta."
            )


            if archivo_entrada is not None:

                valido, imagen, error = procesar_foto_camara(
                    archivo_entrada
                )


                if not valido:

                    st.error(
                        error
                    )

                    archivo_entrada = None


    # ========================================================
    # IMAGEN DISPONIBLE
    # ========================================================

    if (
        archivo_entrada is not None
        and
        imagen is not None
    ):

        archivo_hash = hashlib.sha256(
            archivo_entrada.getvalue()
        ).hexdigest()


        resultado_ia = st.session_state.resultado_ia


        mismo_archivo = (
            resultado_ia is not None
            and
            resultado_ia.get(
                "hash"
            ) == archivo_hash
        )


        # ====================================================
        # ANTES DE ANALIZAR
        # ====================================================

        if not mismo_archivo:

            st.write("")


            espacio1, vista, espacio2 = st.columns(
                [
                    0.8,
                    1.5,
                    0.8
                ]
            )


            with vista:

                st.image(
                    imagen,
                    caption="Fotografía seleccionada",
                    width="stretch"
                )


                analizar = st.button(
                    "Analizar planta",
                    type="primary",
                    width="stretch"
                )


            if analizar:

                with st.spinner(
                    "Analizando la fotografía..."
                ):

                    planta, confianza, predicciones = analizar_imagen(
                        imagen
                    )


                st.session_state.resultado_ia = {

                    "hash":
                        archivo_hash,

                    "planta":
                        planta,

                    "confianza":
                        confianza,

                    "predicciones":
                        predicciones.tolist()
                }


                st.rerun()


        # ====================================================
        # RESULTADO
        # ====================================================

        else:

            planta = resultado_ia[
                "planta"
            ]


            confianza = resultado_ia[
                "confianza"
            ]


            predicciones = np.array(
                resultado_ia[
                    "predicciones"
                ]
            )


            UMBRAL = 75.0


            st.write("")
            st.divider()
            st.write("")


            foto_col, resultado_col, top_col = st.columns(
                [
                    1.1,
                    0.9,
                    1.15
                ],
                gap="large"
            )


            # ================================================
            # FOTO
            # ================================================

            with foto_col:

                st.markdown(
                    """
<div class="result-label">
Fotografía analizada
</div>
""",
                    unsafe_allow_html=True
                )


                st.write("")


                st.image(
                    imagen,
                    width="stretch"
                )


            # ================================================
            # RESULTADO
            # ================================================

            with resultado_col:

                if confianza >= UMBRAL:

                    st.markdown(
                        f"""
<div class="result-box">

<div class="result-label">
Planta identificada
</div>

<div class="result-name">
{seguro(nombre_para_mostrar(planta))}
</div>

<div style="height:18px;"></div>

<div class="result-label">
Nivel de confianza
</div>

<div class="result-confidence">
{confianza:.2f} %
</div>

</div>
""",
                        unsafe_allow_html=True
                    )


                else:

                    st.markdown(
                        f"""
<div class="result-box">

<div class="result-label">
Resultado
</div>

<div class="result-name">
Identificación no concluyente
</div>

<div style="height:18px;"></div>

<div class="result-label">
Mayor probabilidad
</div>

<div class="result-confidence">
{confianza:.2f} %
</div>

</div>
""",
                        unsafe_allow_html=True
                    )


                    st.warning(
                        "Prueba con otra fotografía "
                        "más clara de la planta."
                    )


            # ================================================
            # TOP 3
            # ================================================

            with top_col:

                st.subheader(
                    "Resultados más probables"
                )


                top3 = np.argsort(
                    predicciones
                )[-3:][::-1]


                for posicion, idx in enumerate(
                    top3,
                    start=1
                ):

                    porcentaje = float(
                        predicciones[
                            idx
                        ] * 100
                    )


                    st.write(
                        f"{posicion}. "
                        f"{nombre_para_mostrar(clases[idx])} "
                        f"— {porcentaje:.2f} %"
                    )


                    st.progress(
                        min(
                            int(
                                porcentaje
                            ),
                            100
                        )
                    )


            # ================================================
            # ANALIZAR OTRA FOTO
            # ================================================

            st.write("")


            reset1, reset2, reset3 = st.columns(
                [
                    1.4,
                    0.8,
                    1.4
                ]
            )


            with reset2:

                if st.button(
                    "Analizar otra fotografía",
                    width="stretch"
                ):

                    st.session_state.resultado_ia = None

                    st.session_state.entrada_version += 1

                    st.rerun()


            # ================================================
            # INFORMACION
            # ================================================

            if confianza >= UMBRAL:

                resultado = datos[
                    datos[
                        "Clase IA"
                    ]
                    .astype(str)
                    .str.strip()
                    ==
                    planta.strip()
                ]


                if resultado.empty:

                    st.warning(
                        "La planta fue identificada, pero "
                        "no se encontró su información."
                    )


                else:

                    info = resultado.iloc[
                        0
                    ]


                    mostrar_ficha_completa(
                        info
                    )


# ============================================================
# GUIA DE PLANTAS
# ============================================================

elif st.session_state.pagina == "Guia":

    st.markdown(
        """
<div class="page-label">
Base de conocimiento
</div>

<div class="page-title">
Guía de plantas
</div>

<div class="accent-line"></div>

<div class="page-subtitle">
Selecciona una planta para consultar su imagen referencial
y todos sus cuidados.
</div>
""",
        unsafe_allow_html=True
    )


    opciones = (
        datos[
            "Clase IA"
        ]
        .dropna()
        .astype(str)
        .tolist()
    )


    seleccion = st.selectbox(
        "Seleccionar planta",
        opciones,
        format_func=nombre_para_mostrar
    )


    resultado = datos[
        datos[
            "Clase IA"
        ]
        .astype(str)
        .str.strip()
        ==
        seleccion.strip()
    ]


    if not resultado.empty:

        info = resultado.iloc[
            0
        ]


        imagen_ref = buscar_imagen_referencia(
            seleccion
        )


        st.write("")


        foto_col, nombre_col = st.columns(
            [
                0.70,
                1.4
            ],
            gap="large"
        )


        with foto_col:

            if imagen_ref:

                st.image(
                    imagen_ref,
                    caption=nombre_para_mostrar(
                        seleccion
                    ),
                    width="stretch"
                )


            else:

                st.info(
                    "Imagen referencial no disponible."
                )


        with nombre_col:

            st.markdown(
                f"""
<div class="result-box">

<div class="result-label">
Planta
</div>

<div class="result-name">
{seguro(nombre_para_mostrar(seleccion))}
</div>

<div style="height:14px;"></div>

<div class="result-label">
Nombre científico
</div>

<div style="
    color:#5E6B78;
    font-size:1rem;
    font-weight:650;
    margin-top:5px;
">
{seguro(obtener(info, "Nombre científico"))}
</div>

</div>
""",
                unsafe_allow_html=True
            )


        mostrar_ficha_completa(
            info
        )


# ============================================================
# GUIA DE USO
# ============================================================

elif st.session_state.pagina == "Uso":

    st.markdown(
        """
<div class="page-label">
Ayuda
</div>

<div class="page-title">
Guía de uso
</div>

<div class="accent-line"></div>

<div class="page-subtitle">
Puedes identificar una planta cargando una fotografía
existente o tomando una foto directamente con la cámara.
</div>
""",
        unsafe_allow_html=True
    )


    u1, u2, u3 = st.columns(
        3
    )


    with u1:

        st.markdown(
            """
<div class="help-card">

<div class="step-number">
1
</div>

<div class="help-title">
Elige el método
</div>

<div class="help-text">
Selecciona Subir fotografía si ya tienes una imagen
o Tomar fotografía para utilizar la cámara.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with u2:

        st.markdown(
            """
<div class="help-card">

<div class="step-number">
2
</div>

<div class="help-title">
Obtén la fotografía
</div>

<div class="help-text">
Selecciona la imagen desde tus archivos o permite
el acceso a la cámara y toma una fotografía.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with u3:

        st.markdown(
            """
<div class="help-card">

<div class="step-number">
3
</div>

<div class="help-title">
Analiza la planta
</div>

<div class="help-text">
Presiona Analizar planta para que el modelo
procese la fotografía.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    st.write("")


    u4, u5, u6 = st.columns(
        3
    )


    with u4:

        st.markdown(
            """
<div class="help-card">

<div class="step-number">
4
</div>

<div class="help-title">
Revisa el resultado
</div>

<div class="help-text">
PlantIA mostrará la especie reconocida,
el nivel de confianza y las alternativas principales.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with u5:

        st.markdown(
            """
<div class="help-card">

<div class="step-number">
5
</div>

<div class="help-title">
Consulta los cuidados
</div>

<div class="help-text">
Revisa riego, luz, temperatura, cultivo,
propagación, problemas y recomendaciones para Puno.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with u6:

        st.markdown(
            """
<div class="help-card">

<div class="step-number">
6
</div>

<div class="help-title">
Prueba otra fotografía
</div>

<div class="help-text">
Si el resultado es poco confiable utiliza otra
fotografía más clara y mejor enfocada.
</div>

</div>
""",
            unsafe_allow_html=True
        )


# ============================================================
# PIE
# ============================================================

st.write("")
st.divider()


st.caption(
    "PlantIA — Asistente inteligente para el reconocimiento "
    "y cuidado de plantas."
)