from rich.panel import Panel
from rich.console import Console
from rich.panel import Panel

console = Console()

lista_pedidos = [{"produtos": [{"nome_produto": "Lasanha", "quantidade": 1}, {"nome_produto": "Coca-Cola-2l", "quantidade": 2}, {"nome_produto": "Macarr\u00c3\u00a3o com Bacon", "quantidade": 1}], "id": "7711908795", "status": "Confirmado"}]
string_pedido = ''
for index, pedido in enumerate(lista_pedidos):
    for i in pedido['produtos']:
        string_pedido = string_pedido + f"{i['quantidade']}x {i['nome_produto']}\n"
    menu_pedidos = Panel(string_pedido.strip() + f"\nStatus: {pedido['status']}", title=f"{index+1}")
    console.print(menu_pedidos)
