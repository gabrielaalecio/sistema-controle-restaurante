from rich.console import Console
from rich.panel import Panel
import re

console = Console()

def criar_prato(nome,descricao,tag, preco, tempo, imagem):
    prato = {"nome": nome, "descricao": descricao, "tag":tag, "preco": preco, "tempo": tempo, "img": imagem}
    return prato

def buscar_prato(nome, lista): #ver como vamos usar a função para modificar
    for prato_lista in lista:
        if prato_lista['nome'] == nome:
            return prato_lista
    return None

def listar_pratos(lista):
    if tem_pratos(lista):
        for index, prato in enumerate(lista):
            painel = Panel(f"Nome: {prato['nome']}\nDescrição: {prato['descricao']}\nTag: {prato['tag']}\nPreço: {prato['preco']}\nTempo de preparo: {prato['tempo']}\nCaminho da imagem: {prato['img']}", title=f"{index + 1}")
            console.print(painel)
        return True
    return False

def editar_prato(prato, opcao):
    match opcao:
        case 1:
            nome_novo = console.input("Nome: ")
            if verificar_nome(nome_novo):
                prato['nome'] = nome_novo 
        case 2:
            descricao_nova = console.input("Descrição: ")
        case 3:
            tag_nova = console.input("Tag: ")
        case 4:
            preco_novo = console.input("Preço: ")
        case 5:
            tempo_novo = console.input("Tempo de preparo: ")
        case 6:
            img_nova = console.input("Imagem: ")
        case 7:
            console.print("Saindo...")
            return
        case _:
            console.print("[bold red]Digite uma opção válida![/bold red]")
    
def tamanho_lista(lista):
    return len(lista)

def tem_pratos(lista):
    return len(lista) > 0

def verificar_nome(nome):
    return bool(re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ ]+", nome))

def verificar_decimal(decimal):
    return bool(re.fullmatch(r"\d+(\.\d{1,2})?", decimal))