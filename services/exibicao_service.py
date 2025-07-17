import pandas as pd
import streamlit as st
import datetime
from db.connection import conectar
from mysql.connector import Error

def _filme_existe(cursor, num_filme):
    cursor.execute("SELECT COUNT(*) FROM filme WHERE num_filme = %s", (num_filme,))
    return cursor.fetchone()[0] > 0

def _canal_existe(cursor, num_canal):
    cursor.execute("SELECT COUNT(*) FROM canal WHERE num_canal = %s", (num_canal,))
    return cursor.fetchone()[0] > 0

def _exibicao_existe(cursor, num_filme, num_canal, data, hora):
    query = """
        SELECT COUNT(*) 
        FROM exibicao 
        WHERE num_filme = %s AND num_canal = %s AND data_exibicao = %s AND hora_exibicao = %s
    """
    cursor.execute(query, (num_filme, num_canal, data, hora))
    return cursor.fetchone()[0] > 0

def _verificar_conflito_de_horario(cursor, num_filme_novo, num_canal, data, hora, ignorar_exibicao=None):
    cursor.execute("SELECT duracao FROM filme WHERE num_filme = %s", (num_filme_novo,))
    resultado = cursor.fetchone()
    if not resultado or not resultado[0] or resultado[0] <= 0:
        return False, "O filme a ser agendado não possui uma duração válida cadastrada."
    duracao_novo_filme = resultado[0]

    inicio_novo = datetime.datetime.combine(data, hora)
    fim_novo = inicio_novo + datetime.timedelta(minutes=duracao_novo_filme)

    query = """
        SELECT e.num_filme, e.data_exibicao, e.hora_exibicao, f.duracao, f.nome AS nome_filme_existente
        FROM exibicao e
        JOIN filme f ON e.num_filme = f.num_filme
        WHERE e.num_canal = %s AND e.data_exibicao = %s
    """
    cursor.execute(query, (num_canal, data))
    exibicoes_existentes = cursor.fetchall()

    for num_filme_existente, data_existente, hora_existente_td, duracao_existente, nome_filme_existente in exibicoes_existentes:
        if ignorar_exibicao and (num_filme_existente, data_existente.strftime('%Y-%m-%d'), (datetime.datetime.min + hora_existente_td).time()) == ignorar_exibicao:
            continue

        if not duracao_existente or duracao_existente <= 0:
            continue

        hora_existente_time = (datetime.datetime.min + hora_existente_td).time()
        inicio_existente = datetime.datetime.combine(data, hora_existente_time)
        fim_existente = inicio_existente + datetime.timedelta(minutes=duracao_existente)

        if inicio_novo < fim_existente and inicio_existente < fim_novo:
            msg_erro = (
                f"Conflito: Sobrepõe o filme '{nome_filme_existente}' "
                f"({inicio_existente.strftime('%H:%M')} - {fim_existente.strftime('%H:%M')})."
            )
            return False, msg_erro

    return True, None

def read_exibicoes():
    try:
        conexao = conectar()
        if not conexao:
            st.error("Falha na conexão com o banco de dados.")
            return pd.DataFrame()
        
        query = """
            SELECT num_filme, num_canal, data_exibicao, hora_exibicao
            FROM exibicao
            ORDER BY num_filme ASC, data_exibicao DESC, hora_exibicao DESC
        """
        return pd.read_sql(query, conexao, parse_dates=['data_exibicao'])
    except Error as e:
        st.error(f"Erro ao ler exibições: {e}")
        return pd.DataFrame()
    finally:
        if 'conexao' in locals() and conexao and conexao.is_connected():
            conexao.close()

def create_exibicao(num_filme, num_canal, data, hora):
    conexao = None
    try:
        conexao = conectar()
        if not conexao: return False, "Falha na conexão com o banco de dados."

        with conexao.cursor() as cursor:
            if not _filme_existe(cursor, num_filme): return False, f"Filme com ID {num_filme} não encontrado."
            if not _canal_existe(cursor, num_canal): return False, f"Canal com ID {num_canal} não encontrado."
            if _exibicao_existe(cursor, num_filme, num_canal, data, hora): return False, "Essa exibição já está cadastrada."

            horario_valido, msg_erro = _verificar_conflito_de_horario(cursor, num_filme, num_canal, data, hora)
            if not horario_valido: return False, msg_erro 

            cursor.execute(
                "INSERT INTO exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) VALUES (%s, %s, %s, %s)",
                (num_filme, num_canal, data, hora)
            )
        
        conexao.commit()
        return True, "Exibição agendada com sucesso."
    except Error as e:
        if conexao: conexao.rollback()
        return False, f"Erro de banco de dados: {e}"
    finally:
        if conexao and conexao.is_connected(): conexao.close()

def update_exibicao(old_num_filme, old_num_canal, old_data, old_hora, 
                    new_num_filme, new_num_canal, new_data, new_hora):
    conexao = None
    try:
        conexao = conectar()
        if not conexao: return False, "Falha na conexão com o banco de dados."

        with conexao.cursor() as cursor:
            keys_changed = (old_num_filme != new_num_filme or old_num_canal != new_num_canal or 
                            old_data != new_data or old_hora != new_hora)
            if not keys_changed: return True, "Nenhuma alteração detectada."

            if not _filme_existe(cursor, new_num_filme): return False, f"Novo ID de filme {new_num_filme} não encontrado."
            if not _canal_existe(cursor, new_num_canal): return False, f"Novo ID de canal {new_num_canal} não encontrado."
            
            if _exibicao_existe(cursor, new_num_filme, new_num_canal, new_data, new_hora):
                return False, "Já existe uma exibição cadastrada para a nova combinação de filme, canal, data e hora."

            exibicao_a_ignorar = (old_num_filme, old_data.strftime('%Y-%m-%d'), old_hora)
            horario_valido, msg_erro = _verificar_conflito_de_horario(
                cursor, new_num_filme, new_num_canal, new_data, new_hora, ignorar_exibicao=exibicao_a_ignorar
            )
            if not horario_valido: return False, msg_erro

            query = """
                UPDATE exibicao 
                SET num_filme = %s, num_canal = %s, data_exibicao = %s, hora_exibicao = %s 
                WHERE num_filme = %s AND num_canal = %s AND data_exibicao = %s AND hora_exibicao = %s
            """
            params = (new_num_filme, new_num_canal, new_data, new_hora, 
                      old_num_filme, old_num_canal, old_data, old_hora)
            cursor.execute(query, params)
        
        conexao.commit()
        return True, "Agendamento atualizado com sucesso."
    except Error as e:
        if conexao: conexao.rollback()
        return False, f"Erro de banco de dados: {e}"
    finally:
        if conexao and conexao.is_connected(): conexao.close()

def delete_exibicao(num_filme, num_canal, data, hora):
    """Deleta uma exibição do banco de dados."""
    conexao = None
    try:
        conexao = conectar()
        if not conexao: return False, "Falha na conexão com o banco de dados."

        with conexao.cursor() as cursor:
            cursor.execute(
                "DELETE FROM exibicao WHERE num_filme = %s AND num_canal = %s AND data_exibicao = %s AND hora_exibicao = %s",
                (num_filme, num_canal, data, hora)
            )
        conexao.commit()
        return True, "Agendamento removido com sucesso."
    except Error as e:
        if conexao: conexao.rollback()
        return False, f"Erro de banco de dados: {e}"
    finally:
        if conexao and conexao.is_connected(): conexao.close()