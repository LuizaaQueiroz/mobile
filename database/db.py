"""
database/db.py
==============
Conexão central com o SQLite e criação das tabelas na primeira execução.
"""

import sqlite3
import pathlib

DB_PATH = pathlib.Path(__file__).parent.parent / "studyflow.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    _criar_tabelas(conn)
    return conn


def _criar_tabelas(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT    NOT NULL,
            email     TEXT    NOT NULL UNIQUE,
            senha     TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tarefas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id  INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            nome        TEXT    NOT NULL,
            prioridade  TEXT    NOT NULL DEFAULT 'Média',
            concluida   INTEGER NOT NULL DEFAULT 0,
            data_limite TEXT,
            criada_em   TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS anotacoes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id  INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            materia     TEXT    NOT NULL,
            titulo      TEXT    NOT NULL,
            conteudo    TEXT    NOT NULL,
            criada_em   TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS cronograma (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id  INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            dia         TEXT    NOT NULL,
            materia     TEXT    NOT NULL,
            horario     TEXT    NOT NULL
        );
    """)
    conn.commit()