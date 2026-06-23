"""
database/tarefas.py
===================
CRUD de tarefas.
"""

from .db import get_conn


def _row_para_dict(row) -> dict:
    return {
        "id":          row["id"],
        "usuario_id":  row["usuario_id"],
        "nome":        row["nome"],
        "prioridade":  row["prioridade"],
        "concluida":   bool(row["concluida"]),
        "data_limite": row["data_limite"],
        "criada_em":   row["criada_em"],
    }


def criar(usuario_id: int, nome: str, prioridade: str = "Média", data_limite: str | None = None) -> int:
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO tarefas (usuario_id, nome, prioridade, data_limite) VALUES (?, ?, ?, ?)",
            (usuario_id, nome.strip(), prioridade, data_limite),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def listar(usuario_id: int, filtro: str = "Todas") -> list[dict]:
    conn = get_conn()
    try:
        if filtro == "Pendentes":
            where = "AND concluida = 0"
        elif filtro == "Concluídas":
            where = "AND concluida = 1"
        else:
            where = ""

        rows = conn.execute(
            f"SELECT * FROM tarefas WHERE usuario_id = ? {where} ORDER BY id DESC",
            (usuario_id,),
        ).fetchall()
        return [_row_para_dict(r) for r in rows]
    finally:
        conn.close()


def concluir(tarefa_id: int, valor: bool) -> None:
    conn = get_conn()
    try:
        conn.execute(
            "UPDATE tarefas SET concluida = ? WHERE id = ?",
            (int(valor), tarefa_id),
        )
        conn.commit()
    finally:
        conn.close()


def excluir(tarefa_id: int) -> None:
    conn = get_conn()
    try:
        conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        conn.commit()
    finally:
        conn.close()


def limpar_todas(usuario_id: int) -> None:
    conn = get_conn()
    try:
        conn.execute("DELETE FROM tarefas WHERE usuario_id = ?", (usuario_id,))
        conn.commit()
    finally:
        conn.close()