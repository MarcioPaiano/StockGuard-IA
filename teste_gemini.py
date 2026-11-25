

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)

modelo = os.getenv("CHAT_MODEL")

print("=== STOCKGUARD IA ===")
print("Modelo:", modelo)

llm = ChatGoogleGenerativeAI(
    model=modelo,
    temperature=0,
    timeout=30,
    max_retries=0
)

pergunta = input("\nDigite sua pergunta: ")

print("\nConsultando inteligência artificial...", flush=True)

try:
    resposta = llm.invoke(pergunta)

    print("\n=== RESPOSTA DO GEMINI ===\n")
    print(resposta.text)

except Exception as erro:
    print("\nErro:", erro)
