import flet as ft
import psycopg2 as psql
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

try:
    conexao = psql.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        database=os.getenv('DB'),
        user=os.getenv('USUARIO'),
        password=os.getenv('SENHADB')
    )
    conexao.set_client_encoding('UTF8')
    conexao.autocommit = True
    cursor = conexao.cursor()

except psql.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

def paginaAlterarTreino(page: ft.Page):
    page.title = "Treino Quest"
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.scroll = ft.ScrollMode.ADAPTIVE

    ft.ThemeMode.LIGHT

    def check_item_clicked(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode != ft.ThemeMode.LIGHT else ft.ThemeMode.DARK
        )
        page.update()

    def logoff_clicked(e):
        page.go("/login")
        # page.logout() # Não existe método logout em ft.Page
        page.update()


    letras = ['A', 'B', 'C', 'D']
    def buscar_dados(letra):
        cursor.execute("SELECT nome, repeticoes, series, parte_treino FROM exercicios WHERE tipo_treino = %s", (letra,))
        return cursor.fetchall()


    mostrar_na_tela_controls = []
    for letra in letras:
        dados = buscar_dados(letra)

        # Criar uma seção para cada tabela
        tabela_titulo = ft.Text(f"Tabela para {letra}", style=ft.TextStyle(size=20, weight="bold"))
        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Repetições")),
                ft.DataColumn(ft.Text("Séries")),
                ft.DataColumn(ft.Text("Ordem de Treino")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(campo))) for campo in linha
                    ]
                ) for linha in dados
            ],
        )

        # Adicionar título e tabela à lista de controles
        mostrar_na_tela_controls.append(tabela_titulo)
        mostrar_na_tela_controls.append(tabela)




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


    mostrar_na_tela = ft.Column(
        mostrar_na_tela_controls,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )

    def destino_selecionado(e):
        if rail.selected_index == 0:
            print("Treino selecionado!")
            # Aqui, execute a função relacionada ao treino
            page.go("/inicial")
            page.update()


    rail = ft.NavigationRail(
        selected_index=1,
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
        "/alterarTreino",
        [
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=5),
                    mostrar_na_tela
                ],
                expand=True, 
                scroll=ft.ScrollMode.ALWAYS
            )
        ],
        appbar=appbar_inicio,
    )
