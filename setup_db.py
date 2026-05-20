import sqlite3

# cria ou abre o banco
conn = sqlite3.connect("saracaFarma.db")
cursor = conn.cursor()

# lê o script SQL
with open("schema.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# executa o script
cursor.executescript(sql_script)

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")

