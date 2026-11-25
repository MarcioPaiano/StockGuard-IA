
from tools import consultar_produto


def analisar_estoque(produto):

    # Verificar se ocorreu algum erro
    if not isinstance(produto, dict):
        return {"erro": "resposta_invalida"}

    if "erro" in produto:
        return produto

    # Obter as quantidades
    atual = produto.get("quantidade_atual")
    minimo = produto.get("estoque_minimo")

    # Validar os dados recebidos
    if (
        type(atual) is not int
        or type(minimo) is not int
        or atual < 0
        or minimo < 0
    ):
        return {
            "erro": "dados_invalidos",
            "mensagem": "Quantidades de estoque inválidas."
        }

    # Calcular a reposição necessária
    reposicao = max(0, minimo - atual)

    # Classificar o estoque
    if atual == 0:
        situacao = "ESGOTADO"
        recomendacao = "Priorizar a reposição."

    elif atual < minimo:
        situacao = "BAIXO"
        recomendacao = "Recomenda-se reposição."

    elif atual == minimo:
        situacao = "NORMAL"
        recomendacao = "Estoque no limite. Monitorar."

    else:
        situacao = "NORMAL"
        recomendacao = "Manter monitoramento."

    # Devolver a análise
    return {
        **produto,
        "situacao": situacao,
        "reposicao_necessaria": reposicao,
        "recomendacao": recomendacao
    }


if __name__ == "__main__":

    codigo = input("Digite o código do produto: ")

    produto = consultar_produto(codigo)

    resultado = analisar_estoque(produto)

    print("\n=== STOCKGUARD IA ===\n")

    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")
