import yfinance as yf 
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

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

def cotacao_formatada(valor, moeda="BRL"):
    if moeda == "BRL":
        return f"R$ {valor}".replace(",","X").replace(".",",").replace("X",".")
    elif moeda == "USD":
        return f"US$ {valor}"

mapa_criptos = {
    "Bitcoin": ("BTC-USD", "bitcoin.png", "bitcoin"),
    "Bitcoin Cash": ("BCH-USD", "bitcoin-cash.png", "bitcoin-cash"),
    "Ethereum": ("ETH-USD", "ethereum.png", "ethereum"),
    "Dogecoin": ("DOGE-USD", "dogecoin.png", "dogecoin"),
    "Ripple": ("XRP-USD", "ripple.png", "ripple"),
    "Litecoin": ("LTC-USD", "litecoin.png", "litecoin"),
    "Solana": ("SOL-USD", "solana.png", "solana")
}

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def render_crypto_info(nome_cripto, img_cripto, id_cripto):
    col1, col2 = st.columns([2, 2])
    
    img_path = os.path.join(imageDir, img_cripto)
    img_base64 = get_image_base64(img_path)
    
    with col1:
        st.markdown(
            f"""
            <div class="header-graf">
                <img src="data:image/png;base64,{img_base64}"/>
                <h1>{nome_cripto}</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col2:
        cotacao_brl = pegar_cotacao_crypto(id_cripto)
        cotacao_usd = pegar_cotacao_crypto2(id_cripto)
        cotacao_brl_formatada = cotacao_formatada(cotacao_brl, "BRL")
        cotacao_usd_formatada = cotacao_formatada(cotacao_usd, "USD")

        st.markdown(f"""
            <div class="crypto-info {id_cripto}">
                <span>
                    Valor BRL: {cotacao_brl_formatada} <br>
                    Valor USD: {cotacao_usd_formatada}
                </span>
            </div>
        """, unsafe_allow_html=True)

def render_grafico():
    col1, col2 = st.columns([1,4])

    with col1:
        opcoes_cripto = st.selectbox("Escolha sua criptomoeda: ", list(mapa_criptos.keys()))

        data_inicial = st.date_input("Data Inicial:", date.today() - relativedelta(months=1))

        data_final = st.date_input("Data Final:", date.today())

        intervalo_datas = st.selectbox("Período:", ("1 minuto", "2 minutos", "5 minutos", "15 minutos", "30 minutos", "1 hora", "1 dia", "5 dias", "1 semana", "1 mês", "3 meses"))

        seletor_de_valor = st.selectbox("Selecione o valor base:", ("Abertura", "Alta", "Baixa", "Fechamento", "Volume"))

        if st.button("Gerar"):
            with col2:
                simbolo_cripto, img_cripto, id_cripto = mapa_criptos[opcoes_cripto]
                ticker = yf.Ticker(simbolo_cripto)

                datas_dict = {"1 minuto":"1m", "2 minutos":"2m", "5 minutos":"5m", "15 minutos":"15m","30 minutos":"30m","1 hora":"1h","1 dia":"1d","5 dias":"5d","1 semana":"1wk","1 mês":"1mo","3 meses":"3mo"}

                hist_cripto = ticker.history(start=data_inicial, end=data_final, interval=datas_dict[intervalo_datas])

                valor_dict = { "Abertura": "Open", "Alta":"High","Baixa":"Low","Fechamento":"Close","Volume":"Volume"}
                valor_selecionado = valor_dict[seletor_de_valor]

                fig = px.line(hist_cripto, x=hist_cripto.index, y=valor_selecionado, labels={"x": "Data", valor_selecionado: "Valor"})

                render_crypto_info(opcoes_cripto, img_cripto, id_cripto)

                st.plotly_chart(fig, use_container_width=True)

render_grafico()

st.markdown("""
    <footer>
        <p> Desenvolvido por João Flávio C. Lopes | &copy; 2024 Crypto Tracker. Todos os direitos reservados. </p>
    </footer>
            
""",unsafe_allow_html=True)
