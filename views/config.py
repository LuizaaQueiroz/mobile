import flet as ft
from theme.paleta import criar_card


def view_config(p, estado, trocar_tema):

    # Retorna a view "Configurações" como uma lista rolável
    return ft.ListView(
        expand=True,  # Ocupa todo o espaço disponível na tela
        padding=20,
        spacing=20,
        controls=[
            # Título da página
            ft.Text("⚙️ Configurações", size=28, weight=ft.FontWeight.BOLD, color=p["text"]),

            # Card: alternância de tema claro/escuro
            criar_card(
                "Tema",
                ft.Column(
                    [
                        ft.Switch(
                            label="Modo escuro",
                            value=estado["dark"],  # Reflete o estado atual do tema
                            on_change=trocar_tema, # Callback definido no app.py
                        )
                    ]
                ),
                p,
            ),

            # Card: informações estáticas do projeto
            criar_card(
                "Informações",
                ft.Column(
                    [
                        ft.Text("StudyFlow desenvolvido com Python + Flet.", color=p["text"]),
                        ft.Text("Versão 1.0", color=p["subtext"]),
                    ]
                ),
                p,  # Paleta de cores ativa (claro ou escuro)
            ),
        ],
    )