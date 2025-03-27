import requests
import pandas as pd
import streamlit as st
import plotly.express as px

url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?language=pt'
response = requests.get(url)
dados = response.json()

# CRIAÇÃO DO DATAFRAME PANDAS COM OS DADOS RECEBEIDOS DA API
df = pd.DataFrame(dados['data'])

# FILTRANDO AS PRINCIPAIS COLUNAS DO DATAFRAME
df_filtered_columns = df[['name', 'type', 'atk', 'def', 'desc']]

# FILTRANDO OS PRINCIPAIS TIPOS DE CARTAS PARA PASSAR COMO DEFAULT AO MULTISELECT
df_default_types =  df_filtered_columns[df_filtered_columns['type'].isin(['Effect Monster', 'Spell Card', 'Trap Card', 'Normal Monster', 'Fusion Monster', 'Skill Card'])]

st.title('Dashboard API YuGiOh')
filter_option = st.selectbox('Escolha uma opção', ['---', 'Mostrar tudo', 'Filtrar por tipo'])

if filter_option == 'Mostrar tudo':
    st.dataframe(df_filtered_columns, hide_index=True)
elif filter_option == 'Filtrar por tipo':
    # CHECKBOX PARA SELECIONAR TODOS OS TIPOS NO MULTISELECT
    select_all = st.sidebar.checkbox('Selecionar todos', False)
    if select_all:
        # CASO O CHECKBOX SEJA ATIVADO, O PARÂMETRO DEFAULT DO MULTISELECT RECEBE O DATAFRAME COM TODOS OS TIPOS
        selection = st.sidebar.multiselect('Selecione os tipos para mostrar o gráfico', df_filtered_columns['type'].drop_duplicates(), df_filtered_columns['type'].drop_duplicates())
    else:
        # CASO O CHECKBOX NÃO SEJA ATIVADO, O PARâMETRO DEFAULT DO MULTISELECT RECEBE O DATAFRAME FILTRADO
        selection = st.sidebar.multiselect('Selecione os tipos para mostrar o gráfico', df_filtered_columns['type'].drop_duplicates(), df_default_types['type'].drop_duplicates())
    
    # VERIFICA OS TIPOS SELECIONADOS NO MULTISELECT
    df_selected_types =  df_filtered_columns[df_filtered_columns['type'].isin(selection)]
    # FAZ A CONTAGEM DA QUANTIDADE DE CARTAS COM DETERMINADO TIPO
    df_type_count = df_selected_types['type'].value_counts().reset_index()
    st.write(f'Total de Cartas ({len(df_filtered_columns)})')

    # CRIAR O CONTAINER COM O PIE CHART MOSTRANDO OS TIPOS FILTRADOS E A QUANTIDADE DE CARTAS ATRIBUIDAS
    with st.container(border=True):
        fig = px.pie(df_type_count, values='count', names='type', title="Distribuição de Tipos")
        st.plotly_chart(fig)
