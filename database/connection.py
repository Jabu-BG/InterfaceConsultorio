import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

SQL_CRIAR_TABELAS = """
"""

SQL_DADOS_INICIAIS = """
"""

def get_connection():
    conexao = sqlite3.connect(DB_PATH, check_same_thread=False)
    conexao.row_factory = sqlite3.Row
    return conexao

def inicializar_banco():
    print("[DB] Inicializando banco de dados...")

    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.executescript(SQL_CRIAR_TABELAS)
    cursor.executescript(SQL_DADOS_INICIAIS)

    conexao.commit()

    print("[DB] Tabelas criadas e banco pronto!")

    conexao.close()