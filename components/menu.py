import flet as ft


def menu_lateral(p, estado, navegar):
    """
    Componente de menu lateral fixo do app.
    Exibe navegação principal, seção de sistema e perfil do usuário no rodapé.

    Parâmetros:
        p       — dicionário de cores da paleta ativa
        estado  — dicionário global de estado do app
        navegar — callback que atualiza a rota ativa e re-renderiza a página
    """

    def section_label(texto):
        """
        Rótulo de seção em caixa alta e tamanho reduzido.
        Separa visualmente grupos de itens no menu (ex: "PRINCIPAL", "SISTEMA").
        """
        return ft.Container(
            content=ft.Text(
                texto.upper(),
                size=10,
                weight=ft.FontWeight.BOLD,
                color=p["subtext"],
            ),
            padding=ft.Padding(left=10, top=6, right=0, bottom=2),
        )

    def item(nome, rota, icone):
        """
        Item de navegação do menu.
        Destaca visualmente o item correspondente à rota ativa no estado.

        Parâmetros:
            nome  — texto exibido no item
            rota  — rota associada ao item (ex: "/tarefas")
            icone — ícone Flet exibido à esquerda do texto
        """
        ativo = estado["rota"] == rota

        # Fundo do item ativo: roxo escuro no dark mode, lilás suave no claro
        if ativo:
            bg = "#312e81" if estado["dark"] else "#ede9fe"
        else:
            bg = None

        return ft.Container(
            content=ft.Row(
                [
                    # Ícone: cor primária se ativo, subtext se inativo
                    ft.Icon(
                        icone,
                        size=17,
                        color=p["primary"] if ativo else p["subtext"],
                    ),
                    # Texto: cor primária e negrito se ativo, normal se inativo
                    ft.Text(
                        nome,
                        size=13,
                        color=p["primary"] if ativo else p["text"],
                        weight=(
                            ft.FontWeight.W_500 if ativo
                            else ft.FontWeight.NORMAL
                        ),
                    ),
                ],
                spacing=9,
            ),
            padding=ft.Padding(left=10, top=8, right=10, bottom=8),
            border_radius=9,
            bgcolor=bg,
            # Captura a rota via default arg para evitar closure com valor errado
            on_click=lambda e, r=rota: navegar(r),
        )

    # ==========================================================================
    # PERFIL DO USUÁRIO (rodapé do menu)
    # Exibe inicial do nome em avatar circular, nome completo e e-mail ou "Online"
    # ==========================================================================

    # Lê os dados do usuário do estado, com fallback para "Visitante"
    u       = estado.get("usuario") or {}
    nome    = u.get("nome", "") or "Visitante"
    email   = u.get("email", "")
    inicial = nome[0].upper()   # Primeira letra do nome para o avatar

    perfil = ft.Container(
        content=ft.Row(
            [
                # Avatar circular com a inicial do nome sobre fundo primário
                ft.Container(
                    content=ft.Text(
                        inicial,
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    bgcolor=p["primary"],
                    border_radius=50,   # Círculo perfeito
                    width=32,
                    height=32,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [
                        # Nome do usuário em destaque
                        ft.Text(
                            nome,
                            size=12,
                            weight=ft.FontWeight.W_500,
                            color=p["text"],
                        ),
                        # E-mail se disponível, senão indicador "● Online"
                        ft.Text(
                            email if email else "● Online",
                            size=10,
                            color=p["subtext"],
                        ),
                    ],
                    spacing=1,
                    tight=True,
                    expand=True,
                ),
            ],
            spacing=9,
        ),
        padding=ft.Padding(left=10, top=9, right=10, bottom=9),
        border_radius=9,
        # Fundo suave no claro; card escuro no dark mode
        bgcolor="#f5f3ff" if not estado["dark"] else p["card"],
        # Clique no perfil navega para a view de usuário
        on_click=lambda e: navegar("/usuario"),
    )

    # ==========================================================================
    # ESTRUTURA DO MENU
    # Container fixo de 240px com logo, seções de navegação e perfil no rodapé
    # ==========================================================================
    return ft.Container(
        width=240,
        bgcolor=p["sidebar"],
        # Borda direita sutil separando o menu do conteúdo principal
        border=ft.border.Border(
            right=ft.border.BorderSide(1, p["border"]),
        ),
        padding=ft.Padding(left=12, top=18, right=12, bottom=18),
        content=ft.Column(
            [
                # Logo do app no topo do menu
                ft.Container(
                    content=ft.Text(
                        "STUDYFLOW",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=p["primary"],
                    ),
                    padding=ft.Padding(left=10, top=0, right=0, bottom=8),
                ),

                # Seção principal: telas de uso diário
                section_label("Principal"),
                item("Dashboard",  "/",           ft.Icons.DASHBOARD_OUTLINED),
                item("Tarefas",    "/tarefas",    ft.Icons.CHECK_CIRCLE_OUTLINE),
                item("Pomodoro",   "/pomodoro",   ft.Icons.TIMER_OUTLINED),
                item("Anotações",  "/anotacoes",  ft.Icons.EDIT_NOTE),
                item("Cronograma", "/cronograma", ft.Icons.CALENDAR_MONTH_OUTLINED),

                ft.Divider(color=p["border"], height=1),

                # Seção sistema: configurações e informações do app
                section_label("Sistema"),
                item("Configurações", "/config", ft.Icons.SETTINGS_OUTLINED),
                item("Sobre",         "/sobre",  ft.Icons.INFO_OUTLINE),

                # Espaço flexível que empurra o perfil para o rodapé
                ft.Container(expand=True),
                ft.Divider(color=p["border"], height=1),

                # Perfil do usuário fixo no rodapé do menu
                perfil,
            ],
            spacing=2,
            expand=True,
        ),
    )