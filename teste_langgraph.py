
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Definir o estado compartilhado
class Estado(TypedDict):
    nome: str
    mensagem: str


# 2. Criar o primeiro nó
def saudacao(estado: Estado):

    nome = estado["nome"]

    print("Executando o nó 1...")

    return {
        "mensagem": f"Olá, {nome}!"
    }


# 3. Criar o segundo nó
def finalizar(estado: Estado):

    print("Executando o nó 2...")

    mensagem = estado["mensagem"]

    return {
        "mensagem": mensagem + " Bem-vindo ao StockGuard IA!"
    }


# 4. Criar o grafo
grafo = StateGraph(Estado)


# 5. Adicionar os nós
grafo.add_node("saudacao", saudacao)
grafo.add_node("finalizar", finalizar)


# 6. Criar as conexões
grafo.add_edge(START, "saudacao")
grafo.add_edge("saudacao", "finalizar")
grafo.add_edge("finalizar", END)


# 7. Compilar o grafo
app = grafo.compile()


# 8. Receber o nome do usuário
nome = input("Digite seu nome: ")


# 9. Executar o grafo
resultado = app.invoke({
    "nome": nome,
    "mensagem": ""
})


# 10. Mostrar o resultado
print("\n=== RESULTADO FINAL ===")
print(resultado["mensagem"])
