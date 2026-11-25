
import os
import re

from typing import TypedDict, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

from tools import consultar_produto
from analise import analisar_estoque


# CONFIGURACAO DA INTELIGENCIA ARTIFICIAL

load_dotenv(override=True)

llm = ChatGoogleGenerativeAI(
    model=os.environ["CHAT_MODEL"],
    timeout=30,
    max_retries=0
)


# ESTRUTURA DA INTENCAO

class Intencao(BaseModel):

    intencao: Literal[
        "CONSULTA",
        "CONCEITO",
        "ESCLARECIMENTO",
        "FORA_ESCOPO",
        "ALTERACAO"
    ]

    codigo: str = Field(
        description="Codigo do produto ou texto vazio."
    )


interpretador = llm.with_structured_output(Intencao)


# ESTADO COMPARTILHADO DO LANGGRAPH

class Estado(TypedDict, total=False):

    pergunta: str
    intencao: str
    codigo: str
    dados: dict
    resposta: str


# NO 1 - INTERPRETAR A PERGUNTA

def interpretar(estado: Estado):

    print("[NO 1] Interpretando pergunta...")

    instrucoes = """
    Voce e o interpretador do StockGuard IA.

    Classifique a solicitacao em:

    CONSULTA: consulta de produto com codigo.
    CONCEITO: pergunta teorica sobre estoque.
    ESCLARECIMENTO: pergunta ambigua ou sem codigo.
    FORA_ESCOPO: assunto nao relacionado a estoque.
    ALTERACAO: pedido para modificar, excluir ou
    cadastrar produtos ou alterar quantidades.

    Priorize ALTERACAO em pedidos de escrita.

    Nao invente codigos.

    Extraia apenas codigos informados pelo usuario.

    O formato valido e PRD-XXX, com tres digitos.

    Retorne codigo vazio quando nao houver codigo valido.
    """

    try:

        resultado = interpretador.invoke([
            ("system", instrucoes),
            ("human", estado["pergunta"])
        ])

        intencao = resultado.intencao
        codigo = resultado.codigo.strip().upper()

        # Validacao independente da inteligencia artificial

        codigos = set(re.findall(
            r"\bPRD-[0-9]{3}\b",
            estado["pergunta"].upper()
        ))

        if intencao == "CONSULTA":

            if len(codigos) != 1 or codigo not in codigos:

                intencao = "ESCLARECIMENTO"
                codigo = ""

        print("Intencao:", intencao)
        print("Codigo:", codigo)

        return {
            "intencao": intencao,
            "codigo": codigo
        }

    except Exception:

        return {
            "intencao": "ERRO",
            "codigo": "",
            "resposta": (
                "Nao foi possivel interpretar a pergunta. "
                "Tente novamente mais tarde."
            )
        }


# ROTEAMENTO CONDICIONAL

def decidir(estado: Estado):

    if estado["intencao"] == "CONSULTA":
        return "consultar"

    return "responder"


# NO 2 - CONSULTAR A API

def consultar(estado: Estado):

    print("[NO 2] Consultando API de estoque...")

    produto = consultar_produto(estado["codigo"])

    return {"dados": produto}


# NO 3 - ANALISAR O ESTOQUE

def analisar(estado: Estado):

    print("[NO 3] Analisando estoque...")

    resultado = analisar_estoque(estado["dados"])

    if "erro" in resultado:

        return {
            "resposta": resultado.get(
                "mensagem",
                "Nao foi possivel consultar o produto."
            )
        }

    resposta = (
        f"Produto: {resultado['nome']}\n"
        f"Codigo: {resultado['codigo']}\n"
        f"Categoria: {resultado['categoria']}\n"
        f"Estoque atual: {resultado['quantidade_atual']}"
        f" {resultado['unidade']}\n"
        f"Estoque minimo: {resultado['estoque_minimo']}"
        f" {resultado['unidade']}\n"
        f"Situacao: {resultado['situacao']}\n"
        f"Reposicao necessaria: "
        f"{resultado['reposicao_necessaria']}"
        f" {resultado['unidade']}\n"
        f"Recomendacao: {resultado['recomendacao']}"
    )

    return {"resposta": resposta}


# NO 4 - RESPONDER SEM CONSULTAR A API

def responder(estado: Estado):

    print("[NO 4] Respondendo sem consultar API de estoque...")

    intencao = estado["intencao"]

    if intencao == "CONCEITO":

        try:

            resposta = llm.invoke([
                (
                    "system",
                    "Voce e especialista em gestao de estoque. "
                    "Responda em portugues, de forma objetiva. "
                    "Nao invente dados de produtos ou estoques reais. "
                    "Limite a resposta a tres frases."
                ),
                ("human", estado["pergunta"])
            ])

            return {"resposta": resposta.text}

        except Exception:

            return {
                "resposta": (
                    "Inteligencia artificial temporariamente "
                    "indisponivel."
                )
            }

    if intencao == "ESCLARECIMENTO":

        return {
            "resposta": (
                "Informe um unico codigo de produto "
                "no formato PRD-XXX. Exemplo: PRD-001."
            )
        }

    if intencao == "ALTERACAO":

        return {
            "resposta": (
                "Alteracao nao autorizada. "
                "O StockGuard IA opera somente para consulta. "
                "Nenhum dado foi modificado."
            )
        }

    if intencao == "ERRO":

        return {
            "resposta": estado["resposta"]
        }

    return {
        "resposta": (
            "Sou o StockGuard IA, especializado em "
            "gestao e consulta de estoques."
        )
    }


# CONSTRUCAO DO GRAFO

grafo = StateGraph(Estado)

grafo.add_node("interpretar", interpretar)
grafo.add_node("consultar", consultar)
grafo.add_node("analisar", analisar)
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

grafo.add_edge("consultar", "analisar")
grafo.add_edge("analisar", END)
grafo.add_edge("responder", END)

agente = grafo.compile()


# EXECUCAO DO PROGRAMA

if __name__ == "__main__":

    print("=" * 45)
    print("           STOCKGUARD IA")
    print("    Agente Inteligente de Estoque")
    print("=" * 45)

    while True:

        pergunta = input("\nVoce: ").strip()

        if pergunta.lower() in ["sair", "exit"]:

            print("StockGuard IA encerrado.")
            break

        if not pergunta:
            continue

        resultado = agente.invoke({
            "pergunta": pergunta
        })

        print("\n=== STOCKGUARD IA ===\n")
        print(resultado["resposta"])
