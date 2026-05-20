import flet as ft
from theme.paleta import criar_card


def view_tarefas(p, estado, campos, callbacks):
    # Desempacota os controles de formulário recebidos do app.py
    campo_tarefa      = campos["campo_tarefa"]
    prioridade        = campos["prioridade"]
    slider_foco       = campos["slider_foco"]
    radio_filtro      = campos["radio_filtro"]
    checkbox_lembrete = campos["checkbox_lembrete"]
    date_picker       = campos["date_picker"]
    page              = campos["page"]

    # Desempacota os callbacks de lógica recebidos do app.py
    adicionar_tarefa  = callbacks["adicionar_tarefa"]
    concluir_tarefa   = callbacks["concluir_tarefa"]
    remover_tarefa    = callbacks["remover_tarefa"]
    limpar_tarefas    = callbacks["limpar_tarefas"]
    mostrar_snack     = callbacks["mostrar_snack"]

    # ==========================================================================
    # SLIDER DE FOCO → duração do ciclo de foco no Pomodoro
    # Converte o valor 0–100 para 5–50 minutos e salva no estado do Pomodoro
    # Fórmula: 5min no mínimo + escala proporcional até 50min no máximo
    # ==========================================================================

    def _minutos_de_foco():
        """Converte o valor do slider (0–100) para minutos (5–50)."""
        return max(5, int(slider_foco.value / 2))

    def atualizar_foco(e):
        """
        Chamado ao soltar o slider.
        Atualiza a duração do ciclo de foco no estado do Pomodoro.
        Se o Pomodoro ainda não foi aberto, inicializa o sub-estado antes.
        """
        minutos = _minutos_de_foco()

        # Garante que o sub-estado do Pomodoro existe antes de escrever nele
        if "pomodoro" not in estado:
            estado["pomodoro"] = {
                "segundos_restantes": minutos * 60,
                "rodando":            False,
                "modo":               "foco",
                "ciclos":             0,
            }
        else:
            # Só atualiza o tempo se o Pomodoro não estiver rodando
            # e se o modo atual for foco (evita sobrescrever uma pausa ativa)
            pm = estado["pomodoro"]
            if not pm["rodando"] and pm["modo"] == "foco":
                pm["segundos_restantes"] = minutos * 60

        mostrar_snack(
            f"⏱ Ciclo de foco ajustado para {minutos} minutos.",
            ft.Colors.INDIGO_600,
        )
        page.update()

    # Conecta o handler ao slider
    slider_foco.on_change_end = atualizar_foco

    # ==========================================================================
    # CHECKBOX DE LEMBRETE → SnackBar ao adicionar tarefa
    # Quando marcado, exibe mensagem motivacional ao salvar uma nova tarefa
    # ==========================================================================

    def adicionar_com_lembrete(e):
        """
        Wrapper do callback original de adição.
        Após adicionar, dispara o lembrete se o checkbox estiver ativo.
        """
        adicionar_tarefa(e)

        if checkbox_lembrete.value:
            minutos = _minutos_de_foco()
            mostrar_snack(
                f"🔔 Lembrete: use o Pomodoro ({minutos} min) para focar nessa tarefa!",
                ft.Colors.ORANGE_700,
            )

    # ==========================================================================
    # RADIO FILTRO → filtra a lista exibida
    # Todas: exibe todas | Pendentes: feito=False | Concluídas: feito=True
    # ==========================================================================

    filtro = radio_filtro.value or "Todas"

    tarefas_filtradas = [
        (i, t) for i, t in enumerate(estado["tarefas"])
        if filtro == "Todas"
        or (filtro == "Pendentes"  and not t["feito"])
        or (filtro == "Concluídas" and     t["feito"])
    ]

    # ==========================================================================
    # LISTA DE CARDS DE TAREFAS
    # Renderiza apenas as tarefas que passaram pelo filtro ativo
    # ==========================================================================

    lista = []

    for i, tarefa in tarefas_filtradas:

        # Cor conforme prioridade
        if tarefa["prioridade"] == "Alta":
            cor = p["danger"]
        elif tarefa["prioridade"] == "Média":
            cor = p["warning"]
        else:
            cor = p["success"]

        item = ft.Container(
            content=ft.Row(
                [
                    # Checkbox: alterna feito/pendente pelo índice original (não filtrado)
                    ft.Checkbox(
                        value=tarefa["feito"],
                        on_change=lambda e, idx=i: concluir_tarefa(idx),
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                tarefa["nome"],
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=p["text"],
                            ),
                            ft.Text(
                                f"Prioridade: {tarefa['prioridade']}",
                                size=12,
                                color=cor,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.FLAG, color=cor),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=p["danger"],
                        tooltip="Remover tarefa",
                        on_click=lambda e, idx=i: remover_tarefa(idx),
                    ),
                ]
            ),
            bgcolor=p["card"],
            border_radius=14,
            padding=15,
        )
        lista.append(item)

    # Placeholder quando nenhuma tarefa passa pelo filtro
    if not lista:
        lista.append(
            ft.Text(
                "Nenhuma tarefa encontrada.",
                size=13,
                color=p["subtext"],
            )
        )

    # ==========================================================================
    # LAYOUT FINAL
    # ==========================================================================
    return ft.ListView(
        expand=True,
        padding=20,
        spacing=20,
        controls=[
            criar_card(
                "Adicionar Tarefa",
                ft.Column(
                    [
                        campo_tarefa,
                        ft.Row(
                            [
                                prioridade,
                                ft.Button(
                                    content="Adicionar",
                                    icon=ft.Icons.ADD,
                                    # Usa o wrapper que inclui o lembrete
                                    on_click=adicionar_com_lembrete,
                                ),
                            ]
                        ),
                        ft.Text("Nível de foco (duração do Pomodoro)", color=p["subtext"]),
                        slider_foco,
                        ft.Text(
                            f"Ciclo atual: {_minutos_de_foco()} minutos",
                            size=11,
                            color=p["primary"],
                        ),
                        radio_filtro,
                        checkbox_lembrete,
                        ft.Row(
                            [
                                ft.Button(
                                    content="Selecionar Data",
                                    icon=ft.Icons.DATE_RANGE,
                                    on_click=lambda e: page.show_dialog(date_picker),
                                ),
                                ft.OutlinedButton(
                                    content="Limpar Tudo",
                                    icon=ft.Icons.DELETE,
                                    on_click=limpar_tarefas,
                                ),
                            ]
                        ),
                    ],
                    spacing=15,
                ),
                p,
            ),

            criar_card(
                # Título do card reflete o filtro ativo
                f"Lista de Tarefas — {filtro}",
                ft.Column(lista, spacing=10),
                p,
            ),
        ],
    )