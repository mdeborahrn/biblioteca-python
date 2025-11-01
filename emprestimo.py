# Tela de Empréstimo e Devolução de Livros (não cria janelas no import)
import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar


def abrir_janela():
    """Abre a janela de empréstimo como Toplevel. Não usa mainloop()."""
    janela = tk.Toplevel()
    janela.title("Empréstimo e Devolução de Livros")
    janela.geometry("400x300")
    janela.grab_set()

    # Variáveis locais
    livro_var = tk.StringVar(master=janela)
    usuario_var = tk.StringVar(master=janela)
    livro_devolucao_var = tk.StringVar(master=janela)

    # Widgets
    ttk.Label(janela, text="Empréstimo de Livro").pack(pady=5)
    livro_combo = ttk.Combobox(janela, textvariable=livro_var)
    livro_combo.pack(pady=2)
    usuario_combo = ttk.Combobox(janela, textvariable=usuario_var)
    usuario_combo.pack(pady=2)
    ttk.Button(janela, text="Emprestar Livro", command=lambda: emprestar_livro()).pack(pady=5)

    ttk.Label(janela, text="Devolução de Livro").pack(pady=10)
    livro_devolucao_combo = ttk.Combobox(janela, textvariable=livro_devolucao_var)
    livro_devolucao_combo.pack(pady=2)
    ttk.Button(janela, text="Devolver Livro", command=lambda: devolver_livro()).pack(pady=5)

    # Funções internas que usam os widgets locais
    def carregar_livros_disponiveis():
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT TITULO FROM livros WHERE EMPRESTADO_PARA IS NULL")
        livros = [row[0] for row in cursor.fetchall()]
        conn.close()
        livro_combo['values'] = livros

    def carregar_usuarios():
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT matricula, nome FROM usuarios")
        rows = cursor.fetchall()
        conn.close()
        usuarios_display = [f"{r[0]} - {r[1]}" for r in rows]
        usuario_combo['values'] = usuarios_display

    def carregar_livros_emprestados():
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT TITULO FROM livros WHERE EMPRESTADO_PARA IS NOT NULL")
        livros = [row[0] for row in cursor.fetchall()]
        conn.close()
        livro_devolucao_combo['values'] = livros

    def emprestar_livro():
        titulo = livro_var.get()
        usuario_info = usuario_var.get()
        if not titulo or not usuario_info:
            messagebox.showerror("Erro", "Selecione um livro e um usuário.")
            return
        matricula = usuario_info.split(" - ")[0]
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE livros SET EMPRESTADO_PARA = ? WHERE TITULO = ?", (matricula, titulo))
        conn.commit()
        conn.close()
        carregar_livros_disponiveis()
        carregar_livros_emprestados()
        messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso.")

    def devolver_livro():
        titulo = livro_devolucao_var.get()
        if not titulo:
            messagebox.showerror("Erro", "Selecione um livro para devolução.")
            return
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE livros SET EMPRESTADO_PARA = NULL WHERE TITULO = ?", (titulo,))
        conn.commit()
        conn.close()
        carregar_livros_disponiveis()
        carregar_livros_emprestados()
        messagebox.showinfo("Sucesso", "Devolução realizada com sucesso.")

    # Carregar dados iniciais
    carregar_livros_disponiveis()
    carregar_usuarios()
    carregar_livros_emprestados()

