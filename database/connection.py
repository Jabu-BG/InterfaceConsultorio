import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

def get_connection():
    conexao = sqlite3.connect(DB_PATH, check_same_thread=False)
    conexao.row_factory = sqlite3.Row
    return conexao