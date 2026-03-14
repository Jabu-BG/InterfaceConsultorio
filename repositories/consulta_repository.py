from database.connection import get_connection
from models.consulta import Consulta
from datetime import date, time

class ConsultaRepository:

    def inserir(self, consulta: Consulta) -> Consulta:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            consulta.paciente_id,
            consulta.medico_id,
            consulta.data.isoformat(),
            consulta.hora.strftime("%H:%M"),
            consulta.status_id
        )

        conn.commit()
        consulta.id = cursor.lastrowid
        conn.close()
        
        return consulta
    
    def buscar_por_id(self, id: int) -> Consulta | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(id,)

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        
        return self._row_para_consulta(row)
    
    def listar(self) -> list[Consulta]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute()

        rows = cursor.fetchall()
        conn.close()

        return [self._row_para_consulta(row) for row in rows]
    
    def listar_por_paciente(self, paciente_id: int) -> list[Consulta]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(paciente_id,)

        rows = cursor.fetchall()
        conn.close()

        return [self._row_para_consulta(row) for row in rows]
    
    def existe_conflito(self, medico_id: int, data: date, hora: time, ignorar_id: int = None) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        query = '''medico_id, data, hora, status_id'''

        params = [medico_id, data.isoformat(), hora.strftime("%H:%M")]

        if ignorar_id is not None:
            query += " AND id != ?"
            params.append(ignorar_id)

        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close

        return row["total"] > 0
    
    def atualizar_status(self, consulta_id: int, status_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(status_id, consulta_id)

        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()
        
        return atualizado
    
    def atualizar(self, consulta: Consulta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            consulta.paciente_id,
            consulta.medico_id,
            consulta.data.isoformat(),
            consulta.hora.strftime("%H:%M"),
            consulta.status_id,
            consulta.id
        )

        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()

        return atualizado
    
    def deletar(self, id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Consulta WHERE id = ?", (id,))

        conn.commit()
        deletado = cursor.rowcount > 0
        conn.close()
        
        return deletado
    
    def _row_para_consulta(self, row) -> Consulta:
        return Consulta(
            id = row["id"],
            paciente_id = row["paciente_id"],
            medico_id = row["medico_id"],
            data = date.fromisoformat(row["data"]),
            hora = time.fromisoformat(row["hora"]),
            status_id = row["status_id"],
            paciente_nome = row["paciente_nome"],
            medico_nome = row["medico_nome"],
            status_descricao = row["status_descricao"]
        )