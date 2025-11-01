import tkinter as tk
import csv
from tkinter import ttk, filedialog, messagebox
from banco import conectar


def abrir_janela():
    """Abre a janela principal de interface (Toplevel). Não chama mainloop()."""
    janela = tk.Toplevel()
    janela.title("Sistema de Biblioteca")
    janela.geometry("800x400")

    notebook = ttk.Notebook(janela)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Abas
    aba_livro = ttk.Frame(notebook)
    aba_usuario = ttk.Frame(notebook)
    notebook.add(aba_livro, text='Cadastrar Livro')
    notebook.add(aba_usuario, text='Cadastrar Usuário')

    # Variáveis
    titulo_var = tk.StringVar(master=janela)
    autor_var = tk.StringVar(master=janela)
    ano_var = tk.StringVar(master=janela)
    categoria_var = tk.StringVar(master=janela)
    matricula_var = tk.StringVar(master=janela)
    nome_var = tk.StringVar(master=janela)

    # Treeviews locais
    colunas = ('Título', 'Autor', 'Ano de Publicação', 'Categoria', 'Emprestado Para')
    tree = ttk.Treeview(aba_livro, columns=colunas, show='headings')
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    colunas_usuarios = ('Matrícula/ID', 'Nome')
    tree_usuarios = ttk.Treeview(aba_usuario, columns=colunas_usuarios, show='headings')
    for col in colunas_usuarios:
        tree_usuarios.heading(col, text=col)
        tree_usuarios.column(col, width=200)
    tree_usuarios.pack(fill=tk.BOTH, expand=True)

    # Funções que operam sobre widgets locais
    def listar_livros():
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT TITULO, AUTOR, ANO_PUBLICACAO, CATEGORIA, EMPRESTADO_PARA FROM livros")
        livros = cursor.fetchall()
        conn.close()

        for row in tree.get_children():
            tree.delete(row)
        for livro in livros:
            tree.insert('', 'end', values=livro)

    def cadastrar_livro():
        if not titulo_var.get() or not autor_var.get() or not ano_var.get() or not categoria_var.get():
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM livros WHERE TITULO = ?', (titulo_var.get(),))
        if cursor.fetchone():
            messagebox.showerror("Erro", f"O livro '{titulo_var.get()}' já está cadastrado.")
            conn.close()
            return
        cursor.execute("INSERT INTO livros (TITULO, AUTOR, ANO_PUBLICACAO, CATEGORIA) VALUES (?, ?, ?, ?)",
                       (titulo_var.get(), autor_var.get(), ano_var.get(), categoria_var.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", f"Livro '{titulo_var.get()}' cadastrado com sucesso!")
        titulo_var.set('')
        autor_var.set('')
        ano_var.set('')
        categoria_var.set('')

    def cadastrar_usuario():
        if not nome_var.get() or not matricula_var.get():
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM usuarios WHERE matricula = ?', (matricula_var.get(),))
        if cursor.fetchone():
            messagebox.showerror("Erro", f"O usuário com matrícula '{matricula_var.get()}' já está cadastrado.")
            conn.close()
            return
        cursor.execute("INSERT INTO usuarios (matricula, nome) VALUES (?, ?)", (matricula_var.get(), nome_var.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", f"Usuário '{nome_var.get()}' cadastrado com sucesso!")
        nome_var.set('')
        matricula_var.set('')

    def listar_usuarios():
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT matricula, nome FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()

        for row in tree_usuarios.get_children():
            tree_usuarios.delete(row)
        for usuario in usuarios:
            tree_usuarios.insert('', 'end', values=usuario)

    def exportar_csv():
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not filepath:
            return
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT TITULO, AUTOR, ANO_PUBLICACAO, CATEGORIA, EMPRESTADO_PARA FROM livros")
        livros = cursor.fetchall()
        conn.close()
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            escritor = csv.writer(file)
            escritor.writerow(['Título', 'Autor', 'Ano de Publicação', 'Categoria', 'Emprestado Para'])
            for livro in livros:
                escritor.writerow(livro)

    # Formulário de Livro (aba_livro top)
    frm_livro = ttk.Frame(aba_livro)
    frm_livro.pack(fill='x', padx=10, pady=5)
    ttk.Label(frm_livro, text="Título:").grid(row=0, column=0, sticky='w')
    ttk.Entry(frm_livro, textvariable=titulo_var).grid(row=0, column=1, sticky='ew')
    ttk.Label(frm_livro, text="Autor:").grid(row=1, column=0, sticky='w')
    ttk.Entry(frm_livro, textvariable=autor_var).grid(row=1, column=1, sticky='ew')
    ttk.Label(frm_livro, text="Ano de Publicação:").grid(row=2, column=0, sticky='w')
    ttk.Entry(frm_livro, textvariable=ano_var).grid(row=2, column=1, sticky='ew')
    ttk.Label(frm_livro, text="Categoria:").grid(row=3, column=0, sticky='w')
    ttk.Entry(frm_livro, textvariable=categoria_var).grid(row=3, column=1, sticky='ew')
    ttk.Button(frm_livro, text="Cadastrar Livro", command=cadastrar_livro).grid(row=4, column=0, columnspan=2, pady=8)
    frm_livro.columnconfigure(1, weight=1)

    btn_listar = tk.Button(aba_livro, text="Listar Livros", command=listar_livros)
    btn_listar.pack(pady=5)
    btn_exportar = tk.Button(aba_livro, text="Exportar CSV", command=exportar_csv)
    btn_exportar.pack(pady=5)

    # Formulário de Usuário (aba_usuario)
    frm_usuario = ttk.Frame(aba_usuario)
    frm_usuario.pack(fill='x', padx=10, pady=5)
    ttk.Label(frm_usuario, text="Nome:").grid(row=0, column=0, sticky='w')
    ttk.Entry(frm_usuario, textvariable=nome_var).grid(row=0, column=1, sticky='ew')
    ttk.Label(frm_usuario, text="Matrícula/ID:").grid(row=1, column=0, sticky='w')
    ttk.Entry(frm_usuario, textvariable=matricula_var).grid(row=1, column=1, sticky='ew')
    ttk.Button(frm_usuario, text="Cadastrar Usuário", command=cadastrar_usuario).grid(row=2, column=0, columnspan=2, pady=8)
    frm_usuario.columnconfigure(1, weight=1)

    btn_listar_usuarios = tk.Button(aba_usuario, text="Listar Usuários", command=listar_usuarios)
    btn_listar_usuarios.pack(pady=5)
