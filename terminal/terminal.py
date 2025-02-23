"""Área do Gestor (terminal):
○ Cadastrar pratos e atualizar preços.
○ Gerenciar pedidos e status (em preparo, pronto, entregue).
○ Emitir relatórios de vendas.
"""

from fun_pratos import *
from database import *
from rich.panel import Panel
from rich.console import Console
from time import sleep
import os

console = Console()

def main():
    lista_pratos = carregar_dados("terminal\pratos.json")
    menu_inicial = Panel("1. Cadastrar pratos.\n2. Editar pratos.\n3. Gerenciar pedidos e status.\n4. Emitir relatórios de vendas.\n5. Sair.", title="Menu")
    console.print(menu_inicial)
    try:
        op = int(console.input("Digite a opção desejada: "))
        os.system("cls")
        match op:
            #*Cadastrar pratos e atualizar preços
            case 1:
                nome = console.input("Nome do prato: ")
                descricao = console.input("Escreva a descrição do produto: ")
                tag = console.input("Categoria do prato. Separe por virgula',' Exemplo 'massas, carnes, etc...': ")
                preco = console.input("Preço: ")
                tempo_preparo = console.input("Tempo máximo de preparo: ")
                img = console.input("Digite o nome do arquivo de imagem. Exemplo 'img.png': ")
                lista_pratos.append(criar_prato(nome, descricao, tag, preco, tempo_preparo, img))
                console.print("[bold green]Prato criado com sucesso.[/bold green]")
            #*editar pratos
            case 2:

                return
            #*Gerenciar pedidos
            case 3:
                return
            #*Emitir relatório
            case 4:
                return
            #*sair
            case 5:
                return
    except ValueError:
        console.print("Opção inválida!")
        

main()
