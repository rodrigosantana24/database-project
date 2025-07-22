import streamlit as st

# Título da página
st.title("Introdução ao Armazenamento e Análise de Dados (IAAD) – 2025.1")

# Título para a seção da imagem
st.header("Relacionamento entre as Tabelas")

# Exibindo a imagem
# Certifique-se de que o arquivo 'relacionamentos.png' está na mesma pasta do script
# ou forneça o caminho completo para a imagem.
st.image("relacionamentos.png")

# Legenda detalhada para a imagem usando markdown
st.markdown("""
<hr>

### **Análise dos Relacionamentos**

O esquema do banco de dados ilustra as seguintes conexões entre as tabelas:

* **filme e elenco(Um-para-Muitos - 1-N):**
    * Um **filme** pode ter vários atores/atrizes em seu **elenco**, mas cada registro de ator no elenco pertence a um único filme. A conexão é feita pela chave estrangeira num_filme na tabela elenco

* **filme, canal e exibicao (Muitos-para-Muitos - N-M):**
    * A tabela **exibicao** funciona como uma **tabela associativa** para conectar filme e canal.
    * Isso significa que um **filme** pode ser exibido em múltiplos **canais**, e um **canal** pode exibir múltiplos **filmes**.
    * Cada linha em exibicao representa um evento único: a exibição de um filme específico, em um canal específico, com data e hora definidas.

<hr>
""", unsafe_allow_html=True)