import yfinance as yf 
import streamlit as st
import pandas as pd
import plotly.express as px
import os

from datetime import date
from dateutil.relativedelta import relativedelta
from pycoingecko import CoinGeckoAPI

# Configuração da página
st.set_page_config(
    page_title="Crypto Tracker",
    page_icon=":coin:",
    layout="wide",
    initial_sidebar_state="collapsed"
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

st.title("Crypto Tracker - Gráficos")

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

mapa_criptos = {
    "Bitcoin": ("BTC-USD", "bitcoin.png", "bitcoin"),
    "Bitcoin Cash": ("BCH-USD", "bitcoin-cash.png", "bitcoin-cash"),
    "Ethereum": ("ETH-USD", "ethereum.png", "ethereum"),
    "Dogecoin": ("DOGE-USD", "dogecoin.png", "dogecoin"),
    "Ripple": ("XRP-USD", "ripple.png", "ripple"),
    "Litecoin": ("LTC-USD", "litecoin.png", "litecoin"),
    "Solana": ("SOL-USD", "solana.png", "solana")
}

def render_crypto_info(nome_cripto, img_cripto, id_cripto):
    col1, col2 = st.columns([1,2])
    with col1:
        st.image(os.path.join(imageDir, img_cripto))
        
    with col2:
        cotacao_brl = pegar_cotacao_crypto(id_cripto)
        cotacao_usd = pegar_cotacao_crypto2(id_cripto)
        st.markdown(f"""
            <div class="crypto-info {id_cripto}">
                <span>
                    Cotação BRL: R$ {cotacao_brl} <br>
                    Cotação USD: US$ {cotacao_usd}
                </span>
            </div>
        """, unsafe_allow_html=True)

def render_grafico():
    st.markdown("## **Gráfico:** ", unsafe_allow_html=True)

    col1, col2 = st.columns([1,4])

    with col1:
        opcoes_cripto = st.selectbox("Escolha sua criptomoeda: ", list(mapa_criptos.keys()))

        data_inicial = st.date_input("Data Inicial", date.today() - relativedelta(months=1))

        data_final = st.date_input("Data Final", date.today())

        intervalo_datas = st.selectbox("Período:", ("1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo"))

        seletor_de_valor = st.selectbox("Selecionar valor", ("Open", "High", "Low", "Close", "Volume"))

        if st.button("Gerar"):
            with col2:
                simbolo_cripto, img_cripto, id_cripto = mapa_criptos[opcoes_cripto]
                ticker = yf.Ticker(simbolo_cripto)
                hist_cripto = ticker.history(start=data_inicial, end=data_final, interval=intervalo_datas)

                fig = px.line(hist_cripto, x=hist_cripto.index, y=seletor_de_valor, labels={"x": "Date", seletor_de_valor: "Value"})

                render_crypto_info(opcoes_cripto, img_cripto, id_cripto)

                st.plotly_chart(fig, use_container_width=True)

render_grafico()
