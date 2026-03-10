from dataclasses import dataclass

@dataclass
class Consulta:
    id: int
    paciente_id: int
    medico_id: int
    data: str
    hora: str
    status_id: int