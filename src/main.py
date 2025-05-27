import flet as ft
from flet.auth.providers import GoogleOAuthProvider
from inicio import paginaInicio
from descanco import paginaDescanso
from treino import paginaTreino
from acabou import paginaAcabou
from alterar import paginaAlterarTreino
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

client_id = os.getenv('ID')
client_secret = os.getenv('SECRET_ID')

def main(page: ft.Page):
    page.title = "Login"
    page.go("/")


    print(client_id)
    provider = GoogleOAuthProvider(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url='http://localhost:9000/oauth_callback'
    )

    textresult = ft.Column()

    def logingoogle(e):
        page.login(provider)

    def on_login(e):
        if page.auth.user:
            textresult.controls.clear()
            print(page.auth.user)
            textresult.controls.append(ft.Text(f"nome: {page.auth.user['name']}"))
            textresult.controls.append(ft.Text(f"e-mail: {page.auth.user['email']}"))
            textresult.controls.append(ft.Text(f"sub: {page.auth.user['sub']}"))
            textresult.controls.append(ft.CircleAvatar(
                foreground_image_src=page.auth.user['picture'],
                content=ft.Text(page.auth.user['given_name']),
            ))
            textresult.controls.append(ft.CircleAvatar(
                content=ft.Text(page.auth.user['given_name']),
            ))
            # Adiciona botão de logoff
            textresult.controls.append(ft.ElevatedButton("Logoff", on_click=logoff))
            page.go("/inicial")
            print("Navagando para inicio")
            page.update()
        else:
            textresult.controls.clear()
            textresult.controls.append(ft.Text("Login falhou."))
            page.update()

    def logoff(e):
        page.logout() # Limpa informações de autenticação
        textresult.controls.clear()
        textresult.controls.append(ft.Text("Usuário deslogado."))
        textresult.controls.append(ft.ElevatedButton("Login", on_click=logingoogle))
        page.update()

    page.on_login = on_login

    def mudar_tela(route):
        print(f"Rota atual: {page.route}")
        page.views.clear()

        if page.route == "/inicial":
            print("Carregando paginaInicio...")
            try:
                page.views.append(paginaInicio(page))
            except Exception as e:
                print(f"Erro ao carregar paginaInicio: {e}")
                page.views.append(ft.Text(f"Erro ao carregar paginaInicio: {e}"))
        elif page.route == "/descanso":
            print("Carregando paginaDescanso...")
            try:
                page.views.append(paginaDescanso(page))
            except Exception as e:
                print(f"Erro ao carregar paginaDescanso: {e}")
                page.views.append(ft.Text(f"Erro ao carregar paginaDescanso: {e}"))
        elif page.route == "/treino":
            print("Carregando paginaTreino...")
            try:
                page.views.append(paginaTreino(page))
            except Exception as e:
                print(f"Erro ao carregar paginaTreino: {e}")
                page.views.append(ft.Text(f"Erro ao carregar paginaTreino: {e}"))
        elif page.route == "/acabou":
            print("Carregando paginaAcabou...")
            try:
                page.views.append(paginaAcabou(page))
            except Exception as e:
                print(f"Erro ao carregar paginaAcabou: {e}")
                page.views.append(ft.Text(f"Erro ao carregar paginaAcabou: {e}"))
        elif page.route == "/alterarTreino":
            print("Carregando alterarTreino...")
            try:
                page.views.append(paginaAlterarTreino(page))
            except Exception as e:
                print(f"Erro ao carregar alterarTreino: {e}")
                page.views.append(ft.Text(f"Erro ao carregar alterarTreino: {e}"))
        elif page.route == "/login":
            textresult.controls.clear()
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Text('Logar com o Google')
                        ),
                        ft.Container(
                            content=ft.Image(
                                src='https://img.icons8.com/?size=512&id=17949&format=png'
                            ),
                            height = 40,
                            on_click=logingoogle,
                            alignment = ft.alignment.center
                        ),
                        textresult,
                    ],
                    vertical_alignment= ft.MainAxisAlignment.CENTER,
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER
                )
            )
        else:
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Text('Logar com o Google')
                        ),
                        ft.Container(
                            content=ft.Image(
                                src='https://img.icons8.com/?size=512&id=17949&format=png'
                            ),
                            height = 40,
                            on_click=logingoogle,
                            alignment = ft.alignment.center
                        ),
                        textresult,
                    ],
                    vertical_alignment= ft.MainAxisAlignment.CENTER,
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER
                )
            )
        page.update()

    page.on_route_change = mudar_tela
    mudar_tela(page.route) # Carrega a tela inicial corretamente

ft.app(target=main, assets_dir="assets", port=9000, view=ft.AppView.FLET_APP_WEB)