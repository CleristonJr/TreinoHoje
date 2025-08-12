import flet as ft
#from flet.auth.providers import GoogleOAuthProvider
#import os
#from dotenv import load_dotenv

#load_dotenv(encoding='utf-8')


def paginaInicio(page: ft.Page):
    page.title = "Treino Quest"
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'

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

    def tela_Treino(e):
        print("Navegando para Treino")
        page.go("/treino")

    leading_content = ft.Text("Login")

    if page.auth and page.auth.user:
        leading_content = ft.Column(
            [
                ft.CircleAvatar(
                    foreground_image_src=page.auth.user['picture'],
                    content=ft.Text(page.auth.user['given_name'][0].upper()),
                ),
                ft.Text(page.auth.user['given_name'],weight=ft.FontWeight.BOLD,)
            ],
            alignment= ft.MainAxisAlignment.START,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        )

    def destino_selecionado(e):
        if rail.selected_index == 1:
            print("Alterar Treino selecionado!")
            # Aqui, execute a função relacionada ao treino
            page.go("/alterarTreino")
            page.update()


    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=10,
        min_extended_width=40,
        leading=leading_content,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.FITNESS_CENTER),
                label="Treino",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.EDIT_NOTE),
                label="Alterar Treino",
            ),
            
        ],
        width=70,
        on_change=destino_selecionado
    )
    appbar_inicio = ft.CupertinoAppBar(
        leading=ft.IconButton(icon=ft.Icons.WB_SUNNY_OUTLINED, on_click=check_item_clicked, icon_size=20),
        middle=ft.Text("Treino Quest"),
        trailing=ft.IconButton(
            icon=ft.Icons.LOGOUT,
            on_click=logoff_clicked,
            icon_size=20
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    )

    return ft.View(
        "/inicial",
        [
            ft.Row([
                rail,
                ft.VerticalDivider(width=5),
                ft.Column(
                    [
                        ft.ElevatedButton(
                            "Treino de Hoje",
                            style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=60),
                            elevation=2,
                            on_click = tela_Treino
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            ],expand=True)
        ],
        appbar=appbar_inicio,
    )
