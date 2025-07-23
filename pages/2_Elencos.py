import streamlit as st
import time
from services import elenco_service

st.set_page_config(page_title="Gerenciar Elencos", layout="wide")
st.title("🎭 Gerenciamento de Elencos")

if "user_message" not in st.session_state:
    st.session_state.user_message = None
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

if st.session_state.get("user_message"):
    success_message, text = st.session_state.user_message
    if success_message:
        st.success(text)
    else:
        st.error(text)
    st.session_state.user_message = None
    time.sleep(3) 
    st.rerun()

with st.expander("➕ Adicionar Novo Ator/Atriz ao Elenco", expanded=True):
    with st.form("new_elenco_form", clear_on_submit=True):
        st.subheader("Dados do Novo Registro")
        
        num_filme = st.number_input(
            "Número do Filme", 
            value=None, 
            min_value=1, 
            step=1, 
        )
        
        nome_ator = st.text_input("Nome do Ator/Atriz")
        is_protagonista = st.checkbox("É protagonista?")
        
        submitted = st.form_submit_button("Adicionar ao Elenco")
        if submitted:
            if not nome_ator.strip() or num_filme is None:
                st.warning("Por favor, preencha todos os campos obrigatórios.")
            else:
                success, message = elenco_service.create_elenco(num_filme, nome_ator, is_protagonista)
                st.session_state.user_message = (success, message)
                st.rerun()

st.header("🎬 Elenco Cadastrado")
elenco_df = elenco_service.read_elenco()

if elenco_df.empty:
    st.info("Nenhum registro de elenco encontrado.")
else:
    col1, col2, col3, col4 = st.columns([1.5, 4, 1.5, 2])
    with col1: st.write("**Nº Filme**")
    with col2: st.write("**Nome do Ator/Atriz**")
    with col3: st.write("**Protagonista**")
    with col4: st.write("**Ações**")
    st.markdown("<hr style='margin-top: 0; margin-bottom: 1rem;'>", unsafe_allow_html=True)

    for _, row in elenco_df.iterrows():
        actor_id = (row['num_filme'], row['nome_ator_atriz'])
        is_editing = st.session_state.get("editing_id") == actor_id

        if is_editing:
            with st.form(key=f"edit_form_{actor_id[0]}_{actor_id[1]}"):
                c1, c2, c3, c4 = st.columns([1.5, 4, 1.5, 2])
                with c1:
                    new_num_filme = st.number_input("Nº Filme", value=row['num_filme'], min_value=1, step=1, label_visibility="collapsed")
                with c2:
                    new_nome_ator = st.text_input("Nome Ator", value=row['nome_ator_atriz'], label_visibility="collapsed")
                with c3:
                    new_protagonista = st.checkbox("É protagonista?", value=bool(row['protagonista']), key=f"edit_check_{actor_id}")
                with c4:
                    form_cols = st.columns(2)
                    if form_cols[0].form_submit_button("Salvar", use_container_width=True):
                        success, message = elenco_service.update_elenco(
                            old_num_filme=row['num_filme'], 
                            old_nome_ator=row['nome_ator_atriz'],
                            new_num_filme=new_num_filme,
                            new_nome_ator=new_nome_ator,
                            new_protagonista=new_protagonista
                        )
                        st.session_state.user_message = (success, message)
                        st.session_state.editing_id = None 
                        st.rerun()

                    if form_cols[1].form_submit_button("Cancelar", type="secondary", use_container_width=True):
                        st.session_state.editing_id = None 
                        st.rerun()
        else:
            col1, col2, col3, col4 = st.columns([1.5, 4, 1.5, 2])
            with col1:
                st.write(row['num_filme'])
            with col2:
                st.write(row['nome_ator_atriz'])
            with col3:
                st.write(int(row['protagonista']))
            with col4:
                action_cols = st.columns(2)
                if action_cols[0].button("Editar", key=f"edit_{actor_id}", help="Editar registro", use_container_width=True):
                    st.session_state.editing_id = actor_id
                    st.rerun()
                if action_cols[1].button("Remover", key=f"del_{actor_id}", help="Remover do elenco", use_container_width=True):
                    success, message = elenco_service.delete_elenco(row['num_filme'], row['nome_ator_atriz'])
                    st.session_state.user_message = (success, message)
                    st.rerun()