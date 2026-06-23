"""
database/anotacoes.py
=====================
CRUD de anotações.
"""

from .db import get_conn


def _row_para_dict(row) -> dict:
    return {
        "id":         row["id"],
        "usuario_id": row["usuario_id"],
        "materia":    row["materia"],
        "titulo":     row["titulo"],
        "conteudo":   row["conteudo"],
        "criada_em":  row["criada_em"],
    }


def criar(usuario_id: int, materia: str, titulo: str, conteudo: str) -> int:
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO anotacoes (usuario_id, materia, titulo, conteudo) VALUES (?, ?, ?, ?)",
            (usuario_id, materia.strip(), titulo.strip(), conteudo.strip()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def listar(usuario_id: int) -> list[dict]:
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM anotacoes WHERE usuario_id = ? ORDER BY id DESC",
            (usuario_id,),
        ).fetchall()
        return [_row_para_dict(r) for r in rows]
    finally:
        conn.close()


def excluir(anotacao_id: int) -> None:
    conn = get_conn()
    try:
        conn.execute("DELETE FROM anotacoes WHERE id = ?", (anotacao_id,))
        conn.commit()
    finally:
        conn.close()