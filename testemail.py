import flet as ft
import psycopg2 as psql
import pandas as pd
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

def paginaTreino(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.title = "Treino"

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

    def carregar_filtrar_e_salvar(page):
        
        resultados.controls.clear()


        try:
            cursor.execute('SELECT COUNT(*) FROM exercicios WHERE tipo_treino = %s AND series_atual > %s', ('A', 0))
            quantidadeA = cursor.fetchone()
            if (int(quantidadeA[0])) > 0:
                quantidade = quantidadeA
                letra = 'A'
            else:
                cursor.execute('UPDATE tipos_de_treino SET feito = TRUE WHERE tipo_de_treino = %s', ( 'A',))
                cursor.execute('SELECT COUNT(*) FROM exercicios WHERE tipo_treino = %s AND series_atual > %s', ('B', 0))
                quantidadeB = cursor.fetchone()
                if (int(quantidadeB[0])) > 0:
                    quantidade = quantidadeB
                    letra = 'B'
                else:
                    cursor.execute('UPDATE tipos_de_treino SET feito = TRUE WHERE tipo_de_treino = %s', ( 'B',))
                    cursor.execute('SELECT COUNT(*) FROM exercicios WHERE tipo_treino = %s AND series_atual > %s', ('C', 0))
                    quantidadeC = cursor.fetchone()
                    if (int(quantidadeB[0])) > 0:
                        quantidade = quantidadeC
                        letra = 'C'
                    else:
                        cursor.execute('UPDATE tipos_de_treino SET feito = FALSE')
                        cursor.execute('UPDATE exercicios SET series_atual = series')
                        page.go("/acabou")
                        page.update()



            print(int(quantidade[0]))

            if (int(quantidade[0])) > 0: 
                cursor.execute('SELECT nome, repeticoes, series, series_atual FROM exercicios WHERE tipo_treino = %s AND series_atual > %s ORDER BY parte_treino ASC', (letra, 0))
                resultado_pesquisa = cursor.fetchone()
                
                nome_exercicio = resultado_pesquisa[0]
                repeticoes = resultado_pesquisa[1]
                #series = resultado_pesquisa[0][3]

                cursor.execute(
                    'UPDATE exercicios SET series_atual = series_atual - 1 WHERE nome = %s',
                    (resultado_pesquisa[0],)
                )

                resultados.controls.append(ft.Text(f"{nome_exercicio}", size=60, weight=ft.FontWeight.BOLD,expand=True, text_align=ft.TextAlign.CENTER))

                resultados.controls.append(ft.Text(f"Repetições: {repeticoes}"))
                
                resultados.controls.append(
                    ft.Image(
                        src="https://www.mundoboaforma.com.br/wp-content/uploads/2021/03/abdominal-alternado-no-chao.gif",
                        #width=200,
                        expand= True
                    )
                )
            else:
                page.go("/acabou")
                page.update()

        except psql.Error as e:
            resultados.controls.append(ft.Text(f"Erro ao executar a consulta: {e}"))

        page.update()

       

    resultados = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        #expand=True
    )

    def exercicio_finalizado(e):
        page.go("/descanso")
        page.update()

    appbar_treino = ft.CupertinoAppBar(
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

    botao_finalizado = ft.FloatingActionButton("Finalizado", on_click=exercicio_finalizado, width=300)

    # Carregar e exibir o primeiro exercício ao carregar a página
    carregar_filtrar_e_salvar(page)

    return ft.View(
        "/treino",
        [
            resultados
        ],
        floating_action_button=botao_finalizado,
        appbar=appbar_treino,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_FLOAT
    )
