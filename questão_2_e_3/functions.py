import torch
from transformers import pipeline, GenerationConfig
from langchain_huggingface import HuggingFacePipeline

def load_llm_enal_pipeline():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    pipe = pipeline(
        task="translation",
        model="Helsinki-NLP/opus-mt-en-de",
        device = device
    )

    llm = HuggingFacePipeline(pipeline=pipe)

    return llm


def translate_text(llm, frase):
    resultado = llm.invoke(frase)
    return resultado