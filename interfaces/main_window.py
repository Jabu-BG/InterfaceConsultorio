import tkinter as tk
from tkinter import ttk, messagebox

class MainWindow:

    def __init__(self, root):
        self.root = root
        self._configurar_janela()
        self._configurar_estilos()
        self._construir_tela()

    def _configurar_janela(self):
        self.root.title("Sistema de Hospital")
        self.root.geometry("900x600+100+100")
        self.root.resizable(True, True)
        self.root.configure(bg="#1a1a2e")

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Sidebar.TFrame", background="#16213e")

        style.configure("Menu.TButton",
            background="#16213e",
            foreground="#aaaacc",
            font=("Segoe UI", 12),
            padding=(16, 14),
            relief="flat",
            anchor="w"
        )
        style.map("Menu.TButton",
            background=[("active", "#0f3460")],
            foreground=[("active", "#ffffff")]
        )

        style.configure("MenuAtivo.TButton",
            background="#4361ee",
            foreground="#ffffff",
            font=("Segoe UI", 12, "bold"),
            padding=(16, 14),
            relief="flat",
            anchor="w"
        )

        style.configure("Content.TFrame", background="#f0f2f5")

        style.configure("Titulo.TLabel",
            background="#f0f2f5",
            foreground="#16213e",
            font=("Segoe UI", 20, "bold")
        )
        style.configure("Sub.TLabel",
            background="#f0f2f5",
            foreground="#888888",
            font=("Segoe UI", 10)
        )

    def _construir_tela(self):
        self.sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ttk.Label(self.sidebar, text="Hospital",
                  background="#16213e", foreground="#ffffff",
                  font=("Segoe UI", 14, "bold"),
                  padding=(16, 20)).pack(fill="x")

        ttk.Separator(self.sidebar).pack(fill="x", padx=16)

        self.botoes_menu = {}

        opcoes = [
            ("Pacientes",  self._abrir_pacientes),
            ("Médicos",    self._abrir_medicos),
            ("Consultas",  self._abrir_consultas),
        ]

        for texto, comando in opcoes:
            btn = ttk.Button(self.sidebar, text=texto,
                             style="Menu.TButton",
                             command=lambda c=comando, t=texto: self._navegar(c, t))
            btn.pack(fill="x", padx=8, pady=2)
            self.botoes_menu[texto] = btn

        ttk.Separator(self.sidebar).pack(fill="x", padx=16, side="bottom", pady=8)
        ttk.Button(self.sidebar, text="Sair",
                   style="Menu.TButton",
                   command=self._sair).pack(fill="x", padx=8, pady=2,
                                            side="bottom")

        self.frame_conteudo = ttk.Frame(self.root, style="Content.TFrame")
        self.frame_conteudo.pack(side="left", fill="both", expand=True)

        self._mostrar_boas_vindas()

        self.botao_ativo = None

    def _navegar(self, comando, texto_botao):
        for texto, btn in self.botoes_menu.items():
            btn.configure(style="Menu.TButton")

        self.botoes_menu[texto_botao].configure(style="MenuAtivo.TButton")
        self.botao_ativo = texto_botao
        comando()

    def _limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def _mostrar_boas_vindas(self):
        self._limpar_conteudo()

        frame = ttk.Frame(self.frame_conteudo, style="Content.TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="🏥", font=("Segoe UI", 48),
                  background="#f0f2f5").pack()
        ttk.Label(frame, text="Bem-vindo ao Sistema de Hospital",
                  style="Titulo.TLabel").pack(pady=(8, 4))
        ttk.Label(frame, text="Selecione uma opção no menu lateral para começar.",
                  style="Sub.TLabel").pack()

    def _abrir_pacientes(self):
        self._limpar_conteudo()
        from interfaces.pacientes_view import PacientesView
        PacientesView(self.frame_conteudo)

    def _abrir_medicos(self):
        self._limpar_conteudo()
        from interfaces.medicos_view import MedicosView
        MedicosView(self.frame_conteudo)

    def _abrir_consultas(self):
        self._limpar_conteudo()
        from interfaces.consultas_view import ConsultasView
        ConsultasView(self.frame_conteudo)

    def _sair(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.root.destroy()