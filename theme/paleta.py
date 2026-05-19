import flet as ft


def paleta(dark=False):
    """Retorna o dicionário de cores do tema. dark=True para modo escuro."""

    if dark:
        # Tema escuro: tons de azul-marinho e roxo
        return {
            "bg":      "#0f172a",  # Fundo da página
            "sidebar": "#111827",  # Fundo do menu lateral
            "card":    "#1e293b",  # Fundo dos cards
            "text":    "#f8fafc",  # Texto principal
            "subtext": "#94a3b8",  # Texto secundário / labels
            "primary": "#8b5cf6",  # Cor de destaque (roxo claro)
            "border":  "#334155",  # Bordas dos cards
            "success": "#22c55e",  # Verde (prioridade baixa / concluída)
            "danger":  "#ef4444",  # Vermelho (prioridade alta)
            "warning": "#f59e0b",  # Amarelo (prioridade média / produtividade)
        }

    # Tema claro: tons de cinza-gelo e roxo
    return {
        "bg":      "#f8fafc",  # Fundo da página
        "sidebar": "#ffffff",  # Fundo do menu lateral
        "card":    "#ffffff",  # Fundo dos cards
        "text":    "#0f172a",  # Texto principal
        "subtext": "#475569",  # Texto secundário / labels
        "primary": "#7c3aed",  # Cor de destaque (roxo)
        "border":  "#cbd5e1",  # Bordas dos cards
        "success": "#16a34a",  # Verde (prioridade baixa / concluída)
        "danger":  "#dc2626",  # Vermelho (prioridade alta)
        "warning": "#d97706",  # Amarelo (prioridade média / produtividade)
    }


def criar_card(titulo, conteudo, p):
    """
    Componente reutilizável de card com título e conteúdo dinâmico.

    Parâmetros:
        titulo  — texto exibido como cabeçalho do card
        conteudo — qualquer controle Flet inserido no corpo do card
        p       — dicionário de cores da paleta ativa
    """
    return ft.Container(
        content=ft.Column(
            [
                # Cabeçalho do card
                ft.Text(
                    titulo,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=p["text"],
                ),
                # Corpo do card: qualquer widget passado como argumento
                conteudo,
            ],
            spacing=15,
        ),
        bgcolor=p["card"],
        # Borda em todos os lados com a cor do tema atual
        border=ft.border.Border(
            left=ft.border.BorderSide(1, p["border"]),
            top=ft.border.BorderSide(1, p["border"]),
            right=ft.border.BorderSide(1, p["border"]),
            bottom=ft.border.BorderSide(1, p["border"]),
        ),
        border_radius=18,
        padding=20,
    )