import requests
from langchain_core.tools import tool
from utils import limpar_cep

@tool
def consultar_cep_viacep(cep: str) -> str:
    """
    Consulta o endereço completo de um CEP braisleiro usando a API ViaCEP.
    Recebe um CEP (com ou sem formatação) e retorna o endereço ou erro.
    """

    # Validação básica do CEP
    cep_limpo = limpar_cep(cep)

    # Validar se o CEP tem 8 dígitos
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        return "Erro: CEP inválido. Deve conter 8 dígitos numéricos."
    
    # Consultar a API ViaCEP
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    try:
        response = requests.get(url, timeout=5)

        # Tratamento de erro HTTP (Bad Request)
        if response.status_code == 400:
            return "Erro: CEP inválido (Bad Request)."
        
        response.raise_for_status()
        data = response.json()

        # Tratamento de erro de CEP não encontrado ("erro": true)
        if "erro" in data and data["erro"] is True:
            return f"Erro: O CEP {cep_limpo} não foi encontrado."
        
        return str(data)
    
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão com a API ViaCEP: {e}"
