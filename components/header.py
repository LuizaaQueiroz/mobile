import flet as ft


# Mapeia rota → título exibido no header
# Usado para evitar hardcode do título dentro da função
TITULOS = {
    "/":           "Dashboard",
    "/tarefas":    "Tarefas",
    "/pomodoro":   "Pomodoro",
    "/anotacoes":  "Anotações",
    "/cronograma": "Cronograma",
    "/config":     "Configurações",
    "/sobre":      "Sobre",
    "/usuario":    "Perfil",
}


def header(p, estado, mostrar_snack, toggle_tema):
    """
    Barra de cabeçalho global exibida no topo de todas as telas.
    Mostra o título da rota ativa à esquerda e os botões de ação à direita.

    Parâmetros:
        p            — dicionário de cores da paleta ativa
        estado       — dicionário global de estado do app
        mostrar_snack — callback para exibir SnackBar (reservado para o botão de notificações)
        toggle_tema  — callback que alterna entre tema claro e escuro
    """

    # Resolve o título da rota atual; fallback para "StudyFlow" em rotas desconhecidas
    titulo = TITULOS.get(estado["rota"], "StudyFlow")

    return ft.Container(
        content=ft.Row(
            [
                # Título da rota ativa — atualizado a cada navegação via route_change
                ft.Text(
                    titulo,
                    size=17,
                    weight=ft.FontWeight.BOLD,
                    color=p["text"],
                ),

                # Grupo de botões de ação no lado direito do header
                ft.Row(
                    [
                        # Botão de alternância de tema
                        # Ícone indica para qual tema o botão vai MUDAR (não o atual):
                        # dark=True  → mostra sol  (vai mudar para claro)
                        # dark=False → mostra lua  (vai mudar para escuro)
                        ft.IconButton(
                            icon=(
                                ft.Icons.LIGHT_MODE_OUTLINED
                                if estado["dark"]
                                else ft.Icons.DARK_MODE_OUTLINED
                            ),
                            icon_color=p["subtext"],
                            tooltip="Alternar tema",
                            on_click=lambda e: toggle_tema(),
                        ),
                    ],
                    spacing=0,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=p["sidebar"],
        # Borda inferior sutil separando o header do conteúdo da view
        border=ft.border.Border(
            bottom=ft.border.BorderSide(1, p["border"]),
        ),
        padding=ft.Padding(left=20, top=0, right=12, bottom=0),
        height=56,   # Altura fixa para manter consistência com o menu lateral
    )