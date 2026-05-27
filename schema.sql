-- Criação das tabelas principais do sistema SaracaFarma

CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    perfil TEXT CHECK(perfil IN ('admin','funcionario')) NOT NULL
);

CREATE TABLE IF NOT EXISTS Produto (
    codigo_barras TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    apresentacao TEXT,
    dosagem TEXT,
    fabricante TEXT
);

CREATE TABLE IF NOT EXISTS LoteProduto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_barras TEXT NOT NULL,
    lote TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    validade TEXT NOT NULL,
    preco REAL NOT NULL,
    FOREIGN KEY (codigo_barras) REFERENCES Produto(codigo_barras)
);


CREATE TABLE IF NOT EXISTS Venda (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    id_usuario INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_total REAL NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto)
);


CREATE TABLE IF NOT EXISTS Relatorio (
    id_relatorio INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT CHECK(tipo IN ('vendas','estoque')) NOT NULL,
    periodo TEXT,
    data_geracao DATE NOT NULL
);