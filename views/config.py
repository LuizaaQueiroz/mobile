import flet as ft
from theme.paleta import criar_card


def view_config(p, estado, trocar_tema):
    """
    View de Configurações do app.
    Agrupa opções de aparência, notificações e privacidade em cards separados.

    Parâmetros:
        p          — dicionário de cores da paleta ativa
        estado     — dicionário global de estado do app
        trocar_tema — callback que alterna entre tema claro e escuro
    """

    # ==========================================================================
    # CARD: APARÊNCIA
    # Controla o tema (claro/escuro) e exibe o tema de cores ativo
    # ==========================================================================
    aparencia = criar_card(
        "Aparência",
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.DARK_MODE_OUTLINED, color=ft.Colors.INDIGO_400),
                        ft.Switch(
                            label="Modo Escuro",
                            value=estado["dark"],      # Reflete o estado atual do tema
                            on_change=trocar_tema,     # Chama o toggle definido no main.py
                            active_color=ft.Colors.INDIGO_400,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Divider(height=1, color=p["border"]),
                # Informativo estático — tema de cores não é alterável nesta versão
                ft.Row(
                    [
                        ft.Icon(ft.Icons.PALETTE_OUTLINED, color=ft.Colors.BLUE_400),
                        ft.Text("Tema: Roxo (padrão)", size=14, color=p["subtext"]),
                    ],
                    spacing=8,
                ),
            ],
            spacing=10,
            tight=True,
        ),
        p,
    )

    # ==========================================================================
    # CARD: NOTIFICAÇÕES
    # Switches para ativar notificações e sons do sistema
    # Nota: os valores são locais ao widget — não persistem no estado global
    # ==========================================================================
    notificacoes = criar_card(
        "Notificações",
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE_OUTLINED, color=ft.Colors.ORANGE_400),
                        ft.Switch(
                            label="Ativar notificações",
                            value=True,
                            active_color=ft.Colors.ORANGE_400,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.VOLUME_UP_OUTLINED, color=ft.Colors.ORANGE_300),
                        ft.Switch(
                            label="Sons do sistema",
                            value=False,
                            active_color=ft.Colors.ORANGE_400,
                        ),
                    ],
                    spacing=8,
                ),
            ],
            spacing=10,
            tight=True,
        ),
        p,
    )

    # ==========================================================================
    # CARD: PRIVACIDADE
    # Switches para controle de armazenamento local e compartilhamento de dados
    # Nota: os valores são locais ao widget — não persistem no estado global
    # ==========================================================================
    privacidade = criar_card(
        "Privacidade",
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.LOCK_OUTLINE, color=ft.Colors.GREEN_500),
                        ft.Switch(
                            label="Salvar dados localmente",
                            value=True,
                            active_color=ft.Colors.GREEN_500,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.ANALYTICS_OUTLINED, color=ft.Colors.GREEN_400),
                        ft.Switch(
                            label="Compartilhar analytics",
                            value=False,
                            active_color=ft.Colors.GREEN_500,
                        ),
                    ],
                    spacing=8,
                ),
            ],
            spacing=10,
            tight=True,
        ),
        p,
    )

    # ==========================================================================
    # LAYOUT FINAL
    # Cards empilhados verticalmente com rodapé de versão
    # ==========================================================================
    return ft.ListView(
        expand=True,
        padding=20,
        spacing=16,
        controls=[
            aparencia,    # Tema claro/escuro e cor do app
            notificacoes, # Alertas e sons
            privacidade,  # Armazenamento e analytics
            # Rodapé com versão do app — texto discreto no final da lista
            ft.Text("StudyFlow v1.0 — Python + Flet 0.85.1", size=11, color=p["subtext"]),
        ],
    )