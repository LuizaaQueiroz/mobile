import flet as ft
from theme.paleta import criar_card


def view_tarefas(p, estado, campos, callbacks):
    # Desempacota os controles de formulário recebidos do app.py
    campo_tarefa      = campos["campo_tarefa"]       # TextField de nova tarefa
    prioridade        = campos["prioridade"]          # Dropdown de prioridade
    slider_foco       = campos["slider_foco"]         # Slider de nível de foco
    radio_filtro      = campos["radio_filtro"]        # RadioGroup de filtro
    checkbox_lembrete = campos["checkbox_lembrete"]   # Checkbox de lembretes
    date_picker       = campos["date_picker"]         # DatePicker (serviço)
    page              = campos["page"]                # Referência à página (para abrir dialogs)

    # Desempacota os callbacks de lógica recebidos do app.py
    adicionar_tarefa  = callbacks["adicionar_tarefa"]  # Adiciona tarefa ao estado
    concluir_tarefa   = callbacks["concluir_tarefa"]   # Alterna feito/pendente
    remover_tarefa = callbacks["remover_tarefa"]       # Remove tarefa do estado
    limpar_tarefas    = callbacks["limpar_tarefas"]    # Remove todas as tarefas

    # -------------------------------------------------------------------------
    # Monta a lista de cards de tarefas existentes
    # -------------------------------------------------------------------------
    lista = []

    for i, tarefa in enumerate(estado["tarefas"]):

        # Define a cor do item conforme a prioridade
        if tarefa["prioridade"] == "Alta":
            cor = p["danger"]
        elif tarefa["prioridade"] == "Média":
            cor = p["warning"]
        else:
            cor = p["success"]

        # Card individual de tarefa: checkbox + nome/prioridade + ícone de bandeira
        item = ft.Container(
            content=ft.Row(
                [
                    # Checkbox: ao mudar, chama concluir_tarefa com o índice correto
                    # idx=i captura o valor atual de i no loop (evita bug de closure)
                    ft.Checkbox(
                        value=tarefa["feito"],
                        on_change=lambda e, idx=i: concluir_tarefa(idx),
                    ),
                    ft.Column(
                        [
                            ft.Text(tarefa["nome"], size=16, weight=ft.FontWeight.BOLD, color=p["text"]),
                            ft.Text(f"Prioridade: {tarefa['prioridade']}", size=12, color=cor),
                        ],
                        spacing=2,
                        expand=True,  # Ocupa o espaço horizontal disponível
                    ),
                    ft.Icon(ft.Icons.FLAG, color=cor),  # Indicador visual de prioridade
                    #botão de remoção: chama remover_tarefa com o índice correto
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

    # -------------------------------------------------------------------------
    # Monta e retorna a view completa como ListView rolável
    # -------------------------------------------------------------------------
    return ft.ListView(
        expand=True,   # Ocupa todo o espaço disponível na tela
        padding=20,
        spacing=20,
        controls=[
            ft.Text("✅ Tarefas", size=28, weight=ft.FontWeight.BOLD, color=p["text"]),

            # Card superior: formulário para adicionar nova tarefa
            criar_card(
                "Adicionar Tarefa",
                ft.Column(
                    [
                        campo_tarefa,  # TextField de entrada

                        ft.Row(
                            [
                                prioridade,  # Dropdown Baixa / Média / Alta
                                ft.Button(
                                    content="Adicionar",
                                    icon=ft.Icons.ADD,
                                    on_click=adicionar_tarefa,
                                ),
                            ]
                        ),

                        ft.Text("Nível de foco", color=p["subtext"]),
                        slider_foco,       # Slider 0–100%
                        radio_filtro,      # Filtro Todas / Pendentes / Concluídas
                        checkbox_lembrete, # Ativa/desativa lembretes

                        ft.Row(
                            [
                                ft.Button(
                                    content="Selecionar Data",
                                    icon=ft.Icons.DATE_RANGE,
                                    # Abre o DatePicker via show_dialog
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

            # Card inferior: lista de tarefas já cadastradas
            criar_card(
                "Lista de Tarefas",
                ft.Column(lista, spacing=10),
                p,
            ),
        ],
    )
