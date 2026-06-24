# from-zero-to-agents

Trilha completa em Python para aprender a construir agentes de IA **do zero**, partindo da API crua da OpenAI, passando pelo LangChain e chegando ao LangGraph com sistemas multi-agente, ferramentas externas, persistência de memória, roteamento dinâmico via `Command` e **RAG**.

Cada módulo é incremental: um conceito novo por arquivo, com refatorações em pontos-chave para mostrar como o código evolui de scripts simples para um pacote modular.

---

## Trilha de Aprendizado

A ordem importa. Cada parte assume o conhecimento da anterior:

| Ordem | Pasta | Foco | README |
|---|---|---|---|
| 1 | [`part_openai/`](./part_openai/README.md) | Primeiro contato com a API da OpenAI via **SDK oficial**, sem framework. Mostra o fluxo cru: cliente, mensagens como `list[dict]`, `chat.completions.create` | [Ler ›](./part_openai/README.md) |
| 2 | [`part_langchain/`](./part_langchain/README.md) | Abstrações do **LangChain**: tipos de mensagem, LCEL, templates, output parsers, tools, memória e um sistema multi-agente refatorado em duas etapas | [Ler ›](./part_langchain/README.md) |
| 3 | [`part_langgraph/`](./part_langgraph/README.md) | Construção de grafos com **LangGraph**: estado, reducers, persistência via checkpoint, agentes com LLMs reais, roteamento dinâmico com a `Command` API, RAG vetorial com embeddings e vector store, **observabilidade com Langfuse** e **evals do router** | [Ler ›](./part_langgraph/README.md) |

Cada pasta tem um README próprio detalhando os exemplos, conceitos introduzidos e como executar.

---

## Pré-requisitos

- Conhecimento básico de Python
- [UV](https://docs.astral.sh/uv/) instalado
- Uma chave de API da OpenAI

---

## Setup Inicial

Faça este setup **uma única vez** na raiz do projeto. Vale para todas as partes da trilha.

### 1. Clonar e entrar no projeto

```bash
git clone https://github.com/lspraciano/from-zero-to-agents.git
cd from-zero-to-agents
```

### 2. Instalar dependências

```bash
uv sync
```

### 3. Configurar a chave da OpenAI

Copie o template e preencha sua chave:

```bash
cp .env.exemples .env
```

Edite o `.env`:

```
OPENAI_API_KEY=sk-...

# Necessário apenas para os módulos 15 e 16 (Langfuse)
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## Estrutura do Projeto

```
from-zero-to-agents/
├── part_openai/        # Etapa 1 — SDK oficial da OpenAI
├── part_langchain/     # Etapa 2 — LangChain do zero aos multi-agentes
├── part_langgraph/     # Etapa 3 — LangGraph, Command API e RAG
│
├── main.py
├── pyproject.toml
├── uv.lock
├── .env.exemples       # Template do .env
└── .python-version
```

---

## Como Executar os Exemplos

Todos os exemplos rodam a partir da **raiz do projeto** com `python -m`, para que as importações relativas funcionem corretamente:

```bash
# Etapa 1 — OpenAI
python -m part_openai.introduce_openai_1

# Etapa 2 — LangChain
python -m part_langchain.introduce_langchain_1

# Etapa 3 — LangGraph
python -m part_langgraph.introduce_langgraph_1
```

Os comandos completos de cada etapa estão documentados no README correspondente.

> ⚠️ A maioria dos exemplos faz chamadas reais à API da OpenAI e gera custo por execução. Os módulos finais do LangGraph também consultam APIs públicas externas (ex: PokeAPI), usam o modelo `text-embedding-3-small` para RAG vetorial e requerem uma conta no [Langfuse](https://cloud.langfuse.com) para observabilidade (módulos 15 e 16).

---

## Modelo Utilizado

Todos os exemplos com chamadas a LLM usam o modelo `gpt-4.1-mini` da OpenAI.

---

## Por Onde Começar

Se é a primeira vez aqui, o caminho é:

1. Faça o **setup inicial** acima
2. Abra o [README da `part_openai`](./part_openai/README.md) e rode o exemplo único — entende o fluxo cru da API
3. Vá para [`part_langchain`](./part_langchain/README.md) e siga a numeração dos arquivos do `_1` ao `_18`
4. Termine em [`part_langgraph`](./part_langgraph/README.md), também na ordem numérica, até o módulo mais recente
