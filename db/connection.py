import mysql.connector
import os 
import time

def create_connection():
    for i in range(10):
        try:
            connection = mysql.connector.connect(
                # Variáveis de ambiente
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            print("Conexão com o banco de dados bem-sucedida!")
            return connection
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao MySQL: {err}. Tentando novamente em 5 segundos...")
            time.sleep(5) 
    
    print("Não foi possível conectar ao banco de dados após várias tentativas.")
    return None


