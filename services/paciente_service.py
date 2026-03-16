from models.paciente import Paciente
from repositories.paciente_repository import PacienteRepository
from datetime import date
import re

class PacienteService:

    def __init__(self):
        self._repo = PacienteRepository

    def cadastrar(self, nome: str, cpf: str, data_nascimento: date, telefone: str = None, endereco: str = None) -> Paciente:
        if not nome or not nome.strip():
            raise ValueError("Nome do paciente é obrigatório.")
        
        cpf_limpo = self._limpar_cpf(cpf)
        if not self._cpf_valido(cpf_limpo):
            raise ValueError("CPF inválido. Use o formato 000.000.000-00.")
        
        if self._repo.buscar_por_cpf(cpf_limpo):
            raise ValueError(f"CPF {cpf} já está cadastrado no sistema.")
        
        if data_nascimento > date.today():
            raise ValueError("Data de nascimento não pode ser uma data futura.")
        
        paciente = Paciente(
            nome = nome.strip(),
            cpf = cpf_limpo,
            data_nascimento = data_nascimento,
            telefone = telefone,
            endereco = endereco
        )

        return self._repo.inserir(paciente)
    
    def buscar_por_id(self, id: int) -> Paciente:
        paciente = self._repo.buscar_por_id(id)
        if paciente is None:
            raise ValueError(f"Paciente com id {id} não encontrado.")
        return paciente
    
    def listar(self) -> list[Paciente]:
        return self._repo.listar()
    
    def atualizar(self, paciente: Paciente) -> Paciente:
        if not paciente.id:
            raise ValueError("Paciente sem id não pode ser atualizado.")
        
        if not paciente.nome or not paciente.nome.strip():
            raise ValueError("Nome do paciente é obrigatório")
        
        cpf_limpo = self._limpar_cpf(paciente.cpf)
        if not self._cpf_valido(cpf_limpo):
            raise ValueError("CPF inválido.")
        
        existente = self._repo.buscar_por_cpf(cpf_limpo)
        if existente and existente.id != paciente.id:
            raise ValueError(f"CPF {paciente.id} já pertence a outro paciente.")
        
        paciente.cpf = cpf_limpo
        self._repo.atualizar(paciente)
        return paciente
    
    def deletar(self, id: int) -> None:
        if not self._repo.buscar_por_id(id):
            raise ValueError(f"Paciente com id {id} não encontrado.")
        self._repo.deletar(id)

    def _limpar_cpf(self, cpf: str) -> str:
        return re.sub(r'\D', '', cpf)
    
    def _cpf_valido(self, cpf: str) -> bool:
        if len(cpf) != 11:
            return False
        
        if cpf == cpf[0] * 11:
            return False
        
        soma = sum(int(cpf[i]) * (10 - 1) for i in range(9))
        d1 = 0 if (soma * 10 % 11) >= 10 else (soma * 10 % 11)
        if d1 != int(cpf[9]):
            return False
        
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        d2 = 0 if (soma * 10 % 11) >= 10 else (soma * 10 % 11)
        if d2 != int(cpf[10]):
            return False
        
        return True