import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from graph import graph
from prompts import SYSTEM_PROMPT

load_dotenv()

def main():
    print("--- Agente de CEP Iniciado ---" )
    print("Digite um CEP para consultar ou 'sair' para encerrar o programa.")

    # Inicializa o estado do agente com a mensagem do sistema
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    while True:
        try:
            user_input = input("Usuário: ")
            if user_input.lower() == "sair":
                break

            messages.append(HumanMessage(content=user_input))

            config = {"recursion_limit": 10}
            
            result = graph.invoke({"messages": messages}, config=config)

            last_message = result["messages"][-1]
            conteudo = last_message.content
            
            # Formatação para lidar com diferentes formatos de resposta
            if isinstance(conteudo, list):
                texto_final = ""
                
                for bloco in conteudo:
                    if isinstance(bloco, dict) and "text" in bloco:
                        texto_final += bloco["text"]
                
                    elif isinstance(bloco, str):
                        texto_final += bloco
                print(f"==Agente CEP==: {texto_final}")
            else:
                print(f"==Agente CEP==: {conteudo}")
            
            messages = result["messages"]

        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    # Verifica se a variável de ambiente está definidas
    if not os.getenv("GOOGLE_API_KEY"):
        print("Erro: A variável de ambiente 'GOOGLE_API_KEY' não está definida.")
    else:
        main()