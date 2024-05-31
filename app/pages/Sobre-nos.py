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
    
st.title("Crypto Tracker - Sobre nós")

st.markdown(""" 

    O **Crypto Tracker** é uma ferramenta poderosa projetada para acompanhar a cotação atual e gerar gráficos detalhados das principais criptomoedas, incluindo Bitcoin, Ethereum e Dogecoin. Com interface intuitiva e funcionalidades abrangentes, este aplicativo oferece uma visão completa do mercado de criptomoedas em tempo real.

    **Recursos Principais:**

    - **Cotação em Tempo Real:** Acompanhe o preço atual das criptomoedas em relação ao BRL (Real Brasileiro).

    - **Análise de Dados:** Gere gráficos dinâmicos e informativos para visualizar tendências de preço ao longo do tempo.

    - **Seleção Personalizada:** Escolha sua criptomoeda de interesse e ajuste o período de análise conforme suas necessidades.
        <hr>
""", unsafe_allow_html=True)
    
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(" ### Doações em BTC: ")
    st.image(os.path.join(imageDir, "qrcode_wallet.jpeg"), use_column_width=True)

with col2:
    st.markdown(" ### Doações: ")
    st.image(os.path.join(imageDir, "bin_any_final.jpeg"), use_column_width=True)
        
with col3:
    st.markdown(" ### Doações em BTC: ")

with col4:
    st.markdown(" ### Doações em BTC: ")


st.markdown("""
    <footer>
        <p> Desenvolvido por João Flávio C. Lopes | &copy; 2024 Crypto Tracker. Todos os direitos reservados. </p>
    </footer>
            
""",unsafe_allow_html=True)