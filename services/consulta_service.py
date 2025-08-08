import streamlit as st
import pandas as pd
from db.connection import create_connection


def filmes_por_ator(nome_atores):
    conn = create_connection()
    if not conn or not nome_atores:
        return pd.DataFrame()
    placeholders = ','.join(['%s'] * len(nome_atores))
    query = f"""
        SELECT e.nome_ator_atriz, GROUP_CONCAT(f.nome SEPARATOR ', ') AS filmes
        FROM filme AS f
        INNER JOIN elenco AS e ON f.num_filme = e.num_filme
        WHERE e.nome_ator_atriz IN ({placeholders})
        GROUP BY e.nome_ator_atriz
        HAVING COUNT(f.num_filme) > 0
    """
    df = pd.read_sql(query, conn, params=nome_atores)
    conn.close()
    return df


def filmes_em_exibicao(filmes, data_inicio, data_fim):
    conn = create_connection()
    if not conn:
        return pd.DataFrame()
    placeholders = ','.join(['%s'] * len(filmes))
    query = f"""
        SELECT f.nome AS filme, 
               c.nome AS canal, 
               DATE_FORMAT(e.data_exibicao,"%d/%m/%Y") AS data, 
               TIME_FORMAT(e.hora_exibicao, "%H:%i") AS horário
        FROM filme AS f
        JOIN exibicao AS e ON f.num_filme = e.num_filme
        JOIN canal AS c ON e.num_canal = c.num_canal
        WHERE f.nome IN ({placeholders})
          AND e.data_exibicao BETWEEN DATE(%s) AND DATE(%s)
        ORDER BY e.data_exibicao, e.hora_exibicao
    """
    params = filmes + [data_inicio, data_fim]
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


def get_filmes_disponiveis():
    conn = create_connection()
    if not conn:
        return []
    query = "SELECT nome FROM filme"
    cursor = conn.cursor()
    cursor.execute(query)
    filmes = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return filmes


def get_atores_disponiveis():
    conn = create_connection()
    if not conn:
        return []
    query = "SELECT DISTINCT nome_ator_atriz FROM elenco"
    cursor = conn.cursor()
    cursor.execute(query)
    atores = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return atores


def get_limites_datas_exibicao():
    conn = create_connection()
    if not conn:
        return None, None
    query = "SELECT MIN(e.data_exibicao), MAX(e.data_exibicao) FROM exibicao AS e"
    cursor = conn.cursor()
    cursor.execute(query)
    min_data, max_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return min_data, max_data
