import flet as ft
from theme.paleta import criar_card
from datetime import datetime


def _saudacao():
    """Retorna saudação (Bom dia/tarde/noite) conforme o horário atual."""
    h = datetime.now().hour
    if h < 12:
        return "Bom dia"
    if h < 18:
        return "Boa tarde"
    return "Boa noite"


def view_home(p, estado, progress):
    """
    View principal do app (Dashboard).

    Parâmetros:
        p        — dicionário de cores da paleta ativa (claro ou escuro)
        estado   — dicionário global de estado do app
        progress — ProgressBar compartilhado, atualizado por atualizar_progresso()
    """

    # Contadores derivados da lista de tarefas no estado global
    total      = len(estado["tarefas"])
    concluidas = len([t for t in estado["tarefas"] if t["feito"]])
    pct        = int(progress.value * 100)  # Converte 0.0–1.0 para 0–100

    # Extrai o primeiro nome do usuário logado, com fallback para "Visitante"
    u          = estado.get("usuario", {})
    nome       = u.get("nome", "") or "Visitante"
    nome_curto = nome.split()[0]

    # ==========================================================================
    # CARDS DE MÉTRICAS
    # Cada card exibe: ícone colorido, valor principal, label e texto delta
    # ==========================================================================

    def metric_card(icon, icon_bg, icon_color, valor, label, delta, col):
        """
        Constrói um card de métrica reutilizável.

        Parâmetros:
            icon       — ícone Flet (ft.Icons.*)
            icon_bg    — cor de fundo do container do ícone
            icon_color — cor do ícone
            valor      — string exibida como número principal (ex: "3", "75%")
            label      — nome da métrica (ex: "Tarefas")
            delta      — texto de contexto abaixo do divisor (ex: "3 no total")
            col        — dict responsivo para ft.ResponsiveRow (xs/sm)
        """
        return ft.Container(
            content=ft.Column(
                [
                    # Ícone dentro de um container com fundo suave e cantos arredondados
                    ft.Container(
                        content=ft.Icon(icon, size=18, color=icon_color),
                        bgcolor=icon_bg,
                        border_radius=10,
                        width=36,
                        height=36,
                        alignment=ft.Alignment.CENTER,
                    ),
                    # Valor numérico principal
                    ft.Text(valor, size=28, weight=ft.FontWeight.BOLD, color=p["text"]),
                    # Nome da métrica
                    ft.Text(label, size=12, color=p["subtext"]),
                    # Linha divisória antes do texto delta
                    ft.Divider(color=p["border"], height=1),
                    # Texto de contexto adicional
                    ft.Text(delta, size=11, color=p["subtext"]),
                ],
                spacing=8,
            ),
            col=col,
            padding=20,
            border_radius=14,
            bgcolor=p["card"],
            border=ft.Border.all(1, p["border"]),
        )

    # Textos delta: variam conforme o estado atual das tarefas
    delta_tarefas    = "Nenhuma tarefa cadastrada" if total == 0 else f"{total} no total"
    delta_concluidas = f"{concluidas} de {total} finalizadas"
    delta_produt     = "Adicione tarefas para começar" if total == 0 else f"{pct}% de aproveitamento"

    # Grade responsiva com os três cards lado a lado no desktop (1/3 cada)
    cards = ft.ResponsiveRow(
        [
            metric_card(
                ft.Icons.CHECK_CIRCLE_OUTLINE, "#ede9fe", p["primary"],
                str(total), "Tarefas", delta_tarefas,
                {"xs": 12, "sm": 4},
            ),
            metric_card(
                ft.Icons.TASK_ALT, "#dcfce7", p["success"],
                str(concluidas), "Concluídas", delta_concluidas,
                {"xs": 12, "sm": 4},
            ),
            metric_card(
                ft.Icons.SHOW_CHART, "#fef3c7", p["warning"],
                f"{pct}%", "Produtividade", delta_produt,
                {"xs": 12, "sm": 4},
            ),
        ],
        spacing=14,
        run_spacing=14,
    )

    # ==========================================================================
    # CARD DE PROGRESSO
    # Exibe a ProgressBar compartilhada com label "X de Y tarefas" e percentual
    # ==========================================================================
    barra_progresso = criar_card(
        "Progresso geral",
        ft.Column(
            [
                ft.Row(
                    [
                        # Lado esquerdo: contagem absoluta
                        ft.Text(
                            f"{concluidas} de {total} tarefas concluídas",
                            size=12,
                            color=p["subtext"],
                        ),
                        # Lado direito: percentual em destaque
                        ft.Text(
                            f"{pct}%",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=p["primary"],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                # ProgressBar vinda do main.py — valor entre 0.0 e 1.0
                progress,
            ],
            spacing=8,
        ),
        p,
    )

    # ==========================================================================
    # CARD DE TAREFAS RECENTES
    # Lista as últimas 5 tarefas cadastradas, da mais nova para a mais antiga
    # ==========================================================================

    # Mapeamento de prioridade → cor do ponto e da tag para tarefas pendentes
    COR_DOT = {"Alta": p["danger"], "Média": p["warning"], "Baixa": p["success"]}

    def tarefa_row(t):
        """
        Constrói uma linha para exibir uma tarefa na lista de recentes.

        Estrutura: [ponto colorido] [nome da tarefa] [badge de status/prioridade]

        Tarefas concluídas recebem tratamento visual completo:
            - Ponto verde independente da prioridade original
            - Nome tachado e com cor apagada
            - Badge "✓ Concluída" em verde substituindo a tag de prioridade
            - Fundo levemente esverdeado para destacar da linha pendente
        """
        feito = t["feito"]

        return ft.Container(
            content=ft.Row(
                [
                    # Ponto: verde fixo se concluída, cor da prioridade se pendente
                    ft.Container(
                        width=8, height=8,
                        border_radius=4,
                        bgcolor=(
                            p["success"]
                            if feito
                            else COR_DOT.get(t["prioridade"], p["subtext"])
                        ),
                    ),

                    # Nome da tarefa em coluna para suportar o tachado via decoration
                    ft.Column(
                        [
                            ft.Text(
                                t["nome"],
                                size=13,
                                # Cor apagada se concluída, normal se pendente
                                color=p["subtext"] if feito else p["text"],
                                # Tachado se concluída
                                style=ft.TextStyle(
                                    decoration=ft.TextDecoration.LINE_THROUGH if feito else None,
                                ),
                            ),
                        ],
                        expand=True,
                        spacing=0,
                    ),

                    # Badge direito: "✓ Concluída" se feita, prioridade se pendente
                    ft.Container(
                        content=ft.Text(
                            "✓ Concluída" if feito else t["prioridade"],
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=(
                                p["success"]
                                if feito
                                else COR_DOT.get(t["prioridade"], p["subtext"])
                            ),
                        ),
                        bgcolor=(
                            "#dcfce7" if feito
                            else "#fee2e2" if t["prioridade"] == "Alta"
                            else "#fef3c7" if t["prioridade"] == "Média"
                            else "#dcfce7"
                        ),
                        border_radius=99,
                        padding=ft.Padding(left=8, top=2, right=8, bottom=2),
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            # Fundo esverdeado se concluída para diferenciar visualmente da pendente
            bgcolor="#f0fdf4" if feito else p["bg"],
            border_radius=9,
            padding=ft.Padding(left=12, top=10, right=12, bottom=10),
        )

    # Fatia as últimas 5 tarefas e inverte para exibir a mais recente no topo
    recentes = estado["tarefas"][-5:][::-1]

    # Se houver tarefas, monta a lista; caso contrário, exibe mensagem vazia
    lista_tarefas = (
        ft.Column([tarefa_row(t) for t in recentes], spacing=6)
        if recentes
        else ft.Text("Nenhuma tarefa cadastrada ainda.", size=13, color=p["subtext"])
    )

    card_recentes = criar_card("Tarefas recentes", lista_tarefas, p)

    # ==========================================================================
    # LAYOUT FINAL
    # ListView rolável com padding uniforme e espaçamento entre seções
    # ==========================================================================
    return ft.ListView(
        expand=True,      # Ocupa todo o espaço disponível na coluna de conteúdo
        padding=24,
        spacing=20,
        controls=[
            # Saudação personalizada com nome do usuário e horário
            ft.Column(
                [
                    ft.Text(
                        f"{_saudacao()}, {nome_curto} 👋",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=p["text"],
                    ),
                    ft.Text(
                        "Aqui está um resumo dos seus estudos hoje.",
                        size=13,
                        color=p["subtext"],
                    ),
                ],
                spacing=4,
            ),
            cards,            # Grade de métricas (tarefas / concluídas / produtividade)
            barra_progresso,  # Card com ProgressBar e contagem textual
            card_recentes,    # Card com as últimas 5 tarefas cadastradas
        ],
    )