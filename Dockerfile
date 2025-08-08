# Img base oficial do Python
FROM python:3.11-slim
# Diretório de trabalho dentro do contêiner
WORKDIR /app
# Arquivo de dependências
COPY requirements.txt .
# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt
# Copiar todo o resto do código do projeto para o diretório de trabalho no contêiner
COPY . .
# Porta padrao Streamlit 
EXPOSE 8501
# CMD para rodar a aplicação quando 
CMD ["streamlit", "run", "app.py"]