from db.connection import conectar

def listar_filmes():
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM filme")
        filmes = cursor.fetchall()
        cursor.close()
        conexao.close()
        return filmes
    return []