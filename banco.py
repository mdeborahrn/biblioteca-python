# Banco de Dados da Biblioteca

"""
- Criar e conectar a um banco SQLite com sqlite3
- Criar tabelas (livros, usuarios)
- Inserir, consultar, atualizar e deletar dados com SQL
- Integrar isso às suas classes Livro, Usuario, Biblioteca
"""
import sqlite3
from sqlite3 import Error


def conectar(nome_banco):
    """ Cria uma conexão com o banco de dados SQLite """
    conexao = None
    try:
        conexao = sqlite3.connect(nome_banco)
        # print("Conexão bem-sucedida ao banco de dados SQLite")
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conexao


def criar_tabelas(nome_banco):
    conn = conectar(nome_banco)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        matricula TEXT PRIMARY KEY,
        nome TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        TITULO TEXT PRIMARY KEY,
        AUTOR TEXT NOT NULL,
        ANO_PUBLICACAO INTEGER NOT NULL,
        CATEGORIA TEXT NOT NULL,
        EMPRESTADO_PARA TEXT,
        FOREIGN KEY (EMPRESTADO_PARA) REFERENCES usuarios (matricula)
    )
    """)
    conn.commit()
    conn.close()
