"""
views/anotacoes.py
==================
CRUD completo: Create, Read, Update, Delete
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

    # ------------------------------------------------------------------
    # Estado local de edição
    # Quando editando_id tem valor, o formulário está em modo edição
    # ------------------------------------------------------------------
    editando = {"id": None}

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

    # Texto do botão muda conforme o modo (criar ou editar)
    btn_salvar = ft.Button(
        content="Salvar Anotação",
        icon=ft.Icons.SAVE,
    )

    titulo_form = ft.Text(
        "Nova Anotação",
        size=15,
        weight=ft.FontWeight.BOLD,
        color=p["text"],
    )

    def _limpar_form():
        campo_materia.value  = ""
        campo_titulo.value   = ""
        campo_conteudo.value = ""
        editando["id"]       = None
        btn_salvar.content   = "Salvar Anotação"
        btn_salvar.icon      = ft.Icons.SAVE
        titulo_form.value    = "Nova Anotação"

    def salvar(e):
        materia  = campo_materia.value.strip()
        titulo   = campo_titulo.value.strip()
        conteudo = campo_conteudo.value.strip()

        if not materia or not titulo or not conteudo:
            page.show_dialog(ft.SnackBar(
                content=ft.Text("Preencha todos os campos."), bgcolor=ft.Colors.RED,
            ))
            return

        if editando["id"] is None:
            # CREATE
            db_anotacoes.criar(usuario_id, materia, titulo, conteudo)
            msg = "Anotação salva!"
        else:
            # UPDATE
            db_anotacoes.atualizar(editando["id"], materia, titulo, conteudo)
            msg = "Anotação atualizada!"

        _limpar_form()
        page.show_dialog(ft.SnackBar(content=ft.Text(msg), bgcolor=ft.Colors.GREEN))
        lista_col.controls = _build_lista()
        page.update()

    btn_salvar.on_click = salvar

    def editar_nota(nota: dict):
        """Preenche o formulário com os dados da nota para edição."""
        editando["id"]       = nota["id"]
        campo_materia.value  = nota["materia"]
        campo_titulo.value   = nota["titulo"]
        campo_conteudo.value = nota["conteudo"]
        btn_salvar.content   = "Atualizar Anotação"
        btn_salvar.icon      = ft.Icons.EDIT
        titulo_form.value    = "Editar Anotação"
        page.update()

    def cancelar_edicao(e):
        _limpar_form()
        page.update()

    def remover_nota(anotacao_id: int):
        if editando["id"] == anotacao_id:
            _limpar_form()
        db_anotacoes.excluir(anotacao_id)
        lista_col.controls = _build_lista()
        page.update()

    def _build_lista():
        notas = db_anotacoes.listar(usuario_id)
        if not notas:
            return [ft.Text("Nenhuma anotação ainda.", color=p["subtext"])]

        items = []
        for nota in notas:
            editando_agora = editando["id"] == nota["id"]
            items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            # Badge da matéria
                            ft.Container(
                                content=ft.Text(
                                    nota["materia"], size=11,
                                    weight=ft.FontWeight.BOLD, color="#ffffff",
                                ),
                                bgcolor=p["primary"] if not editando_agora else p["warning"],
                                border_radius=20,
                                padding=ft.Padding(left=10, top=4, right=10, bottom=4),
                            ),
                            ft.Text(
                                nota["titulo"], size=15,
                                weight=ft.FontWeight.BOLD, color=p["text"], expand=True,
                            ),
                            # Botão editar
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_color=p["primary"],
                                tooltip="Editar nota",
                                on_click=lambda e, n=nota: editar_nota(n),
                            ),
                            # Botão deletar
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=p["danger"],
                                tooltip="Remover nota",
                                on_click=lambda e, aid=nota["id"]: remover_nota(aid),
                            ),
                        ], spacing=8),
                        ft.Text(nota["conteudo"], color=p["subtext"], size=13),
                        ft.Text(
                            f"📅 {nota['criada_em'][:16]}",
                            size=10, color=p["subtext"],
                        ),
                    ], spacing=6),
                    bgcolor=p["card"],
                    border_radius=14,
                    padding=15,
                    border=ft.Border.all(2, p["warning"]) if editando_agora else None,
                )
            )
        return items

    lista_col = ft.Column(controls=_build_lista(), spacing=10)

    # Botão cancelar edição — só aparece quando está editando
    btn_cancelar = ft.TextButton(
        "Cancelar edição",
        icon=ft.Icons.CLOSE,
        on_click=cancelar_edicao,
        style=ft.ButtonStyle(color=p["danger"]),
    )

    return ft.ListView(
        expand=True, padding=20, spacing=20,
        controls=[
            ft.Text(
                "Registre conteúdos por matéria. Dados salvos no banco local.",
                color=p["subtext"],
            ),
            criar_card(
                "Anotações",
                ft.Column([
                    titulo_form,
                    ft.Row([campo_materia, campo_titulo], spacing=10),
                    campo_conteudo,
                    ft.Row([btn_salvar, btn_cancelar], spacing=10),
                ], spacing=12),
                p,
            ),
            criar_card("Minhas Anotações", lista_col, p),
        ],
    )