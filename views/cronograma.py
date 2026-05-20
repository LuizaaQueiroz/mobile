import flet as ft
from theme.paleta import criar_card


# Lista fixa dos dias da semana — usada tanto no dropdown quanto na grade
DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def view_cronograma(p, estado, page):
    """
    View de Cronograma Semanal.
    Permite adicionar e remover slots de estudo por dia da semana.

    Parâmetros:
        p      — dicionário de cores da paleta ativa
        estado — dicionário global de estado do app
        page   — instância da página Flet (necessária para page.update)

    Estado local (dentro de estado["cronograma"]):
        slots — dict com chave = dia da semana, valor = lista de dicts
                cada item: {"materia": str, "horario": str}
    """

    # Inicializa o sub-estado do cronograma com listas vazias para cada dia
    if "cronograma" not in estado:
        estado["cronograma"] = {"slots": {dia: [] for dia in DIAS}}

    # Atalho para o sub-estado (referência, não cópia)
    cr = estado["cronograma"]

    # ==========================================================================
    # CAMPOS DO FORMULÁRIO DE ADIÇÃO
    # ==========================================================================

    # Campo de texto para o nome da matéria
    campo_materia = ft.TextField(
        label="Matéria",
        border_radius=12,
        prefix_icon=ft.Icons.BOOK,
        expand=True,
    )

    # Campo de texto para o horário (formato livre, ex: "14:00 – 15:30")
    campo_horario = ft.TextField(
        label="Horário  (ex: 14:00 – 15:30)",
        border_radius=12,
        prefix_icon=ft.Icons.ACCESS_TIME,
        width=220,
    )

    # Dropdown para seleção do dia da semana — padrão: Segunda
    dropdown_dia = ft.Dropdown(
        label="Dia da semana",
        width=180,
        value="Segunda",
        options=[ft.dropdown.Option(d) for d in DIAS],
    )

    # ==========================================================================
    # LÓGICA DOS BOTÕES
    # ==========================================================================

    def adicionar_slot(e):
        """
        Valida os campos e adiciona o slot ao dia selecionado no estado.
        Após adicionar, limpa os campos e reconstrói a grade semanal.
        """
        materia = campo_materia.value.strip()
        horario = campo_horario.value.strip()
        dia     = dropdown_dia.value

        # Validação: ambos os campos são obrigatórios
        if not materia or not horario:
            page.show_dialog(ft.SnackBar(
                content=ft.Text("Preencha matéria e horário."),
                bgcolor=ft.Colors.RED,
            ))
            return

        # Insere o novo slot na lista do dia correspondente
        cr["slots"][dia].append({"materia": materia, "horario": horario})

        # Limpa os campos para a próxima entrada
        campo_materia.value = ""
        campo_horario.value = ""

        page.show_dialog(ft.SnackBar(
            content=ft.Text(f"Adicionado em {dia}!"),
            bgcolor=ft.Colors.GREEN,
        ))

        # Reconstrói a grade para refletir o novo slot
        grade_col.controls = _build_grade()
        page.update()

    def remover_slot(dia, index):
        """
        Remove o slot do índice especificado no dia informado.
        Reconstrói a grade após a remoção.
        """
        cr["slots"][dia].pop(index)
        grade_col.controls = _build_grade()
        page.update()

    # ==========================================================================
    # GRADE SEMANAL
    # Constrói uma coluna por dia da semana com os slots cadastrados
    # ==========================================================================

    def _build_grade():
        """
        Reconstrói a grade semanal com base no estado atual dos slots.
        Retorna uma lista com um único ft.Row contendo todas as colunas de dias.
        """
        colunas = []

        for dia in DIAS:
            slots = cr["slots"][dia]

            # Constrói um container por slot do dia
            itens = []
            for i, slot in enumerate(slots):
                itens.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        # Nome da matéria em destaque
                                        ft.Text(
                                            slot["materia"],
                                            size=13,
                                            weight=ft.FontWeight.BOLD,
                                            color=p["text"],
                                        ),
                                        # Horário em texto menor e apagado
                                        ft.Text(
                                            slot["horario"],
                                            size=11,
                                            color=p["subtext"],
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                # Botão de remoção do slot — captura dia e índice via default args
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_size=14,
                                    icon_color=p["danger"],
                                    tooltip="Remover",
                                    on_click=lambda e, d=dia, idx=i: remover_slot(d, idx),
                                ),
                            ]
                        ),
                        bgcolor=p["bg"],
                        border_radius=8,
                        padding=ft.Padding(left=8, right=8, top=6, bottom=6),
                    )
                )

            # Coluna do dia: cabeçalho colorido + lista de slots (ou "—" se vazio)
            colunas.append(
                ft.Container(
                    content=ft.Column(
                        [
                            # Cabeçalho com o nome do dia sobre fundo primário
                            ft.Container(
                                content=ft.Text(
                                    dia,
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color="#ffffff",
                                ),
                                bgcolor=p["primary"],
                                border_radius=8,
                                padding=ft.Padding(left=10, right=10, top=6, bottom=6),
                                alignment=ft.Alignment.CENTER,
                            ),
                            # Slots do dia ou traço indicando dia vazio
                            *(
                                itens
                                if itens
                                else [ft.Text("—", color=p["subtext"], size=12)]
                            ),
                        ],
                        spacing=6,
                    ),
                    expand=True,  # Cada dia ocupa espaço igual na Row
                    padding=8,
                )
            )

        # Retorna lista com um único Row horizontal contendo todas as colunas
        return [ft.Row(colunas, spacing=6)]

    # Container mutável da grade — seus controls são substituídos a cada atualização
    grade_col = ft.Column(
        controls=_build_grade(),
        spacing=0,
    )

    # ==========================================================================
    # LAYOUT FINAL
    # ==========================================================================
    return ft.ListView(
        expand=True,
        padding=20,
        spacing=20,
        controls=[
            ft.Text("Organize seus estudos ao longo da semana.", color=p["subtext"]),

            # Card com o formulário de adição de slots
            criar_card(
                "Adicionar ao Cronograma",
                ft.Column(
                    [
                        # Linha 1: campo de matéria + campo de horário
                        ft.Row([campo_materia, campo_horario], spacing=10),
                        # Linha 2: dropdown de dia + botão de adição
                        ft.Row(
                            [
                                dropdown_dia,
                                ft.Button(
                                    content="Adicionar",
                                    icon=ft.Icons.ADD,
                                    on_click=adicionar_slot,
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=12,
                ),
                p,
            ),

            # Card com a grade semanal — atualizado dinamicamente
            criar_card("Grade Semanal", grade_col, p),
        ],
    )