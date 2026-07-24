import sqlite3
from db import conexao, cursor

# Executa schema para garantir tabelas
with open('schema.sql', 'r', encoding='utf-8') as f:
    schema = f.read()
cursor.executescript(schema)
conexao.commit()

# Insere usuário de teste
cursor.execute("SELECT id_usuario FROM Usuario WHERE login=?", ('test_user',))
row = cursor.fetchone()
if not row:
    cursor.execute("INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)", ('Teste', 'test_user', 'senha', 'funcionario'))
    conexao.commit()
    cursor.execute("SELECT id_usuario FROM Usuario WHERE login=?", ('test_user',))
    row = cursor.fetchone()
user_id = row[0]
print('user_id=', user_id)

# Insere produto e lote
codigo = 'TEST123'
cursor.execute("SELECT * FROM Produto WHERE codigo_barras=?", (codigo,))
if not cursor.fetchone():
    cursor.execute("INSERT INTO Produto (codigo_barras, nome, categoria) VALUES (?, ?, ?)", (codigo, 'Produto Teste', 'Medicamento'))

cursor.execute("SELECT * FROM LoteProduto WHERE codigo_barras=? AND lote=?", (codigo, 'L1'))
if not cursor.fetchone():
    cursor.execute("INSERT INTO LoteProduto (codigo_barras, lote, quantidade, validade, preco) VALUES (?, ?, ?, ?, ?)", (codigo, 'L1', 10, '2030-01-01', 5.0))

conexao.commit()

# Simula venda: decrementa estoque, cria Venda e ItensVenda
qtd_vendida = 2
cursor.execute("UPDATE LoteProduto SET quantidade = quantidade - ? WHERE codigo_barras = ? AND lote = ?", (qtd_vendida, codigo, 'L1'))

cursor.execute("INSERT INTO Venda (data, id_usuario, id_produto, quantidade, valor_total, forma_pagamento, id_cliente) VALUES (datetime('now'), ?, ?, ?, ?, ?, ?)", (user_id, codigo, qtd_vendida, qtd_vendida * 5.0, 'dinheiro', None))
vid = cursor.lastrowid
cursor.execute("INSERT INTO ItensVenda (id_venda, codigo_barras, lote, quantidade, preco_unitario, subtotal) VALUES (?, ?, ?, ?, ?, ?)", (vid, codigo, 'L1', qtd_vendida, 5.0, qtd_vendida * 5.0))

conexao.commit()

cursor.execute("SELECT quantidade FROM LoteProduto WHERE codigo_barras=? AND lote=?", (codigo, 'L1'))
restante = cursor.fetchone()[0]
print('Venda simulada. Estoque restante do lote L1:', restante)

print('OK')
