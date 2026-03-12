from  database.connection import get_connection
from models.medico import Medico 

class MedicoRepository:

    def inserir(self, medico: Medico) -> Medico:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            medico.nome,
            medico.crm,
            medico.especialidade,
            medico.telefone
        )

        conn.commit()
        medico.id = cursor.lastrowid
        conn.close()
        return medico
    
    def buscar_por_id(self, id: int) -> Medico | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Medico WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        
        return self._row_para_medico(row)
    
    def buscar_por_crm(self, crm: str) -> Medico | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Medico WHERE crm = ?", (crm,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        
        return self._row_para_medico(row)
    
    def listar(self) -> list[Medico]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Medico ORDER BY nome")
        rows = cursor.fetchall()
        conn.close()

        return [self._row_para_medico(row) for row in rows]
    
    def listar_por_especialidade(self, especialidade: str) -> list[Medico]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM Medico WHERE especialidade LIKE ? ORDER BY nome",
            (f"%{especialidade}")
        )

        rows = cursor.fetchall()
        conn.close()

        return [self._row_para_medico(row) for row in rows]
    
    def atualizar(self, medico: Medico) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            medico.nome,
            medico.crm,
            medico.especialidade,
            medico.telefone,
            medico.id
        )

        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()
        return atualizado
    
    def deletar(self, id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Medico WHERE id = ?", (id,))

        conn.commit()
        deletado = cursor.rowcount > 0
        conn.cursor()
        return deletado
    
    def _row_para_medico(self, row) -> Medico:
        return Medico(
            id = row["id"],
            nome = row["nome"],
            crm = row["crm"],
            especialidade = row["especialidade"],
            telefone = row["telefone"]
        )
