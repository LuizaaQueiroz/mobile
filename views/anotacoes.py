import flet as ft
from theme.paleta import criar_card


def view_anotacoes(p, estado, page):
    """
    View de Anotações por Matéria.
    Permite criar e remover anotações vinculadas a uma matéria.

    Parâmetros:
        p      — dicionário de cores da paleta ativa
        estado — dicionário global de estado do app
        page   — instância da página Flet (necessária para page.update)

    Estado local (dentro de estado["anotacoes"]):
        lista — list of dicts: {"materia": str, "titulo": str, "conteudo": str}
    """

    # Inicializa o sub-estado de anotações se ainda não existir
    if "anotacoes" not in estado:
        estado["anotacoes"] = {"lista": []}

    # Atalho para o sub-estado (referência, não cópia)
    an = estado["anotacoes"]

    # ==========================================================================
    # CAMPOS DO FORMULÁRIO
    # ==========================================================================

    # Campo para identificar a matéria da anotação
    campo_materia = ft.TextField(
        label="Matéria",
        border_radius=12,
        prefix_icon=ft.Icons.BOOK,
        width=200,
    )

    # Campo para o título da anotação — expande para ocupar o espaço restante
    campo_titulo = ft.TextField(
        label="Título",
        border_radius=12,
        prefix_icon=ft.Icons.TITLE,
        expand=True,
    )

    # Campo multiline para o conteúdo da anotação — cresce até 6 linhas
    campo_conteudo = ft.TextField(
        label="Anotação",
        border_radius=12,
        multiline=True,
        min_lines=3,
        max_lines=6,
        expand=True,
    )

    # ==========================================================================
    # LÓGICA DOS BOTÕES
    # ==========================================================================

    def adicionar_nota(e):
        """
        Valida os campos e salva a nova anotação no estado global.
        Limpa o formulário e reconstrói a lista após salvar.
        """
        materia  = campo_materia.value.strip()
        titulo   = campo_titulo.value.strip()
        conteudo = campo_conteudo.value.strip()

        # Todos os campos são obrigatórios
        if not materia or not titulo or not conteudo:
            page.show_dialog(ft.SnackBar(
                content=ft.Text("Preencha todos os campos."),
                bgcolor=ft.Colors.RED,
            ))
            return

        # Adiciona a nova nota ao estado global
        an["lista"].append({
            "materia":  materia,
            "titulo":   titulo,
            "conteudo": conteudo,
        })

        # Limpa os campos para a próxima entrada
        campo_materia.value  = ""
        campo_titulo.value   = ""
        campo_conteudo.value = ""

        page.show_dialog(ft.SnackBar(
            content=ft.Text("Anotação salva!"),
            bgcolor=ft.Colors.GREEN,
        ))

        # Primeiro update: confirma o SnackBar e limpa os campos
        page.update()

        # Reconstrói a lista e aplica o segundo update para exibir a nova nota
        lista_col.controls = _build_lista()
        page.update()

    def remover_nota(index):
        """Remove a nota do índice especificado e reconstrói a lista."""
        an["lista"].pop(index)
        lista_col.controls = _build_lista()
        page.update()

    # ==========================================================================
    # RENDERIZAÇÃO DA LISTA DE NOTAS
    # ==========================================================================

    def _build_lista():
        """
        Constrói a lista de cards de notas existentes.
        Retorna placeholder se não houver anotações.
        """
        if not an["lista"]:
            return [ft.Text("Nenhuma anotação ainda.", color=p["subtext"])]

        items = []
        for i, nota in enumerate(an["lista"]):
            items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    # Badge pill com o nome da matéria sobre fundo primário
                                    ft.Container(
                                        content=ft.Text(
                                            nota["materia"],
                                            size=11,
                                            weight=ft.FontWeight.BOLD,
                                            color="#ffffff",
                                        ),
                                        bgcolor=p["primary"],
                                        border_radius=20,
                                        padding=ft.Padding(
                                            left=10, top=4, right=10, bottom=4
                                        ),
                                    ),
                                    # Título da nota — expande para ocupar o espaço disponível
                                    ft.Text(
                                        nota["titulo"],
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        color=p["text"],
                                        expand=True,
                                    ),
                                    # Botão de remoção — captura o índice via default arg
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=p["danger"],
                                        tooltip="Remover nota",
                                        on_click=lambda e, idx=i: remover_nota(idx),
                                    ),
                                ],
                                spacing=8,
                            ),
                            # Conteúdo completo da anotação
                            ft.Text(nota["conteudo"], color=p["subtext"], size=13),
                        ],
                        spacing=6,
                    ),
                    bgcolor=p["card"],
                    border_radius=14,
                    padding=15,
                )
            )
        return items

    # Container mutável da lista — seus controls são substituídos a cada atualização
    lista_col = ft.Column(
        controls=_build_lista(),
        spacing=10,
    )

    # ==========================================================================
    # LAYOUT FINAL
    # ==========================================================================
    return ft.ListView(
        expand=True,
        padding=20,
        spacing=20,
        controls=[
            ft.Text("Registre conteúdos por matéria.", color=p["subtext"]),

            # Card com o formulário de criação de nova anotação
            criar_card(
                "Nova Anotação",
                ft.Column(
                    [
                        # Linha 1: matéria + título lado a lado
                        ft.Row([campo_materia, campo_titulo], spacing=10),
                        # Linha 2: campo de conteúdo multiline
                        campo_conteudo,
                        # Botão de salvamento
                        ft.Button(
                            content="Salvar Anotação",
                            icon=ft.Icons.SAVE,
                            on_click=adicionar_nota,
                        ),
                    ],
                    spacing=12,
                ),
                p,
            ),

            # Card com a lista de anotações salvas — atualizado dinamicamente
            criar_card("Minhas Anotações", lista_col, p),
        ],
    )