import re

def limpar_cep(cep: str) -> str:
    """
    Remove caracteres não numéricos do CEP.
    Ex: '12.345-678' -> '12345678'
    """
    return re.sub(r'\D', '', cep)