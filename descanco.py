import flet as ft
import threading
import time

def paginaDescanso(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.title = "Descanso"

    ft.ThemeMode.LIGHT
    def check_item_clicked(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode != ft.ThemeMode.LIGHT else ft.ThemeMode.DARK
        )
        page.update()

    timer_picker_value_ref = ft.Ref[ft.Text]()

    def handle_timer_picker_change(e):
        val = int(e.data)
        timer_picker_value_ref.current.value = time.strftime(
            "%M:%S", time.gmtime(val)
        )
        e.control.page.update()

    timer_picker = ft.CupertinoTimerPicker(
        value=60,  # Tempo inicial em segundos (1 minuto)
        second_interval=5,
        minute_interval=1,
        mode=ft.CupertinoTimerPickerMode.MINUTE_SECONDS,
        on_change=handle_timer_picker_change,
        #bgcolor= ft.Colors.GREY_800
    )

    tempo_selecionado = ft.Text("01:00", size=40, ref=timer_picker_value_ref)

    def abrir_seletor_tempo(e):
        page.overlay.append(
            ft.CupertinoBottomSheet(
                timer_picker,
                height=216,
                #bgcolor=ft.CupertinoColors.SYSTEM_BACKGROUND,
                padding=ft.padding.only(top=6),
                open=True,
                on_dismiss=lambda _: page.overlay.clear()
            )
        )
        page.update()

    seletor_tempo = ft.Column(
        tight=True,
        alignment= ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row([
                ft.Text("Tempo do Descanso:", size=23),
                ft.TextButton(
                    content=tempo_selecionado,
                    on_click=abrir_seletor_tempo,
                ),
            ],alignment= ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, adaptive= True, wrap=True,)
        ]
    )

    cronometro_ativo = False  # Declare cronometro_ativo aqui
    segundos = 0
    minutos = 1
    def pular_cronometro(e):
        nonlocal cronometro_ativo
        cronometro_ativo = False
        nonlocal minutos
        minutos = 0
        nonlocal segundos
        segundos = 0
        tempo_cronometro.value = "00:00"
        page.go("/treino")
        page.update()

    def atualizar_tempo():
        nonlocal segundos
        nonlocal minutos
        nonlocal cronometro_ativo
        while cronometro_ativo and (minutos > 0 or segundos > 0):
            if segundos == 0:
                minutos -= 1
                segundos = 59
            else:
                segundos -= 1
            tempo_cronometro.value = f"{minutos:02d}:{segundos:02d}"
            try:
                page.update()
            except Exception as e:
                print(f"Erro ao atualizar a página: {e}")
                break
            time.sleep(1)
        cronometro_ativo = False
        minutos = 0
        segundos = 0
        pular_cronometro(None)

    def iniciar_cronometro(e):
        nonlocal cronometro_ativo
        nonlocal minutos
        nonlocal segundos
        if not cronometro_ativo:
            try:
                minutos, segundos = map(int, timer_picker_value_ref.current.value.split(':'))
                tempo.controls.remove(botao_iniciar)
            except ValueError:
                print("Erro ao obter o tempo do seletor.")
                return
            cronometro_ativo = True
            threading.Thread(target=atualizar_tempo).start()

    

    def logoff_clicked(e):
        page.go("/login")
        page.logout()
        page.update()

    appbar_descanso = ft.CupertinoAppBar(
        leading=ft.IconButton(icon=ft.Icons.WB_SUNNY_OUTLINED, on_click=check_item_clicked, icon_size=20),
        middle=ft.Text("Treino Quest"),
        trailing=ft.IconButton(
            icon=ft.Icons.LOGOUT,
            on_click=logoff_clicked,
            icon_size=20
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        # actions=[
        #     ft.IconButton(icon=ft.Icons.MENU_OUTLINED , on_click= abrir_drawer),
        # ]
    )
    tempo_cronometro = ft.Text("00:00", size=100, weight=ft.FontWeight.BOLD, expand=True)
    botao_iniciar = ft.ElevatedButton("Iniciar", on_click=iniciar_cronometro,  width = 300, height=100, icon= ft.Icons.PLAY_ARROW, adaptive=True, expand=True)
    botao_pular = ft.FloatingActionButton("Pular", on_click=pular_cronometro)
    tempo = ft.Column(
        [
            tempo_cronometro,
            botao_iniciar,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        #expand=True
    )
  

    return ft.View(
        "/descanso", 
        [
            ft.Image(
                src="unnamed1.png",
                width=200,
            ),
            ft.Text(
                "Descanse um pouco e beba água...",
                size=30,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
            ),
            seletor_tempo,
            tempo
            
            
        ],
        floating_action_button= botao_pular,
        appbar= appbar_descanso,
        vertical_alignment = ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
