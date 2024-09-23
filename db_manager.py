import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect('belo_pets.db')
c = conn.cursor()

# Criação das tabelas
def criar_tabelas():
    c.execute('''CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                pet TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                produto_id INTEGER,
                valor REAL,
                data TEXT,
                FOREIGN KEY(cliente_id) REFERENCES Clientes(id),
                FOREIGN KEY(produto_id) REFERENCES Produtos(id))''')
    conn.commit()

# Função para cadastrar cliente
def cadastrar_cliente(nome, telefone, pet):
    c.execute('INSERT INTO Clientes (nome, telefone, pet) VALUES (?, ?, ?)', (nome, telefone, pet))
    conn.commit()

# Função para remover cliente (pet)
def remover_cliente(cliente_id):
    c.execute('DELETE FROM Clientes WHERE id = ?', (cliente_id,))
    conn.commit()

# Função para listar pets
def listar_pets():
    c.execute('SELECT * FROM Clientes')
    return c.fetchall()

# Função para cadastrar venda
def cadastrar_venda(cliente_id, produto_id, valor, data):
    c.execute('INSERT INTO Vendas (cliente_id, produto_id, valor, data) VALUES (?, ?, ?, ?)', (cliente_id, produto_id, valor, data))
    conn.commit()

# Função para listar vendas
def listar_vendas():
    c.execute('SELECT * FROM Vendas')
    return c.fetchall()

# Fechamento da conexão com o banco de dados
def fechar_conexao():
    conn.close()

def listar_clientes():
    c.execute('SELECT * FROM Clientes')
    return c.fetchall()  # Retorna todos os registros da tabela Clientes

def fechar_conexao():
    conn.close()