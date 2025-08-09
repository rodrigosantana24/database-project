# 🎬 Gerenciador de Filmes com Streamlit e Docker
![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)

Um projeto de aplicação web para gerenciar um catálogo de filmes e seus elencos. A interface interativa foi construída com Streamlit e toda a infraestrutura (aplicação, banco de dados e gerenciador de banco) é orquestrada com Docker e Docker Compose, permitindo uma execução simples e portável.

## ✨ Funcionalidades

- **CRUD Completo para Filmes:** Crie, leia, atualize e delete registros de filmes.
- **CRUD Completo para Elencos:** Adicione, leia, atualize e delete atores/atrizes do elenco de cada filme.
- **Interface Web Interativa:** Navegação e manipulação de dados de forma visual e intuitiva através do Streamlit.
- **Ambiente "Dockerizado":** Todo o projeto roda em contêineres isolados, facilitando a configuração e execução.
- **Gerenciador de Banco de Dados Web:** Acompanha o Adminer, uma interface web para visualizar e gerenciar o banco de dados diretamente no navegador.

## 🛠️ Tecnologias Utilizadas

- **Backend/Frontend:** Python 3.11, Streamlit
- **Banco de Dados:** MySQL 8.0
- **Containerização:** Docker, Docker Compose
- **Gerenciador de BD (Web):** Adminer

## Estrutura do Projeto:
```bash
.
├── data/                  
├── db/                    
│   ├── connection.py     
│   └── setup.sql          
├── pages/                 
├── services/              
├── .dockerignore          
├── .env.example           
├── app.py                 
├── compose.yaml           
├── Dockerfile             
└── requirements.txt 
```
## 👨‍💻 Desenvolvedores

| Nome                | E-mail                     |
|---------------------|-----------------------------|
| Gabriel Vinícius     | gabrielvto18@gmail.com   |
| Luan Vinícius     | limaluan32104@gmail.com   |
| Rodrigo Santana     | rodrigosantana.dev@gmail.com   |
| Victor de Souza     | victorsouza183@gmail.com   |
| Thalyson Kauan    | thalyson.kauan7@gmail.com |


## 🚀 Como Executar o Projeto

Graças ao Docker, você não precisa instalar Python ou MySQL na sua máquina. Apenas o Docker Desktop é necessário.

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.

### Passo a Passo

**1. Clone o Repositório**
```bash
git clone https://github.com/Luanv02/projeto-iaad.git
cd projeto-iaad
```
**2. Inicie a Aplicação com Docker Compose**
Com o Docker Desktop rodando, execute o seguinte comando na pasta raiz do projeto. Ele irá construir as imagens, criar os contêineres e iniciar tudo em modo de "watch", que atualiza a aplicação em tempo real conforme você edita o código.
```bash
docker compose up --watch
```
⚠️ Se não quiser o modo watch (recarregamento automático), use:
```bash
 docker compose up
```
**3. Acesse os Serviços**
Após a inicialização, os seguintes serviços estarão disponíveis no seu navegador:

| Serviço             | URL                                            |
| ------------------- | ---------------------------------------------- |
| Aplicação Streamlit | [http://localhost:8501](http://localhost:8501) |
| Adminer (BD Web UI) | [http://localhost:8081](http://localhost:8081) |

```bash
Preencha os dados para login:
Sistema: MySQL
Servidor: db
Usuário: root
Senha: 123456 (Definido no compose)
Base de dados: programacoes_filmes
```

**🛑 Como Parar e Remover os Contêineres**
Para parar e remover todos os contêineres e redes criadas pelo projeto, execute:
```bash
docker compose down
```
Para remover também os volumes (dados do banco), execute:
```bash
docker compose down -v
```




