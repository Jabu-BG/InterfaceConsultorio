from dataclasses import dataclass
from typing import Optional
from datetime import date, time

@dataclass
class Consulta:
    paciente_id: int
    medico_id: int
    data: str
    hora: str

    status_id: int = 1

    id: Optional[int] = None

    paciente_nome: Optional[str] = None
    medico_nome: Optional[str] = None
    status_descricao: Optional[str] = None

    def __str__(self):
        paciente = self.paciente_nome or f"id={self.paciente_id}"
        medico = self.medico_nome or f"id={self.medico_id}"
        return (
            f"Consulta(id={self.id}, "
            f"paciente={paciente}, "
            f"medico={medico}, "
            f"data={self.data}, hora={self.hora}, "
            f"status={self.status_descricao or self.status_id})"
        )