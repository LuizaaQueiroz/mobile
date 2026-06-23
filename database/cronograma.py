"""
database/cronograma.py
======================
CRUD de slots do cronograma semanal.
"""

from .db import get_conn

DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def _row_para_dict(row) -> dict:
    return {
        "id":         row["id"],
        "usuario_id": row["usuario_id"],
        "dia":        row["dia"],
        "materia":    row["materia"],
        "horario":    row["horario"],
    }


def criar(usuario_id: int, dia: str, materia: str, horario: str) -> int:
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO cronograma (usuario_id, dia, materia, horario) VALUES (?, ?, ?, ?)",
            (usuario_id, dia, materia.strip(), horario.strip()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def listar_por_dia(usuario_id: int) -> dict[str, list[dict]]:
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM cronograma WHERE usuario_id = ? ORDER BY id ASC",
            (usuario_id,),
        ).fetchall()

        resultado: dict[str, list[dict]] = {dia: [] for dia in DIAS}
        for row in rows:
            d = row["dia"]
            if d in resultado:
                resultado[d].append(_row_para_dict(row))
        return resultado
    finally:
        conn.close()


def excluir(slot_id: int) -> None:
    conn = get_conn()
    try:
        conn.execute("DELETE FROM cronograma WHERE id = ?", (slot_id,))
        conn.commit()
    finally:
        conn.close()