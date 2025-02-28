import json

def salvar_dados(lista, arq):
    with open(arq, 'w') as arquivo:
        json.dump(lista, arquivo)

def carregar_dados(arq):
    try:
        with open(arq, 'r') as arquivo:
            return json.load(arquivo)
    except:
        return []


