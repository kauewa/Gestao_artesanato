import sqlite3


banco = sqlite3.connect('dados.db')

c = banco.cursor()

# Crie a tabela Clientes
c.execute('''
    CREATE TABLE Clientes (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT,
        dt_nasc TEXT,
        email TEXT,
        endereco TEXT,
        telefone TEXT,
        CPF TEXT
    )
''')

# Crie a tabela Artesao
c.execute('''
    CREATE TABLE Artesao (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT,
        dt_nasc TEXT,
        email TEXT,
        telefone TEXT,
        CPF_CNPJ TEXT
    )
''')

# Crie a tabela Categoria
c.execute('''
    CREATE TABLE Categoria (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_categoria TEXT
    )
''')

# Crie a tabela Produtos
c.execute('''
    CREATE TABLE Produtos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome_produto TEXT,
        preco REAL,
        Artesao INTEGER,
        categoria INTEGER,
        descricao TEXT,
        FOREIGN KEY(Artesao) REFERENCES Artesao(ID),
        FOREIGN KEY(categoria) REFERENCES Categoria(ID)
    )
''')

c.execute('''
    CREATE TABLE produto_estoque (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        produto INTEGER,
        data TEXT,
        Quantidade INTEGER,
        FOREIGN KEY(produto) REFERENCES Produtos(ID)
    )
''')

c.execute('''
    CREATE TABLE produto_venda (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        produto INTEGER,
        venda INTEGER,
        Quantidade INTEGER,
        FOREIGN KEY(produto) REFERENCES Produtos(ID),
        FOREIGN KEY(venda) REFERENCES Vendas(ID)
    )
''')

# Crie a tabela Vendas
c.execute('''
    CREATE TABLE Vendas (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        artesao INTEGER,
        Forma_pagamento TEXT DEFAULT 'Dinheiro',
        Valor REAL,
        primeira_parcela REAL,
        parcelas REAL,
        Data TEXT,
        Cliente INTEGER,
        FOREIGN KEY(artesao) REFERENCES Artesao(ID),
        FOREIGN KEY(Cliente) REFERENCES Clientes(ID)
    )
''')


banco.commit()