from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from fastapi import FastAPI
import os
import time

from models import TextEn, TextAl
from functions import load_llm_enal_pipeline, translate_text

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
    use_responses_api=False,
    timeout=20,
    max_retries=1
)

# Define o prompt com uma variável para o texto recebido
prompt = PromptTemplate.from_template(
    "Translate the following English text into French. "
    "Return only the translation.\n"
    "Text: {texto}"
)

# Conecta o prompt ao modelo utilizando LangChain
chain = prompt | llm

app = FastAPI()

@app.post("/Translate/Fr")
def Traduzir_En_Fr(texto: TextEn):

    inicio = time.perf_counter()

    # Envia a entrada para a cadeia
    resposta = chain.invoke({"texto": texto.text})

    fim = time.perf_counter()
    duracao = fim - inicio
    print(f"Tempo de execução: {duracao:.2f} segundos")

    return {
        "Inglês": texto.text,
        "Francês": resposta.content
    }


# ----------------------------------------------- Questão 3 ----------------------------------------- #
all = load_llm_enal_pipeline()

@app.post("/Translate/Al")
def Traduzir_En_Al(texto: TextAl):
    resposta = translate_text(all, texto.text_al)
    return {
    "Inglês": texto.text_al,
    "Alemão": resposta
    }