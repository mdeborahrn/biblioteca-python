# Tela Principal do Sistema de Biblioteca
import tkinter as tk
from tkinter import messagebox
import cadastro, emprestimo, interface

def abrir_cadastro():
    cadastro.abrir_janela()

def abrir_emprestimo():
    emprestimo.abrir_janela()

def abrir_listagem():
    interface.abrir_janela()

def sair():
    resposta = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
    if resposta:
        janela.quit()

# Janela Principal
janela = tk.Tk()
janela.title("Sistema de Biblioteca")
janela.geometry("400x200")

#Menu de opções
menu_barra = tk.Menu(janela)

menu_arquivo = tk.Menu(menu_barra, tearoff=0)
menu_arquivo.add_command(label="Cadastrar", command=abrir_cadastro)
menu_arquivo.add_command(label="Empréstimo/Devolução", command=abrir_emprestimo)
menu_arquivo.add_command(label="Listar/Exportar", command=abrir_listagem)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=sair)

menu_barra.add_cascade(label="Menu", menu=menu_arquivo)
janela.config(menu=menu_barra)

# Mensagem de boas-vindas
label_boas_vindas = tk.Label(janela, text="Bem-vindo ao Sistema de Biblioteca!", font=("Arial", 14))
label_boas_vindas.pack(pady=40)

janela.mainloop()