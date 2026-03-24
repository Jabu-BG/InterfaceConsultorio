import tkinter as tk
from tkinter import ttk, messagebox

class PacientesView:

    def __init__(self, root):
        self.root = root
        self._janela_paciente()
        self._configurar_estilos()
        self._tela_paciente()

    def _janela_paciente(self):
        self.root.title("Sistema de Hospital - Paciente")
        self.root.geometry("600x600+200+200")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1a1a2e")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("TLabel",
            background="#ffffff",
            foreground="#333333",
            font=("Segoe UI", 11)
        )
        style.configure("Titulo.TLabel",
            background="#ffffff",
            foreground="#16213e",
            font=("Segoe UI", 10, "bold")
        )
        style.configure("Sub.TLabel",
            background="#ffffff",
            foreground="#888888",
            font=("Segoe UI", 8)
        )

        style.configure("Primary.TButton",
            background="#35394a",
            foreground="#ffffff",
            font=("Segoe UI", 6, "bold"),
            padding=(0, 6),
            relief="flat"
        )
        style.map("Primary.TButton",
            background=[("active", "#35394a")]
        )

    def _tela_paciente(self):
        frame_externo = ttk.Frame(self.root)
        frame_externo.pack(fill="both", expand=True)
        self.card = ttk.Frame(frame_externo, style="Card.TFrame", padding=30)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=600)

        ttk.Label(self.card, text="🏥", font=("Segoe UI", 20), background="#ffffff").pack(pady=(0, 8))
        ttk.Label(self.card, text="Sistema de Hospital", style="Titulo.TLabel").pack()
        ttk.Label(self.card, text="Sistema de Incersão de Pacientes", style="Sub.TLabel").pack(pady=(4, 24 ))

        self._labels()
        self._buttons()
        self._lista_pacientes()

    def _labels(self):

        frame_form = ttk.Frame(self.card)
        frame_form.pack(fill="x", pady=10)
        linha1 = ttk.Frame(frame_form)
        linha1.pack(fill="x", pady=5)

        ttk.Label(linha1, text="Nome").pack(side="left", padx=5)
        self.entry_nome = ttk.Entry(linha1)
        self.entry_nome.pack(side="left", fill="x", expand=True, padx=5)

        ttk.Label(linha1, text="CPF").pack(side="left", padx=5)
        self.entry_CPF = ttk.Entry(linha1)
        self.entry_CPF.pack(side="left", fill="x", expand=True, padx=5)

        linha2 = ttk.Frame(frame_form)
        linha2.pack(fill="x", pady=5)

        ttk.Label(linha2, text="Nascimento").pack(side="left", padx=5)
        self.entry_nascimento = ttk.Entry(linha2)
        self.entry_nascimento.pack(side="left", fill="x", expand=True, padx=5)

        ttk.Label(linha2, text="Telefone").pack(side="left", padx=5)
        self.entry_telefone = ttk.Entry(linha2)
        self.entry_telefone.pack(side="left", fill="x", expand=True, padx=5)

        linha3 = ttk.Frame(frame_form)
        linha3.pack(fill="x", pady=5)

        ttk.Label(linha3, text="Endereço").pack(side="left", padx=5)
        self.entry_endereco = ttk.Entry(linha3)
        self.entry_endereco.pack(side="left", fill="x", expand=True, padx=5)

    def _buttons(self):

        frame_botoes = ttk.Frame(self.card)
        frame_botoes.pack(fill="x", pady=15)

        ttk.Button(frame_botoes, text="Novo", style="Primary.TButton").pack(side="left", expand=True, padx=5)
        ttk.Button(frame_botoes, text="Salvar", style="Primary.TButton").pack(side="left", expand=True, padx=5)
        ttk.Button(frame_botoes, text="Editar", style="Primary.TButton").pack(side="left", expand=True, padx=5)
        ttk.Button(frame_botoes, text="Limpar", style="Primary.TButton").pack(side="left", expand=True, padx=5)
        ttk.Button(frame_botoes, text="Excluir", style="Primary.TButton").pack(side="left", expand=True, padx=5)
    
    def _lista_pacientes(self):
        frame_lista = ttk.Frame(self.card)
        frame_lista.pack(fill="both", expand=True, pady=10)
        self.lista = ttk.Treeview(frame_lista,columns=("cpf","nome","endereço","telefone","nascimento"),show="headings")

        self.lista.pack(fill="both", expand=True)
        self.lista.heading("cpf", text="CPF")
        self.lista.heading("nome", text="Nome")
        self.lista.heading("endereço", text="Endereço")
        self.lista.heading("telefone", text="Telefone")
        self.lista.heading("nascimento", text="Nascimento")

        self.lista.column("cpf", width=80)
        self.lista.column("nome", width=100)
        self.lista.column("endereço", width=120)
        self.lista.column("telefone", width=90)
        self.lista.column("nascimento", width=9)

root = tk.Tk()
PacientesView(root)
root.mainloop()