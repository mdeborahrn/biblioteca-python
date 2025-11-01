#Classes e funções para o sistema de biblioteca

from banco import conectar, criar_tabelas


def menu():
    print("Sistema de Biblioteca", flush=True)
    print("1. Cadastrar Livro", flush=True)
    print("2. Cadastrar Usuário", flush=True)
    print("3. Emprestar Livro", flush=True)
    print("4. Devolver Livro", flush=True)
    print("5. Listar Livros", flush=True)
    print("6. Sair", flush=True)

class Livro:
    def __init__(self, titulo, autor, ano_publicacao, categoria):
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.categoria = categoria
        self.emprestado = None  # Nenhum usuário no inicio

    def emprestar(self, usuario):
        self.emprestado = usuario

    def devolver(self):
        self.emprestado = None
    
    def esta_disponivel(self):
        return self.emprestado is None

class Usuario:
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula

class Biblioteca:
    def __init__(self):
        self.livros = []
        self.usuarios = []

    def cadastrar_livro(self, livro):
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO livros (TITULO, AUTOR, ANO_PUBLICACAO, CATEGORIA) VALUES (?, ?, ?, ?)
        """, (livro.titulo, livro.autor, livro.ano_publicacao, livro.categoria))
        conn.commit()
        conn.close()

    def cadastrar_usuario(self, usuario):
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO usuarios (matricula, nome) VALUES (?, ?)
        """, (usuario.matricula, usuario.nome))
        conn.commit()
        conn.close()
    def emprestar_livro(self, titulo, usuario):
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        # Check if the book is already loaned out
        cursor.execute("""
        SELECT EMPRESTADO_PARA FROM livros WHERE TITULO = ?
        """, (titulo,))
        result = cursor.fetchone()
        if result and result[0] is None:
            cursor.execute("""
            UPDATE livros SET EMPRESTADO_PARA = ? WHERE TITULO = ?
            """, (usuario.matricula, titulo))
            conn.commit()
            sucesso = True
        else:
            sucesso = False
        conn.close()
        return sucesso

    def devolver_livro(self, titulo):
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        # Check if the book is currently loaned out
        cursor.execute("""
        SELECT EMPRESTADO_PARA FROM livros WHERE TITULO = ?
        """, (titulo,))
        result = cursor.fetchone()
        if result and result[0] is not None:
            cursor.execute("""
            UPDATE livros SET EMPRESTADO_PARA = NULL WHERE TITULO = ?
            """, (titulo,))
            conn.commit()
            sucesso = True
        else:
            sucesso = False
        conn.close()
        return sucesso

    def listar_livros(self, apenas_disponiveis=False, apenas_emprestados=False):
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        if apenas_emprestados:
            cursor.execute("""
            SELECT TITULO, AUTOR, ANO_PUBLICACAO, CATEGORIA, EMPRESTADO_PARA FROM livros WHERE EMPRESTADO_PARA IS NOT NULL
            """)
        elif apenas_disponiveis:
            cursor.execute("""
            SELECT TITULO, AUTOR, ANO_PUBLICACAO, CATEGORIA, EMPRESTADO_PARA FROM livros WHERE EMPRESTADO_PARA IS NULL
            """)
        else:
            cursor.execute("""
            SELECT TITULO, AUTOR, ANO_PUBLICACAO, CATEGORIA, EMPRESTADO_PARA FROM livros
            """)
        livros = cursor.fetchall()
        conn.close()
        self.livros = []
        for livro_data in livros:
            livro = Livro(livro_data[0], livro_data[1], livro_data[2], livro_data[3])
            if livro_data[4] is not None:
                livro.emprestado = livro_data[4]
            self.livros.append(livro)
        return self.livros
    def listar_usuarios(self):
        conn = conectar('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT matricula, nome FROM usuarios
        """)
        usuarios_data = cursor.fetchall()
        conn.close()
        self.usuarios = []
        for usuario_data in usuarios_data:
            usuario = Usuario(nome=usuario_data[1], matricula=usuario_data[0])
            self.usuarios.append(usuario)
        return self.usuarios
