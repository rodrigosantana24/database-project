import pandas as pd
import streamlit as st
from db.connection import conectar
from mysql.connector import Error

def read_elenco():
    conexao = conectar()
    if conexao:
        try:
            query = "SELECT num_filme, nome_ator_atriz, protagonista FROM elenco ORDER BY num_filme, nome_ator_atriz"
            df = pd.read_sql(query, conexao)
            return df
        except Error as e:
            st.error(f"Erro ao buscar elencos: {e}")
            return pd.DataFrame()
        finally:
            if conexao.is_connected():
                conexao.close()
    return pd.DataFrame()

def check_filme_exists(num_filme):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            query = "SELECT COUNT(*) FROM filme WHERE num_filme = %s"
            cursor.execute(query, (num_filme,))
            if cursor.fetchone()[0] > 0:
                return True
            return False
        except Error as e:
            st.error(f"Erro ao verificar a existência do filme: {e}")
            return False
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
    return False

def create_elenco(num_filme, nome_ator_atriz, protagonista):
    if not nome_ator_atriz or not nome_ator_atriz.strip():
        return False, "O nome do ator/atriz é obrigatório."
        
    conexao = conectar()
    if not conexao:
        return False, "Falha na conexão com o banco de dados."
    
    try:
        cursor = conexao.cursor()
        
        if not check_filme_exists(num_filme):
            return False, f"O filme com número '{num_filme}' não foi encontrado."

        query_check = "SELECT COUNT(*) FROM elenco WHERE num_filme = %s AND nome_ator_atriz = %s"
        cursor.execute(query_check, (num_filme, nome_ator_atriz))
        if cursor.fetchone()[0] > 0:
            return False, f"O ator/atriz '{nome_ator_atriz}' já está no elenco do filme {num_filme}."

        protagonista_int = 1 if protagonista else 0
        
        query_insert = "INSERT INTO elenco (num_filme, nome_ator_atriz, protagonista) VALUES (%s, %s, %s)"
        cursor.execute(query_insert, (num_filme, nome_ator_atriz.strip(), protagonista_int))
        
        conexao.commit()
        return True, "Registro de elenco criado com sucesso."
    except Error as e:
        conexao.rollback()
        return False, f"Erro do banco de dados ao criar registro: {e}"
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

def update_elenco(old_num_filme, old_nome_ator, new_num_filme, new_nome_ator, new_protagonista):
    if not new_nome_ator or not new_nome_ator.strip():
        return False, "O nome do ator/atriz é obrigatório."

    conexao = conectar()
    if not conexao:
        return False, "Falha na conexão com o banco de dados."
    
    try:
        cursor = conexao.cursor()

        if not check_filme_exists(new_num_filme):
            return False, f"O novo filme com número '{new_num_filme}' não existe."

        if (old_num_filme, old_nome_ator) != (new_num_filme, new_nome_ator.strip()):
            query_check = "SELECT COUNT(*) FROM elenco WHERE num_filme = %s AND nome_ator_atriz = %s"
            cursor.execute(query_check, (new_num_filme, new_nome_ator.strip()))
            if cursor.fetchone()[0] > 0:
                return False, f"Já existe um registro para o ator '{new_nome_ator}' no filme '{new_num_filme}'."

        protagonista_int = 1 if new_protagonista else 0
        
        query_update = """
            UPDATE elenco 
            SET num_filme = %s, nome_ator_atriz = %s, protagonista = %s 
            WHERE num_filme = %s AND nome_ator_atriz = %s
        """
        cursor.execute(query_update, (new_num_filme, new_nome_ator.strip(), protagonista_int, old_num_filme, old_nome_ator))
        
        conexao.commit()
        return True, "Elenco atualizado com sucesso."
    except Error as e:
        conexao.rollback()
        return False, f"Erro do banco de dados ao atualizar elenco: {e}"
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

def delete_elenco(num_filme, nome_ator_atriz):
    conexao = conectar()
    if not conexao:
        return False, "Falha na conexão com o banco de dados."
    try:
        cursor = conexao.cursor()
        query = "DELETE FROM elenco WHERE num_filme = %s AND nome_ator_atriz = %s"
        cursor.execute(query, (num_filme, nome_ator_atriz))
        conexao.commit()
        if cursor.rowcount > 0:
            return True, "Registro removido do elenco com sucesso."
        else:
            return False, "Nenhum registro encontrado para deletar."
    except Error as e:
        conexao.rollback()
        return False, f"Erro do banco de dados ao remover do elenco: {e}"
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
