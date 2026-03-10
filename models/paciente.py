from dataclasses import dataclass

@dataclass
class Paciente:
    id: int
    nome: str
    cpf: str
    data_nascimento: str
    telefone: str
    endereco: str