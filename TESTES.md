
# StockGuard IA — Relatório de Testes

## 1. Objetivo

Validar o funcionamento do agente inteligente de gestão de
estoques StockGuard IA, desenvolvido como projeto final
do curso de Agentes de Inteligência Artificial do SENAI.

Os testes verificam a interpretação de perguntas, a tomada
de decisão, a consulta à API de estoque, a classificação
dos produtos, o tratamento de erros, a segurança e a
integração com o n8n.

## 2. Ambiente de testes

- Sistema operacional: Windows 11
- Linguagem: Python 3.12.10
- IDE: Visual Studio Code
- Modelo de IA: Gemini 3.5 Flash Lite
- Orquestração: LangGraph
- Comunicação HTTP: HTTPX
- Servidor: FastAPI e Uvicorn
- Automação: n8n 2.49.5
- API de estoque: porta 8000
- API StockGuard IA: porta 8001
- Interface n8n: porta 5678

## 3. Testes funcionais

### Teste 01 — Estoque baixo

- Entrada: Preciso repor o estoque do PRD-001?
- Esperado: identificar estoque abaixo do mínimo.
- Observado: Mouse sem fio, estoque atual de 5 unidades,
  mínimo de 10 unidades e reposição de 5 unidades.
- Classificação: BAIXO.
- Resultado: APROVADO.

### Teste 02 — Estoque normal

- Entrada: Qual o estoque do PRD-002?
- Esperado: identificar estoque suficiente.
- Observado: Teclado USB, estoque atual de 40 unidades,
  mínimo de 15 unidades e reposição igual a zero.
- Classificação: NORMAL.
- Resultado: APROVADO.

### Teste 03 — Estoque esgotado

- Entrada: Qual o estoque do PRD-004?
- Esperado: identificar ausência de estoque.
- Observado: Cabo HDMI 2 m, estoque atual de zero
  unidades, mínimo de 20 e necessidade de reposição de 20.
- Classificação: ESGOTADO.
- Resultado: APROVADO.

### Teste 04 — Estoque no limite

- Entrada: Qual o estoque do PRD-005?
- Esperado: identificar estoque igual ao mínimo.
- Observado: Papel sulfite A4, estoque atual de 30
  pacotes e estoque mínimo de 30 pacotes.
- Classificação: NORMAL.
- Recomendação: Estoque no limite. Monitorar.
- Resultado: APROVADO.

### Teste 05 — Produto inexistente

- Entrada: Qual o estoque do PRD-999?
- Esperado: tratar produto não encontrado.
- Retorno da API: HTTP 404.
- Observado: Produto não encontrado.
- Resultado: APROVADO.

### Teste 06 — Serviço indisponível

- Entrada: Consulte o PRD-503.
- Esperado: tratar indisponibilidade da API.
- Retorno da API: HTTP 503.
- Observado: Serviço temporariamente indisponível.
- Resultado: APROVADO.

### Teste 07 — Código inválido

- Entrada: ABC-1.
- Componente testado: ferramenta HTTP em Python.
- Esperado: rejeitar código fora do padrão PRD-XXX.
- Observado: código inválido, com orientação sobre
  o formato correto.
- Resultado: APROVADO.

### Teste 08 — Pergunta conceitual

- Entrada: O que é estoque mínimo?
- Esperado: responder sem consultar a API de estoque.
- Observado: explicação conceitual produzida pelo Gemini.
- Fluxo observado: interpretar e responder.
- Nó de consulta não executado.
- Resultado: APROVADO.

### Teste 09 — Pergunta ambígua

- Entrada: Como está meu estoque?
- Esperado: solicitar informações adicionais.
- Observado: solicitação de um código de produto
  no formato PRD-XXX.
- Resultado: APROVADO.

### Teste 10 — Pergunta fora do escopo

- Entrada: Qual a capital da França?
- Esperado: não responder a assuntos não relacionados
  à gestão de estoque.
- Observado: apresentação do StockGuard IA como
  assistente especializado em gestão de estoques.
- Resultado: APROVADO.

### Teste 11 — Segurança e alteração de estoque

- Entrada: Altere o estoque do PRD-001 para 100 unidades.
- Esperado: bloquear operações de escrita.
- Observado: alteração não autorizada. O agente
  opera somente para consulta.
- Nenhuma operação de escrita foi executada pelo agente.
- Resultado: APROVADO.

### Teste 12 — Consulta de múltiplos produtos

- Entrada: Consulte os produtos PRD-001 e PRD-002.
- Esperado: solicitar apenas um código por consulta.
- Observado: solicitação de esclarecimento.
- Resultado: APROVADO.

## 4. Testes de integração com n8n

O workflow foi desenvolvido com três nós:

1. Chat Trigger.
2. HTTP Request.
3. Edit Fields.

O n8n recebe a pergunta, encaminha uma requisição HTTP
POST ao servidor Python e apresenta a resposta do agente.

| Cenário | Resultado |
|---|---|
| Estoque esgotado | Aprovado |
| Estoque baixo | Aprovado |
| Estoque normal | Aprovado |
| Produto inexistente | Aprovado |
| Serviço indisponível | Aprovado |
| Pergunta conceitual | Aprovado |
| Pergunta ambígua | Aprovado |
| Pergunta fora do escopo | Aprovado |
| Bloqueio de alteração | Aprovado |

Os nove testes de integração foram realizados manualmente
e confirmados pelo desenvolvedor.

Em uma consulta ao produto PRD-004, o workflow executou
os três nós com sucesso em 1,483 segundo.

## 5. Resumo dos resultados

| Categoria | Realizados | Aprovados |
|---|---:|---:|
| Testes funcionais | 12 | 12 |
| Testes de integração | 9 | 9 |
| Total | 21 | 21 |

Taxa de aprovação dos cenários testados: 100%.

## 6. Evidências

As capturas de tela e registros de execução deverão
ser armazenados na pasta evidencias/.

A organização dos arquivos comprobatórios está em andamento.

## 7. Limitações

- Consulta de apenas um produto por solicitação.
- Dependência da disponibilidade do Gemini.
- Dependência da disponibilidade da API de estoque.
- Operação exclusivamente de leitura.
- Execução em ambiente local.
- Testes realizados manualmente.
- Instalação em um ambiente independente ainda não validada.

## 8. Conclusão

Os testes realizados demonstraram que o StockGuard IA
interpreta perguntas em linguagem natural, utiliza
roteamento condicional com LangGraph, consulta uma API
externa quando necessário, classifica o estoque, trata
falhas e bloqueia solicitações de alteração de dados.

A integração com o n8n permite a utilização do agente
por meio de uma interface conversacional.

Os cenários funcionais e de integração testados foram
aprovados.
