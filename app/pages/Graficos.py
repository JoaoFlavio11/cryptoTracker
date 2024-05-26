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

mapa_criptos = {"Bitcoin": "BTC-USD", "Bitcoin Cash":"BCH-USD", "Ethereum": "ETH-USD", "Dogecoin": "DOGE-USD", "Ripple":"XRP-USD", "Litecoin":"LTC-USD", "Solana":"SOL-USD"}

def render_grafico():
    st.markdown("## **Gráfico:** ", unsafe_allow_html=True)

    col1, col2 = st.columns([1,4])

    with col1:
        opcoes_cripto = st.selectbox("Escolha sua criptomoeda: ", ("Bitcoin", "Bitcoin Cash", "Ethereum", "Dogecoin", "Ripple", "Litecoin", "Solana"))

        data_inicial = st.date_input("Data Inicial", date.today() - relativedelta(months=1))

        data_final = st.date_input("Data Final", date.today())

        intervalo_datas = st.selectbox("Período:", ("1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo"))

        # Ver a função
        seletor_de_valor = st.selectbox("Selecionar valor", ("Open", "High", "Low", "Close", "Volume"))

        if st.button("Gerar"):
            with col2:
                simbolo_cripto = mapa_criptos[opcoes_cripto]
                ticker = yf.Ticker(simbolo_cripto)
                hist_cripto = ticker.history(start=data_inicial, end=data_final, interval=intervalo_datas)

                fig = px.line(hist_cripto, x=hist_cripto.index, y=seletor_de_valor, labels={"x": "Date", seletor_de_valor: "Value"})

                if opcoes_cripto == "Bitcoin":
                    col1, col2 = st.columns([1,2])
                    with col1:
                        st.write(pegar_cotacao_crypto("bitcoin"))
                        st.image(os.path.join(imageDir, "bitcoin.png"), width=400)
                    with col2:
                        st.write(f"""
                            <span style="font-family: 'Source Sans Pro'; font-weight: bold; font-style: italic; font-size: 30px; color: #f7931a; display: block; text-align: center;">
                                Cotação BRL: R$ {pegar_cotacao_crypto("bitcoin")} .<br>
                                Cotação USD: US$ {pegar_cotacao_crypto2("bitcoin")} .
                            </span>
                        """, unsafe_allow_html=True)

                elif opcoes_cripto == "Ethereum":
                    col1, col2 = st.columns([1,2])
                    with col1:
                        st.image(os.path.join(imageDir, "ethereum.png"), width=400)
                    with col2:
                        st.write(f"""
                            <span style="font-family: 'Source Sans Pro'; font-weight: bold; font-style: italic; font-size: 30px; color: #8c8c8c; display: block; text-align: center;">
                                Cotação BRL: R$ {pegar_cotacao_crypto("ethereum")} .<br>
                                Cotação USD: US$ {pegar_cotacao_crypto2("ethereum")} .
                            </span>
                        """, unsafe_allow_html=True)
                        
                elif opcoes_cripto == "Dogecoin":
                    col1, col2 = st.columns([1,2])
                    with col1:
                        st.image(os.path.join(imageDir, "dogecoin.png"), width=400)
                    with col2:
                        st.write(f"""
                            <span style="font-family: 'Source Sans Pro'; font-weight: bold; font-style: italic; font-size: 30px; color: #f8bf1a; display: block; text-align: center;">
                                Cotação BRL: R$ {pegar_cotacao_crypto("dogecoin")} .<br>
                                Cotação USD: US$ {pegar_cotacao_crypto2("dogecoin")} .
                            </span>
                        """, unsafe_allow_html=True)
                    
                st.plotly_chart(fig, use_container_width=True)

render_grafico()
