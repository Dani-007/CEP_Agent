import os
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from state import AgentState
from tools import consultar_cep_viacep
from prompts import SYSTEM_PROMPT

# Configuração do modelo LLM do Google Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

# Lista de ferramentas disponíveis
ferramentas = [consultar_cep_viacep]

llm_com_tools = llm.bind_tools(ferramentas)

# Definição dos Nós
def agent_node(state: AgentState):
    messages = state["messages"]
    response = llm_com_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(ferramentas)

# Definição do Grafo
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

builder.set_entry_point("agent")

builder.add_conditional_edges(
    "agent",
    tools_condition
)

builder.add_edge("tools", "agent")

graph = builder.compile()