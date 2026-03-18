from models.medico import Medico
from models.agenda_medica import AgendaMedica
from repositories.medico_repository import MedicoRepository
from repositories.agenda_repository import AgendaRepository
from datetime import time
from utils.validacoes import formatar_crm, crm_valido

class MedicoService:
    def __init__(self):
        self._repo_medico = MedicoRepository()
        self._repo_agenda = AgendaRepository()

    def cadastrar(self, nome: str, crm: str, especialidade: str = None, telefone: str = None) -> Medico:
        if not nome or not nome.strip():
            raise ValueError("Nome do médico é obrigatório.")
        
        crm_limpo = formatar_crm(crm)
        if not crm_valido(crm_limpo):
            raise ValueError("CRM inválido. Use o formato CRM/UF 000000.")
        
        if self._repo_medico.buscar_por_crm(crm_limpo):
            raise ValueError(f"CRM {crm} já está cadastrado no sistema.")
        
        medico = Medico(
            nome = nome.strip(),
            crm = crm_limpo,
            especialidade = especialidade,
            telefone = telefone
        )

        return self._repo_medico.inserir(medico)
    
    def buscar_por_id(self, id: int) -> Medico:
        medico = self._repo_medico.buscar_por_id(id)
        if medico is None:
            raise ValueError(f"Medico com id {id} não encontrado.")
        return medico
    
    def listar(self) -> list[Medico]:
        return self._repo_medico.listar()
    
    def listar_por_especialidade(self, especialidade: str) -> list[Medico]:
        return self._repo_medico.listar_por_especialidade(especialidade)
    
    def atualizar(self, medico: Medico) -> Medico:
        if not medico.id:
            raise ValueError("Médico sem id não pode ser atualizado.")
        
        if not medico.nome or not medico.nome.strip():
            raise ValueError("Nome do médico é obrigatório.")
        
        crm_limpo = formatar_crm(medico.crm)
        if not crm_valido(crm_limpo):
            raise ValueError("CRM inválido.")
        
        existente = self._repo_medico.buscar_por_crm(crm_limpo)
        if existente and existente.id != medico.id:
            raise ValueError(f"CRM {medico.crm} já pertence a outro médico.")
        
        medico.crm = crm_limpo
        self._repo_medico.atualizar(medico)
        return medico
    
    def deletar(self, id: int) -> None:
        if not self._repo_medico.buscar_por_id(id):
            raise ValueError(f"Médico com id {id} não encontrado.")
        self._repo_medico.deletar(id)

    def adicionar_horario_agenda(self, medico_id: int, dia_semana: int, hora_inicio: time, hora_fim: time) -> AgendaMedica:
        if not self._repo_medico.buscar_por_id(medico_id):
            raise ValueError(f"Médico com id {medico_id} não encontrado.")
        
        if dia_semana not in range(7):
            raise ValueError("Dia da semana inválido. Use 0 (Segunda) a 6 (Domingo).")
        
        if hora_fim <= hora_inicio:
            raise ValueError("Horário de fim deve ser depois do horário de início.")
        
        agenda = AgendaMedica(
            medico_id = medico_id,
            dia_semana = dia_semana,
            hora_inicio = hora_inicio,
            hora_fim = hora_fim
        )

        return self._repo_agenda.inserir(agenda)
    
    def listar_agenda(self, medico_id: int) -> list[AgendaMedica]:
        return self._repo_agenda.listar_por_medico(medico_id)
    
    def remover_horario_agenda(self, agenda_id: int) -> None:
        removido = self._repo_agenda.deletar(agenda_id)
        if not removido:
            raise ValueError(f"Horário de agenda com id {agenda_id} não encontrado.")