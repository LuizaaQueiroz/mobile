"""
views/tarefas.py
================
CRUD completo: Create, Read, Update, Delete
"""

import flet as ft
from theme.paleta import criar_card
import database.tarefas as db_tarefas


def view_tarefas(p, estado, campos, callbacks):

    campo_tarefa      = campos["campo_tarefa"]
    prioridade        = campos["prioridade"]
    slider_foco       = campos["slider_foco"]
    radio_filtro      = campos["radio_filtro"]
    checkbox_lembrete = campos["checkbox_lembrete"]
    date_picker       = campos["date_picker"]
    page              = campos["page"]

    adicionar_tarefa  = callbacks["adicionar_tarefa"]
    mostrar_snack     = callbacks["mostrar_snack"]

    usuario = estado.get("usuario")
    if not usuario:
        return ft.ListView(
            expand=True, padding=20,
            controls=[ft.Text(
                "⚠️ Faça login na aba Usuário para gerenciar suas tarefas.",
                color=p["danger"], size=15,
            )],
        )

    usuario_id = usuario["id"]

    # ------------------------------------------------------------------
    # Estado local de edição
    # ------------------------------------------------------------------
    editando = {"id": None}

    # Campo e dropdown de edição inline (separados dos campos do form principal)
    campo_edit_nome = ft.TextField(
        label="Editar nome", border_radius=12,
        prefix_icon=ft.Icons.EDIT, expand=True, visible=False,
    )
    drop_edit_prior = ft.Dropdown(
        label="Prioridade", width=150, visible=False,
        options=[
            ft.dropdown.Option("Baixa"),
            ft.dropdown.Option("Média"),
            ft.dropdown.Option("Alta"),
        ],
    )
    btn_confirmar_edit = ft.Button(
        content="Confirmar", icon=ft.Icons.CHECK, visible=False,
    )
    btn_cancelar_edit = ft.TextButton(
        "Cancelar", icon=ft.Icons.CLOSE, visible=False,
    )

    def _minutos_de_foco():
        return max(5, int(slider_foco.value / 2))

    def atualizar_foco(e):
        minutos = _minutos_de_foco()
        if "pomodoro" not in estado:
            estado["pomodoro"] = {
                "segundos_restantes": minutos * 60,
                "rodando": False,
                "modo": "foco",
                "ciclos": 0,
            }
        else:
            pm = estado["pomodoro"]
            if not pm["rodando"] and pm["modo"] == "foco":
                pm["segundos_restantes"] = minutos * 60
        mostrar_snack(f"⏱ Ciclo de foco ajustado para {minutos} minutos.", ft.Colors.INDIGO_600)
        page.update()

    slider_foco.on_change_end = atualizar_foco

    def adicionar_com_lembrete(e):
        adicionar_tarefa(e)
        if checkbox_lembrete.value:
            minutos = _minutos_de_foco()
            mostrar_snack(
                f"🔔 Lembrete: use o Pomodoro ({minutos} min) para focar nessa tarefa!",
                ft.Colors.ORANGE_700,
            )

    def concluir_tarefa(tarefa_id: int, valor: bool):
        db_tarefas.concluir(tarefa_id, valor)
        _sincronizar_estado()
        lista_col.controls = _build_lista()
        page.update()

    def remover_tarefa(tarefa_id: int):
        if editando["id"] == tarefa_id:
            _fechar_edicao()
        db_tarefas.excluir(tarefa_id)
        _sincronizar_estado()
        lista_col.controls = _build_lista()
        page.update()

    def limpar_tarefas(e):
        db_tarefas.limpar_todas(usuario_id)
        _fechar_edicao()
        _sincronizar_estado()
        lista_col.controls = _build_lista()
        page.update()

    def abrir_edicao(tarefa: dict):
        """Abre os campos de edição inline preenchidos com os dados da tarefa."""
        editando["id"]          = tarefa["id"]
        campo_edit_nome.value   = tarefa["nome"]
        drop_edit_prior.value   = tarefa["prioridade"]
        campo_edit_nome.visible = True
        drop_edit_prior.visible = True
        btn_confirmar_edit.visible = True
        btn_cancelar_edit.visible  = True
        lista_col.controls = _build_lista()
        page.update()

    def _fechar_edicao():
        editando["id"]             = None
        campo_edit_nome.visible    = False
        drop_edit_prior.visible    = False
        btn_confirmar_edit.visible = False
        btn_cancelar_edit.visible  = False

    def confirmar_edicao(e):
        nome = campo_edit_nome.value.strip()
        if not nome:
            mostrar_snack("Digite o nome da tarefa.", ft.Colors.RED)
            return
        db_tarefas.atualizar(editando["id"], nome, drop_edit_prior.value or "Média")
        _fechar_edicao()
        _sincronizar_estado()
        lista_col.controls = _build_lista()
        mostrar_snack("Tarefa atualizada!", ft.Colors.GREEN)
        page.update()

    btn_confirmar_edit.on_click = confirmar_edicao
    btn_cancelar_edit.on_click  = lambda e: (_fechar_edicao(), lista_col.__setattr__("controls", _build_lista()), page.update())

    def _sincronizar_estado():
        rows = db_tarefas.listar(usuario_id)
        estado["tarefas"] = [
            {"nome": r["nome"], "prioridade": r["prioridade"], "feito": r["concluida"]}
            for r in rows
        ]

    filtro = radio_filtro.value or "Todas"

    def _build_lista():
        tarefas = db_tarefas.listar(usuario_id, filtro)
        if not tarefas:
            return [ft.Text("Nenhuma tarefa encontrada.", size=13, color=p["subtext"])]

        items = []
        for tarefa in tarefas:
            cor = (
                p["danger"]  if tarefa["prioridade"] == "Alta"  else
                p["warning"] if tarefa["prioridade"] == "Média" else
                p["success"]
            )
            esta_editando = editando["id"] == tarefa["id"]

            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Checkbox(
                            value=tarefa["concluida"],
                            on_change=lambda e, tid=tarefa["id"]: concluir_tarefa(tid, e.control.value),
                        ),
                        ft.Column([
                            ft.Text(
                                tarefa["nome"], size=16,
                                weight=ft.FontWeight.BOLD, color=p["text"],
                            ),
                            ft.Text(f"Prioridade: {tarefa['prioridade']}", size=12, color=cor),
                            *(
                                [ft.Text(f"📅 Até: {tarefa['data_limite']}", size=11, color=p["subtext"])]
                                if tarefa.get("data_limite") else []
                            ),
                        ], spacing=2, expand=True),
                        ft.Icon(ft.Icons.FLAG, color=cor),
                        # Botão editar
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color=p["primary"],
                            tooltip="Editar tarefa",
                            on_click=lambda e, t=tarefa: abrir_edicao(t),
                        ),
                        # Botão deletar
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color=p["danger"],
                            tooltip="Remover tarefa",
                            on_click=lambda e, tid=tarefa["id"]: remover_tarefa(tid),
                        ),
                    ]),
                    # Campos de edição inline — visíveis só na tarefa sendo editada
                    *(
                        [ft.Row([campo_edit_nome, drop_edit_prior], spacing=10),
                         ft.Row([btn_confirmar_edit, btn_cancelar_edit], spacing=8)]
                        if esta_editando else []
                    ),
                ], spacing=6),
                bgcolor=p["card"],
                border_radius=14,
                padding=15,
                border=ft.Border.all(2, p["primary"]) if esta_editando else None,
            )
            items.append(card)
        return items

    _sincronizar_estado()
    lista_col = ft.Column(controls=_build_lista(), spacing=10)

    return ft.ListView(
        expand=True, padding=20, spacing=20,
        controls=[
            criar_card(
                "Adicionar Tarefa",
                ft.Column([
                    campo_tarefa,
                    ft.Row([
                        prioridade,
                        ft.Button(content="Adicionar", icon=ft.Icons.ADD, on_click=adicionar_com_lembrete),
                    ]),
                    ft.Text("Nível de foco (duração do Pomodoro)", color=p["subtext"]),
                    slider_foco,
                    ft.Text(f"Ciclo atual: {_minutos_de_foco()} minutos", size=11, color=p["primary"]),
                    radio_filtro,
                    checkbox_lembrete,
                    ft.Row([
                        ft.Button(
                            content="Selecionar Data", icon=ft.Icons.DATE_RANGE,
                            on_click=lambda e: page.show_dialog(date_picker),
                        ),
                        ft.OutlinedButton(
                            content="Limpar Tudo", icon=ft.Icons.DELETE, on_click=limpar_tarefas,
                        ),
                    ]),
                ], spacing=15),
                p,
            ),
            criar_card(f"Lista de Tarefas — {filtro}", lista_col, p),
        ],
    )