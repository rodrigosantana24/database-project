import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='programacoes_filmes'
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None