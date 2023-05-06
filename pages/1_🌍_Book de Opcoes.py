import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit_extras
import requests
import json
from plotly import graph_objs as go
from bs4 import BeautifulSoup

# Config
st.set_page_config(page_title='Book de Opções', page_icon='🌍', layout='wide')

st.title('🌍 Book de Opções')

DATA_INICIO = '2000-01-01'

DATA_FIM = dt.datetime.today()


st.title('Analise de ações')

def pegar_dados_acoes():

    path = 'acoes.csv'
    return pd.read_csv(path, delimiter=';')


df_acao = pegar_dados_acoes()


acao = df_acao['snome']


nome_acao_escolhida = st.selectbox('Escolha uma ação', acao)

df_ativo = df_acao[df_acao['snome'] == nome_acao_escolhida]
acao_escolhida = df_ativo.iloc[0]['sigla_acao']
acao_escolhida = acao_escolhida + '.SA'
acao_escolhida_opcao = df_ativo.iloc[0]['sigla_acao']

@st.cache_data
def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM)
    df.reset_index(inplace=True)
    return df

df_valores = pegar_valores_online(acao_escolhida).sort_values('Date', ascending=False)


# Criar grafico
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['Adj Close'], name='Preço', line_color='blue'))
st.plotly_chart(fig)

st.subheader('Tabela de valores - ' + nome_acao_escolhida)
# Criar colunas
col1, col2 = st.columns(2)

with col1:
    st.write(df_valores)

with col2:
    st.subheader("Cotação atual:")
    st.title(df_valores['Adj Close'].iloc[0])


st.write(dt.datetime.now())

# Defina o DataFrame pandas com as colunas que deseja
df = pd.DataFrame()
pd.set_option('display.max_columns', None)

# Configurações Webscraping
url = f'https://oplab.com.br/mercado/acoes/{acao_escolhida_opcao}'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
script = soup.find('script', {'id': '__NEXT_DATA__'})
json_data = json.loads(script.string)

if 'series' not in json_data['props']['pageProps']:
    st.warning(' Essa ação não possui book de opções', icon="⚠️")
    st.stop()

# Dados opções
series = json_data['props']['pageProps']['series']
for option in series:
    due_date = option['due_date']
    days_to_maturity = option['days_to_maturity']
    strikes = option['strikes']
    for strike in strikes:
        strike_price = strike['strike']
        tipo_call = strike['call']['category']
        tipo_put = strike['put']['category']
        call_symbol = strike['call']['symbol']
        put_symbol = strike['put']['symbol']
        call_bid = strike['call']['bid']
        put_bid = strike['put']['bid']
        call_ask = strike['call']['ask']
        put_ask = strike['put']['ask']
        market_maker_call = strike['call']['market_maker']
        market_maker_put = strike['put']['market_maker']
        due_date = pd.to_datetime(due_date).strftime('%d/%m/%Y')
        maturity_type_call = strike['call']['maturity_type']
        maturity_type_put = strike['put']['maturity_type']
        volume_call = strike['call']['volume']
        volume_put = strike['put']['volume']
        financial_volume_call = strike['call']['financial_volume']
        financial_volume_put = strike['put']['financial_volume']
        time_call = strike['call']['time']
        time_put = strike['put']['time']
        liquidity_call = strike['call']['liquidity']
        liquidity_put = strike['put']['liquidity']
        variation_call = strike['call']['variation']
        variation_put = strike['put']['variation']
        open_call = strike['call']['open']
        open_put = strike['put']['open']
        high_call = strike['call']['high']
        high_put = strike['put']['high']
        low_call = strike['call']['low']
        low_put = strike['put']['low']
        close_call = strike['call']['close']
        close_put = strike['put']['close']
        contract_size_call = strike['call']['contract_size']
        contract_size_put = strike['put']['contract_size']
        # Black Scholes e gregas
        bs_moneyness_call = strike['call']['bs']['moneyness']
        bs_moneyness_put = strike['put']['bs']['moneyness']
        bs_preco_call = strike['call']['bs']['price']
        bs_preco_put = strike['put']['bs']['price']
        bs_premium_call = strike['call']['bs']['premium']
        bs_premium_put = strike['put']['bs']['premium']
        bs_vi_call = strike['call']['bs']['vi']
        bs_vi_put = strike['put']['bs']['vi']
        bs_ve_call = strike['call']['bs']['ve']
        bs_ve_put = strike['put']['bs']['ve']
        bs_cost_if_exercised_call = strike['call']['bs']['cost-if-exercised']
        bs_cost_if_exercised_put = strike['put']['bs']['cost-if-exercised']
        bs_delta_call = strike['call']['bs']['delta']
        bs_delta_put = strike['put']['bs']['delta']
        bs_gamma_call = strike['call']['bs']['gamma']
        bs_gamma_put = strike['put']['bs']['gamma']
        bs_vega_call = strike['call']['bs']['vega']
        bs_vega_put = strike['put']['bs']['vega']
        bs_theta_call = strike['call']['bs']['theta']
        bs_theta_put = strike['put']['bs']['theta']
        bs_rho_call = strike['call']['bs']['rho']
        bs_rho_put = strike['put']['bs']['rho']
        bs_volatility_call = strike['call']['bs']['volatility']
        bs_volatility_put = strike['put']['bs']['volatility']
        bs_poe_call = strike['call']['bs']['poe']
        bs_poe_put = strike['put']['bs']['poe']
        bs_protection_rate_call = strike['call']['bs']['protection-rate']
        bs_protection_rate_put = strike['put']['bs']['protection-rate']
        bs_profit_rate_call = strike['call']['bs']['profit-rate']
        bs_profit_rate_put = strike['put']['bs']['profit-rate']
        bs_protection_rate_over_cost_call = strike['call']['bs']['protection-rate-over-cost']
        bs_protection_rate_over_cost_put = strike['put']['bs']['protection-rate-over-cost']
        bs_profit_rate_if_exercised_call = strike['call']['bs']['profit-rate-if-exercised']
        bs_profit_rate_if_exercised_put = strike['put']['bs']['profit-rate-if-exercised']
        bs_ve_over_strike_call = strike['call']['bs']['ve-over-strike']
        bs_ve_over_strike_put = strike['put']['bs']['ve-over-strike']

