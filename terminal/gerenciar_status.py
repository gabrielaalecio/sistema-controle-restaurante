from rich.panel import Panel
from rich.console import Console
from rich.panel import Panel
import json

console = Console()

def gerenciar_status(lista_pedidos, num_pedido, op):
    num_pedido = num_pedido -1
    match op:
        case 1: #!Confirmado
            lista_pedidos[num_pedido]['status'] = 'Confirmado'
            return True
        case 2: #!Em preparo
            lista_pedidos[num_pedido]['status'] = 'Em preparo'
            return True
        case 3: #!Pronto
            lista_pedidos[num_pedido]['status'] = 'Pronto'
            return True
        case 4: #!Entregue
            lista_pedidos[num_pedido]['status'] = 'Entrege'
            return True
    return False

def mostrar_pedidos(lista_pedidos):
    if len(lista_pedidos) > 0:
        string_pedido = ''
        for index, pedido in enumerate(lista_pedidos):
            for i in pedido['produtos']:
                string_pedido = string_pedido + f"{i['quantidade']}x {i['nome_produto']}\n"
            menu_pedidos = Panel(string_pedido.strip() + f"\nStatus: {pedido['status']}", title=f"{index+1}")
            console.print(menu_pedidos)
        return True
    else:
        return False

def apagar_pedido(lista_pedidos):
    return
