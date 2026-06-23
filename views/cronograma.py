"""
views/cronograma.py
===================
View de Cronograma Semanal — com persistência em SQLite.
"""

import flet as ft
from theme.paleta import criar_card
import database.cronograma as db_cronograma

DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def view_cronograma(p, estado, page):

    usuario = estado.get("usuario")
    if not usuario:
        return ft.ListView(
            expand=True, padding=20,
            controls=[ft.Text(
                "⚠️ Faça login na aba Usuário para ver seu cronograma.",
                color=p["danger"], size=15,
            )],
        )

    usuario_id = usuario["id"]

    campo_materia = ft.TextField(
        label="Matéria", border_radius=12,
        prefix_icon=ft.Icons.BOOK, expand=True,
    )
    campo_horario = ft.TextField(
        label="Horário  (ex: 14:00 – 15:30)", border_radius=12,
        prefix_icon=ft.Icons.ACCESS_TIME, width=220,
    )
    dropdown_dia = ft.Dropdown(
        label="Dia da semana", width=180, value="Segunda",
        options=[ft.dropdown.Option(d) for d in DIAS],
    )

    def adicionar_slot(e):
        materia = campo_materia.value.strip()
        horario = campo_horario.value.strip()
        dia     = dropdown_dia.value

        if not materia or not horario:
            page.show_dialog(ft.SnackBar(
                content=ft.Text("Preencha matéria e horário."), bgcolor=ft.Colors.RED,
            ))
            return

        db_cronograma.criar(usuario_id, dia, materia, horario)
        campo_materia.value = ""
        campo_horario.value = ""

        page.show_dialog(ft.SnackBar(
            content=ft.Text(f"Adicionado em {dia}!"), bgcolor=ft.Colors.GREEN,
        ))

        grade_col.controls = _build_grade()
        page.update()

    def remover_slot(slot_id: int):
        db_cronograma.excluir(slot_id)
        grade_col.controls = _build_grade()
        page.update()

    def _build_grade():
        slots_por_dia = db_cronograma.listar_por_dia(usuario_id)
        colunas = []

        for dia in DIAS:
            slots = slots_por_dia[dia]
            itens = []
            for slot in slots:
                itens.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(slot["materia"], size=13,
                                        weight=ft.FontWeight.BOLD, color=p["text"]),
                                ft.Text(slot["horario"], size=11, color=p["subtext"]),
                            ], spacing=2, expand=True),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE, icon_size=14,
                                icon_color=p["danger"], tooltip="Remover",
                                on_click=lambda e, sid=slot["id"]: remover_slot(sid),
                            ),
                        ]),
                        bgcolor=p["bg"], border_radius=8,
                        padding=ft.Padding(left=8, right=8, top=6, bottom=6),
                    )
                )

            colunas.append(
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Text(
                                dia, size=13, weight=ft.FontWeight.BOLD, color="#ffffff",
                            ),
                            bgcolor=p["primary"], border_radius=8,
                            padding=ft.Padding(left=10, right=10, top=6, bottom=6),
                            alignment=ft.Alignment.CENTER,
                        ),
                        *(itens if itens else [ft.Text("—", color=p["subtext"], size=12)]),
                    ], spacing=6),
                    expand=True, padding=8,
                )
            )

        return [ft.Row(colunas, spacing=6)]

    grade_col = ft.Column(controls=_build_grade(), spacing=0)

    return ft.ListView(
        expand=True, padding=20, spacing=20,
        controls=[
            ft.Text(
                "Organize seus estudos ao longo da semana. Dados salvos no banco local.",
                color=p["subtext"],
            ),
            criar_card(
                "Adicionar ao Cronograma",
                ft.Column([
                    ft.Row([campo_materia, campo_horario], spacing=10),
                    ft.Row([
                        dropdown_dia,
                        ft.Button(content="Adicionar", icon=ft.Icons.ADD, on_click=adicionar_slot),
                    ], spacing=10),
                ], spacing=12),
                p,
            ),
            criar_card("Grade Semanal", grade_col, p),
        ],
    )