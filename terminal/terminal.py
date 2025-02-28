from fun_pratos import *
from gerenciar_status import *
from database import *
from rich.panel import Panel
from rich.console import Console
from time import sleep
import os

console = Console()

def main():
    arquivo = "foto-pratos\image.png"
    arquivo_pedidos = "pedidos.json"
    while True:
        lista_pratos = carregar_dados(arquivo)
        lista_pedidos = carregar_dados(arquivo_pedidos)
        menu_inicial = Panel("1. Cadastrar pratos.\n2. Editar pratos.\n3. Gerenciar pedidos e status.\n4. Emitir relatórios de vendas.\n5. Sair.", title="Menu")
        console.print(menu_inicial)
        try:
            op = int(console.input("Digite a opção desejada: "))
            os.system("cls")
            match op:
                #*Cadastrar pratos e atualizar preços
                case 1:
                    nome = console.input("Nome do prato: ")
                    if not verificar_nome(nome):
                        console.print("Nome inválido!")
                        break
                    descricao = console.input("Escreva a descrição do produto: ")
                    tag = console.input("Categoria do prato. Separe por virgula ',' Exemplo 'massas, carnes, etc...': ")
                    preco = console.input("Preço: ")
                    if not verificar_decimal(preco):
                        console.print("Preço inválido!")
                        break
                    tempo_preparo = console.input("Tempo máximo de preparo em minutos: ")
                    if not verificar_decimal(tempo_preparo):
                        console.print("Tempo inválido!")
                    img = console.input("Digite o nome do arquivo de imagem. Exemplo 'img.png': ")
                    try:
                        open(img, 'r')
                    except:
                        console.print("[bold red]Imagem não encontrada![/bold red]")
                        break
                    lista_pratos.append(criar_prato(nome, descricao, tag, preco, tempo_preparo, img))
                    console.print("[bold green]Prato criado com sucesso.[/bold green]")
                #*editar pratos
                case 2:
                    if listar_pratos(lista_pratos):
                        prato_indice = int(input("Digite o número do prato: ")) - 1
                        if 0 <= prato_indice <= tamanho_lista(lista_pratos):
                            menu_editar = Panel("1. Editar nome.\n2. Editar descrição.\n3. Editar Tags.\n4. Editar Preços.\n5. Editar tempo de preparo.\n6. Editar caminho da imagem.\n7. Sair.", title="Menu de Edição")
                            console.print(menu_editar)
                            op_editar = int(input("Digite a opção desejada: "))
                            prato_editar = lista_pratos[prato_indice]
                            if editar_prato(prato_editar, op_editar):
                                console.print("[bold green]Prato editado com sucesso![/bold green]")
                #*Gerenciar pedidos
                case 3:
                    if mostrar_pedidos(lista_pedidos):
                        opcao_pedido = int(console.input("Digite o número do pedido: "))
                        if 1 <= opcao_pedido <= len(lista_pedidos):
                            gerenciar_status(lista_pedidos, opcao_pedido)
                    else:
                        console.print("[bold red]Não há pedidos em andamento.[/bold red]")
                    return
                #*Emitir relatório
                case 4:
                    return
                #*sair
                case 5:
                    return
            salvar_dados(lista_pratos, arquivo)
            sleep(2)
            os.system("cls")
        except ValueError:
            console.print("Opção inválida!")
        

main()
