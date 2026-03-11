from dataclasses import dataclass, field
from typing import Optional
from datetime import date

@dataclass
class Paciente:
    nome: str
    cpf: str
    data_nascimento: date

    telefone: Optional[str] = None
    endereco: Optional[str] = None

    id: Optional[int] = None

    def __str__(self):
        return f"Paciente(id={self.id}, nome={self.nome}, cpf={self.cpf})"