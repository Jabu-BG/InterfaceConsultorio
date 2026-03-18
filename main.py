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

paciente = Paciente(
    nome="Maria Luiza",
    cpf="000.987.654-32",
    data_nascimento=date(1742, 2, 25),
    telefone="(12) 73255-2214"
)

medico = Medico(
    nome="Dra. Ana Costa",
    crm="CRM/SP 12345",
    especialidade="Cardiologia"
)

medico = Medico(
    nome="Dr. Paulo Freire",
    crm="CRM/RJ 123426",
    especialidade="Odontologia"
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
    data=date(2025, 5, 15),
    hora=time(14, 30),
    status_id=1,
    paciente_nome="João Silva",
    medico_nome="Dra. Ana Costa"
)

status = StatusConsulta(id=2, descricao="Agendada")

agenda = AgendaMedica(
    medico_id=2,
    dia_semana=0,
    hora_inicio=time(8, 0),
    hora_fim=time(12, 0)
)

consulta = Consulta(
    paciente_id=2,
    medico_id=2,
    data=date(2025, 5, 15),
    hora=time(1, 30),
    status_id=2,
    paciente_nome="Maria Luiza",
    medico_nome="Dr. Paulo Freire"
)

status = StatusConsulta(id=2, descricao="Agendada")

agenda = AgendaMedica(
    medico_id=2,
    dia_semana=0,
    hora_inicio=time(8, 0),
    hora_fim=time(12, 0)
)

consulta = Consulta(
    paciente_id=3,
    medico_id=3,
    data=date(2025, 5, 15),
    hora=time(14, 30),
    status_id=2,
    paciente_nome="Maria Luiza",
    medico_nome="Dra. Ana Costa"
)

print("=== Teste dos Models ===\n")
print(paciente)
print(medico)
print(status)
print(agenda)
print(consulta)