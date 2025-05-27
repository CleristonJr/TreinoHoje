import flet as ft
import psycopg2 as psql
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

conexao = None
cursor = None
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

def main(page: ft.Page):
    page.title = "Exibir Primeiro Exercício Filtrado"

    resultados_coluna = ft.Column()

    if cursor:
        try:
            cursor.execute('SELECT COUNT(*) FROM exercicios WHERE tipo_treino = %s AND series >= %s', ('A', 1))
            quantidade = cursor.fetchone()
            print(int(quantidade[0]))

            cursor.execute('SELECT nome, repeticoes, series FROM exercicios WHERE tipo_treino = %s AND series >= %s', ('A', 1))
            resultado_pesquisa = cursor.fetchall()
            
            for i in range(int(quantidade[0])):
                if i < len(resultado_pesquisa):
                    exercicio = resultado_pesquisa[i]
                    nome_exercicio = exercicio[0]
                    repeticoes = exercicio[1]
                    series = exercicio[2]

                    resultados_coluna.controls.append(ft.Text(f"Nome: {nome_exercicio}"))
                    resultados_coluna.controls.append(ft.Text(f"Repetições: {repeticoes}"))
                    resultados_coluna.controls.append(ft.Text(f"Séries: {series}"))
                    resultados_coluna.controls.append(ft.Divider())
                else:
                    resultados_coluna.controls.append(ft.Text(f"Erro: Tentativa de acessar índice {i} fora dos limites dos resultados."))
        

        except psql.Error as e:
            resultados_coluna.controls.append(ft.Text(f"Erro ao executar a consulta: {e}"))
    else:
        resultados_coluna.controls.append(ft.Text("Não foi possível conectar ao banco de dados."))

    page.add(
        resultados_coluna,
    )

if __name__ == "__main__":
    ft.app(target=main)

if conexao:
    cursor.close()
    conexao.close()