import tkinter as tk
from tkinter import ttk, messagebox
from services.paciente_service import PacienteService
from utils.formatadores import formatar_cpf, formatar_idade
from utils.datas import str_para_date, formatar_data
from datetime import date


class PacientesView:

    def __init__(self, parent):
        self.parent  = parent
        self.service = PacienteService()
        self.paciente_selecionado = None

        self._configurar_estilos()
        self._construir_tela()
        self._carregar_tabela()

    def _configurar_estilos(self):
        style = ttk.Style()

        style.configure("Card.TFrame",
            background="#ffffff",
            relief="flat"
        )
        style.configure("Form.TLabel",
            background="#ffffff",
            foreground="#333333",
            font=("Segoe UI", 10)
        )
        style.configure("Form.TEntry",
            font=("Segoe UI", 10),
            padding=6
        )
        style.configure("Primary.TButton",
            background="#4361ee",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            relief="flat"
        )
        style.configure("Danger.TButton",
            background="#e63946",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            relief="flat"
        )
        style.configure("Secondary.TButton",
            background="#6c757d",
            foreground="#ffffff",
            font=("Segoe UI", 10),
            padding=(12, 8),
            relief="flat"
        )
        style.map("Primary.TButton",   background=[("active", "#3a56d4")])
        style.map("Danger.TButton",    background=[("active", "#c1121f")])
        style.map("Secondary.TButton", background=[("active", "#5a6268")])

        style.configure("Treeview",
            font=("Segoe UI", 10),
            rowheight=30,
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#333333"
        )
        style.configure("Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#f0f2f5",
            foreground="#16213e",
            padding=8
        )
        style.map("Treeview", background=[("selected", "#4361ee")])

    def _construir_tela(self):
        header = ttk.Frame(self.parent, style="Content.TFrame", padding=(32, 24, 32, 0))
        header.pack(fill="x")

        ttk.Label(header, text="👤  Pacientes",
                  font=("Segoe UI", 20, "bold"),
                  background="#f0f2f5",
                  foreground="#16213e").pack(side="left")
        
        paned = ttk.PanedWindow(self.parent, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=32, pady=16)

        card_form = ttk.Frame(paned, style="Card.TFrame", padding=24)
        paned.add(card_form, weight=1)

        ttk.Label(card_form, text="Dados do Paciente",
                  background="#ffffff",
                  foreground="#16213e",
                  font=("Segoe UI", 13, "bold")).grid(
                      row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        campos = [
            ("Nome *",             "nome"),
            ("CPF *",              "cpf"),
            ("Data de Nascimento *\n(DD/MM/AAAA)", "nascimento"),
            ("Telefone",           "telefone"),
            ("Endereço",           "endereco"),
        ]

        self.vars = {}

        for i, (label, chave) in enumerate(campos, start=1):
            ttk.Label(card_form, text=label,
                      style="Form.TLabel").grid(
                          row=i, column=0, sticky="w",
                          padx=(0, 12), pady=(0, 4))

            var = tk.StringVar()
            self.vars[chave] = var

            ttk.Entry(card_form, textvariable=var,
                      width=26).grid(
                          row=i, column=1, sticky="ew", pady=(0, 10))

        card_form.columnconfigure(1, weight=1)

        frame_btns = ttk.Frame(card_form, style="Card.TFrame")
        frame_btns.grid(row=len(campos)+1, column=0,
                        columnspan=2, sticky="ew", pady=(8, 0))

        ttk.Button(frame_btns, text="💾 Salvar",
                   style="Primary.TButton",
                   command=self._salvar).pack(side="left", padx=(0, 8))

        ttk.Button(frame_btns, text="✏️ Editar",
                   style="Secondary.TButton",
                   command=self._editar).pack(side="left", padx=(0, 8))

        ttk.Button(frame_btns, text="🗑️ Excluir",
                   style="Danger.TButton",
                   command=self._excluir).pack(side="left", padx=(0, 8))

        ttk.Button(frame_btns, text="🧹 Limpar",
                   style="Secondary.TButton",
                   command=self._limpar_form).pack(side="left")

        card_tabela = ttk.Frame(paned, style="Card.TFrame", padding=24)
        paned.add(card_tabela, weight=2)

        ttk.Label(card_tabela, text="Pacientes Cadastrados",
                  background="#ffffff",
                  foreground="#16213e",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 12))

        frame_tree = ttk.Frame(card_tabela)
        frame_tree.pack(fill="both", expand=True)

        colunas = ("id", "nome", "cpf", "nascimento", "telefone")
        self.tabela = ttk.Treeview(frame_tree, columns=colunas,
                                   show="headings", selectmode="browse")

        self.tabela.heading("id",          text="ID")
        self.tabela.heading("nome",        text="Nome")
        self.tabela.heading("cpf",         text="CPF")
        self.tabela.heading("nascimento",  text="Nascimento")
        self.tabela.heading("telefone",    text="Telefone")

        self.tabela.column("id",          width=40,  anchor="center")
        self.tabela.column("nome",        width=180)
        self.tabela.column("cpf",         width=120, anchor="center")
        self.tabela.column("nascimento",  width=100, anchor="center")
        self.tabela.column("telefone",    width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical",
                                  command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabela.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _carregar_tabela(self):
        """Limpa e recarrega todos os pacientes na tabela."""
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        for p in self.service.listar():
            self.tabela.insert("", "end", iid=p.id, values=(
                p.id,
                p.nome,
                formatar_cpf(p.cpf),
                formatar_data(p.data_nascimento),
                p.telefone or "—"
            ))

    def _ao_selecionar(self, event):
        selecionado = self.tabela.selection()
        if not selecionado:
            return

        paciente_id = int(selecionado[0])
        self.paciente_selecionado = self.service.buscar_por_id(paciente_id)

    def _salvar(self):
        try:
            nome       = self.vars["nome"].get()
            cpf        = self.vars["cpf"].get()
            nasc_str   = self.vars["nascimento"].get()
            telefone   = self.vars["telefone"].get() or None
            endereco   = self.vars["endereco"].get() or None

            nascimento = str_para_date(nasc_str)
            if nascimento is None:
                messagebox.showwarning("Atenção", "Data de nascimento inválida.\nUse o formato DD/MM/AAAA.")
                return

            self.service.cadastrar(nome, cpf, nascimento, telefone, endereco)
            messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
            self._limpar_form()
            self._carregar_tabela()

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def _editar(self):
        if not self.paciente_selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente na tabela.")
            return

        try:
            p = self.paciente_selecionado
            p.nome     = self.vars["nome"].get()
            p.cpf      = self.vars["cpf"].get()
            nasc_str   = self.vars["nascimento"].get()
            p.telefone = self.vars["telefone"].get() or None
            p.endereco = self.vars["endereco"].get() or None

            nascimento = str_para_date(nasc_str)
            if nascimento is None:
                messagebox.showwarning("Atenção", "Data de nascimento inválida.\nUse o formato DD/MM/AAAA.")
                return

            p.data_nascimento = nascimento
            self.service.atualizar(p)
            messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")
            self._limpar_form()
            self._carregar_tabela()

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def _excluir(self):
        if not self.paciente_selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente na tabela.")
            return

        nome = self.paciente_selecionado.nome
        if messagebox.askyesno("Confirmar", f"Excluir o paciente '{nome}'?"):
            try:
                self.service.deletar(self.paciente_selecionado.id)
                messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")
                self._limpar_form()
                self._carregar_tabela()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _limpar_form(self):
        for var in self.vars.values():
            var.set("")
        self.paciente_selecionado = None
        self.tabela.selection_remove(self.tabela.selection())

    def preencher_form(self, event=None):
        selecionado = self.tabela.selection()
        if not selecionado:
            return

        paciente_id = int(selecionado[0])
        p = self.service.buscar_por_id(paciente_id)
        self.paciente_selecionado = p

        self.vars["nome"].set(p.nome)
        self.vars["cpf"].set(formatar_cpf(p.cpf))
        self.vars["nascimento"].set(formatar_data(p.data_nascimento))
        self.vars["telefone"].set(p.telefone or "")
        self.vars["endereco"].set(p.endereco or "")

        self.tabela.bind("<Double-1>", self.preencher_form)