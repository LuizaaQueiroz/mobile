"""
views/anotacoes.py
==================
View de Anotações — com persistência em SQLite.
"""

import flet as ft
from theme.paleta import criar_card
import database.anotacoes as db_anotacoes


def view_anotacoes(p, estado, page):

    usuario = estado.get("usuario")
    if not usuario:
        return ft.ListView(
            expand=True, padding=20,
            controls=[ft.Text(
                "⚠️ Faça login na aba Usuário para ver suas anotações.",
                color=p["danger"], size=15,
            )],
        )

    usuario_id = usuario["id"]

    campo_materia = ft.TextField(
        label="Matéria", border_radius=12,
        prefix_icon=ft.Icons.BOOK, width=200,
    )
    campo_titulo = ft.TextField(
        label="Título", border_radius=12,
        prefix_icon=ft.Icons.TITLE, expand=True,
    )
    campo_conteudo = ft.TextField(
        label="Anotação", border_radius=12,
        multiline=True, min_lines=3, max_lines=6, expand=True,
    )

    def adicionar_nota(e):
        materia  = campo_materia.value.strip()
        titulo   = campo_titulo.value.strip()
        conteudo = campo_conteudo.value.strip()

        if not materia or not titulo or not conteudo:
            page.show_dialog(ft.SnackBar(
                content=ft.Text("Preencha todos os campos."), bgcolor=ft.Colors.RED,
            ))
            return

        db_anotacoes.criar(usuario_id, materia, titulo, conteudo)

        campo_materia.value  = ""
        campo_titulo.value   = ""
        campo_conteudo.value = ""

        page.show_dialog(ft.SnackBar(
            content=ft.Text("Anotação salva!"), bgcolor=ft.Colors.GREEN,
        ))

        lista_col.controls = _build_lista()
        page.update()

    def remover_nota(anotacao_id: int):
        db_anotacoes.excluir(anotacao_id)
        lista_col.controls = _build_lista()
        page.update()

    def _build_lista():
        notas = db_anotacoes.listar(usuario_id)
        if not notas:
            return [ft.Text("Nenhuma anotação ainda.", color=p["subtext"])]

        items = []
        for nota in notas:
            items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    nota["materia"], size=11,
                                    weight=ft.FontWeight.BOLD, color="#ffffff",
                                ),
                                bgcolor=p["primary"], border_radius=20,
                                padding=ft.Padding(left=10, top=4, right=10, bottom=4),
                            ),
                            ft.Text(
                                nota["titulo"], size=15,
                                weight=ft.FontWeight.BOLD, color=p["text"], expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=p["danger"], tooltip="Remover nota",
                                on_click=lambda e, aid=nota["id"]: remover_nota(aid),
                            ),
                        ], spacing=8),
                        ft.Text(nota["conteudo"], color=p["subtext"], size=13),
                        ft.Text(f"📅 {nota['criada_em'][:16]}", size=10, color=p["subtext"]),
                    ], spacing=6),
                    bgcolor=p["card"], border_radius=14, padding=15,
                )
            )
        return items

    lista_col = ft.Column(controls=_build_lista(), spacing=10)

    return ft.ListView(
        expand=True, padding=20, spacing=20,
        controls=[
            ft.Text("Registre conteúdos por matéria. Dados salvos no banco local.", color=p["subtext"]),
            criar_card(
                "Nova Anotação",
                ft.Column([
                    ft.Row([campo_materia, campo_titulo], spacing=10),
                    campo_conteudo,
                    ft.Button(content="Salvar Anotação", icon=ft.Icons.SAVE, on_click=adicionar_nota),
                ], spacing=12),
                p,
            ),
            criar_card("Minhas Anotações", lista_col, p),
        ],
    )