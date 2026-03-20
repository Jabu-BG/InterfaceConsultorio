import tkinter as tk
from tkinter import ttk, messagebox

USUARIO = "admin"
SENHA = "1234"

class TelaLogin:

    def __init__(self, root):
        self.root = root
        self._configurar_janela()
        self._configurar_estilos()
        self._construir_tela()

    def _configurar_janela(self):
        self.root.title("Sistema de Hospital - Login")
        self.root.geometry("400x500+500+200")
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
            font=("Segoe UI", 22, "bold")
        )
        style.configure("Sub.TLabel",
            background="#ffffff",
            foreground="#888888",
            font=("Segoe UI", 10)
        )

        style.configure("Primary.TButton",
            background="#4361ee",
            foreground="#ffffff",
            font=("Segoe UI", 11, "bold"),
            padding=(0, 12),
            relief="flat"
        )
        style.map("Primary.TButton",
            background=[("active", "#3a56d4")]
        )

    def _construir_tela(self):
        frame_externo = ttk.Frame(self.root)
        frame_externo.pack(fill="both", expand=True)

        card = ttk.Frame(frame_externo, style="Card.TFrame", padding=40)
        card.place(relx=0.5, anchor="center", width=320, height=400)

        ttk.Label(card, text="🏥", font=("Segoe UI", 36), background="#ffffff").pack(pady=(0, 8))
        ttk.Label(card, text="Sistema de Hospital", style="Titulo.TLabel").pack()
        ttk.Label(card, text="Sistema de Gestão de Consultas", style="Sub.TLabel").pack(pady=(4, 24 ))
        ttk.Label(card, text="Usuário").pack(anchor="w")

        self.var_usuario = tk.StringVar()
        ttk.Entry(card, textvariable=self.var_usuario, width=30).pack(fill="x", pady=(4, 16))

        ttk.Label(card, text="Senha").pack(anchor="w")

        self.var_senha = tk.StringVar()
        ttk.Entry(card, textvariable=self.var_senha, show="●", width=30).pack(fill="x", pady=(4, 24))

        btn = ttk.Button(card, text="Entrar", style="Primary.TButton", command=self._fazer_login)
        btn.pack(fill="x")

        self.root.bind("<Return>", lambda e: self._fazer_login())

    def _fazer_login(self):
        usuario = self.var_usuario.get().strip()
        senha = self.var_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha usuário e senha.")
            return
        
        if usuario == USUARIO and senha == SENHA:
            self.root.destroy()
            nova_janela = tk.Tk()
            from interfaces.main_window import MainWindow
            MainWindow(nova_janela)
            nova_janela.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
