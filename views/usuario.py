"""
views/usuario.py
================
View de identificação — com persistência em SQLite.
"""

import flet as ft
from theme.paleta import criar_card
from database.usuarios import criar_usuario, autenticar


def view_usuario(p, estado, page):

    campo_nome = ft.TextField(
        label="Nome",
        border_radius=12,
        prefix_icon=ft.Icons.PERSON,
    )
    campo_email = ft.TextField(
        label="E-mail",
        border_radius=12,
        prefix_icon=ft.Icons.EMAIL,
    )
    texto_result = ft.Text("")

    if estado.get("usuario"):
        campo_nome.value  = estado["usuario"]["nome"]
        campo_email.value = estado["usuario"]["email"]

    def entrar(e):
        nome  = campo_nome.value.strip()
        email = campo_email.value.strip()

        if not nome or not email:
            texto_result.value = "Preencha todos os campos."
            texto_result.color = p["danger"]
            page.update()
            return

        # Tenta autenticar; se não existir, cria o usuário
        usuario = autenticar(email, email)
        if usuario is None:
            criar_usuario(nome, email, email)
            usuario = autenticar(email, email)

        if usuario is None:
            texto_result.value = "Erro ao carregar usuário. Tente novamente."
            texto_result.color = p["danger"]
            page.update()
            return

        estado["usuario"] = usuario
        texto_result.value = f"✓ Bem-vindo(a), {usuario['nome']}!"
        texto_result.color = p["success"]
        page.update()

    return ft.ListView(
        expand=True,
        padding=20,
        spacing=20,
        controls=[
            ft.Text("👤 Usuário", size=28, weight=ft.FontWeight.BOLD, color=p["text"]),
            ft.Text(
                "Seu progresso é salvo automaticamente no banco de dados local.",
                size=13, color=p["subtext"],
            ),
            criar_card(
                "Identificação",
                ft.Column([
                    campo_nome,
                    campo_email,
                    ft.ElevatedButton("Entrar", icon=ft.Icons.LOGIN, on_click=entrar),
                    texto_result,
                ], spacing=15),
                p,
            ),
        ],
    )