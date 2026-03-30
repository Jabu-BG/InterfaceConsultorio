import tkinter as tk
from tkinter import ttk, messagebox
from services.medico_service import MedicoService
from utils.datas import formatar_hora, str_para_time
from datetime import time


class MedicosView:

    def __init__(self, parent):
        self.parent  = parent
        self.service = MedicoService()
        self.medico_selecionado = None

        self._configurar_estilos()
        self._construir_tela()
        self._carregar_tabela()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Form.TLabel", background="#ffffff",
                        foreground="#333333", font=("Segoe UI", 10))
        style.map("Primary.TButton",   background=[("active", "#3a56d4")])
        style.map("Danger.TButton",    background=[("active", "#c1121f")])
        style.map("Secondary.TButton", background=[("active", "#5a6268")])

    def _construir_tela(self):
        header = ttk.Frame(self.parent, style="Content.TFrame", padding=(32, 24, 32, 0))
        header.pack(fill="x")

        ttk.Label(header, text="👨‍⚕️  Médicos",
                  font=("Segoe UI", 20, "bold"),
                  background="#f0f2f5",
                  foreground="#16213e").pack(side="left")

        paned = ttk.PanedWindow(self.parent, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=32, pady=16)

        card_form = ttk.Frame(paned, style="Card.TFrame", padding=24)
        paned.add(card_form, weight=1)

        ttk.Label(card_form, text="Dados do Médico",
                  background="#ffffff", foreground="#16213e",
                  font=("Segoe UI", 13, "bold")).grid(
                      row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        campos = [
            ("Nome *",         "nome"),
            ("CRM *\n(CRM/UF 000000)", "crm"),
            ("Especialidade",  "especialidade"),
            ("Telefone",       "telefone"),
        ]

        self.vars = {}
        for i, (label, chave) in enumerate(campos, start=1):
            ttk.Label(card_form, text=label, style="Form.TLabel").grid(
                row=i, column=0, sticky="w", padx=(0, 12), pady=(0, 4))
            var = tk.StringVar()
            self.vars[chave] = var
            ttk.Entry(card_form, textvariable=var, width=26).grid(
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

        ttk.Label(card_tabela, text="Médicos Cadastrados",
                  background="#ffffff", foreground="#16213e",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 12))

        frame_tree = ttk.Frame(card_tabela)
        frame_tree.pack(fill="both", expand=True)

        colunas = ("id", "nome", "crm", "especialidade", "telefone")
        self.tabela = ttk.Treeview(frame_tree, columns=colunas,
                                   show="headings", selectmode="browse")

        self.tabela.heading("id",            text="ID")
        self.tabela.heading("nome",          text="Nome")
        self.tabela.heading("crm",           text="CRM")
        self.tabela.heading("especialidade", text="Especialidade")
        self.tabela.heading("telefone",      text="Telefone")

        self.tabela.column("id",            width=40,  anchor="center")
        self.tabela.column("nome",          width=160)
        self.tabela.column("crm",           width=120, anchor="center")
        self.tabela.column("especialidade", width=130)
        self.tabela.column("telefone",      width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical",
                                  command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabela.bind("<<TreeviewSelect>>", self._ao_selecionar)
        self.tabela.bind("<Double-1>", self._preencher_form)

    def _carregar_tabela(self):
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        for m in self.service.listar():
            self.tabela.insert("", "end", iid=m.id, values=(
                m.id,
                m.nome,
                m.crm,
                m.especialidade or "—",
                m.telefone or "—"
            ))

    def _ao_selecionar(self, event):
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        self.medico_selecionado = self.service.buscar_por_id(int(selecionado[0]))

    def _preencher_form(self, event=None):
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        m = self.service.buscar_por_id(int(selecionado[0]))
        self.medico_selecionado = m
        self.vars["nome"].set(m.nome)
        self.vars["crm"].set(m.crm)
        self.vars["especialidade"].set(m.especialidade or "")
        self.vars["telefone"].set(m.telefone or "")

    def _salvar(self):
        try:
            self.service.cadastrar(
                nome          = self.vars["nome"].get(),
                crm           = self.vars["crm"].get(),
                especialidade = self.vars["especialidade"].get() or None,
                telefone      = self.vars["telefone"].get() or None
            )
            messagebox.showinfo("Sucesso", "Médico cadastrado com sucesso!")
            self._limpar_form()
            self._carregar_tabela()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def _editar(self):
        if not self.medico_selecionado:
            messagebox.showwarning("Atenção", "Selecione um médico na tabela.")
            return
        try:
            m = self.medico_selecionado
            m.nome          = self.vars["nome"].get()
            m.crm           = self.vars["crm"].get()
            m.especialidade = self.vars["especialidade"].get() or None
            m.telefone      = self.vars["telefone"].get() or None
            self.service.atualizar(m)
            messagebox.showinfo("Sucesso", "Médico atualizado com sucesso!")
            self._limpar_form()
            self._carregar_tabela()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def _excluir(self):
        if not self.medico_selecionado:
            messagebox.showwarning("Atenção", "Selecione um médico na tabela.")
            return
        nome = self.medico_selecionado.nome
        if messagebox.askyesno("Confirmar", f"Excluir o médico '{nome}'?"):
            try:
                self.service.deletar(self.medico_selecionado.id)
                messagebox.showinfo("Sucesso", "Médico excluído com sucesso!")
                self._limpar_form()
                self._carregar_tabela()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _limpar_form(self):
        for var in self.vars.values():
            var.set("")
        self.medico_selecionado = None
        self.tabela.selection_remove(self.tabela.selection())