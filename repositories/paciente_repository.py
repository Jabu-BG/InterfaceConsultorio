from database.connection import get_connection
from models.paciente import Paciente
from datetime import date

class PacienteRepository:

    def inserir(self, paciente: Paciente) -> Paciente:
        
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            paciente.nome,
            paciente.cpf,
            paciente.data_nascimento,
            paciente.telefone,
            paciente.endereco
        )

        conn.commit()
        paciente.id = cursor.lastrowid
        conn.close()
        return paciente
    
    def buscar_por_id(self, id: int) -> Paciente | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Paciente Where id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        
        return self._row_para_paciente(row)
    
    def buscar_por_cpf(self, cpf: str) -> Paciente | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Paciente WHERE cpf = ?" (cpf,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        
        return self._row_para_paciente(row)
    
    def listar(self) -> list[Paciente]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Paciente ORDER BY nome")
        rows = cursor.fetchall()
        conn.close

        return [self._row_para_paciente(row) for row in rows]
    
    def atualizar(self, paciente: Paciente) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            paciente.nome,
            paciente.cpf,
            paciente.data_nascimento,
            paciente.telefone,
            paciente.endereco,
            paciente.id
        )

        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()
        return atualizado
    
    def deletar(self, id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Paciente WHERE id = ?", (id,))

        conn.commit()
        deletado = cursor.rowcount > 0
        conn.close()
        return deletado
    
    def _row_para_paciente(self, row) -> Paciente:
        return Paciente(
            id = row["id"],
            nome = row["nome"],
            cpf = row["cpf"],
            data_nascimento = date.fromisocalendar(row["data_nascimento"]),
            telefone = row["telefone"],
            endereco = row["endereco"]
        )