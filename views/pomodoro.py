import flet as ft
from theme.paleta import criar_card


def view_pomodoro(p, estado, page):
    """
    View do Timer Pomodoro.
    Ciclo de foco: duração definida pelo slider da view de Tarefas (padrão 25min).
    Ciclo padrão: foco → 5 min pausa curta → a cada 4 ciclos, 15 min pausa longa.

    Parâmetros:
        p      — dicionário de cores da paleta ativa
        estado — dicionário global de estado do app
        page   — instância da página Flet (necessária para page.run_task e page.update)

    Estado local (dentro de estado["pomodoro"]):
        segundos_restantes — tempo atual em segundos
        rodando            — bool, se o timer está ativo
        modo               — "foco", "pausa_curta" ou "pausa_longa"
        ciclos             — quantos ciclos de foco foram concluídos
    """

    # Lê a duração de foco definida pelo slider de tarefas (padrão 25min)
    # O slider vai de 0–100; a conversão é max(5, valor/2) → 5 a 50 minutos
    slider_val    = estado.get("campos_slider_foco_value", 50)
    minutos_foco  = max(5, int(slider_val / 2))

    # Inicializa o sub-estado do pomodoro apenas na primeira vez que a view é carregada
    # Se já existir (usuário voltou para a tela), preserva o estado atual
    if "pomodoro" not in estado:
        estado["pomodoro"] = {
            "segundos_restantes": minutos_foco * 60,
            "rodando":            False,
            "modo":               "foco",
            "ciclos":             0,
        }

    # Atalho para o sub-estado (referência, não cópia)
    pm = estado["pomodoro"]

    # Durações em segundos — foco lê do estado para refletir o slider
    DURAÇÕES = {
        "foco":        pm["segundos_restantes"]
                       if pm["modo"] == "foco"
                       else minutos_foco * 60,
        "pausa_curta":  5 * 60,
        "pausa_longa": 15 * 60,
    }

    # Labels exibidos na interface para cada modo
    LABELS_MODO = {
        "foco":        "🎯 Foco",
        "pausa_curta": "☕ Pausa Curta",
        "pausa_longa": "🛋️ Pausa Longa",
    }

    # ==========================================================================
    # CONTROLES DE EXIBIÇÃO
    # ==========================================================================

    def formatar_tempo(segundos):
        """Converte segundos inteiros para string no formato MM:SS."""
        m, s = divmod(segundos, 60)
        return f"{m:02d}:{s:02d}"

    # Display principal do timer — tamanho grande para destaque visual
    texto_tempo = ft.Text(
        formatar_tempo(pm["segundos_restantes"]),
        size=72,
        weight=ft.FontWeight.BOLD,
        color=p["primary"],
    )

    # Indica o modo atual (foco / pausa curta / pausa longa)
    texto_modo = ft.Text(
        LABELS_MODO[pm["modo"]],
        size=20,
        color=p["subtext"],
    )

    # Contador de ciclos de foco concluídos na sessão
    texto_ciclos = ft.Text(
        f"Ciclos concluídos: {pm['ciclos']}",
        size=14,
        color=p["subtext"],
    )

    # Informa ao usuário qual duração de foco está configurada pelo slider
    texto_config = ft.Text(
        f"Duração do foco: {minutos_foco} min (ajuste pelo slider em Tarefas)",
        size=11,
        color=p["subtext"],
    )

    # ==========================================================================
    # LÓGICA DO TIMER
    # Função assíncrona que decrementa o tempo a cada segundo enquanto rodando=True
    # ==========================================================================

    async def tick():
        """
        Corrotina que executa o tick do timer a cada 1 segundo.
        Roda em background via page.run_task — não bloqueia a UI.
        Ao zerar o tempo, avança automaticamente para o próximo modo.
        """
        import asyncio
        while pm["rodando"]:
            await asyncio.sleep(1)

            # Dupla verificação: pode ter sido pausado durante o sleep
            if not pm["rodando"]:
                break

            pm["segundos_restantes"] -= 1
            texto_tempo.value = formatar_tempo(pm["segundos_restantes"])

            # Ciclo encerrado: tempo chegou a zero
            if pm["segundos_restantes"] <= 0:
                pm["rodando"] = False

                if pm["modo"] == "foco":
                    pm["ciclos"] += 1
                    texto_ciclos.value = f"Ciclos concluídos: {pm['ciclos']}"

                    # A cada 4 ciclos de foco completos → pausa longa; senão → pausa curta
                    if pm["ciclos"] % 4 == 0:
                        pm["modo"] = "pausa_longa"
                    else:
                        pm["modo"] = "pausa_curta"
                else:
                    # Após qualquer pausa → volta para foco
                    pm["modo"] = "foco"

                # Recarrega o tempo do novo modo e atualiza os displays
                pm["segundos_restantes"] = DURAÇÕES[pm["modo"]]
                texto_tempo.value        = formatar_tempo(pm["segundos_restantes"])
                texto_modo.value         = LABELS_MODO[pm["modo"]]

                # Reseta o botão para "Iniciar" ao fim do ciclo
                btn_iniciar.text = "Iniciar"
                btn_iniciar.icon = ft.Icons.PLAY_ARROW

                # Notifica o usuário sobre a troca de modo
                page.show_dialog(ft.SnackBar(
                    content=ft.Text(f"Modo alterado para: {LABELS_MODO[pm['modo']]}"),
                    bgcolor=p["primary"],
                ))

            page.update()

    # ==========================================================================
    # HANDLERS DOS BOTÕES
    # ==========================================================================

    def iniciar_pausar(e):
        """
        Alterna entre Iniciar / Pausar / Continuar.
        Ao iniciar, dispara a corrotina tick() em background.
        """
        pm["rodando"] = not pm["rodando"]
        if pm["rodando"]:
            btn_iniciar.text = "Pausar"
            btn_iniciar.icon = ft.Icons.PAUSE
            page.run_task(tick)   # Inicia o loop assíncrono do timer
        else:
            btn_iniciar.text = "Continuar"
            btn_iniciar.icon = ft.Icons.PLAY_ARROW
        page.update()

    def reiniciar(e):
        """Para o timer e restaura o tempo do modo atual sem trocar de modo."""
        pm["rodando"]            = False
        pm["segundos_restantes"] = DURAÇÕES[pm["modo"]]
        texto_tempo.value        = formatar_tempo(pm["segundos_restantes"])
        btn_iniciar.text         = "Iniciar"
        btn_iniciar.icon         = ft.Icons.PLAY_ARROW
        page.update()

    def trocar_modo(modo):
        """
        Troca manualmente para o modo informado, parando o timer atual.
        Para o modo foco, usa a duração configurada pelo slider de tarefas.
        """
        pm["rodando"]            = False
        pm["modo"]               = modo
        # Foco usa duração do slider; pausas usam valores fixos
        pm["segundos_restantes"] = DURAÇÕES[modo]
        texto_tempo.value        = formatar_tempo(pm["segundos_restantes"])
        texto_modo.value         = LABELS_MODO[modo]
        btn_iniciar.text         = "Iniciar"
        btn_iniciar.icon         = ft.Icons.PLAY_ARROW
        page.update()

    # ==========================================================================
    # BOTÕES
    # ==========================================================================

    # Botão principal: alterna entre Iniciar / Pausar / Continuar
    btn_iniciar = ft.Button(
        content="Iniciar",
        icon=ft.Icons.PLAY_ARROW,
        on_click=iniciar_pausar,
    )

    # Botão secundário: reinicia o timer do modo atual
    btn_reiniciar = ft.OutlinedButton(
        content="Reiniciar",
        icon=ft.Icons.REPLAY,
        on_click=reiniciar,
    )

    # Seleção rápida de modo — permite pular diretamente para foco ou pausa
    botoes_modo = ft.Row(
        [
            ft.TextButton("🎯 Foco",        on_click=lambda e: trocar_modo("foco")),
            ft.TextButton("☕ Pausa Curta",  on_click=lambda e: trocar_modo("pausa_curta")),
            ft.TextButton("🛋️ Pausa Longa", on_click=lambda e: trocar_modo("pausa_longa")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # ==========================================================================
    # LAYOUT FINAL
    # ==========================================================================
    return ft.ListView(
        expand=True,
        padding=20,
        spacing=20,
        controls=[
            ft.Text("⏱️ Pomodoro", size=28, weight=ft.FontWeight.BOLD, color=p["text"]),
            ft.Text("Mantenha o foco com ciclos de estudo e pausa.", color=p["subtext"]),

            # Card principal com o timer, botões de controle e seleção de modo
            criar_card(
                "Timer",
                ft.Column(
                    [
                        texto_modo,     # Label do modo atual (foco/pausa)
                        ft.Container(
                            content=texto_tempo,           # Display MM:SS centralizado
                            alignment=ft.Alignment.CENTER,
                        ),
                        texto_ciclos,   # Contador de ciclos concluídos
                        texto_config,   # Informa duração configurada pelo slider
                        ft.Row(
                            [btn_iniciar, btn_reiniciar],  # Controles principais
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15,
                        ),
                        ft.Divider(),
                        botoes_modo,    # Seleção rápida de modo
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                p,
            ),

            # Card explicativo com as regras do método pomodoro
            criar_card(
                "Como funciona",
                ft.Column(
                    [
                        ft.Text("① Estude pelo tempo configurado no slider sem interrupções.", color=p["text"]),
                        ft.Text("② Descanse 5 minutos.",                                      color=p["text"]),
                        ft.Text("③ A cada 4 ciclos, faça uma pausa de 15 min.",               color=p["text"]),
                        ft.Text("④ Ajuste a duração do foco pelo slider na tela de Tarefas.", color=p["text"]),
                    ],
                    spacing=8,
                ),
                p,
            ),
        ],
    )