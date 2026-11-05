# DR3_TP2 — Parte 2 | LangChain, FastAPI e Modelos de Linguagem

## Descrição do projeto

Este projeto foi desenvolvido para o Teste de Performance (TP2) da disciplina de Desenvolvimento de Data Driven Apps com Python.

O objetivo é desenvolver aplicações utilizando FastAPI e LangChain, explorando diferentes maneiras de integrar modelos de linguagem.

Foram desenvolvidas três funcionalidades:

- **Questão 1 — Fake LLM:** chatbot simulado com respostas predefinidas.
- **Questão 2 — Tradução inglês-francês:** integração com o modelo GPT-OSS 20B através do GroqCloud.
- **Questão 3 — Tradução inglês-alemão:** integração com o modelo Helsinki-NLP do Hugging Face.

Todas as aplicações recebem requisições HTTP e retornam respostas em JSON.

## Tecnologias utilizadas

- **Python:** linguagem de programação.
- **FastAPI e Pydantic:** criação das APIs e validação dos dados.
- **LangChain:** integração e gerenciamento dos modelos.
- **FakeListLLM:** simulação de respostas.
- **ChatOpenAI e GroqCloud:** acesso remoto ao GPT-OSS 20B.
- **Transformers e HuggingFacePipeline:** execução e integração dos modelos Hugging Face.
- **PyTorch:** processamento dos modelos locais.
- **Uvicorn:** servidor das aplicações.

## Estrutura do projeto

```text
Parte 2/
│
├── questão_1/
│   ├── app.py
│   └── Models.py
│
├── questão_2_e_3/
│   ├── app.py
│   ├── functions.py
│   └── models.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

O `app.py` contém as rotas FastAPI, os arquivos `models.py` definem as entradas com Pydantic e o `functions.py` contém as funções utilizadas na integração com Hugging Face.

## Instalação

**1. Clonar o repositório**

```bash
git clone URL_DO_REPOSITORIO
```

Acesse a pasta do projeto pelo terminal.

**2. Criar e ativar o ambiente virtual**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Instalar as dependências**

```powershell
python -m pip install -r requirements.txt
```

O projeto utiliza Transformers 4.x para manter a compatibilidade com o pipeline de tradução.

---

## Questão 1 — Chatbot com Fake LLM

A aplicação simula um chatbot utilizando `FakeListLLM` do LangChain.

As perguntas são associadas a respostas predefinidas através de um dicionário Python. O Fake LLM simula a execução do modelo, sem realizar inferência real.

### Execução

```powershell
cd "questão_1"
uvicorn app:app --reload
```

Acesse o Swagger UI:

http://127.0.0.1:8000/docs

**Endpoint:** `POST /Fake`

**Exemplo de entrada:**

```json
{
  "texto": "oi"
}
```

**Resposta:**

```json
"Olá!"
```

### Funcionamento

O FastAPI recebe a pergunta, o Pydantic valida os dados e um dicionário seleciona a resposta correspondente. O FakeListLLM devolve a resposta simulada.

Essa abordagem permite testar a estrutura da aplicação rapidamente, sem utilizar modelos reais ou APIs externas.

---

## Questão 2 — Tradução inglês-francês com GroqCloud

A aplicação utiliza o modelo `openai/gpt-oss-20b`, desenvolvido pela OpenAI e hospedado no GroqCloud.

A integração é realizada através do `ChatOpenAI` do LangChain, utilizando uma API compatível com a OpenAI.

### Configuração da API

Crie uma chave em:

https://console.groq.com/keys

No PowerShell, configure:

```powershell
$env:GROQ_API_KEY="SUA_CHAVE_AQUI"
```

A chave deve ser mantida privada e não pode ser publicada no GitHub.

### Execução

A partir da pasta principal da Parte 2:

```powershell
cd "questão_2_e_3"
uvicorn app:app --reload
```

Acesse `http://127.0.0.1:8000/docs`.

**Endpoint:** `POST /Translate/Fr`

**Exemplo de entrada:**

```json
{
  "text": "Artificial intelligence is changing the world."
}
```

**Resposta:**

```json
{
  "Inglês": "Artificial intelligence is changing the world.",
  "Francês": "L'intelligence artificielle change le monde."
}
```

### Funcionamento

O FastAPI recebe o texto em inglês e o LangChain utiliza um template de prompt para solicitar a tradução ao modelo hospedado no GroqCloud.

Foram adicionados parâmetros de `timeout` e `max_retries` para controlar o comportamento das chamadas em situações de falha.

Também foi utilizada a função `time.perf_counter()` para medir a duração da execução.

### Testes de latência

| Teste | Tempo | Status HTTP |
|---|---|---|
| Texto curto | 0,83 s | 200 |
| Texto maior | 1,29 s | 200 |

Nos testes realizados, as chamadas foram concluídas em menos de dois segundos. Entretanto, esses tempos podem variar conforme a conexão, a disponibilidade do serviço e o tamanho dos textos.

As medições representam o tempo de execução da cadeia LangChain, não o tempo total da requisição HTTP.

---

## Questão 3 — Tradução inglês-alemão com Hugging Face

A aplicação utiliza o modelo `Helsinki-NLP/opus-mt-en-de` para traduzir textos do inglês para o alemão.

Diferentemente da Questão 2, o processamento ocorre localmente, utilizando Transformers e PyTorch.

### Execução

Utiliza o mesmo servidor da Questão 2:

```powershell
cd "questão_2_e_3"
uvicorn app:app --reload
```

Na primeira execução, os arquivos do modelo poderão ser baixados automaticamente.

**Endpoint:** `POST /Translate/Al`

**Exemplo de entrada:**

```json
{
  "text_al": "Artificial intelligence is changing the world."
}
```

**Resposta:**

```json
{
  "Inglês": "Artificial intelligence is changing the world.",
  "Alemão": "Künstliche Intelligenz verändert die Welt."
}
```

### Funcionamento

O texto é recebido pelo FastAPI e enviado ao modelo Helsinki-NLP.

O modelo é carregado pelo Transformers e integrado ao LangChain através da classe `HuggingFacePipeline`.

A tradução é executada com `.invoke()` e retornada como JSON. Como o modelo é especializado em tradução inglês-alemão, não foi necessário utilizar um PromptTemplate.

---

## Testes e observações

As três aplicações foram testadas utilizando o Swagger UI.

- **Questão 1:** respostas simuladas para perguntas predefinidas.
- **Questão 2:** tradução inglês-francês e medição de latência.
- **Questão 3:** tradução inglês-alemão com frases e textos maiores.

As requisições bem-sucedidas retornaram HTTP `200`.

O FakeListLLM não realiza inferência real. A Questão 2 depende de conexão com o GroqCloud e chave válida, enquanto a Questão 3 utiliza recursos computacionais locais.

## Considerações finais

O desenvolvimento das aplicações permitiu praticar a integração do LangChain com FastAPI, utilizando três abordagens diferentes: simulação com Fake LLM, inferência remota com GroqCloud e inferência local com Hugging Face.

Também foi possível compreender melhor o funcionamento de prompts, chamadas aos modelos, validação de dados e desempenho de APIs de inteligência artificial.