import flet as ft
import psycopg2 as psql
import os
from dotenv import load_dotenv
import threading
import time

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





    letra_atual = None
    cont = False




    def abrir_tela_descanso(page):
        resultados.controls.clear()
        timer_picker_value_ref = ft.Ref[ft.Text]()
        cronometro_ativo = False
        segundos = 0
        minutos = 1

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
        )

        tempo_selecionado = ft.Text("01:00", size=40, ref=timer_picker_value_ref)

        def abrir_seletor_tempo(e):
            page.overlay.append(
                ft.CupertinoBottomSheet(
                    timer_picker,
                    height=216,
                    padding=ft.padding.only(top=6),
                    open=True,
                    on_dismiss=lambda _: page.overlay.clear()
                )
            )
            page.update()

        seletor_tempo = ft.Column(
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([
                    ft.Text("Tempo do Descanso:", size=23),
                    ft.TextButton(
                        content=tempo_selecionado,
                        on_click=abrir_seletor_tempo,
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, adaptive=True, wrap=True,)
            ]
        )

        tempo_cronometro = ft.Text("00:00", size=100, weight=ft.FontWeight.BOLD, expand=True)

        def pular_cronometro(page):
            nonlocal cronometro_ativo
            cronometro_ativo = False
            nonlocal minutos
            minutos = 0
            nonlocal segundos
            segundos = 0
            tempo_cronometro.value = "00:00"
            ir_para_carregar_filtrar_e_salvar(page)

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
            pular_cronometro(page)

        def iniciar_cronometro(e):
            nonlocal cronometro_ativo
            nonlocal minutos
            nonlocal segundos
            if not cronometro_ativo:
                try:
                    minutos, segundos = map(int, timer_picker_value_ref.current.value.split(':'))
                    tempo.controls.remove(botao_iniciar)
                    page.update()
                except ValueError:
                    print("Erro ao obter o tempo do seletor.")
                    return
                cronometro_ativo = True
                threading.Thread(target=atualizar_tempo).start()

        botao_iniciar = ft.ElevatedButton("Iniciar", on_click=iniciar_cronometro, width=300, height=100, icon=ft.Icons.PLAY_ARROW, adaptive=True, expand=True)
        botao_pular = ft.FloatingActionButton("Pular", on_click=pular_cronometro)
        tempo = ft.Column(
            [
                tempo_cronometro,
                botao_iniciar,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        tela_descanso = ft.Column(
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
                tempo,
                botao_pular
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        resultados.controls.append(tela_descanso)
        page.update()






    def ir_para_carregar_filtrar_e_salvar(page):
        verificar_letras(page)
        



    def exercicio_finalizado(e):
        abrir_tela_descanso(page)


    def verificar_letras(e):
        print("carregou o verificar")
        nonlocal letra_atual
        nonlocal letra_do_dia
        nonlocal cont
        letras_treino = ['A', 'B', 'C', 'D']

        cursor.execute('SELECT COUNT(*) FROM tipos_de_treino WHERE feito = FALSE')
        resultado_pesquisa_letras = cursor.fetchone()
        print("resultado_pesquisa_letras = ", resultado_pesquisa_letras)
        if not resultado_pesquisa_letras or int(resultado_pesquisa_letras[0]) == 0:
            cursor.execute('UPDATE tipos_de_treino SET feito = FALSE')
            cursor.execute('UPDATE exercicios SET series_atual = series')
            print("atualizou a tabela zerada")

        for letra in letras_treino:
            cursor.execute('SELECT COUNT(*) FROM exercicios WHERE tipo_treino = %s AND series_atual > 0', (letra,))
            quantidade_letra = cursor.fetchone()
            print("testou a letra ", letra)
            print("quantidade_letra = ", quantidade_letra)
            if quantidade_letra and int(quantidade_letra[0]) > 0:
                letra_atual = letra
                print("definiu a letra para ", letra_atual)
                break
            else:
                cursor.execute('UPDATE tipos_de_treino SET feito = TRUE WHERE tipo_de_treino = %s', (letra,))
                print(f"mudou a letra {letra} para TRUE")

        if letra_atual != letra_do_dia and cont == 0:
            letra_do_dia = letra_atual
            print("vamos para carregar filtrar do inicio")
            carregar_filtrar_e_salvar(page)
            cont = True
        elif letra_atual != letra_do_dia and cont: # Considere quando 'cont' deve incrementar
            print("vamos para carregar acabou")
            page.go("/acabou")
            page.update()
        else:
            print("vamos para carregar filtrar")
            carregar_filtrar_e_salvar(page) # Carrega o primeiro exercício para a letra do dia
            





    def carregar_filtrar_e_salvar(page):
        print("chegamos em carregar filtrar")



        resultados.controls.clear()




        nonlocal letra_atual
        nonlocal letra_do_dia
        nonlocal cont

        



        try:
           

            cursor.execute('SELECT nome, repeticoes, series, series_atual, tipo_treino, img_exercicios FROM exercicios WHERE tipo_treino = %s AND series_atual > %s ORDER BY parte_treino ASC LIMIT 1', (letra_atual, 0))
            resultado_pesquisa = cursor.fetchone()
            print("fizemos o select")
            nome_exercicio = resultado_pesquisa[0]
            print(f"nome = {nome_exercicio}")
            repeticoes = resultado_pesquisa[1]
            print(f"nome = {repeticoes}")
            series_atual = resultado_pesquisa[3]
            print(f"nome = {series_atual}")

            cursor.execute(
                'UPDATE exercicios SET series_atual = series_atual - 1 WHERE nome = %s',
                (resultado_pesquisa[0],)
            )
            print("fizemos o update -1")

            resultados.controls.append(ft.Text(f"{nome_exercicio}", size=60, weight=ft.FontWeight.BOLD, expand=True, text_align=ft.TextAlign.CENTER))
            resultados.controls.append(ft.Text(f"Repetições: {repeticoes}"))
            resultados.controls.append(ft.Text(f"Séries Restantes: {series_atual}"))
            resultados.controls.append(ft.Text(f"Letra: {resultado_pesquisa[4]}"))
            resultados.controls.append(
                ft.Image(
                    src=resultado_pesquisa[5],
                    
                    expand=True
                )
            )
            resultados.controls.append(ft.ElevatedButton("Finalizar Exercício", on_click=exercicio_finalizado, width=300))
        

            print(f"Letra Atual: {letra_atual}")

        except psql.Error as e:
            resultados.controls.append(ft.Text(f"Erro ao executar a consulta: {e}"))
            print(f"Erro ao executar a consulta: {e}")
            if conexao:
                conexao.rollback()

        page.update()


    letra_do_dia = None
    

    resultados = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    appbar_treino = ft.CupertinoAppBar(
        leading=ft.IconButton(icon=ft.Icons.WB_SUNNY_OUTLINED, on_click=check_item_clicked, icon_size=20),
        middle=ft.Text("Treino Quest"),
        trailing=ft.IconButton(
            icon=ft.Icons.LOGOUT,
            on_click=logoff_clicked,
            icon_size=20
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    )
    print("pagina treino veio 1")
    ir_para_carregar_filtrar_e_salvar(page)
    print("pagina treino veio")

    return ft.View(
        "/treino",
        [
            resultados
        ],
        appbar=appbar_treino,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )