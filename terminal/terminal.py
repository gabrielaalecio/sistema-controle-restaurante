from fun_pratos import *
from database import *
from rich.panel import Panel
from rich.console import Console
from time import sleep
import os

console = Console()

def main():
    arquivo = "terminal\pratos.json"
    while True:
        lista_pratos = carregar_dados(arquivo)
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
                    if not verificar_preco(preco):
                        console.print("Preço inválido!")
                        break
                    tempo_preparo = console.input("Tempo máximo de preparo em minutos: ")
                    img = console.input("Digite o nome do arquivo de imagem. Exemplo 'img.png': ")
                    lista_pratos.append(criar_prato(nome, descricao, tag, preco, tempo_preparo, img))
                    console.print("[bold green]Prato criado com sucesso.[/bold green]")
                #*editar pratos
                case 2:
                    if listar_pratos(lista_pratos): #"nome": nome, "descricao": descricao, "tag":tag, "preco": preco, "tempo": tempo, "img": imagem
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
