import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conectar = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='programacoes_filmes'
        )
        if conectar.is_connected():
            return conectar
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

if __name__ == "__main__":
    conectar = conectar()
    if conectar:
        print("Conexão estabelecida com sucesso!")
        conectar.close()
    else:
        print("Falha na conexão.")