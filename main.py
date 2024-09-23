from tkinter import *
from tkinter import messagebox
import numpy as np
from scipy import stats
import pandas as pd  # Para gerar planilhas Excel
import db_manager  # Importa as funções do banco de dados


# Função para exibir pets cadastrados
def exibir_pets():
    pets = db_manager.listar_pets()
    pets_window = Toplevel()
    pets_window.title("Pets Registrados")
    Label(pets_window, text="Clientes e seus Pets", width=50, bg='#d1d0e0').grid(row=0, column=0)
    pets_window.geometry('700x500')
    pets_window.configure(bg='#d1d0e0')


    for i, pet in enumerate(pets, start=1):
        Label(pets_window, text=f"ID: {pet[0]}, Nome: {pet[1]}, Pet: {pet[3]}", bg='#d1d0e0').grid(row=i, column=0)

    # Campo para remover pet
    Label(pets_window, text="ID para remover:", bg='#d1d0e0', width=50).grid(row=i + 1, column=0)
    id_remover = Entry(pets_window, width=40)
    id_remover.grid(row=i + 1, column=1)

    Button(pets_window, text="Remover", bg='#ea5e76', command=lambda: remover_cliente(id_remover.get())).grid(row=i + 2, column=1)


# Função para remover clientes (pets)
def remover_cliente(cliente_id):
    db_manager.remover_cliente(cliente_id)
    messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")  # Notificação ao excluir


# Função para gerar planilha Excel
def gerar_planilha():
    vendas = db_manager.listar_vendas()

    if not vendas:
        messagebox.showinfo("Erro", "Nenhuma venda registrada para gerar a planilha")
        return

    # Cria dataframe e salva como Excel
    df = pd.DataFrame(vendas, columns=['ID', 'Cliente_ID', 'Produto_ID', 'Valor', 'Data'])
    df.to_excel('relatorio_vendas.xlsx', index=False)

    # Exibe sucesso
    messagebox.showinfo("Sucesso", "Planilha gerada com sucesso!")  # Notificação ao gerar planilha


# Função para previsão de receitas com base nas vendas passadas
def previsao_receitas():
    vendas = db_manager.listar_vendas()

    if len(vendas) < 7:
        messagebox.showinfo("Erro", "Dados insuficientes para previsão")
        return

    # Usa os valores de vendas passadas para prever a receita futura
    vendas_valores = np.array([v[3] for v in vendas])
    dias = np.arange(1, len(vendas_valores) + 1)

    slope, intercept, r_value, p_value, std_err = stats.linregress(dias, vendas_valores)
    receita_prevista = slope * (len(vendas_valores) + 1) + intercept

    previsao_window = Toplevel()
    previsao_window.title("Previsão de Receitas")

    Label(previsao_window, text=f"Receita prevista para o próximo período: R$ {receita_prevista:.2f}").grid(row=0,
                                                                                                            column=0)


# Função para análise de regressão linear baseada nas vendas
def analise_regressao_linear():
    vendas = db_manager.listar_vendas()

    if len(vendas) < 7:
        messagebox.showinfo("Erro", "Dados insuficientes para análise de regressão")
        return

    vendas_valores = np.array([v[3] for v in vendas])
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
    janela.geometry('800x700')
    janela.configure(bg='lightblue')

    Label(janela, text="Nome:", bg='lightblue').grid(row=0, pady=5)
    Label(janela, text="Telefone:", bg='lightblue').grid(row=1, pady=5)
    Label(janela, text="Pet:", bg='lightblue').grid(row=2, pady=5)

    nome_entry = Entry(janela, width=80)
    telefone_entry = Entry(janela,  width=80)
    pet_entry = Entry(janela,  width=80)

    nome_entry.grid(row=0, column=1)
    telefone_entry.grid(row=1, column=1)
    pet_entry.grid(row=2, column=1)

    # Lista de produtos
    produtos = {
        1: "1 - Banho e Tosa",
        2: "2 - Banho",
        3: "3 - Tosa",
        4: "4 - Cuidados Pet",
        5: "5 - Outros",
        6: '       '
    }

    # Variável para armazenar o produto selecionado
    produto_selecionado = StringVar(janela)
    produto_selecionado.set("Selecione um produto")  # Valor padrão

    OptionMenu(janela, produto_selecionado, *produtos.values()).grid(row=9, column=3, pady=5, padx=10)

    Button(janela, text="Cadastrar",
           command=lambda: cadastrar_cliente(nome_entry.get(), telefone_entry.get(), pet_entry.get())).grid(row=3,
                                                                                                            column=1,
                                                                                                            pady=5)
    Button(janela, text="Registrar pet", width=30, bg='#d0f3e1',
           command=lambda: cadastrar_cliente(nome_entry.get(), telefone_entry.get(), pet_entry.get())).grid(row=3,
                                                                                                            column=1, pady=5, padx=0)

    Button(janela, text="Exibir Pets Registrados",bg='#fff0cf', command=exibir_pets, width=30).grid(row=4, column=1, pady=5, padx=0)
    Button(janela, text="Previsão de Vendas", bg='#ceddf2', command=analise_regressao_linear, width=30).grid(row=5, column=1, pady=5, padx=0)
    Button(janela, text="Previsão de Receitas", bg='#ffe2f2', command=previsao_receitas, width=30).grid(row=6, column=1, pady=5, padx=0)
    Button(janela, text="Gerar Planilha de Vendas", bg='#d2d8d8', command=gerar_planilha, width=30).grid(row=7, column=1, pady=5, padx=0)

    # Campos para cadastro de vendas
    Label(janela, text="ID Cliente:", bg='lightblue').grid(row=8, pady=0)
    Label(janela, text="ID Produto:", bg='lightblue').grid(row=9, pady=0)
    Label(janela, text="Valor:", bg='lightblue').grid(row=10, pady=5)
    Label(janela, text="Data (AAAA-MM-DD):", bg='lightblue').grid(row=11, pady=5)

    cliente_id_entry = Entry(janela, width=80)
    produto_id_entry = Entry(janela, width=80)
    valor_entry = Entry(janela, width=80)
    data_entry = Entry(janela, width=80)

    cliente_id_entry.grid(row=8, column=1)
    produto_id_entry.grid(row=9, column=1)
    valor_entry.grid(row=10, column=1)
    data_entry.grid(row=11, column=1)

    Button(janela, text="Registrar Venda", width=30, bg='#d0f3e1',
           command=lambda: cadastrar_venda(cliente_id_entry.get(), produto_id_entry.get(), valor_entry.get(),
                                           data_entry.get())).grid(row=12, column=1, pady=5, padx=0)

    janela.mainloop()


# Função para cadastrar cliente com notificação
def cadastrar_cliente(nome, telefone, pet):
    db_manager.cadastrar_cliente(nome, telefone, pet)
    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")  # Notificação ao cadastrar cliente


# Função para cadastrar venda com notificação
def cadastrar_venda(cliente_id, produto_id, valor, data):
    db_manager.cadastrar_venda(cliente_id, produto_id, valor, data)
    messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")  # Notificação ao cadastrar venda


# Inicialização
if __name__ == "__main__":
    db_manager.criar_tabelas()
    janela_cadastro_cliente()
