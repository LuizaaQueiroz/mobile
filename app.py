import flet as ft
from theme.paleta        import paleta
from components.header   import header
from components.menu     import menu_lateral
from views.home          import view_home
from views.tarefas       import view_tarefas
from views.pomodoro      import view_pomodoro
from views.anotacoes     import view_anotacoes
from views.cronograma    import view_cronograma
from views.config        import view_config
from views.sobre         import view_sobre
from views.usuario       import view_usuario

def main(page: ft.Page):

    # ==========================================================================
    # CONFIGURAÇÕES DA PÁGINA
    # ==========================================================================
    page.title         = "StudyFlow"
    page.padding       = 0
    page.spacing       = 0
    page.theme_mode    = ft.ThemeMode.LIGHT
    page.window.width  = 1200
    page.window.height = 750

    # ==========================================================================
    # ESTADO GLOBAL
    # Dicionário único que centraliza tudo que muda durante o uso do app.
    # Cada view com estado próprio adiciona sua chave aqui sob demanda.
    # ==========================================================================
    estado = {
        "dark":    False,   # Tema atual (False = claro, True = escuro)
        "rota":    "/",     # Rota ativa, usada para destacar o menu e renderizar a view correta
        "mobile":  False,   # Reservado para futura adaptação de layout mobile
        "tarefas": [],      # Lista de dicts: {"nome", "prioridade", "feito"}
        # "pomodoro", "anotacoes" e "cronograma" são inicializados nas próprias views
    }

    # ==========================================================================
    # CONTROLES COMPARTILHADOS
    # Instanciados aqui para persistir entre re-renders (route_change não os recria)
    # ==========================================================================
    campo_tarefa = ft.TextField(
        label="Nova tarefa",
        border_radius=12,
        prefix_icon=ft.Icons.CHECKLIST,
        expand=True,
    )

    prioridade = ft.Dropdown(
        label="Prioridade",
        width=180,
        value="Média",
        options=[
            ft.dropdown.Option("Baixa"),
            ft.dropdown.Option("Média"),
            ft.dropdown.Option("Alta"),
        ],
    )

    slider_foco = ft.Slider(
        min=0, max=100, value=50, divisions=10, label="{value}%",
    )

    radio_filtro = ft.RadioGroup(
        value="Todas",
        content=ft.Row(
            [
                ft.Radio(value="Todas",      label="Todas"),
                ft.Radio(value="Pendentes",  label="Pendentes"),
                ft.Radio(value="Concluídas", label="Concluídas"),
            ]
        ),
    )

    checkbox_lembrete = ft.Checkbox(label="Receber lembretes", value=True)

    # Barra de progresso: valor entre 0.0 e 1.0, atualizada por atualizar_progresso()
    progress = ft.ProgressBar(width=400, value=0)

    # DatePicker registrado como serviço da página (padrão Flet 0.80+)
    date_picker = ft.DatePicker()
    page.services.append(date_picker)

    # ==========================================================================
    # HELPERS
    # ==========================================================================

    def get_palette():
        # Retorna o dicionário de cores conforme o tema atual do estado
        return paleta(estado["dark"])

    def mostrar_snack(msg, cor):
        # Exibe uma mensagem temporária na parte inferior da tela
        page.show_dialog(ft.SnackBar(content=ft.Text(msg), bgcolor=cor))

    def atualizar_progresso():
        # Recalcula o valor da ProgressBar com base nas tarefas concluídas
        total = len(estado["tarefas"])
        if total == 0:
            progress.value = 0
            return
        concluidas = len([t for t in estado["tarefas"] if t["feito"]])
        progress.value = concluidas / total  # Resultado entre 0.0 e 1.0

    # ==========================================================================
    # LÓGICA DE TAREFAS
    # ==========================================================================

    def adicionar_tarefa(e):
        nome = campo_tarefa.value.strip()
        if nome == "":
            mostrar_snack("Digite uma tarefa.", ft.Colors.RED)
            return
        # Adiciona novo dict ao estado e limpa o campo de entrada
        estado["tarefas"].append({"nome": nome, "prioridade": prioridade.value, "feito": False})
        campo_tarefa.value = ""
        atualizar_progresso()
        mostrar_snack("Tarefa adicionada!", ft.Colors.GREEN)
        route_change()

    def concluir_tarefa(index):
        # Alterna o estado feito/pendente da tarefa no índice recebido
        estado["tarefas"][index]["feito"] = not estado["tarefas"][index]["feito"]
        atualizar_progresso()
        route_change()

    def remover_tarefa(index):
        # Remove a tarefa do índice especificado e re-renderiza
        estado["tarefas"].pop(index)
        atualizar_progresso()
        route_change()

    def limpar_tarefas(e):
        # Remove todas as tarefas do estado
        estado["tarefas"].clear()
        atualizar_progresso()
        mostrar_snack("Tarefas removidas.", ft.Colors.ORANGE)
        route_change()

    # ==========================================================================
    # TEMA
    # ==========================================================================

    def trocar_tema(e=None):
        # Inverte o flag de tema e sincroniza com o ThemeMode da página
        estado["dark"] = not estado["dark"]
        page.theme_mode = ft.ThemeMode.DARK if estado["dark"] else ft.ThemeMode.LIGHT
        route_change()

    # ==========================================================================
    # NAVEGAÇÃO
    # ==========================================================================

    def navegar(rota):
        # Atualiza a rota ativa no estado e re-renderiza
        estado["rota"] = rota
        route_change()

    def route_change(e=None):
        p = get_palette()
        page.bgcolor = p["bg"]  # Atualiza o fundo da página com a cor do tema atual

        # Agrupa os controles de formulário para repassar à view de tarefas
        campos = {
            "campo_tarefa":      campo_tarefa,
            "prioridade":        prioridade,
            "slider_foco":       slider_foco,
            "radio_filtro":      radio_filtro,
            "checkbox_lembrete": checkbox_lembrete,
            "date_picker":       date_picker,
            "page":              page,
        }

        # Agrupa os callbacks de lógica para repassar à view de tarefas
        callbacks = {
            "adicionar_tarefa": adicionar_tarefa,
            "concluir_tarefa":  concluir_tarefa,
            "remover_tarefa":   remover_tarefa,
            "limpar_tarefas":   limpar_tarefas,
             "mostrar_snack":    mostrar_snack,
        }

        # Mapa de rotas: cada entrada é uma lambda que constrói a view sob demanda
        views = {
            "/":           lambda: view_home(p, estado, progress),
            "/tarefas":    lambda: view_tarefas(p, estado, campos, callbacks),
            "/pomodoro":   lambda: view_pomodoro(p, estado, page),
            "/anotacoes":  lambda: view_anotacoes(p, estado, page),
            "/cronograma": lambda: view_cronograma(p, estado, page),
            "/usuario":    lambda: view_usuario(p, estado, page),
            "/config":     lambda: view_config(p, estado, trocar_tema),
            "/sobre":      lambda: view_sobre(p),
        }

        # Resolve a view da rota ativa, com fallback para home
        conteudo = views.get(estado["rota"], views["/"])()

        # Reconstrói a página: menu lateral + header + conteúdo da rota
        page.controls.clear()
        page.add(
            ft.Row(
                [
                    menu_lateral(p, estado, navegar),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        [
                            header(p, estado, mostrar_snack, trocar_tema),
                            conteudo,
                        ],
                        expand=True,
                        spacing=0,
                    ),
                ],
                expand=True,
            )
        )

    # Renderização inicial ao abrir o app
    route_change()
