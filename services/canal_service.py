import streamlit as st
import pandas as pd
from db.connection import conectar
from mysql.connector import Error

def read_canais():
    conexao = conectar()
    if conexao:
        try:
            query = "SELECT num_canal, nome FROM canal ORDER BY num_canal"
            return pd.read_sql(query, conexao)
        except Error as e:
            st.error(f"Erro ao ler canais: {e}")
        finally:
            if conexao.is_connected():
                conexao.close()
    return pd.DataFrame()

def create_canal(num_canal, nome):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) FROM canal WHERE num_canal = %s", (num_canal,))
            if cursor.fetchone()[0] > 0:
                return False, f"Violação de Chave Primária: O número de canal '{num_canal}' já existe."
            cursor.execute("INSERT INTO canal (num_canal, nome) VALUES (%s, %s)", (num_canal, nome))
            conexao.commit()
            return True, "Canal criado com sucesso."
        except Error as e:
            conexao.rollback()
            return False, f"Erro de banco de dados ao criar canal: {e}"
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
    return False, "Falha na conexão com o banco de dados."

# --- FUNÇÃO MODIFICADA/ADICIONADA ---
def update_canal(num_canal_antigo, num_canal_novo, nome_novo):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()

            if int(num_canal_antigo) != int(num_canal_novo):
                cursor.execute("SELECT COUNT(*) FROM canal WHERE num_canal = %s", (num_canal_novo,))
                if cursor.fetchone()[0] > 0:
                    return False, f"Erro: O novo número de canal '{num_canal_novo}' já está em uso por outro canal."

            sql = "UPDATE canal SET num_canal = %s, nome = %s WHERE num_canal = %s"
            cursor.execute(sql, (num_canal_novo, nome_novo, num_canal_antigo))
            
            conexao.commit()
            
            if cursor.rowcount == 0:
                return False, "Nenhum canal encontrado com o número original para atualizar."

            return True, "Canal atualizado com sucesso."
        except Error as e:
            conexao.rollback()
            return False, f"Erro de Banco de Dados: {e}"
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
    return False, "Falha na conexão com o banco de dados."

def delete_canal(num_canal):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM exibicao WHERE num_canal = %s", (num_canal,))
            cursor.execute("DELETE FROM canal WHERE num_canal = %s", (num_canal,))
            conexao.commit()
            return True, "Canal deletado com sucesso."
        except Error as e:
            conexao.rollback()
            return False, f"Erro de banco de dados ao deletar canal: {e}"
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
    return False, "Falha na conexão com o banco de dados."