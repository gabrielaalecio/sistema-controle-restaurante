import re

def string_vazia(texto):
    if texto.split() == "":
        return True
    return False

def idade(idade):
    if idade.isdigit():
        idade = int(idade)
        if idade >= 18 and idade <= 110:
            return True
    return False

def cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    if cpf == "0": #apenas para testes
        return True
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    # Verifica se os dígitos calculados são iguais aos informados
    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])

def cep(cep):
    cep = cep.replace("-", "")  
    return cep.isdigit() and len(cep) == 8

