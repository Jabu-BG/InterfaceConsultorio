from dataclasses import dataclass
from typing import Optional
from datetime import time

DIAS_SEMANA = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

@dataclass
class AgendaMedica:
    medico_id: int
    dia_semana: str
    hora_inicio: time
    hora_fim: time

    id: Optional[int] = None

    def nome_dia(self) -> str:
        return DIAS_SEMANA.get(self.dia_semana, "Dia inválido")
    
    def __str__(self):
        return (
            f"AgendaMedica(medico_id={self.medico_id}, "
            f"dia={self.nome_dia()}, "
            f"{self.hora_inicio}-{self.hora_fim})"
        )