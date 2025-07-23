import streamlit as st
import datetime
from services import exibicao_service

st.set_page_config(page_title="Gerenciar Exibições", layout="wide")
st.title("📅 Gerenciamento de Exibições")

def handle_add_exibicao():
    num_filme = st.session_state.form_num_filme
    num_canal = st.session_state.form_num_canal
    data = st.session_state.form_data
    hora = st.session_state.form_hora

    if not num_filme or not num_canal:
        st.error("Por favor, insira um Nº de Filme e um Nº de Canal.")
        return
    
    if not hora:
        st.error("Por favor, selecione um horário.")
        return

    success, message = exibicao_service.create_exibicao(num_filme, num_canal, data, hora)
    
    if success:
        st.toast(f"✅ {message}", icon="✅")
        st.session_state.form_num_filme = None
        st.session_state.form_num_canal = None
        st.session_state.form_data = datetime.date.today()
        st.session_state.form_hora = None 
    else:
        st.error(message)
        st.session_state.form_hora = None

if "form_num_filme" not in st.session_state:
    st.session_state.form_num_filme = None
if "form_num_canal" not in st.session_state:
    st.session_state.form_num_canal = None
if "form_data" not in st.session_state:
    st.session_state.form_data = datetime.date.today()
if "form_hora" not in st.session_state:
    st.session_state.form_hora = None
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

with st.expander("➕ Agendar Nova Exibição", expanded=True):
    with st.form("new_exibicao_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.number_input("Nº Filme", key="form_num_filme", min_value=1, step=1, format="%d")
            st.date_input("Data da Exibição", key="form_data", format="DD/MM/YYYY")
        with col2:
            st.number_input("Nº Canal", key="form_num_canal", min_value=1, step=1, format="%d")
            st.time_input("Hora da Exibição", key="form_hora", step=datetime.timedelta(minutes=5))
        
        st.form_submit_button("Agendar Exibição", on_click=handle_add_exibicao, use_container_width=True)

st.header("Exibições Agendadas")
exibicoes_df = exibicao_service.read_exibicoes()

if exibicoes_df.empty:
    st.info("Nenhuma exibição agendada.")
else:
    col_defs = [1.5, 1.5, 1.8, 1.2, 2] 
    cols = st.columns(col_defs, gap="small")
    headers = ["Nº Filme", "Nº Canal", "Data", "Hora", "Ações"]
    for col, header in zip(cols, headers):
        col.write(f"**{header}**")
    st.markdown("<hr style='margin: 1px 0; border-color: grey;'>", unsafe_allow_html=True)

    for index, exibicao in exibicoes_df.iterrows():
        exibicao_id_tuple = (
            exibicao['num_filme'], 
            exibicao['num_canal'], 
            exibicao['data_exibicao'].strftime('%Y-%m-%d'),
            (datetime.datetime.min + exibicao['hora_exibicao']).time().strftime('%H:%M:%S')
        )
        exibicao_id_str = str(exibicao_id_tuple)
        is_editing = st.session_state.get("editing_id") == exibicao_id_str

        if is_editing:
            with st.form(f"edit_form_{exibicao_id_str}"):
                c1, c2, c3, c4, c5 = st.columns(col_defs, gap="small")
                with c1: new_num_filme = st.number_input("Nº Filme", value=exibicao['num_filme'], min_value=1, step=1, label_visibility="collapsed", format="%d")
                with c2: new_num_canal = st.number_input("Nº Canal", value=exibicao['num_canal'], min_value=1, step=1, label_visibility="collapsed", format="%d")
                with c3: nova_data = st.date_input("Data", value=exibicao['data_exibicao'], label_visibility="collapsed", format="DD/MM/YYYY")
                with c4: nova_hora = st.time_input("Hora", value=(datetime.datetime.min + exibicao['hora_exibicao']).time(), label_visibility="collapsed", step=datetime.timedelta(minutes=5))
                
                with c5:
                    col_save, col_cancel = st.columns(2)
                    if col_save.form_submit_button("Salvar", use_container_width=True, help="Salvar alterações"):
                        old_hora = (datetime.datetime.min + exibicao['hora_exibicao']).time()
                        success, message = exibicao_service.update_exibicao(
                            exibicao['num_filme'], exibicao['num_canal'], 
                            exibicao['data_exibicao'].date(), old_hora, 
                            new_num_filme, new_num_canal, nova_data, nova_hora
                        )
                        if success:
                            st.toast(f"✅ {message}", icon="✅")
                            st.session_state.editing_id = None
                            st.rerun()
                        else:
                            st.error(message)
                            
                    if col_cancel.form_submit_button("Cancelar", type="secondary", use_container_width=True, help="Cancelar edição"):
                        st.session_state.editing_id = None
                        st.rerun()
        else:
            c1, c2, c3, c4, c5 = st.columns(col_defs, gap="small")
            with c1: st.write(exibicao['num_filme'])
            with c2: st.write(exibicao['num_canal'])
            with c3: st.write(exibicao['data_exibicao'].strftime('%d/%m/%Y'))
            with c4: st.write((datetime.datetime.min + exibicao['hora_exibicao']).time().strftime('%H:%M'))
            
            with c5:
                col_edit, col_delete = st.columns(2)
                if col_edit.button("Editar", key=f"edit_{exibicao_id_str}", use_container_width=True, help="Editar agendamento"):
                    st.session_state.editing_id = exibicao_id_str
                    st.rerun()
                if col_delete.button("Remover", key=f"del_{exibicao_id_str}", use_container_width=True, help="Remover agendamento"):
                    hora_para_deletar = (datetime.datetime.min + exibicao['hora_exibicao']).time()
                    success, message = exibicao_service.delete_exibicao(
                        exibicao['num_filme'], exibicao['num_canal'], 
                        exibicao['data_exibicao'].date(), hora_para_deletar
                    )
                    if success:
                        st.toast(f"🗑️ {message}", icon="🗑️")
                        st.rerun()
                    else:
                        st.error(message)
