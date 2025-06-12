import pandas as pd
import streamlit as st
import joblib

# Dicionário com os campos numéricos que o usuário irá preencher
x_numericos = {
    "latitude": 0,
    "longitude": 0,
    "accommodates": 0,
    "bathrooms": 0,
    "bedrooms": 0,
    "beds": 0,
    "extra_people": 0,
    "minimum_nights": 0,
    "ano": 0,
    "mes": 0,
    "n_amenities": 0,
    "host_listings_count": 0,
}

# Dicionário para campos booleanos (True/False) que serão preenchidos pelo usuário
x_tf = {"host_is_superhost": 0, "instant_bookable": 0}

# Dicionário com as opções das variáveis categóricas (listas de categorias possíveis)
x_listas = {
    "property_type": [
        "Apartment",
        "Bed and breakfast",
        "Condominium",
        "Guest suite",
        "Guesthouse",
        "Hostel",
        "House",
        "Loft",
        "Outros",
        "Serviced apartment",
    ],
    "room_type": ["Entire home/apt", "Hotel room", "Private room", "Shared room"],
    "cancellation_policy": [
        "flexible",
        "moderate",
        "strict",
        "strict_14_with_grace_period",
    ],
}

# Cria um dicionário para armazenar as variáveis dummies das categorias, inicializando todas com 0
dicionario = {}
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f"{item}_{valor}"] = 0

# Cria os campos de entrada numéricos no Streamlit para o usuário preencher
for item in x_numericos:
    if item == "latitude" or item == "longitude":
        valor = st.number_input(f"{item}", step=0.00001, value=0.0, format="%.5f")
    elif item == "extra_people":
        valor = st.number_input(f"{item}", step=0.01, value=0.0)
    else:
        valor = st.number_input(f"{item}", step=1, value=0)
    x_numericos[item] = valor

# Cria os campos de seleção para as variáveis booleanas (Sim/Não)
for item in x_tf:
    valor = st.selectbox(f"{item}", ("Sim", "Não"))
    if valor == "Sim":
        x_tf[item] = 1
    else:
        x_tf[item] = 0

# Cria os campos de seleção para as variáveis categóricas e marca a categoria escolhida como 1
for item in x_listas:
    valor = st.selectbox(f"{item}", x_listas[item])
    dicionario[f"{item}_{valor}"] = 1

# Botão para o usuário solicitar a previsão do valor do imóvel
botao = st.button("Prever Valor do Imóvel")

if botao:
    # Atualiza o dicionário com os valores numéricos e booleanos preenchidos pelo usuário
    dicionario.update(x_numericos)
    dicionario.update(x_tf)
    # Cria um DataFrame com os dados de entrada do usuário
    valores_x = pd.DataFrame(dicionario, index=[0])
    # Lê o arquivo de dados para obter a ordem correta das colunas
    dados = pd.read_csv("dados.csv")
    colunas = list(dados.columns)[1:-1]  # Remove a primeira e última coluna (caso haja ID ou target duplicado)
    valores_x = valores_x[colunas]  # Garante que as colunas estejam na ordem correta
    # Carrega o modelo treinado
    modelo = joblib.load("modelo.joblib")
    # Faz a previsão do preço com base nos dados do usuário
    preco = modelo.predict(valores_x)
    # Exibe o valor previsto na tela
    st.write(preco[0])