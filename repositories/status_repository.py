from database.connection import get_connection
from models.status_consulta import StatusConsulta

class StatusConsulta:

    def buscar_por_id(self, id: int) -> StatusConsulta | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM StatusConsulta WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        
        return self._row_para_status(row)
    
    def listar(self) -> list[StatusConsulta]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM StatusConsulta ORDER BY id")
        rows = cursor.fetchall()
        conn.close()

        return [self._row_para_status(row) for row in rows]
    
    def _row_para_status(self, row) -> StatusConsulta:
        return StatusConsulta(
            id = row["id"],
            descricao = row["descricao"]
        )