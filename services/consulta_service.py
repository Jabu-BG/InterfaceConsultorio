from models.consulta import Consulta
from repositories.consulta_repository import ConsultaRepository
from repositories.paciente_repository import PacienteRepository
from repositories.medico_repository import MedicoRepository
from repositories.agenda_repository import AgendaRepository
from datetime import date, time
from utils.datas import data_e_passada


class ConsultaService:

    def __init__(self):
        self._repo_consulta = ConsultaRepository()
        self._repo_paciente = PacienteRepository()
        self._repo_medico   = MedicoRepository()
        self._repo_agenda   = AgendaRepository()

    def agendar(self, paciente_id: int, medico_id: int,
                data: date, hora: time) -> Consulta:

        if not self._repo_paciente.buscar_por_id(paciente_id):
            raise ValueError(f"Paciente com id {paciente_id} não encontrado.")

        if not self._repo_medico.buscar_por_id(medico_id):
            raise ValueError(f"Médico com id {medico_id} não encontrado.")

        if data_e_passada(data):
            raise ValueError("Não é possível agendar consultas em datas passadas.")

        dia_semana = data.weekday()

        if not self._repo_agenda.medico_atende_no_horario(medico_id, dia_semana, hora):
            raise ValueError(
                "O médico não possui agenda disponível nesse dia e horário."
            )

        if self._repo_consulta.existe_conflito(medico_id, data, hora):
            raise ValueError(
                "O médico já possui uma consulta agendada nesse dia e horário."
            )

        consulta = Consulta(
            paciente_id = paciente_id,
            medico_id   = medico_id,
            data        = data,
            hora        = hora,
            status_id   = 1
        )

        return self._repo_consulta.inserir(consulta)

    def buscar_por_id(self, id: int) -> Consulta:
        consulta = self._repo_consulta.buscar_por_id(id)
        if consulta is None:
            raise ValueError(f"Consulta com id {id} não encontrada.")
        return consulta

    def listar(self) -> list[Consulta]:
        return self._repo_consulta.listar()

    def listar_por_paciente(self, paciente_id: int) -> list[Consulta]:
        return self._repo_consulta.listar_por_paciente(paciente_id)

    def reagendar(self, consulta_id: int, nova_data: date, novo_hora: time) -> Consulta:
        consulta = self._repo_consulta.buscar_por_id(consulta_id)
        if consulta is None:
            raise ValueError(f"Consulta com id {consulta_id} não encontrada.")

        if consulta.status_id == 3:
            raise ValueError("Não é possível reagendar uma consulta cancelada.")

        if consulta.status_id == 2:
            raise ValueError("Não é possível reagendar uma consulta já realizada.")

        if data_e_passada(nova_data):
            raise ValueError("Não é possível agendar consultas em datas passadas.")

        dia_semana = nova_data.weekday()
        if not self._repo_agenda.medico_atende_no_horario(
            consulta.medico_id, dia_semana, novo_hora
        ):
            raise ValueError(
                "O médico não possui agenda disponível nesse dia e horário."
            )

        if self._repo_consulta.existe_conflito(
            consulta.medico_id, nova_data, novo_hora, ignorar_id=consulta_id
        ):
            raise ValueError(
                "O médico já possui outra consulta nesse dia e horário."
            )

        consulta.data = nova_data
        consulta.hora = novo_hora
        self._repo_consulta.atualizar(consulta)
        return consulta

    def cancelar(self, consulta_id: int) -> None:
        consulta = self._repo_consulta.buscar_por_id(consulta_id)
        if consulta is None:
            raise ValueError(f"Consulta com id {consulta_id} não encontrada.")

        if consulta.status_id == 3:
            raise ValueError("Consulta já está cancelada.")

        if consulta.status_id == 2:
            raise ValueError("Não é possível cancelar uma consulta já realizada.")

        self._repo_consulta.atualizar_status(consulta_id, 3)

    def marcar_realizada(self, consulta_id: int) -> None:
        consulta = self._repo_consulta.buscar_por_id(consulta_id)
        if consulta is None:
            raise ValueError(f"Consulta com id {consulta_id} não encontrada.")

        if consulta.status_id == 3:
            raise ValueError("Não é possível realizar uma consulta cancelada.")

        if consulta.status_id == 2:
            raise ValueError("Consulta já está marcada como realizada.")

        self._repo_consulta.atualizar_status(consulta_id, 2)