# Cadastro de Livros e Usuários
import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar

def cadastrar_livro():
    conn = conectar('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO livros (titulo, autor, ano_publicacao, categoria)
        VALUES (?, ?, ?, ?)
    """, (titulo_var.get(), autor_var.get(), ano_var.get(), categoria_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", f"Livro '{titulo_var.get()}' cadastrado!")
    limpar_campos_livro()

def cadastrar_usuario():
    conn = conectar('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (matricula, nome)
        VALUES (?, ?)
    """, (matricula_var.get(), nome_usuario_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", f"Usuário '{nome_usuario_var.get()}' cadastrado!")
    limpar_campos_usuario()

def limpar_campos_livro():
    titulo_var.set("")
    autor_var.set("")
    ano_var.set("")
    categoria_var.set("")

def limpar_campos_usuario():
    nome_usuario_var.set("")
    matricula_var.set("")

# Função para abrir janela de cadastro
def abrir_janela():
    # Torna as variáveis acessíveis para as funções de callback
    global titulo_var, autor_var, ano_var, categoria_var, nome_usuario_var, matricula_var

    # Janela de cadastro como Toplevel
    janela = tk.Toplevel()
    janela.title("Cadastro de Biblioteca")
    janela.geometry("400x300")
    janela.grab_set()  # Torna a janela modal

    notebook = ttk.Notebook(janela)
    notebook.pack(fill="both", expand=True)

    # Abas
    aba_livro = ttk.Frame(notebook)
    aba_usuario = ttk.Frame(notebook)
    notebook.add(aba_livro, text="Cadastrar Livro")
    notebook.add(aba_usuario, text="Cadastrar Usuário")

    # Variáveis (associadas à janela pai)
    titulo_var = tk.StringVar(master=janela)
    autor_var = tk.StringVar(master=janela)
    ano_var = tk.StringVar(master=janela)
    categoria_var = tk.StringVar(master=janela)
    nome_usuario_var = tk.StringVar(master=janela)
    matricula_var = tk.StringVar(master=janela)

    # Formulário de Livro
    ttk.Label(aba_livro, text="Título:").pack()
    ttk.Entry(aba_livro, textvariable=titulo_var).pack()
    ttk.Label(aba_livro, text="Autor:").pack()
    ttk.Entry(aba_livro, textvariable=autor_var).pack()
    ttk.Label(aba_livro, text="Ano:").pack()
    ttk.Entry(aba_livro, textvariable=ano_var).pack()
    ttk.Label(aba_livro, text="Categoria:").pack()
    ttk.Entry(aba_livro, textvariable=categoria_var).pack()
    ttk.Button(aba_livro, text="Cadastrar Livro", command=cadastrar_livro).pack(pady=10)

    # Formulário de Usuário
    ttk.Label(aba_usuario, text="Nome:").pack()
    ttk.Entry(aba_usuario, textvariable=nome_usuario_var).pack()
    ttk.Label(aba_usuario, text="Matrícula:").pack()
    ttk.Entry(aba_usuario, textvariable=matricula_var).pack()
    ttk.Button(aba_usuario, text="Cadastrar Usuário", command=cadastrar_usuario).pack(pady=10)
