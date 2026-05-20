import flet as ft
from theme.paleta import criar_card


def view_usuario(p, estado, page):
    """
    View de perfil do usuário.
    Permite editar nome e e-mail, que são salvos no estado global
    e refletidos no menu lateral e na saudação do dashboard.

    Parâmetros:
        p      — dicionário de cores da paleta ativa
        estado — dicionário global de estado do app
        page   — instância da página Flet (necessária para page.update())

    Estado gerenciado (estado["usuario"]):
        nome  — str: nome exibido no menu e no dashboard
        email — str: e-mail exibido no menu lateral
    """

    # Garante que a chave "usuario" existe no estado antes de acessá-la
    if "usuario" not in estado:
        estado["usuario"] = {"nome": "", "email": ""}

    # Atalho para o sub-dicionário do usuário (referência, não cópia)
    u = estado["usuario"]

    # ==========================================================================
    # CAMPOS DO FORMULÁRIO
    # Pré-preenchidos com os valores atuais do estado para persistir entre rotas
    # ==========================================================================

    campo_nome = ft.TextField(
        label="Seu nome",
        hint_text="Ex: João Silva",
        border_radius=12,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        value=u["nome"],   # Restaura o valor salvo anteriormente
        expand=True,
    )

    campo_email = ft.TextField(
        label="E-mail",
        hint_text="Ex: joao@email.com",
        border_radius=12,
        prefix_icon=ft.Icons.MAIL_OUTLINE,
        value=u["email"],  # Restaura o valor salvo anteriormente
        expand=True,
    )

    # Texto de feedback ao usuário — muda de cor e conteúdo conforme o resultado
    texto_result = ft.Text("", color=p["success"], size=13)

    # ==========================================================================
    # LÓGICA DOS BOTÕES
    # ==========================================================================

    def processar(e):
        """
        Valida e salva os dados do formulário no estado global.
        Exibe mensagem de erro se algum campo estiver vazio,
        ou mensagem de sucesso com o nome do usuário.
        """
        nome  = campo_nome.value.strip()
        email = campo_email.value.strip()

        # Validação básica: ambos os campos são obrigatórios
        if not nome or not email:
            texto_result.color = p["danger"]
            texto_result.value = "Preencha todos os campos."
            page.update()
            return

        # Persiste os dados no estado global (reflete no menu e no dashboard)
        u["nome"]  = nome
        u["email"] = email

        texto_result.color = p["success"]
        texto_result.value = f"✓ Dados salvos! Olá, {nome}."
        page.update()

    def limpar(e):
        """Limpa os campos do formulário e o texto de feedback."""
        campo_nome.value   = ""
        campo_email.value  = ""
        texto_result.value = ""
        page.update()

    # ==========================================================================
    # DICA INFORMATIVA
    # Banner laranja explicando o impacto de preencher o nome no app
    # ==========================================================================
    dica = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=ft.Colors.ORANGE_400, size=16),
                ft.Text(
                    "Preencha seu nome para personalizar o dashboard.",
                    size=13,
                    color=ft.Colors.ORANGE_700,
                    expand=True,
                ),
            ],
            spacing=8,
        ),
        bgcolor=ft.Colors.ORANGE_50,
        border_radius=8,
        padding=12,
        border=ft.Border.all(1, ft.Colors.ORANGE_200),
    )

    # ==========================================================================
    # CARD DO FORMULÁRIO
    # Agrupa campos, botões de ação e o texto de resultado em um card reutilizável
    # ==========================================================================
    formulario = criar_card(
        "Dados do Usuário",
        ft.Column(
            [
                campo_nome,
                campo_email,
                ft.Row(
                    [
                        # Botão primário: valida e salva os dados
                        ft.Button(
                            content="Enviar",
                            icon=ft.Icons.SEND,
                            on_click=processar,
                            expand=True,
                        ),
                        # Botão secundário: limpa o formulário sem salvar
                        ft.OutlinedButton(
                            content="Limpar",
                            icon=ft.Icons.CLEAR,
                            on_click=limpar,
                            expand=True,
                        ),
                    ],
                    spacing=8,
                ),
                # Feedback visual: aparece após tentativa de envio
                texto_result,
            ],
            spacing=12,
            tight=True,
        ),
        p,
    )

    # ==========================================================================
    # LAYOUT FINAL
    # ListView rolável com título, dica e formulário empilhados verticalmente
    # ==========================================================================
    return ft.ListView(
        expand=True,
        padding=20,
        spacing=16,
        controls=[
            ft.Text("👤 Usuário", size=28, weight=ft.FontWeight.BOLD, color=p["text"]),
            dica,       # Banner informativo sobre o impacto do nome
            formulario, # Card com campos de nome, e-mail e botões
        ],
    )