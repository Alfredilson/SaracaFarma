# db.py
import sqlite3

# Cria uma conexão única para todo o sistema
conexao = sqlite3.connect("saracafarma.db", timeout=10, check_same_thread=False)
cursor = conexao.cursor()
