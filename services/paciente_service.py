from models.paciente import Paciente
from repositories.paciente_repository import PacienteRepository
from datetime import date
from utils.validacoes import limpar_cpf, cpf_valido
from utils.datas import data_e_futura

class PacienteService:

    def __init__(self):
        self._repo = PacienteRepository()

    def cadastrar(self, nome: str, cpf: str, data_nascimento: date, telefone: str = None, endereco: str = None) -> Paciente:
        if not nome or not nome.strip():
            raise ValueError("Nome do paciente é obrigatório.")
        
        cpf_limpo = limpar_cpf(cpf)
        if not cpf_valido(cpf_limpo):
            raise ValueError("CPF inválido. Use o formato 000.000.000-00.")
        
        if self._repo.buscar_por_cpf(cpf_limpo):
            raise ValueError(f"CPF {cpf} já está cadastrado no sistema.")
        
        if data_e_futura(data_nascimento):
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
        
        cpf_limpo = limpar_cpf(paciente.cpf)
        if not cpf_valido(cpf_limpo):
            raise ValueError("CPF inválido.")
        
        existente = self._repo.buscar_por_cpf(cpf_limpo)
        if existente and existente.id != paciente.id:
            raise ValueError(f"CPF {paciente.cpf} já pertence a outro paciente.")
        
        paciente.cpf = cpf_limpo
        self._repo.atualizar(paciente)
        return paciente
    
    def deletar(self, id: int) -> None:
        if not self._repo.buscar_por_id(id):
            raise ValueError(f"Paciente com id {id} não encontrado.")
        self._repo.deletar(id)
