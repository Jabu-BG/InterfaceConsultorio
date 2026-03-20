from database.connection import get_connection
from models.agenda_medica import AgendaMedica
from datetime import time

class AgendaRepository:

    def inserir(self, agenda: AgendaMedica) -> AgendaMedica:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO AgendaMedica (medico_id, dia_semana, hora_inicio, hora_fim)
            VALUES (?, ?, ?, ?)
        """, (
            agenda.medico_id,
            agenda.dia_semana,
            agenda.hora_inicio.strftime("%H:%M"),
            agenda.hora_fim.strftime("%H:%M")
        ))

        conn.commit()
        agenda.id = cursor.lastrowid
        conn.close()

        return agenda

    def listar_por_medico(self, medico_id: int) -> list[AgendaMedica]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM AgendaMedica
             WHERE medico_id = ?
             ORDER BY dia_semana, hora_inicio
        """, (medico_id,))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_para_agenda(row) for row in rows]

    def medico_atende_no_horario(self, medico_id: int, dia_semana: int, hora: time) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        hora_str = hora.strftime("%H:%M")

        cursor.execute("""
            SELECT COUNT(*) as total
              FROM AgendaMedica
             WHERE medico_id   = ?
               AND dia_semana  = ?
               AND hora_inicio <= ?
               AND hora_fim    >= ?
        """, (medico_id, dia_semana, hora_str, hora_str))

        row = cursor.fetchone()
        conn.close()

        return row["total"] > 0

    def deletar(self, id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM AgendaMedica WHERE id = ?", (id,))

        conn.commit()
        deletado = cursor.rowcount > 0
        conn.close()

        return deletado

    def _row_para_agenda(self, row) -> AgendaMedica:
        return AgendaMedica(
            id          = row["id"],
            medico_id   = row["medico_id"],
            dia_semana  = row["dia_semana"],
            hora_inicio = time.fromisoformat(row["hora_inicio"]),
            hora_fim    = time.fromisoformat(row["hora_fim"])
        )