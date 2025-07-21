import streamlit as st
import pandas as pd
from services import consulta_service

st.title("Consultas de Filmes por Atores")

# Consulta 1: Filmes por Ator
atores_opcoes = consulta_service.get_atores_disponiveis()
atores_selecionados = st.multiselect(
    "Nome do Ator/Atriz",
    options=atores_opcoes
)
filmes_ator_df = consulta_service.filmes_por_ator(atores_selecionados)

if filmes_ator_df.empty:
    st.info("Selecione um ator.")
else:
    col1, col2 = st.columns([1, 2], gap="small")
    with col1:
        st.write("**Ator/Atriz**")
    with col2:
        st.write("**Filmes**")
    st.markdown("<hr style='margin: 1px 0;'>", unsafe_allow_html=True)

    for index, filme_ator in filmes_ator_df.iterrows():
        col1, col2 = st.columns([1, 2], gap="small")
        with col1:
            st.write(filme_ator['nome_ator_atriz'])
        with col2:
            st.write(filme_ator['filmes'])

st.markdown("<hr style='margin: 1px 0;'>", unsafe_allow_html=True)

st.title("Consultas de Exibições de Filmes")

# Consulta 2: Filmes em Exibição
filmes_opcoes = consulta_service.get_filmes_disponiveis()
filmes_selecionados = st.multiselect(
    "Selecione os filmes",
    options=filmes_opcoes
)

min_data, max_data = consulta_service.get_limites_datas_exibicao()
if min_data and max_data:

    col1, col2 = st.columns([1, 3], gap="small")
    with col1:
        data_inicio, data_fim = st.slider(
            "Selecione o intervalo de datas",
            value=(pd.to_datetime(min_data).date(),
                   pd.to_datetime(max_data).date()),
            format="DD/MM/YYYY"
        )
else:
    data_inicio = pd.to_datetime("today")
    data_fim = pd.to_datetime("2025-08-30")

if filmes_selecionados:
    filmes_exibicao_df = consulta_service.filmes_em_exibicao(
        filmes_selecionados, str(data_inicio), str(data_fim)
    )
    if filmes_exibicao_df.empty:
        st.info("Nenhuma exibição encontrada.")
    else:

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="small")
        with col1:
            st.write("**Filme**")
        with col2:
            st.write("**Canal**")
        with col3:
            st.write("**Data**")
        with col4:
            st.write("**Horário**")
        st.markdown("<hr style='margin: 1px 0;'>", unsafe_allow_html=True)

        for index, exibicao in filmes_exibicao_df.iterrows():
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="small")
            with col1:
                st.write(exibicao['filme'])
            with col2:
                st.write(exibicao['canal'])
            with col3:
                st.write(exibicao['data'])
            with col4:
                st.write(exibicao['horário'])
else:
    st.info("Selecione um filme para consultar exibições.")
