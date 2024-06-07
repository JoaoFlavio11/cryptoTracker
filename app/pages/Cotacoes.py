import streamlit as st
import os
import base64
from pycoingecko import CoinGeckoAPI

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

# Função que pega o preço atual das criptomoedas
def pegar_cotacao_crypto(crypto):
    cg = CoinGeckoAPI()
    price = cg.get_price(ids=crypto, vs_currencies='brl')
    return price[crypto]['brl']

# Função em USD
def pegar_cotacao_crypto2(crypto):
    cg = CoinGeckoAPI()
    price2 = cg.get_price(ids=crypto, vs_currencies='usd')
    return price2[crypto]['usd']

def cotacao_formatada(valor, moeda="BRL"):
    if moeda == "BRL":
        return f"R$ {valor}".replace(",", "X").replace(".", ",").replace("X", ".")
    elif moeda == "USD":
        return f"US$ {valor}"

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def render_crypto_info(nome_cripto, img_cripto, id_cripto, coluna):
    img_path = os.path.join(imageDir, img_cripto)
    img_base64 = get_image_base64(img_path)
    
    cotacao_brl = pegar_cotacao_crypto(id_cripto)
    cotacao_usd = pegar_cotacao_crypto2(id_cripto)
    cotacao_brl_formatada = cotacao_formatada(cotacao_brl, "BRL")
    cotacao_usd_formatada = cotacao_formatada(cotacao_usd, "USD")
    
    coluna.markdown(
        f"""
        <div class="crypto-info" style="text-align: center;">
            <img src="data:image/png;base64,{img_base64}"/>
            <h3 style="margin: 0; font-size: 18px;">{nome_cripto}</h3>
            <p>BRL: {cotacao_brl_formatada}</p>
            <p>USD: {cotacao_usd_formatada}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

def render_cotacao():
    st.markdown("## **Cotações Atualizadas:** ", unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    if col1.button("Buscar BTC"):
        st.session_state.selected_crypto = ("Bitcoin", "bitcoin.png", "bitcoin", col1)

    if col2.button("Buscar ETH"):
        st.session_state.selected_crypto = ("Ethereum", "ethereum.png", "ethereum", col2)

    if col3.button("Buscar DOGE"):
        st.session_state.selected_crypto = ("Dogecoin", "dogecoin.png", "dogecoin", col3)

    if col4.button("Buscar XRP"):
        st.session_state.selected_crypto = ("Ripple", "ripple.png", "ripple", col4)

    if col5.button("Buscar LTC"):
        st.session_state.selected_crypto = ("Litecoin", "litecoin.png", "litecoin", col5)

    if col6.button("Buscar SOL"):
        st.session_state.selected_crypto = ("Solana", "solana.png", "solana", col6)

# Inicializar o estado da sessão
if "selected_crypto" not in st.session_state:
    st.session_state.selected_crypto = None

render_cotacao()

if st.session_state.selected_crypto:
    nome_cripto, img_cripto, id_cripto, coluna = st.session_state.selected_crypto
    render_crypto_info(nome_cripto, img_cripto, id_cripto, coluna)

st.markdown("""
    <footer>
        <p> Desenvolvido por João Flávio C. Lopes | &copy; 2024 Crypto Tracker. Todos os direitos reservados. </p>
    </footer>
""", unsafe_allow_html=True)
