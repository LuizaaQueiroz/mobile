import flet as ft
from theme.paleta import criar_card


def view_sobre(p):
    # Retorna a view "Sobre" como uma lista rolável
    return ft.ListView(
        expand=True,  # Ocupa todo o espaço disponível na tela
        padding=20,
        spacing=20,
        controls=[
            # Título da página
            ft.Text("ℹ️ Sobre", size=28, weight=ft.FontWeight.BOLD, color=p["text"]),

            # Card com informações do projeto
            criar_card(
                "Projeto",
                ft.Column(
                    [
                        ft.Text("Sistema de produtividade acadêmica.", color=p["text"]),
                        ft.Text("Python + Flet 0.85.1", color=p["subtext"]),  # Versão atual
                    ]
                ),
                p,  # Paleta de cores ativa (claro ou escuro)
            ),
        ],
    )