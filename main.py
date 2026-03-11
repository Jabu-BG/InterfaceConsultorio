from database.connection import inicializar_banco
from models.paciente import Paciente
from models.medico import Medico
from models.consulta import Consulta
from models.agenda_medica import AgendaMedica
from models.status_consulta import StatusConsulta
from datetime import date, time

inicializar_banco()

paciente = Paciente(
    nome="João Silva",
    cpf="123.456.789-00",
    data_nascimento=date(1990, 5, 20),
    telefone="(11) 99999-0000"
)

medico = Medico(
    nome="Dra. Ana Costa",
    crm="CRM/SP 12345",
    especialidade="Cardiologia"
)

status = StatusConsulta(id=1, descricao="Agendada")

agenda = AgendaMedica(
    medico_id=1,
    dia_semana=0,
    hora_inicio=time(8, 0),
    hora_fim=time(12, 0)
)

consulta = Consulta(
    paciente_id=1,
    medico_id=1,
    data=date(2025, 3, 15),
    hora=time(14, 30),
    status_id=1,
    paciente_nome="João Silva",
    medico_nome="Dra. Ana Costa"
)

print("=== Teste dos Models ===\n")
print(paciente)
print(medico)
print(status)
print(agenda)
print(consulta)