import pandas as pd
import streamlit as st
from db.connection import create_connection
from mysql.connector import Error

def read_filmes():
    conexao = create_connection()
    if conexao:
        try:
            query = "SELECT num_filme, nome, ano, duracao FROM filme ORDER BY num_filme"
            df_filmes = pd.read_sql(query, conexao)
            return df_filmes
        except Error as e:
            st.error(f"Erro ao ler filmes: {e}")
        finally:
            if conexao.is_connected():
                conexao.close()
    return pd.DataFrame() 

def create_filme(num_filme, nome, ano, duracao):
    if not nome or not nome.strip():
        return False, "O nome do filme é um campo obrigatório."
    if num_filme is None:
        return False, "O número do filme é um campo obrigatório."

    conexao = create_connection()
    if not conexao:
        return False, "Falha na conexão com o banco de dados."
        
    try:
        cursor = conexao.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM filme WHERE num_filme = %s", (num_filme,))
        if cursor.fetchone()[0] > 0:
            return False, f"O número de filme '{num_filme}' já existe."

        cursor.execute("SELECT COUNT(*) FROM filme WHERE nome = %s", (nome,))
        if cursor.fetchone()[0] > 0:
            return False, f"O nome de filme '{nome}' já existe."

        query = "INSERT INTO filme (num_filme, nome, ano, duracao) VALUES (%s, %s, %s, %s)"
        duracao_final = duracao if duracao and duracao > 0 else None
        ano_final = ano if ano and ano > 0 else None
        cursor.execute(query, (num_filme, nome.strip(), ano_final, duracao_final))
        
        conexao.commit()
        return True, "Filme adicionado com sucesso."
    except Error as e:
        conexao.rollback()
        return False, f"Erro de banco de dados ao criar filme: {e}"
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

def update_filme(old_num_filme, new_num_filme, new_nome, new_ano, new_duracao):
    if not new_nome or not new_nome.strip():
        return False, "O nome do filme não pode ser vazio."

    conexao = create_connection()
    if not conexao:
        return False, "Falha na conexão com o banco de dados."
        
    try:
        cursor = conexao.cursor()
        
        if old_num_filme != new_num_filme:
            cursor.execute("SELECT COUNT(*) FROM filme WHERE num_filme = %s", (new_num_filme,))
            if cursor.fetchone()[0] > 0:
                return False, f"O novo número de filme '{new_num_filme}' já está em uso."
        
        cursor.execute("SELECT COUNT(*) FROM filme WHERE nome = %s AND num_filme != %s", (new_nome.strip(), old_num_filme))
        if cursor.fetchone()[0] > 0:
            return False, f"O nome '{new_nome}' já está em uso por outro filme."
        cursor.execute("UPDATE elenco SET num_filme = %s WHERE num_filme = %s", (new_num_filme, old_num_filme))
        cursor.execute("UPDATE exibicao SET num_filme = %s WHERE num_filme = %s", (new_num_filme, old_num_filme))
            
        query = "UPDATE filme SET num_filme = %s, nome = %s, ano = %s, duracao = %s WHERE num_filme = %s"
        duracao_final = new_duracao if new_duracao and new_duracao > 0 else None
        ano_final = new_ano if new_ano and new_ano > 0 else None
        cursor.execute(query, (new_num_filme, new_nome.strip(), ano_final, duracao_final, old_num_filme))
        
        conexao.commit()
        return True, "Filme atualizado com sucesso."
    except Error as e:
        conexao.rollback()
        return False, f"Erro de banco de dados ao atualizar filme: {e}"
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

def delete_filme(num_filme):
    conexao = create_connection()
    if not conexao:
        return False, "Falha na conexão com o banco de dados."
        
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM elenco WHERE num_filme = %s", (num_filme,))
        cursor.execute("DELETE FROM exibicao WHERE num_filme = %s", (num_filme,))
        cursor.execute("DELETE FROM filme WHERE num_filme = %s", (num_filme,))
        
        conexao.commit()
        return True, "Filme e todos os seus registros associados foram deletados."
    except Error as e:
        conexao.rollback()
        return False, f"Erro de banco de dados ao deletar filme: {e}"
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
