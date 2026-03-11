from dataclasses import dataclass
from typing import Optional

@dataclass
class Medico:
    nome: str
    crm: int

    especialidade: Optional[str] = None
    telefone: Optional[str] = None

    id: Optional[int] = None

    def __str__(self):
        return f"Medico(id={self.id}, nome={self.nome}, crm={self.crm})"