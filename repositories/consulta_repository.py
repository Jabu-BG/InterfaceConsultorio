from database.connection import get_connection
from models.consulta import Consulta
from datetime import date, time

class ConsultaRepository:

    def inserir(self, consulta: Consulta) -> Consulta:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Consulta (paciente_id, medico_id, data, hora, status_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            consulta.paciente_id,
            consulta.medico_id,
            consulta.data.isoformat(),
            consulta.hora.strftime("%H:%M"),
            consulta.status_id
        ))

        conn.commit()
        consulta.id = cursor.lastrowid
        conn.close()

        return consulta

    def buscar_por_id(self, id: int) -> Consulta | None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.*,
                p.nome AS paciente_nome,
                m.nome AS medico_nome,
                s.descricao AS status_descricao
            FROM Consulta c
            JOIN Paciente       p ON c.paciente_id = p.id
            JOIN Medico         m ON c.medico_id   = m.id
            JOIN StatusConsulta s ON c.status_id   = s.id
            WHERE c.id = ?
        """, (id,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return self._row_para_consulta(row)

    def listar(self) -> list[Consulta]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.*,
                p.nome AS paciente_nome,
                m.nome AS medico_nome,
                s.descricao AS status_descricao
            FROM Consulta c
            JOIN Paciente       p ON c.paciente_id = p.id
            JOIN Medico         m ON c.medico_id   = m.id
            JOIN StatusConsulta s ON c.status_id   = s.id
            ORDER BY c.data, c.hora
        """)

        rows = cursor.fetchall()
        conn.close()

        return [self._row_para_consulta(row) for row in rows]

    def listar_por_paciente(self, paciente_id: int) -> list[Consulta]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.*,
                p.nome AS paciente_nome,
                m.nome AS medico_nome,
                s.descricao AS status_descricao
            FROM Consulta c
            JOIN Paciente       p ON c.paciente_id = p.id
            JOIN Medico         m ON c.medico_id   = m.id
            JOIN StatusConsulta s ON c.status_id   = s.id
            WHERE c.paciente_id = ?
            ORDER BY c.data DESC, c.hora DESC
        """, (paciente_id,))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_para_consulta(row) for row in rows]

    def existe_conflito(self, medico_id: int, data: date, hora: time, ignorar_id: int = None) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT COUNT(*) as total
              FROM Consulta
             WHERE medico_id = ?
               AND data      = ?
               AND hora      = ?
               AND status_id != 3
        """

        params = [medico_id, data.isoformat(), hora.strftime("%H:%M")]

        if ignorar_id is not None:
            query += " AND id != ?"
            params.append(ignorar_id)

        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()

        return row["total"] > 0

    def atualizar_status(self, consulta_id: int, status_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Consulta SET status_id = ? WHERE id = ?
        """, (status_id, consulta_id))

        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()

        return atualizado

    def atualizar(self, consulta: Consulta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Consulta
               SET paciente_id = ?,
                   medico_id   = ?,
                   data        = ?,
                   hora        = ?,
                   status_id   = ?
             WHERE id = ?
        """, (
            consulta.paciente_id,
            consulta.medico_id,
            consulta.data.isoformat(),
            consulta.hora.strftime("%H:%M"),
            consulta.status_id,
            consulta.id
        ))

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
            id               = row["id"],
            paciente_id      = row["paciente_id"],
            medico_id        = row["medico_id"],
            data             = date.fromisoformat(row["data"]),
            hora             = time.fromisoformat(row["hora"]),
            status_id        = row["status_id"],
            paciente_nome    = row["paciente_nome"],
            medico_nome      = row["medico_nome"],
            status_descricao = row["status_descricao"]
        )