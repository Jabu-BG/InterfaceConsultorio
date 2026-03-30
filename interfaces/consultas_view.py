import tkinter as tk
from tkinter import ttk, messagebox
from services.consulta_service import ConsultaService
from services.paciente_service import PacienteService
from services.medico_service import MedicoService
from utils.datas import str_para_date, str_para_time, formatar_data, formatar_hora
from utils.formatadores import formatar_status


class ConsultasView:

    def __init__(self, parent):
        self.parent           = parent
        self.service          = ConsultaService()
        self.paciente_service = PacienteService()
        self.medico_service   = MedicoService()
        self.consulta_selecionada = None

        self._mapa_pacientes = {}
        self._mapa_medicos   = {}

        self._configurar_estilos()
        self._construir_tela()
        self._carregar_combos()
        self._carregar_tabela()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Form.TLabel", background="#ffffff",
                        foreground="#333333", font=("Segoe UI", 10))
        style.map("Primary.TButton",   background=[("active", "#3a56d4")])
        style.map("Danger.TButton",    background=[("active", "#c1121f")])
        style.map("Secondary.TButton", background=[("active", "#5a6268")])

    def _construir_tela(self):
        header = ttk.Frame(self.parent, style="Content.TFrame", padding=(32, 24, 32, 0))
        header.pack(fill="x")

        ttk.Label(header, text="📋  Consultas",
                  font=("Segoe UI", 20, "bold"),
                  background="#f0f2f5",
                  foreground="#16213e").pack(side="left")

        paned = ttk.PanedWindow(self.parent, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=32, pady=16)

        card_form = ttk.Frame(paned, style="Card.TFrame", padding=24)
        paned.add(card_form, weight=1)

        ttk.Label(card_form, text="Agendar Consulta",
                  background="#ffffff", foreground="#16213e",
                  font=("Segoe UI", 13, "bold")).grid(
                      row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        ttk.Label(card_form, text="Paciente *",
                  style="Form.TLabel").grid(
                      row=1, column=0, sticky="w", padx=(0, 12), pady=(0, 4))

        self.var_paciente = tk.StringVar()
        self.combo_paciente = ttk.Combobox(card_form,
                                           textvariable=self.var_paciente,
                                           state="readonly", width=26)
        self.combo_paciente.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        ttk.Label(card_form, text="Médico *",
                  style="Form.TLabel").grid(
                      row=2, column=0, sticky="w", padx=(0, 12), pady=(0, 4))

        self.var_medico = tk.StringVar()
        self.combo_medico = ttk.Combobox(card_form,
                                         textvariable=self.var_medico,
                                         state="readonly", width=26)
        self.combo_medico.grid(row=2, column=1, sticky="ew", pady=(0, 10))

        ttk.Label(card_form, text="Data *\n(DD/MM/AAAA)",
                  style="Form.TLabel").grid(
                      row=3, column=0, sticky="w", padx=(0, 12), pady=(0, 4))

        self.var_data = tk.StringVar()
        ttk.Entry(card_form, textvariable=self.var_data, width=26).grid(
            row=3, column=1, sticky="ew", pady=(0, 10))

        ttk.Label(card_form, text="Hora *\n(HH:MM)",
                  style="Form.TLabel").grid(
                      row=4, column=0, sticky="w", padx=(0, 12), pady=(0, 4))

        self.var_hora = tk.StringVar()
        ttk.Entry(card_form, textvariable=self.var_hora, width=26).grid(
            row=4, column=1, sticky="ew", pady=(0, 10))

        card_form.columnconfigure(1, weight=1)

        frame_btns = ttk.Frame(card_form, style="Card.TFrame")
        frame_btns.grid(row=5, column=0, columnspan=2,
                        sticky="ew", pady=(8, 0))

        ttk.Button(frame_btns, text="📅 Agendar",
                   style="Primary.TButton",
                   command=self._agendar).pack(side="left", padx=(0, 8))
        ttk.Button(frame_btns, text="🧹 Limpar",
                   style="Secondary.TButton",
                   command=self._limpar_form).pack(side="left")

        ttk.Separator(card_form, orient="horizontal").grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=16)

        ttk.Label(card_form, text="Ações na Consulta Selecionada",
                  background="#ffffff", foreground="#16213e",
                  font=("Segoe UI", 11, "bold")).grid(
                      row=7, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ttk.Label(card_form, text="Nova Data\n(DD/MM/AAAA)",
                  style="Form.TLabel").grid(
                      row=8, column=0, sticky="w", padx=(0, 12), pady=(0, 4))
        self.var_nova_data = tk.StringVar()
        ttk.Entry(card_form, textvariable=self.var_nova_data, width=26).grid(
            row=8, column=1, sticky="ew", pady=(0, 10))

        ttk.Label(card_form, text="Nova Hora\n(HH:MM)",
                  style="Form.TLabel").grid(
                      row=9, column=0, sticky="w", padx=(0, 12), pady=(0, 4))
        self.var_nova_hora = tk.StringVar()
        ttk.Entry(card_form, textvariable=self.var_nova_hora, width=26).grid(
            row=9, column=1, sticky="ew", pady=(0, 10))

        frame_acoes = ttk.Frame(card_form, style="Card.TFrame")
        frame_acoes.grid(row=10, column=0, columnspan=2,
                         sticky="ew", pady=(8, 0))

        ttk.Button(frame_acoes, text="🔄 Reagendar",
                   style="Secondary.TButton",
                   command=self._reagendar).pack(side="left", padx=(0, 8))
        ttk.Button(frame_acoes, text="✅ Realizada",
                   style="Primary.TButton",
                   command=self._marcar_realizada).pack(side="left", padx=(0, 8))
        ttk.Button(frame_acoes, text="❌ Cancelar",
                   style="Danger.TButton",
                   command=self._cancelar).pack(side="left")

        card_tabela = ttk.Frame(paned, style="Card.TFrame", padding=24)
        paned.add(card_tabela, weight=2)

        ttk.Label(card_tabela, text="Consultas Agendadas",
                  background="#ffffff", foreground="#16213e",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 12))

        frame_tree = ttk.Frame(card_tabela)
        frame_tree.pack(fill="both", expand=True)

        colunas = ("id", "paciente", "medico", "data", "hora", "status")
        self.tabela = ttk.Treeview(frame_tree, columns=colunas,
                                   show="headings", selectmode="browse")

        self.tabela.heading("id",       text="ID")
        self.tabela.heading("paciente", text="Paciente")
        self.tabela.heading("medico",   text="Médico")
        self.tabela.heading("data",     text="Data")
        self.tabela.heading("hora",     text="Hora")
        self.tabela.heading("status",   text="Status")

        self.tabela.column("id",       width=40,  anchor="center")
        self.tabela.column("paciente", width=150)
        self.tabela.column("medico",   width=150)
        self.tabela.column("data",     width=90,  anchor="center")
        self.tabela.column("hora",     width=60,  anchor="center")
        self.tabela.column("status",   width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical",
                                  command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabela.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _carregar_combos(self):
        pacientes = self.paciente_service.listar()
        self._mapa_pacientes = {p.nome: p for p in pacientes}
        self.combo_paciente["values"] = list(self._mapa_pacientes.keys())

        medicos = self.medico_service.listar()
        self._mapa_medicos = {m.nome: m for m in medicos}
        self.combo_medico["values"] = list(self._mapa_medicos.keys())

    def _carregar_tabela(self):
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        for c in self.service.listar():
            self.tabela.insert("", "end", iid=c.id, values=(
                c.id,
                c.paciente_nome or "—",
                c.medico_nome   or "—",
                formatar_data(c.data),
                formatar_hora(c.hora),
                formatar_status(c.status_id)
            ))

    def _ao_selecionar(self, event):
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        self.consulta_selecionada = self.service.buscar_por_id(int(selecionado[0]))

    def _agendar(self):
        try:
            nome_paciente = self.var_paciente.get()
            nome_medico   = self.var_medico.get()

            if not nome_paciente or not nome_medico:
                messagebox.showwarning("Atenção", "Selecione paciente e médico.")
                return

            paciente = self._mapa_pacientes[nome_paciente]
            medico   = self._mapa_medicos[nome_medico]

            data = str_para_date(self.var_data.get())
            hora = str_para_time(self.var_hora.get())

            if data is None:
                messagebox.showwarning("Atenção", "Data inválida. Use DD/MM/AAAA.")
                return
            if hora is None:
                messagebox.showwarning("Atenção", "Hora inválida. Use HH:MM.")
                return

            self.service.agendar(paciente.id, medico.id, data, hora)
            messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!")
            self._limpar_form()
            self._carregar_tabela()

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def _reagendar(self):
        if not self.consulta_selecionada:
            messagebox.showwarning("Atenção", "Selecione uma consulta na tabela.")
            return
        try:
            nova_data = str_para_date(self.var_nova_data.get())
            nova_hora = str_para_time(self.var_nova_hora.get())

            if nova_data is None:
                messagebox.showwarning("Atenção", "Nova data inválida. Use DD/MM/AAAA.")
                return
            if nova_hora is None:
                messagebox.showwarning("Atenção", "Nova hora inválida. Use HH:MM.")
                return

            self.service.reagendar(self.consulta_selecionada.id, nova_data, nova_hora)
            messagebox.showinfo("Sucesso", "Consulta reagendada com sucesso!")
            self._limpar_form()
            self._carregar_tabela()

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def _marcar_realizada(self):
        if not self.consulta_selecionada:
            messagebox.showwarning("Atenção", "Selecione uma consulta na tabela.")
            return
        if messagebox.askyesno("Confirmar", "Marcar consulta como realizada?"):
            try:
                self.service.marcar_realizada(self.consulta_selecionada.id)
                messagebox.showinfo("Sucesso", "Consulta marcada como realizada!")
                self._limpar_form()
                self._carregar_tabela()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _cancelar(self):
        if not self.consulta_selecionada:
            messagebox.showwarning("Atenção", "Selecione uma consulta na tabela.")
            return
        if messagebox.askyesno("Confirmar", "Cancelar esta consulta?"):
            try:
                self.service.cancelar(self.consulta_selecionada.id)
                messagebox.showinfo("Sucesso", "Consulta cancelada.")
                self._limpar_form()
                self._carregar_tabela()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _limpar_form(self):
        self.var_paciente.set("")
        self.var_medico.set("")
        self.var_data.set("")
        self.var_hora.set("")
        self.var_nova_data.set("")
        self.var_nova_hora.set("")
        self.consulta_selecionada = None
        self.tabela.selection_remove(self.tabela.selection())