import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Prueba de cámara",
    layout="centered"
)

st.title("Prueba de cámara - PlantIA")

st.write(
    "Presiona el botón de cámara, permite el acceso "
    "y toma una fotografía."
)

foto = st.camera_input(
    "Tomar fotografía",
    resolution="720p",
    width="stretch"
)

if foto is not None:

    imagen = Image.open(foto)

    st.success("La cámara funciona correctamente.")

    st.image(
        imagen,
        caption="Fotografía capturada",
        width="stretch"
    )

    st.write(
        "Resolución:",
        imagen.size
    )