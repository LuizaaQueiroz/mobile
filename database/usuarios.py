"""
database/usuarios.py
====================
CRUD de usuários.
"""

import hashlib
from .db import get_conn


def _hash(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def _row_para_dict(row) -> dict | None:
    if row is None:
        return None
    return {
        "id":    row["id"],
        "nome":  row["nome"],
        "email": row["email"],
    }


def criar_usuario(nome: str, email: str, senha: str) -> int | None:
    try:
        conn = get_conn()
        cur  = conn.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome.strip(), email.strip().lower(), _hash(senha)),
        )
        conn.commit()
        return cur.lastrowid
    except Exception:
        return None
    finally:
        conn.close()


def autenticar(email: str, senha: str) -> dict | None:
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email.strip().lower(), _hash(senha)),
        ).fetchone()
        return _row_para_dict(row)
    finally:
        conn.close()


def buscar_por_id(usuario_id: int) -> dict | None:
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (usuario_id,),
        ).fetchone()
        return _row_para_dict(row)
    finally:
        conn.close()