import sqlite3

# conecta ao banco
conn = sqlite3.connect("saracaFarma.db")
cursor = conn.cursor()

# insere usuários
cursor.execute("INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)",
               ("Administrador", "admin", "1234", "admin"))
cursor.execute("INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)",
               ("Funcionário João", "joao", "abcd", "funcionario"))

# insere medicamentos
cursor.execute("INSERT INTO Medicamento (nome, fabricante, validade, preco, quantidade) VALUES (?, ?, ?, ?, ?)",
               ("Paracetamol 500mg", "Farmaco SA", "2027-12-31", 5.50, 100))
cursor.execute("INSERT INTO Medicamento (nome, fabricante, validade, preco, quantidade) VALUES (?, ?, ?, ?, ?)",
               ("Amoxicilina 875mg", "Saúde Pharma", "2026-08-15", 12.00, 50))

# insere estoque inicial
cursor.execute("INSERT INTO Estoque (id_medicamento, quantidade_atual) VALUES (?, ?)", (1, 100))
cursor.execute("INSERT INTO Estoque (id_medicamento, quantidade_atual) VALUES (?, ?)", (2, 50))

conn.commit()
conn.close()

print("Dados de exemplo inseridos com sucesso!")
