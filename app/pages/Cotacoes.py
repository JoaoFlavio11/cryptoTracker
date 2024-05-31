import streamlit as st
import os

# Configuração da página
st.set_page_config(
    page_title="Crypto Tracker",
    page_icon=":coin:",
    layout="wide",
)

# Caminho deste diretório
currentDir = os.path.dirname(os.path.abspath(__file__))
# Caminho relativo para a pasta de imagens
imageDir = os.path.join(currentDir, "..", "assets", "imgs")
# Caminho relativo para o css
cssDir = os.path.join(currentDir, "..", "assets", "css", "style.css")

# Ler o css
with open(cssDir) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Crypto Tracker - Cotações")



st.markdown("""
    <footer>
        <p> Desenvolvido por João Flávio C. Lopes | &copy; 2024 Crypto Tracker. Todos os direitos reservados. </p>
    </footer>
            
""",unsafe_allow_html=True)