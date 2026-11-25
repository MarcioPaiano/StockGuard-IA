
import httpx
import re

API_URL = "http://127.0.0.1:8000"


def validar_produto(produto, codigo):

    if not isinstance(produto, dict):
        return False

    campos_texto = [
        "codigo",
        "nome",
        "categoria",
        "unidade"
    ]

    for campo in campos_texto:
        valor = produto.get(campo)

        if not isinstance(valor, str) or not valor.strip():
            return False

    if produto["codigo"] != codigo:
        return False

    campos_numericos = [
        "quantidade_atual",
        "estoque_minimo"
    ]

    for campo in campos_numericos:
        valor = produto.get(campo)

        if type(valor) is not int or valor < 0:
            return False

    return True


def consultar_produto(codigo):

    if not isinstance(codigo, str):
        return {
            "erro": "codigo_invalido",
            "mensagem": "O código deve ser um texto."
        }

    codigo = codigo.strip().upper()

    if not re.fullmatch(r"PRD-[0-9]{3}", codigo):
        return {
            "erro": "codigo_invalido",
            "mensagem": "Use o formato PRD-XXX."
        }

    url = f"{API_URL}/produtos/{codigo}"

    try:

        resposta = httpx.get(url, timeout=10)

        if resposta.status_code == 200:

            produto = resposta.json()

            if not validar_produto(produto, codigo):
                return {
                    "erro": "dados_invalidos",
                    "mensagem": "Dados do produto inválidos."
                }

            return produto

        elif resposta.status_code == 404:
            return {
                "erro": "produto_nao_encontrado",
                "mensagem": "Produto não encontrado."
            }

        elif resposta.status_code == 503:
            return {
                "erro": "servico_indisponivel",
                "mensagem": "Serviço temporariamente indisponível."
            }

        else:
            return {
                "erro": "erro_api",
                "mensagem": f"Erro HTTP {resposta.status_code}"
            }

    except httpx.RequestError:
        return {
            "erro": "falha_conexao",
            "mensagem": "Não foi possível conectar à API."
        }

    except ValueError:
        return {
            "erro": "resposta_invalida",
            "mensagem": "A API retornou dados inválidos."
        }


if __name__ == "__main__":

    codigo = input("Digite o código do produto: ")

    resultado = consultar_produto(codigo)

    print("\nResultado da consulta:")
    print(resultado)
