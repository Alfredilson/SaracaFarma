-- Criação das tabelas principais do sistema SaracaFarma

CREATE TABLE Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    perfil TEXT CHECK(perfil IN ('admin','funcionario')) NOT NULL
);

CREATE TABLE Medicamento (
    id_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    fabricante TEXT,
    validade DATE,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL
);

CREATE TABLE Estoque (
    id_estoque INTEGER PRIMARY KEY AUTOINCREMENT,
    id_medicamento INTEGER NOT NULL,
    quantidade_atual INTEGER NOT NULL,
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento)
);

CREATE TABLE Venda (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    id_usuario INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_total REAL NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento)
);

CREATE TABLE Relatorio (
    id_relatorio INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT CHECK(tipo IN ('vendas','estoque')) NOT NULL,
    periodo TEXT,
    data_geracao DATE NOT NULL
);