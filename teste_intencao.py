
import os
from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)


class Intencao(BaseModel):

    intencao: Literal[
        "CONSULTA",
        "CONCEITO",
        "ESCLARECIMENTO",
        "FORA_ESCOPO",
        "ALTERACAO"
    ]

    codigo: str = Field(
        description="Código do produto ou texto vazio."
    )


llm = ChatGoogleGenerativeAI(
    model=os.environ["CHAT_MODEL"],
    timeout=30,
    max_retries=0
)

interpretador = llm.with_structured_output(Intencao)

instrucoes = """
Você é o interpretador do StockGuard IA,
especializado em gestão de estoque.

Classifique a intenção do usuário:

CONSULTA:
Consulta de estoque de um produto com código.

CONCEITO:
Pergunta teórica sobre gestão de estoque.

ESCLARECIMENTO:
Consulta sem código, código inválido ou ambígua.

FORA_ESCOPO:
Pergunta sem relação com gestão de estoque.

ALTERACAO:
Solicitação para alterar, excluir ou cadastrar
produtos ou modificar quantidades.

Priorize ALTERACAO quando houver pedido de escrita.

Não invente códigos de produtos.

Extraia somente códigos informados pelo usuário.

O formato válido é PRD-XXX, com três dígitos.

Converta o código para letras maiúsculas.

Quando não houver código válido,
retorne uma string vazia no campo codigo.
"""

pergunta = input("Digite sua pergunta: ")

print("\nInterpretando pergunta...", flush=True)

try:
    resultado = interpretador.invoke([
        ("system", instrucoes),
        ("human", pergunta)
    ])

    print("\n=== INTERPRETAÇÃO DO GEMINI ===\n")
    print("Intenção:", resultado.intencao)
    print("Código:", resultado.codigo)

except Exception as erro:
    print("Erro:", erro)
