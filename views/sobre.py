import flet as ft
from theme.paleta import criar_card


def view_sobre(p):
    """
    View informativa sobre o projeto StudyFlow.
    Exibe o cronograma de 8 semanas de desenvolvimento e as tecnologias utilizadas.

    Parâmetros:
        p — dicionário de cores da paleta ativa
    """

    # Lista de tuplas: (nome da semana, descrição, cor do badge)
    # As cores progridem de verde → amarelo → laranja → azul → vermelho
    # para indicar visualmente o avanço do projeto
    itens = [
        ("Semana 1", "Tela única: texto + botão",              ft.Colors.GREEN_600),
        ("Semana 2", "Campos e interatividade real",           ft.Colors.GREEN_600),
        ("Semana 3", "Row, Column, Container",                 ft.Colors.YELLOW_700),
        ("Semana 4", "Menu lateral com navegação visual",      ft.Colors.YELLOW_700),
        ("Semana 5", "Navegação real com rotas",               ft.Colors.ORANGE_600),
        ("Semana 6", "AppBar, ícones e SnackBar",              ft.Colors.ORANGE_600),
        ("Semana 7", "Componentização e código escalável",     ft.Colors.BLUE_600),
        ("Semana 8", "Dark mode, refinamento e produto final", ft.Colors.RED_600),
    ]

    # ==========================================================================
    # LISTA DE SEMANAS
    # Cada item é um Container com badge colorido + descrição lado a lado
    # ==========================================================================
    lista = ft.Column(
        [
            ft.Container(
                content=ft.Row(
                    [
                        # Badge colorido com o nome da semana (fundo sólido, texto branco)
                        ft.Container(
                            content=ft.Text(
                                s,
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            bgcolor=c,
                            padding=ft.Padding(8, 4, 8, 4),
                            border_radius=6,
                            width=80,
                        ),
                        # Descrição resumida do conteúdo da semana
                        ft.Text(d, size=13, expand=True, color=p["subtext"]),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(10, 8, 10, 8),
                border_radius=8,
                bgcolor=p["card"],
                border=ft.Border.all(1, p["border"]),
            )
            # List comprehension: gera um container por tupla em itens
            for s, d, c in itens
        ],
        spacing=6,
        tight=True,
    )

    # ==========================================================================
    # BOX DE INFORMAÇÕES TÉCNICAS
    # Exibe a stack tecnológica e o contexto acadêmico do projeto
    # ==========================================================================
    info_box = ft.Container(
        content=ft.Column(
            [
                # Linha 1: linguagem e framework utilizados
                ft.Row(
                    [
                        ft.Icon(ft.Icons.CODE, color=ft.Colors.BLUE_500, size=16),
                        ft.Text("Python + Flet 0.85.1", size=13, color=p["subtext"]),
                    ],
                    spacing=8,
                ),
                # Linha 2: contexto acadêmico do projeto
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL_OUTLINED, color=ft.Colors.BLUE_500, size=16),
                        ft.Text("Disciplina: Tecnologia da Informação", size=13, color=p["subtext"]),
                    ],
                    spacing=8,
                ),
            ],
            spacing=8,
            tight=True,
        ),
        padding=16,
        border_radius=12,
        bgcolor=p["card"],
        border=ft.Border.all(1, p["border"]),
    )

    # ==========================================================================
    # LAYOUT FINAL
    # ListView rolável com título, subtítulo, cronograma e info técnica
    # ==========================================================================
    return ft.ListView(
        expand=True,
        padding=20,
        spacing=16,
        controls=[
            ft.Text(
                "Progressão de 8 semanas construindo o StudyFlow com Python + Flet.",
                size=14,
                color=p["subtext"],
            ),
            ft.Divider(color=p["border"]),
            # Card reutilizável com o cronograma semanal
            criar_card("Cronograma do Projeto", lista, p),
            # Box separado com stack tecnológica e disciplina
            info_box,
        ],
    )