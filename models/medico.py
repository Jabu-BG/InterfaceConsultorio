from dataclasses import dataclass

@dataclass
class Medico:
    id: int
    nome: str
    crm: int
    especialidade: str
    telefone: str