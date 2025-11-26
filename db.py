import sqlite3

class Banco:
    def __init__(self):
        self.conexao = sqlite3.connect("banco.db", check_same_thread = False)
        self.cursor = self.conexao.cursor()
        self.iniciar_banco()

    def iniciar_banco(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS times (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS squad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                idade INTEGER NOT NULL,
                posicao VARCHAR(3),
                nacionalidade TEXT NOT NULL,
                time_id INTEGER,
                FOREIGN KEY(time_id) REFERENCES times(id)
            )
        """)
        self.conexao.commit()

    def pegar_id_time(self, nome_time):
        nome_time = nome_time.strip()
        self.cursor.execute("SELECT id FROM times WHERE nome = ?", (nome_time,))
        resultado = self.cursor.fetchone()
        
        if resultado:
            return resultado[0]
        else:
            self.cursor.execute("INSERT INTO times (nome) VALUES (?)", (nome_time,))
            self.conexao.commit()
            return self.cursor.lastrowid

    def inserir_jogador(self, nome, idade, posicao, nacionalidade, nome_time):
        try:
            time_id = self.pegar_id_time(nome_time)
            
            self.cursor.execute("""
                INSERT INTO squad (nome, idade, posicao, nacionalidade, time_id)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, idade, posicao, nacionalidade, time_id))
            self.conexao.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def listar_jogadores(self):
        self.cursor.execute("""
            SELECT s.id, s.nome, s.idade, s.posicao, s.nacionalidade, t.nome 
            FROM squad s
            JOIN times t ON s.time_id = t.id
        """)
        return self.cursor.fetchall()

    def atualizar_jogador(self, id, nome, idade, posicao, nacionalidade, nome_time):
        time_id = self.pegar_id_time(nome_time)
        self.cursor.execute("""
            UPDATE squad 
            SET nome = ?, idade = ?, posicao = ?, nacionalidade = ?, time_id = ?
            WHERE id = ?
        """, (nome, idade, posicao, nacionalidade, time_id, id))
        self.conexao.commit()
        return self.cursor.rowcount > 0

    def excluir_jogador(self, id):
        self.cursor.execute("DELETE FROM squad WHERE id = ?", (id,))
        self.conexao.commit()
        return self.cursor.rowcount > 0

    def fechar_banco(self):
        self.conexao.close()