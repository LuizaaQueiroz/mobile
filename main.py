import flet as ft
from theme.paleta        import paleta
from components.header   import header
from components.menu     import menu_lateral
from views.home          import view_home
from views.pomodoro      import view_pomodoro
from views.config        import view_config
from views.sobre         import view_sobre

# Views novas (com banco)
from views.tarefas       import view_tarefas
from views.anotacoes     import view_anotacoes
from views.cronograma    import view_cronograma
from views.usuario       import view_usuario

# Banco de dados
import database.tarefas as db_tarefas


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
    # ==========================================================================
    estado = {
        "dark":    False,
        "rota":    "/",
        "mobile":  False,
        "tarefas": [],
        "usuario": None,
        
    }

    # ==========================================================================
    # CONTROLES COMPARTILHADOS
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

    progress = ft.ProgressBar(width=400, value=0)

    date_picker = ft.DatePicker()
    page.services.append(date_picker)

    # ==========================================================================
    # HELPERS
    # ==========================================================================

    def get_palette():
        return paleta(estado["dark"])

    def mostrar_snack(msg, cor):
        page.show_dialog(ft.SnackBar(content=ft.Text(msg), bgcolor=cor))

    def _usuario_id():
        u = estado.get("usuario")
        return u["id"] if u else None

    def _sincronizar_estado():
        """Mantém estado["tarefas"] em sincronia com o banco para o dashboard."""
        uid = _usuario_id()
        if uid is None:
            estado["tarefas"] = []
            return
        rows = db_tarefas.listar(uid)
        estado["tarefas"] = [
            {
                "nome":       r["nome"],
                "prioridade": r["prioridade"],
                "feito":      r["concluida"],
            }
            for r in rows
        ]

    def atualizar_progresso():
        total = len(estado["tarefas"])
        if total == 0:
            progress.value = 0
            return
        concluidas = len([t for t in estado["tarefas"] if t["feito"]])
        progress.value = concluidas / total

    # ==========================================================================
    # LÓGICA DE TAREFAS (agora com banco)
    # ==========================================================================

    def adicionar_tarefa(e):
        uid = _usuario_id()
        if uid is None:
            mostrar_snack("⚠️ Faça login na aba Usuário antes de adicionar tarefas.", ft.Colors.RED)
            return

        nome = campo_tarefa.value.strip()
        if nome == "":
            mostrar_snack("Digite uma tarefa.", ft.Colors.RED)
            return

        db_tarefas.criar(
            usuario_id  = uid,
            nome        = nome,
            prioridade  = prioridade.value or "Média",
            data_limite = estado.get("data_limite_selecionada"),
        )

        campo_tarefa.value = ""
        _sincronizar_estado()
        atualizar_progresso()
        mostrar_snack("Tarefa adicionada!", ft.Colors.GREEN)
        route_change()

    def concluir_tarefa(tarefa_id, status):
        db_tarefas.concluir(tarefa_id, bool(status))
        _sincronizar_estado()
        atualizar_progresso()
        route_change()

    def remover_tarefa(tarefa_id):
        db_tarefas.excluir(tarefa_id)
        _sincronizar_estado()
        atualizar_progresso()
        route_change()

    def limpar_tarefas(e):
        uid = _usuario_id()
        if uid is None:
            return
        db_tarefas.limpar_todas(uid)
        _sincronizar_estado()
        atualizar_progresso()
        mostrar_snack("Tarefas removidas.", ft.Colors.ORANGE)
        route_change()

    # ==========================================================================
    # TEMA
    # ==========================================================================

    def trocar_tema(e=None):
        estado["dark"] = not estado["dark"]
        page.theme_mode = ft.ThemeMode.DARK if estado["dark"] else ft.ThemeMode.LIGHT
        route_change()

    # ==========================================================================
    # NAVEGAÇÃO
    # ==========================================================================

    def navegar(rota):
        estado["rota"] = rota
        route_change()

    def route_change(e=None):
        # Sincroniza o espelho de tarefas a cada troca de tela
        _sincronizar_estado()
        atualizar_progresso()

        p = get_palette()
        page.bgcolor = p["bg"]

        campos = {
            "campo_tarefa":      campo_tarefa,
            "prioridade":        prioridade,
            "slider_foco":       slider_foco,
            "radio_filtro":      radio_filtro,
            "checkbox_lembrete": checkbox_lembrete,
            "date_picker":       date_picker,
            "page":              page,
        }

        callbacks = {
            "adicionar_tarefa": adicionar_tarefa,
            "concluir_tarefa":  concluir_tarefa,
            "remover_tarefa":   remover_tarefa,
            "limpar_tarefas":   limpar_tarefas,
            "mostrar_snack":    mostrar_snack,
        }

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

        conteudo = views.get(estado["rota"], views["/"])()

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

    route_change()


ft.app(target=main)