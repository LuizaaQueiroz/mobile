import flet as ft


def menu_lateral(p, estado, navegar):
    """
    Componente de menu lateral fixo com navegação entre rotas.

    Parâmetros:
        p       — dicionário de cores da paleta ativa
        estado  — estado global do app (usado para saber a rota ativa e o tema)
        navegar — callback do app.py que atualiza a rota e re-renderiza
    """

    def item(nome, rota, icone):
        """Cria um item de menu com destaque visual quando a rota estiver ativa."""

        ativo = estado["rota"] == rota  # True se este item corresponde à rota atual

        return ft.Container(
            content=ft.Row(
                [
                    # Ícone: cor primária se ativo, cor secundária se inativo
                    ft.Icon(
                        icone,
                        color=p["primary"] if ativo else p["subtext"],
                    ),
                    # Label: negrito e cor primária se ativo
                    ft.Text(
                        nome,
                        color=p["primary"] if ativo else p["text"],
                        weight=(
                            ft.FontWeight.BOLD   if ativo
                            else ft.FontWeight.NORMAL
                        ),
                    ),
                ],
                spacing=10,
            ),
            padding=15,
            border_radius=12,
            # Fundo de destaque: lilás no tema claro, azul-escuro no tema escuro
            bgcolor=(
                "#ede9fe" if ativo and not estado["dark"]
                else "#312e81" if ativo and estado["dark"]
                else None  # Sem fundo quando inativo
            ),
            # r=rota captura o valor correto de rota no loop (evita bug de closure)
            on_click=lambda e, r=rota: navegar(r),
        )

    # Container externo: largura fixa, ocupa toda a altura da tela
    return ft.Container(
        width=240,
        bgcolor=p["sidebar"],
        padding=20,
        content=ft.Column(
            [
                # Logo / nome do app
                ft.Text(
                    "STUDYFLOW",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=p["primary"],
                ),
                ft.Divider(),

                # Itens de navegação
                item("Dashboard",     "/",        ft.Icons.HOME),
                item("Tarefas",       "/tarefas", ft.Icons.TASK_ALT),
                item("Configurações", "/config",  ft.Icons.SETTINGS),
                item("Sobre",         "/sobre",   ft.Icons.INFO),
            ],
            spacing=10,
        ),
    )