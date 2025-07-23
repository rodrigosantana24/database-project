import streamlit as st
import time
from services import canal_service 

if "user_message" not in st.session_state:
    st.session_state.user_message = None
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

st.set_page_config(page_title="Gerenciar Canais", layout="wide")
st.title("📺 Gerenciamento de Canais")

def handle_add_canal():
    num_canal_str = st.session_state.form_num_canal
    nome_canal = st.session_state.form_nome_canal.strip()

    if not nome_canal or not num_canal_str:
        st.warning("O 'Número do Canal' e o 'Nome do Canal' são campos obrigatórios.")
        return

    try:
        num_canal_int = int(num_canal_str)
        if num_canal_int <= 0:
            st.warning("O número do canal deve ser um valor inteiro positivo.")
            return

        success, message = canal_service.create_canal(num_canal_int, nome_canal)
        if success:
            st.session_state.form_num_canal = ""
            st.session_state.form_nome_canal = ""
            st.session_state.user_message = f"✅ {message}"
        else:
            st.error(message)
    except ValueError:
        st.error("O número do canal deve ser um número inteiro válido.")

if st.session_state.get("user_message"):
    st.success(st.session_state.user_message)
    st.session_state.user_message = None
    time.sleep(1.5)
    st.rerun()

with st.expander("➕ Adicionar Novo Canal", expanded=True):
    with st.form("new_canal_form"):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.text_input("Número do Canal", key="form_num_canal")
        with col2:
            st.text_input("Nome do Canal", key="form_nome_canal")
        st.form_submit_button("Adicionar Canal", on_click=handle_add_canal)

st.header("Lista de Canais Cadastrados")
canais_df = canal_service.read_canais()

if canais_df.empty:
    st.info("Nenhum canal cadastrado ainda ou falha ao carregar.")
else:
    col1, col2, col3 = st.columns([1, 4, 2], gap="small")
    with col1: st.write("**Número**")
    with col2: st.write("**Nome do Canal**")
    with col3: st.write("**Ações**")
    st.markdown("<hr style='margin: 1px 0;'>", unsafe_allow_html=True)

    for index, canal in canais_df.iterrows():
        is_editing = st.session_state.editing_id == canal['num_canal']
        
        if is_editing:
             with st.form(f"edit_form_{canal['num_canal']}"):
                col1, col2, col3 = st.columns([1, 4, 2], gap="small")
                with col1:
                    novo_num_canal_str = st.text_input("Número", value=str(canal['num_canal']), label_visibility="collapsed")
                with col2:
                    novo_nome = st.text_input("Nome", value=canal['nome'], label_visibility="collapsed")
                with col3:
                    col_save, col_cancel = st.columns(2)
                    if col_save.form_submit_button("Salvar", use_container_width=True):
                        num_canal_antigo = canal['num_canal']
                        
                        if not novo_nome.strip() or not novo_num_canal_str.strip():
                            st.warning("Ambos os campos, Número e Nome, são obrigatórios.")
                        else:
                            try:
                                novo_num_canal_int = int(novo_num_canal_str)
                                
                                success, message = canal_service.update_canal(num_canal_antigo, novo_num_canal_int, novo_nome.strip())
                                
                                if success:
                                    st.session_state.user_message = f"✅ {message}"
                                    st.session_state.editing_id = None
                                    st.rerun()
                                else:
                                    st.error(message)
                            except ValueError:
                                st.error("O número do canal deve ser um número inteiro válido.")

                    if col_cancel.form_submit_button("Cancelar", type="secondary", use_container_width=True):
                        st.session_state.editing_id = None
                        st.rerun()
        else:
            col1, col2, col3 = st.columns([1, 4, 2], gap="small")
            with col1: st.write(canal['num_canal'])
            with col2: st.write(canal['nome'])
            with col3:
                col_edit, col_delete = st.columns(2)
                if col_edit.button("Editar", key=f"edit_{canal['num_canal']}", use_container_width=True):
                    st.session_state.editing_id = canal['num_canal']
                    st.rerun()
                if col_delete.button("Remover", key=f"del_{canal['num_canal']}", use_container_width=True):
                    nome_deletado = canal['nome']
                    success, message = canal_service.delete_canal(canal['num_canal'])
                    if success:
                        st.session_state.user_message = f"🗑️ Canal '{nome_deletado}' deletado."
                        if st.session_state.editing_id == canal['num_canal']:
                            st.session_state.editing_id = None
                        st.rerun()
                    else:
                        st.error(message)