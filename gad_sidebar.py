import streamlit as st
import base64
import os

def show_gad_sidebar():
    def image_to_base64(file_path):
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Ruta absoluta segura a logo_gad.png (en carpeta raíz del proyecto)
    logo_path = os.path.abspath("logo_gad.png")
    logo_base64 = image_to_base64(logo_path)

    st.markdown("""
        <style>
            .gad-footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 18rem;
                padding: 10px 15px;
                font-size: 11px;
                text-align: center;
            }

            .gad-footer p {
                margin: 3px 0;
                font-size: 11px;
                color: white;
            }

            .social-icons a {
                margin: 0 8px;
                display: inline-block;
            }

            .gad-footer b {
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
        <div class="gad-footer">
            <img src="data:image/png;base64,{logo_base64}" width="120"><br>
            <p><b>GOBIERNO AUTÓNOMO DESCENTRALIZADO</b></p>
            <p><b>PARROQUIAL RURAL DE RICAURTE</b></p>
            <p>📍 Av. Ricaurte 2-48 y Padre Vicente Pacheco</p>
            <p>🏙️ Azuay - Cuenca</p>
            <p>📞 0986966570</p>
            <p>📧 sistemas@ricaurte.gob.ec</p>
            <div class="social-icons">
                <a href="https://facebook.com/GADRicaurte" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" width="24">
                </a>
                <a href="https://instagram.com/GADRicaurte" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="24">
                </a>
                <a href="https://twitter.com/GADRicaurte" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/3670/3670151.png" width="24">
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
