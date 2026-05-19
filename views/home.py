import flet as ft
from theme.paleta import criar_card


def view_home(p, estado, progress):

    # Contadores calculados a partir do estado atual
    total      = len(estado["tarefas"])
    concluidas = len([t for t in estado["tarefas"] if t["feito"]])

    # -------------------------------------------------------------------------
    # Linha de cards de resumo (responsivos: 1 coluna no mobile, 3 no desktop)
    # -------------------------------------------------------------------------
    cards = ft.ResponsiveRow(
        [
            # Card: total de tarefas cadastradas
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.TASK_ALT, size=40, color=p["primary"]),
                        ft.Text(str(total), size=30, weight=ft.FontWeight.BOLD, color=p["text"]),
                        ft.Text("Tarefas", color=p["subtext"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                col={"xs": 12, "sm": 4},  # Largura: 100% no mobile, 1/3 no desktop
                padding=20,
                border_radius=18,
                bgcolor=p["card"],
            ),

            # Card: tarefas já marcadas como concluídas
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=40, color=p["success"]),
                        ft.Text(str(concluidas), size=30, weight=ft.FontWeight.BOLD, color=p["text"]),
                        ft.Text("Concluídas", color=p["subtext"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                col={"xs": 12, "sm": 4},
                padding=20,
                border_radius=18,
                bgcolor=p["card"],
            ),

            # Card: percentual de produtividade (derivado do ProgressBar)
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.SHOW_CHART, size=40, color=p["warning"]),
                        ft.Text(
                            f"{int(progress.value * 100)}%",  # Converte 0.0–1.0 para 0–100%
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=p["text"],
                        ),
                        ft.Text("Produtividade", color=p["subtext"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                col={"xs": 12, "sm": 4},
                padding=20,
                border_radius=18,
                bgcolor=p["card"],
            ),
        ]
    )

    # -------------------------------------------------------------------------
    # Monta e retorna a view completa como ListView rolável
    # -------------------------------------------------------------------------
    return ft.ListView(
        expand=True,  # Ocupa todo o espaço disponível na tela
        padding=20,
        spacing=20,
        controls=[
            ft.Text("📚 Dashboard", size=28, weight=ft.FontWeight.BOLD, color=p["text"]),
            ft.Text("Gerencie seus estudos e tarefas.", color=p["subtext"]),

            cards,  # Linha de cards de resumo

            # Card com barra de progresso geral
            criar_card(
                "Progresso",
                ft.Column(
                    [
                        progress,  # ProgressBar compartilhado vindo do app.py
                        ft.Text(f"{int(progress.value * 100)}% concluído", color=p["subtext"]),
                    ]
                ),
                p,
            ),
        ],
    )