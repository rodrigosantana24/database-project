import streamlit as st
from services.exemplo_service import listar_filmes

st.title("Puxando registros do banco.")

filmes = listar_filmes()
for filme in filmes:
    st.subheader(filme['nome'])
    st.write(f"Ano: {filme['ano']}")
    st.write(f"Duração: {filme['duracao']}")