import json

def salvar_dados(lista_pratos, arq):
    with open(arq, 'w') as arquivo:
        json.dump(lista_pratos, arquivo)

def carregar_dados(arq):
    try:
        with open(arq, 'r') as arquivo:
            return json.load(arquivo)
    except:
        return []


