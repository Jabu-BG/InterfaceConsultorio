from dataclasses import dataclass

@dataclass

class Agenda_Medica:
    id: int
    medico_id: int
    dia_semana: str
    hora_inicio: str
    hora_fim: str