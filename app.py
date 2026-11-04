
from langchain_core.language_models.fake import FakeListLLM
from fastapi import FastAPI
from Models import Pergunta

app = FastAPI()

# Perguntas e respostas predefinidas para simular o chatbot
respostas = {
    "oi": "Olá!",
    "quem descobriu o brasil?": "Pedro Álvares Cabral.",
    "qual a idade do planeta terra?": "Aproximadamente 4,54 bilhões de anos!"
}

@app.post("/Fake")
def Fake_llm_test(texto: Pergunta):

    # Recebe o texto do usuário, remove espaços extras
    # e converte para minúsculas para facilitar a comparação.
    pergunta = texto.texto.strip().lower()

    # Procura a pergunta no dicionário.
    # Se não encontrar, retorna uma resposta padrão.
    resposta_escolhida = respostas.get(pergunta, "Desculpe, não sei responder a essa pergunta.")

    # Cria um Fake LLM com a resposta selecionada.
    # O FakeListLLM recebe uma lista de respostas.
    llm = FakeListLLM(responses=[resposta_escolhida])

    # Simula a execução do modelo usando a pergunta recebida.
    resultado = llm.invoke(texto.texto)

    return resultado

