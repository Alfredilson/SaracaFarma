import sqlite3

# conecta ao banco
conn = sqlite3.connect("saracaFarma.db")
cursor = conn.cursor()

print("=== Usuários ===")
for row in cursor.execute("SELECT id_usuario, nome, login, perfil FROM Usuario"):
    print(row)

print("\n=== Medicamentos ===")
for row in cursor.execute("SELECT id_medicamento, nome, fabricante, validade, preco, quantidade FROM Medicamento"):
    print(row)

print("\n=== Estoque ===")
for row in cursor.execute("SELECT id_estoque, id_medicamento, quantidade_atual FROM Estoque"):
    print(row)

conn.close()
