
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agente import agente

app = FastAPI(
    title="StockGuard IA",
    description="API de comunicação entre o n8n e o agente inteligente",
    version="1.0.0"
)


class Pergunta(BaseModel):
    pergunta: str = Field(min_length=1, max_length=2000)


@app.get("/")
def inicio():
    return {
        "servico": "StockGuard IA",
        "status": "online",
        "versao": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def conversar(dados: Pergunta):

    pergunta = dados.pergunta.strip()

    if not pergunta:
        raise HTTPException(
            status_code=422,
            detail="A pergunta não pode estar vazia."
        )

    try:
        resultado = agente.invoke({
            "pergunta": pergunta
        })

        return {
            "pergunta": pergunta,
            "intencao": resultado.get("intencao", ""),
            "codigo": resultado.get("codigo", ""),
            "resposta": resultado["resposta"]
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno no StockGuard IA."
        )
