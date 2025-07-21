# pages/TriggerDemo.py
import streamlit as st
import datetime
from services import filme_service # Importe o módulo filme_service diretamente

st.set_page_config(layout="wide")

# Título da Página
st.title("🎬 Demonstração do Trigger de Validação de Filmes")

st.markdown("""
Esta página demonstra a funcionalidade do **Trigger de Validação de Ano de Lançamento**
diretamente no banco de dados. Este trigger impede que filmes sejam cadastrados
com um ano de lançamento futuro.
""")

st.subheader("Adicionar Novo Filme para Testar o Trigger")

with st.form("form_add_filme_trigger"):
    col1, col2 = st.columns(2)
    with col1:
        # Gerar um número de filme aleatório para facilitar os testes
        num_filme = st.number_input("Número do Filme", min_value=1, value=90000 + (datetime.datetime.now().microsecond % 1000) + datetime.datetime.now().second, step=1)
    with col2:
        nome = st.text_input("Nome do Filme", placeholder="Ex: Aventura no Tempo")

    col3, col4 = st.columns(2)
    with col3:
        # Valor padrão para o ano atual, mas permitindo futuro para o teste do trigger
        ano_atual = datetime.datetime.now().year # Usar 2025 para Recife, PE
        ano = st.number_input("Ano de Lançamento", min_value=1888, value=ano_atual, max_value=2050)
    with col4:
        duracao = st.number_input("Duração (minutos)", min_value=1, value=120)

    submitted = st.form_submit_button("Adicionar Filme e Testar Trigger")

    if submitted:
        if not nome.strip() or num_filme is None:
            st.warning("Por favor, preencha todos os campos obrigatórios (Número e Nome).")
        else:
            ano_final = ano if ano is not None else 0
            duracao_final = duracao if duracao is not None else 0

            # AQUI ESTÁ A MUDANÇA: Capturamos a tupla (success, message) do serviço
            success, message = filme_service.create_filme(num_filme, nome, ano_final, duracao_final)

            if success:
                st.success(f"Filme '{nome}' adicionado com sucesso! (Ano: {ano})")
                st.info(f"Mensagem do serviço: {message}")
                st.info("O trigger não foi acionado, pois o ano é válido.")
            else:
                # Se o serviço retornar False, então é um erro (pode ser o trigger ou outra falha)
                st.error(f"**ERRO AO ADICIONAR FILME:**")
                st.warning(f"O trigger barrou a operação! Mensagem do banco: _{message}_")
                st.markdown(f"""
                **Explicação:** O ano de lançamento ({ano}) é **futuro** (maior que {ano_atual}),
                e nosso trigger de validação no banco de dados impediu que o filme fosse salvo.
                Isso demonstra a integridade dos dados imposta diretamente pelo MySQL.
                """)
                st.markdown("---")
                st.markdown("**Código SQL do Trigger (para referência):**")
                st.code("""
DELIMITER $$
CREATE TRIGGER trg_validar_ano_filme_insert
BEFORE INSERT ON filme
FOR EACH ROW
BEGIN
    IF NEW.ano > YEAR(CURDATE()) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'O ano de lançamento do filme não pode ser futuro.';
    END IF;
END$$
DELIMITER ;
                """, language="sql")

st.markdown("---")
st.subheader("Como Funciona o Trigger:")
st.markdown("""
O trigger `trg_validar_ano_filme_insert` é configurado para ser executado
**ANTES** de cada nova inserção (`BEFORE INSERT`) na tabela `filme`.

Ele verifica se o `ano` do novo filme (`NEW.ano`) é maior que o ano atual
(`YEAR(CURDATE())`). Se for, ele utiliza `SIGNAL SQLSTATE '45000'` para
gerar um erro personalizado, impedindo a operação de inserção e retornando
a mensagem que você viu acima.
""")