import tkinter as tk
from tkinter import ttk, messagebox
from db import Banco

class App:
    def __init__(self, root):
        self.db = Banco() # Conecta ao banco
        self.root = root
        self.root.title("Gestão de Squad - CRUD")
        self.root.geometry("850x600")

        # --- Área de Cadastro ---
        frame_input = tk.LabelFrame(root, text="Dados do Jogador", padx=10, pady=10)
        frame_input.pack(fill="x", padx=10, pady=5)

        # Labels e Entradas (igual aos seus inputs originais)
        tk.Label(frame_input, text="Nome:").grid(row=0, column=0)
        self.txt_nome = tk.Entry(frame_input)
        self.txt_nome.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Idade:").grid(row=0, column=2)
        self.txt_idade = tk.Entry(frame_input)
        self.txt_idade.grid(row=0, column=3, padx=5)

        tk.Label(frame_input, text="Posição (Ex: CAM):").grid(row=1, column=0)
        self.txt_posicao = tk.Entry(frame_input)
        self.txt_posicao.grid(row=1, column=1, padx=5)

        tk.Label(frame_input, text="Nacionalidade:").grid(row=1, column=2)
        self.txt_nacionalidade = tk.Entry(frame_input)
        self.txt_nacionalidade.grid(row=1, column=3, padx=5)

        tk.Label(frame_input, text="Time:").grid(row=2, column=0)
        self.txt_time = tk.Entry(frame_input) # Mantive como texto para simplificar
        self.txt_time.grid(row=2, column=1, padx=5)

        # --- Botões ---
        frame_btn = tk.Frame(root)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Adicionar", command=self.inserir).pack(side="left", padx=10)
        tk.Button(frame_btn, text="Atualizar Selecionado", command=self.atualizar).pack(side="left", padx=10)
        tk.Button(frame_btn, text="Excluir Selecionado", command=self.excluir, bg="red", fg="white").pack(side="left", padx=10)
        tk.Button(frame_btn, text="Limpar Campos", command=self.limpar).pack(side="left", padx=10)

        # --- Lista (Treeview) ---
        self.lista = ttk.Treeview(root, columns=("id", "nome", "idade", "posicao", "nacionalidade", "time"), show="headings")
        self.lista.heading("id", text="ID")
        self.lista.heading("nome", text="Nome")
        self.lista.heading("idade", text="Idade")
        self.lista.heading("posicao", text="Posição")
        self.lista.heading("nacionalidade", text="Nacionalidade")
        self.lista.heading("time", text="Time")

        # Configurar largura das colunas
        self.lista.column("id", width=30)
        self.lista.column("nome", width=150)
        self.lista.column("idade", width=50)
        self.lista.column("posicao", width=60)
        self.lista.column("nacionalidade", width=120)
        self.lista.column("time", width=120)

        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Evento de clique na lista para preencher os campos
        self.lista.bind("<ButtonRelease-1>", self.clique_lista)
        
        self.carregar_dados()

    # --- Funções Logicas ---
    def carregar_dados(self):
        # Limpa a lista visual
        for item in self.lista.get_children():
            self.lista.delete(item)
        # Pega do banco
        dados = self.db.listar_jogadores()
        for linha in dados:
            self.lista.insert("", "end", values=linha)

    def inserir(self):
        try:
            nome = self.txt_nome.get()
            idade = int(self.txt_idade.get())
            posicao = self.txt_posicao.get().upper()
            nac = self.txt_nacionalidade.get()
            time = self.txt_time.get()

            if self.db.inserir_jogador(nome, idade, posicao, nac, time):
                messagebox.showinfo("Sucesso", "Jogador adicionado!")
                self.limpar()
                self.carregar_dados()
            else:
                messagebox.showerror("Erro", "Erro ao adicionar (Nome já existe?)")
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser número.")

    def atualizar(self):
        selecionado = self.lista.selection()
        if not selecionado:
            return
        
        try:
            # Pega o ID da linha selecionada
            item = self.lista.item(selecionado[0])
            id_jogador = item['values'][0]
            
            nome = self.txt_nome.get()
            idade = int(self.txt_idade.get())
            posicao = self.txt_posicao.get().upper()
            nac = self.txt_nacionalidade.get()
            time = self.txt_time.get()

            if self.db.atualizar_jogador(id_jogador, nome, idade, posicao, nac, time):
                messagebox.showinfo("Sucesso", "Jogador atualizado!")
                self.carregar_dados()
                self.limpar()
        except ValueError:
             messagebox.showerror("Erro", "Verifique os dados.")

    def excluir(self):
        selecionado = self.lista.selection()
        if not selecionado:
            return
        
        if messagebox.askyesno("Confirmar", "Deseja excluir este jogador?"):
            item = self.lista.item(selecionado[0])
            id_jogador = item['values'][0]
            self.db.excluir_jogador(id_jogador)
            self.carregar_dados()
            self.limpar()

    def clique_lista(self, event):
        selecionado = self.lista.selection()
        if not selecionado:
            return
        item = self.lista.item(selecionado[0])
        valores = item['values']
        
        self.limpar()
        self.txt_nome.insert(0, valores[1])
        self.txt_idade.insert(0, valores[2])
        self.txt_posicao.insert(0, valores[3])
        self.txt_nacionalidade.insert(0, valores[4])
        self.txt_time.insert(0, valores[5])

    def limpar(self):
        self.txt_nome.delete(0, tk.END)
        self.txt_idade.delete(0, tk.END)
        self.txt_posicao.delete(0, tk.END)
        self.txt_nacionalidade.delete(0, tk.END)
        self.txt_time.delete(0, tk.END)