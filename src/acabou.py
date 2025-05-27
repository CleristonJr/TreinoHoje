import flet as ft

def paginaAcabou(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.title = "PARABÉNS!!"

    ft.ThemeMode.LIGHT
    def check_item_clicked(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode != ft.ThemeMode.LIGHT else ft.ThemeMode.DARK
        )
        page.update()

    def logoff_clicked(e):
        page.go("/login")
        page.logout()
        page.update()

    def exercicio_finalizado(e):
        page.go("/inicial")
        page.update()

    appbar_acabou = ft.CupertinoAppBar(
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
    acabou_texto = ft.Text("ACABOU, PARABÉNS!!!!", size=60, weight=ft.FontWeight.BOLD, expand=True, text_align= ft.TextAlign.CENTER)
    
    botao_finalizado = ft.FloatingActionButton("Finalizado", on_click=exercicio_finalizado, width = 300)
  

    return ft.View(
        "/acabou", 
        [
            acabou_texto,
            ft.Image(
                src="acabou.png",
                #width=400,
                expand=True
            ),
            ft.Text(
                "Descanse um pouco e beba água...",
                size=30,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
            ),
            botao_finalizado
            
            
            
        ],
        appbar= appbar_acabou,
        vertical_alignment = ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )