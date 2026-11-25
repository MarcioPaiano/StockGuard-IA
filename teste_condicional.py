
import re

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from tools import consultar_produto
from analise import analisar_estoque


# 1. Estado compartilhado
class Estado(TypedDict):
    pergunta: str
    codigo: str
    dados: dict
    resposta: str


# 2. Primeiro nó: interpretar a pergunta
def interpretar(estado: Estado):

    print("[NÓ 1] Interpretando a pergunta...")

    pergunta = estado["pergunta"].upper()

    codigo = re.search(r"\bPRD-[0-9]{3}\b", pergunta)

    if codigo:
        return {"codigo": codigo.group()}

    return {"codigo": ""}


# 3. Decidir qual caminho seguir
def decidir(estado: Estado):

    if estado["codigo"]:
        print("[DECISÃO] Consultar a API.")
        return "consultar"

    print("[DECISÃO] Não consultar a API.")
    return "responder"


# 4. Segundo nó: consultar e analisar
def consultar(estado: Estado):

    print("[NÓ 2] Consultando a API...")

    produto = consultar_produto(estado["codigo"])

    dados = analisar_estoque(produto)

    if "erro" in dados:
        resposta = dados.get("mensagem", "Erro na consulta.")

    else:
        resposta = (
            f"Produto: {dados['nome']}\n"
            f"Estoque atual: {dados['quantidade_atual']} "
            f"{dados['unidade']}\n"
            f"Estoque mínimo: {dados['estoque_minimo']} "
            f"{dados['unidade']}\n"
            f"Situação: {dados['situacao']}\n"
            f"Reposição necessária: "
            f"{dados['reposicao_necessaria']} "
            f"{dados['unidade']}\n"
            f"Recomendação: {dados['recomendacao']}"
        )

    return {
        "dados": dados,
        "resposta": resposta
    }


# 5. Terceiro nó: responder sem consultar
def responder(estado: Estado):

    print("[NÓ 3] Respondendo sem consultar a API...")

    return {
        "resposta": (
            "Posso ajudar com consultas de estoque. "
            "Informe um código de produto no formato PRD-XXX."
        )
    }


# 6. Construir o grafo
grafo = StateGraph(Estado)

grafo.add_node("interpretar", interpretar)
grafo.add_node("consultar", consultar)
grafo.add_node("responder", responder)

grafo.add_edge(START, "interpretar")

grafo.add_conditional_edges(
    "interpretar",
    decidir,
    {
        "consultar": "consultar",
        "responder": "responder"
    }
)

grafo.add_edge("consultar", END)
grafo.add_edge("responder", END)

app = grafo.compile()


# 7. Executar o programa
if __name__ == "__main__":

    pergunta = input("Digite sua pergunta: ")

    resultado = app.invoke({
        "pergunta": pergunta,
        "codigo": "",
        "dados": {},
        "resposta": ""
    })

    print("\n=== STOCKGUARD IA ===\n")
    print(resultado["resposta"])
