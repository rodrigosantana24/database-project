import streamlit as st
import pandas as pd
import time
from services import filme_service 

# Configuração da página
st.set_page_config(page_title="Gerenciar Filmes", layout="wide")
st.title("🎬 Gerenciamento de Filmes")

# Inicialização do session_state
if "user_message" not in st.session_state:
    st.session_state.user_message = None
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None
# A chave "deleting_id" não é mais necessária para a confirmação, mas mantê-la como None não causa problemas.
if "deleting_id" not in st.session_state:
    st.session_state.deleting_id = None

# Exibir mensagens de sucesso ou erro e limpar após 3 segundos
if st.session_state.get("user_message"):
    success, message = st.session_state.user_message
    if success:
        st.success(message)
    else:
        st.error(message)
    st.session_state.user_message = None
    time.sleep(3)
    st.rerun()

# Formulário para adicionar novo filme
with st.expander("➕ Adicionar Novo Filme", expanded=True):
    with st.form("new_filme_form", clear_on_submit=True):
        st.subheader("Dados do Novo Filme")
        
        col1, col2 = st.columns(2)
        with col1:
            num_filme = st.number_input("Número do Filme", value=None, min_value=1, step=1)
            ano_filme = st.number_input("Ano de Lançamento", value=None, min_value=1888, max_value=2050)
        with col2:
            nome_filme = st.text_input("Nome do Filme")
            duracao_filme = st.number_input("Duração (minutos)", value=None, min_value=1)
        
        submitted = st.form_submit_button("Adicionar Filme")
        if submitted:
            if not nome_filme.strip() or num_filme is None:
                st.warning("Por favor, preencha todos os campos obrigatórios.")
            else:
                ano_final = ano_filme if ano_filme is not None else 0
                duracao_final = duracao_filme if duracao_filme is not None else 0

                success, message = filme_service.create_filme(num_filme, nome_filme, ano_final, duracao_final)
                st.session_state.user_message = (success, message)
                st.rerun()

# Listagem de filmes cadastrados
st.header("Lista de Filmes Cadastrados")
filmes_df = filme_service.read_filmes()

if filmes_df.empty:
    st.info("Nenhum filme cadastrado ainda.")
else:
    # Cabeçalho da lista
    col1, col2, col3, col4, col5 = st.columns([1.5, 4, 1.5, 1.5, 2])
    with col1: st.write("**Nº Filme**")
    with col2: st.write("**Nome**")
    with col3: st.write("**Ano**")
    with col4: st.write("**Duração**")
    with col5: st.write("**Ações**")
    st.markdown("<hr style='margin-top: 0; margin-bottom: 1rem;'>", unsafe_allow_html=True)

    # Itera sobre os filmes para exibi-los
    for _, filme in filmes_df.iterrows():
        is_editing = st.session_state.get("editing_id") == filme['num_filme']
        
        if is_editing:
            # Formulário de edição (quando o modo de edição está ativo)
            with st.form(f"edit_form_{filme['num_filme']}"):
                c1, c2, c3, c4, c5 = st.columns([1.5, 4, 1.5, 1.5, 2])
                
                duracao_inicial = int(filme['duracao']) if pd.notna(filme['duracao']) else 0
                ano_inicial = int(filme['ano']) if pd.notna(filme['ano']) else 0

                with c1:
                    novo_num_filme = st.number_input("Nº", value=filme['num_filme'], min_value=1, step=1, label_visibility="collapsed")
                with c2:
                    novo_nome = st.text_input("Nome", value=filme['nome'], label_visibility="collapsed")
                with c3:
                    novo_ano = st.number_input("Ano", value=ano_inicial, min_value=0, label_visibility="collapsed")
                with c4:
                    nova_duracao = st.number_input("Duração", value=duracao_inicial, min_value=0, label_visibility="collapsed")
                with c5:
                    col_save, col_cancel = st.columns(2)
                    if col_save.form_submit_button("Salvar", use_container_width=True):
                        if not novo_nome.strip():
                            st.warning("O nome do filme não pode ser vazio.")
                        else:
                            success, message = filme_service.update_filme(
                                old_num_filme=filme['num_filme'], 
                                new_num_filme=novo_num_filme,
                                new_nome=novo_nome, 
                                new_ano=novo_ano, 
                                new_duracao=nova_duracao
                            )
                            st.session_state.user_message = (success, message)
                            st.session_state.editing_id = None
                            st.rerun()
                    if col_cancel.form_submit_button("Cancelar", type="secondary", use_container_width=True):
                        st.session_state.editing_id = None
                        st.rerun()
        else:
            # Exibição normal do filme na lista
            c1, c2, c3, c4, c5 = st.columns([1.5, 4, 1.5, 1.5, 2])
            with c1: st.write(filme['num_filme'])
            with c2: st.write(filme['nome'])
            with c3: 
                st.write(int(filme['ano']) if pd.notna(filme['ano']) and filme['ano'] > 0 else "N/A")
            with c4:
                st.write(f"{int(filme['duracao'])} min" if pd.notna(filme['duracao']) and filme['duracao'] > 0 else "N/A")
            with c5:
                col_edit, col_delete = st.columns(2)
                if col_edit.button("Editar", key=f"edit_{filme['num_filme']}", use_container_width=True):
                    st.session_state.editing_id = filme['num_filme']
                    st.session_state.deleting_id = None # Garante que o outro estado seja limpo
                    st.rerun()

                # --- ALTERAÇÃO PRINCIPAL AQUI ---
                # A exclusão agora é feita diretamente, sem confirmação.
                if col_delete.button("Remover", key=f"del_{filme['num_filme']}", use_container_width=True):
                    success, message = filme_service.delete_filme(filme['num_filme'])
                    st.session_state.user_message = (success, message)
                    st.session_state.editing_id = None # Limpa o estado de edição por segurança
                    st.session_state.deleting_id = None # Limpa o estado de exclusão
                    st.rerun()

