import sqlite3
from tkinter import *
from tkinter import messagebox
import numpy as np
from scipy import stats
import pandas as pd  # Para gerar planilhas Excel

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


# Função para cadastrar clientes
def cadastrar_cliente(nome, telefone, pet):
    c.execute('INSERT INTO Clientes (nome, telefone, pet) VALUES (?, ?, ?)', (nome, telefone, pet))
    conn.commit()
    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")


# Função para remover clientes (pets)
def remover_cliente(cliente_id):
    c.execute('DELETE FROM Clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")


# Função para exibir pets cadastrados
def exibir_pets():
    c.execute('SELECT * FROM Clientes')
    pets = c.fetchall()
    pets_window = Toplevel()
    pets_window.title("Pets Registrados")
    Label(pets_window, text="Clientes e seus Pets").grid(row=0, column=0)

    for i, pet in enumerate(pets, start=1):
        Label(pets_window, text=f"ID: {pet[0]}, Nome: {pet[1]}, Pet: {pet[3]}").grid(row=i, column=0)

    # Campo para remover pet
    Label(pets_window, text="ID para remover:").grid(row=i + 1, column=0)
    id_remover = Entry(pets_window)
    id_remover.grid(row=i + 1, column=1)

    Button(pets_window, text="Remover", command=lambda: remover_cliente(id_remover.get())).grid(row=i + 2, column=1)


# Função para cadastro de vendas
def cadastrar_venda(cliente_id, produto_id, valor, data):
    c.execute('INSERT INTO Vendas (cliente_id, produto_id, valor, data) VALUES (?, ?, ?, ?)',
              (cliente_id, produto_id, valor, data))
    conn.commit()
    messagebox.showinfo("Sucesso", "Venda cadastrada com sucesso!")


# Função para gerar planilha Excel
def gerar_planilha():
    c.execute('SELECT * FROM Vendas')
    vendas = c.fetchall()

    if not vendas:
        messagebox.showinfo("Erro", "Nenhuma venda registrada para gerar a planilha")
        return

    # Cria dataframe e salva como Excel
    df = pd.DataFrame(vendas, columns=['ID', 'Cliente_ID', 'Produto_ID', 'Valor', 'Data'])
    df.to_excel('relatorio_vendas.xlsx', index=False)

    # Exibe sucesso
    messagebox.showinfo("Sucesso", "Planilha gerada com sucesso!")


# Função para previsão de receitas com base nas vendas passadas
def previsao_receitas():
    c.execute('SELECT valor FROM Vendas')
    vendas = c.fetchall()

    if len(vendas) < 7:
        messagebox.showinfo("Erro", "Dados insuficientes para previsão")
        return

    # Usa os valores de vendas passadas para prever a receita futura
    vendas_valores = np.array([v[0] for v in vendas])
    dias = np.arange(1, len(vendas_valores) + 1)

    slope, intercept, r_value, p_value, std_err = stats.linregress(dias, vendas_valores)
    receita_prevista = slope * (len(vendas_valores) + 1) + intercept

    previsao_window = Toplevel()
    previsao_window.title("Previsão de Receitas")

    Label(previsao_window, text=f"Receita prevista para o próximo período: R$ {receita_prevista:.2f}").grid(row=0,
                                                                                                            column=0)


# Função para análise de regressão linear baseada nas vendas
def analise_regressao_linear():
    c.execute('SELECT valor FROM Vendas')
    vendas = c.fetchall()

    if len(vendas) < 7:
        messagebox.showinfo("Erro", "Dados insuficientes para análise de regressão")
        return

    vendas_valores = np.array([v[0] for v in vendas])
    dias = np.arange(1, len(vendas_valores) + 1)

    slope, intercept, r_value, p_value, std_err = stats.linregress(dias, vendas_valores)
    predicao = slope * (len(vendas_valores) + 1) + intercept

    # Exibição na interface gráfica
    reg_window = Toplevel()
    reg_window.title("Análise de Regressão Linear")

    Label(reg_window, text="Previsão de vendas para o próximo dia:").grid(row=0, column=0)
    Label(reg_window, text=f"{predicao:.2f} vendas").grid(row=1, column=0)


# Interface gráfica para cadastro
def janela_cadastro_cliente():
    janela = Tk()
    janela.title("Cadastro de Clientes")

    Label(janela, text="Nome:").grid(row=0)
    Label(janela, text="Telefone:").grid(row=1)
    Label(janela, text="Pet:").grid(row=2)

    nome_entry = Entry(janela)
    telefone_entry = Entry(janela)
    pet_entry = Entry(janela)

    nome_entry.grid(row=0, column=1)
    telefone_entry.grid(row=1, column=1)
    pet_entry.grid(row=2, column=1)

    Button(janela, text="Cadastrar",
           command=lambda: cadastrar_cliente(nome_entry.get(), telefone_entry.get(), pet_entry.get())).grid(row=3,
                                                                                                            column=1)

    Button(janela, text="Exibir Pets Registrados", command=exibir_pets).grid(row=4, column=1)
    Button(janela, text="Análise de Regressão Linear", command=analise_regressao_linear).grid(row=5, column=1)
    Button(janela, text="Previsão de Receitas", command=previsao_receitas).grid(row=6, column=1)
    Button(janela, text="Gerar Planilha de Vendas", command=gerar_planilha).grid(row=7, column=1)

    # Campos para cadastro de vendas
    Label(janela, text="ID Cliente:").grid(row=8)
    Label(janela, text="ID Produto:").grid(row=9)
    Label(janela, text="Valor:").grid(row=10)
    Label(janela, text="Data (AAAA-MM-DD):").grid(row=11)

    cliente_id_entry = Entry(janela)
    produto_id_entry = Entry(janela)
    valor_entry = Entry(janela)
    data_entry = Entry(janela)

    cliente_id_entry.grid(row=8, column=1)
    produto_id_entry.grid(row=9, column=1)
    valor_entry.grid(row=10, column=1)
    data_entry.grid(row=11, column=1)

    Button(janela, text="Cadastrar Venda",
           command=lambda: cadastrar_venda(cliente_id_entry.get(), produto_id_entry.get(), valor_entry.get(),
                                           data_entry.get())).grid(row=12, column=1)

    janela.mainloop()


# Inicialização
if __name__ == "__main__":
    criar_tabelas()
    janela_cadastro_cliente()