# Adicionando tabela de call's
        df = pd.concat([df, pd.DataFrame({'Vencimento': due_date, 'Dias até o Vencimento': days_to_maturity,
                        'Preço do Strike': strike_price, 'Símbolo': call_symbol, 'Bid': call_bid,
                        'Ask': call_ask,  'Opção': tipo_call,
                        'Tipo': maturity_type_call,
                        'Volume': volume_call,
                        'Volume Financeiro': financial_volume_call,
                        'Hora': time_call,
                        'Liquidez': liquidity_call,
                        'Variação': variation_call,
                        'Abertura': open_call,
                        'Máximo': high_call,
                        'Mínimo': low_call,
                        'Fechamento Anterior': close_call,
                        'Tamanho do Contrato': contract_size_call,
                        'Moneyness': bs_moneyness_call,
                        'Preço teórico': bs_preco_call,
                        'Prêmio': bs_premium_call,
                        'VI': bs_vi_call,
                        'VE': bs_ve_call,
                        'Custo do exercício': bs_cost_if_exercised_call,
                        'Delta': bs_delta_call,
                        'Gamma': bs_gamma_call,
                        'Vega': bs_vega_call,
                        'Theta': bs_theta_call,
                        'Rho': bs_rho_call,
                        'Volatilidade Implícita': bs_volatility_call,
                        'POE': bs_poe_call,
                        'Taxa de proteção': bs_protection_rate_call,
                        'Taxa de lucro': bs_profit_rate_call,
                        'Taxa de proteção sobre custo': bs_protection_rate_over_cost_call,
                        'Taxa de lucro se exercido': bs_profit_rate_if_exercised_call,
                        'VE/S': bs_ve_over_strike_call}, index=[0])], ignore_index=True)

# Adicionando tabela de put's
        df = pd.concat([df, pd.DataFrame({'Vencimento': due_date, 'Dias até o Vencimento': days_to_maturity,
                        'Preço do Strike': strike_price, 'Símbolo': call_symbol, 'Bid': call_bid,
                        'Ask': call_ask,  'Opção': tipo_put,
                        'Tipo': maturity_type_put,
                        'Volume': volume_put,
                        'Volume Financeiro': financial_volume_put,
                        'Hora': time_put,
                        'Liquidez': liquidity_put,
                        'Variação': variation_put,
                        'Abertura': open_put,
                        'Máximo': high_put,
                        'Mínimo': low_put,
                        'Fechamento Anterior': close_put,
                        'Tamanho do Contrato': contract_size_put,
                        'Moneyness': bs_moneyness_put,
                        'Preço teórico': bs_preco_put,
                        'Prêmio': bs_premium_put,
                        'VI': bs_vi_put,
                        'VE': bs_ve_put,
                        'Custo do exercício': bs_cost_if_exercised_put,
                        'Delta': bs_delta_put,
                        'Gamma': bs_gamma_put,
                        'Vega': bs_vega_put,
                        'Theta': bs_theta_put,
                        'Rho': bs_rho_put,
                        'Volatilidade Implícita': bs_volatility_put,
                        'POE': bs_poe_put,
                        'Taxa de proteção': bs_protection_rate_put,
                        'Taxa de lucro': bs_profit_rate_put,
                        'Taxa de proteção sobre custo': bs_protection_rate_over_cost_put,
                        'Taxa de lucro se exercido': bs_profit_rate_if_exercised_put,
                        'VE/S': bs_ve_over_strike_put}, index=[0])], ignore_index=True)

# Index DataFrame
df.set_index('Símbolo', inplace=True)

cotacao_ativo = df_valores['Adj Close'].iloc[-1]


# Configuração de filtro e personalização de colunas DataFrame
opcoes_call = df[(df['Bid'] > 0) & 
    (df['Opção'] == 'CALL') & 
    (df['Dias até o Vencimento'] <= 70) &
    (df['Volume Financeiro'] > 10) &
    (df['Preço do Strike'] >= cotacao_ativo) &
    (df['Delta'] <= 0.30) &
    (df['Tipo'] == 'EUROPEAN')].sort_values(['Dias até o Vencimento','Taxa de lucro se exercido'], ascending=[True, False]).iloc[0:5]

opcoes_call['Preço ação'] = cotacao_ativo


opcoes_put = df[(df['Bid'] > 0) & 
(df['Opção'] == 'PUT') &
(df['Dias até o Vencimento'] <= 70) &
(df['Volume Financeiro'] >= 10) &
(df['Preço do Strike'] <= cotacao_ativo) &
(df['Delta'] <= 0.30) &
(df['Tipo'] == 'EUROPEAN')].sort_values(['Dias até o Vencimento','Taxa de lucro se exercido'], ascending=[True, False]).iloc[0:5]

opcoes_put['Preço ação'] = cotacao_ativo

st.markdown('''
### Melhores CALL'S  :chart_with_upwards_trend:''')
st.write(opcoes_call.tail(10))

st.markdown('''
### Melhores PUT'S :chart_with_downwards_trend:''')
st.write(opcoes_put.tail(10))

st.markdown('''
### Todas opções de  ''' + acao_escolhida)
st.write(df)


