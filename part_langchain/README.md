# LangChain  Do Zero aos Agentes

Esta pasta contém uma sequência progressiva de exemplos em Python que introduzem o **LangChain** partindo do básico (invocar um modelo) até a construção de um sistema multi-agente com roteamento. Cada arquivo acrescenta um conceito novo ao anterior, formando uma trilha de aprendizado guiada.

---

## Pré-requisitos

- Conhecimento básico de Python
- [UV](https://docs.astral.sh/uv/) instalado
- Uma chave de API da OpenAI configurada no arquivo `.env` na raiz do projeto:

```
OPENAI_API_KEY=sk-...
```

### Dependências

```bash
uv sync
```

---

## Estrutura de Arquivos

```
part_langchain/
├── introduce_langchain_1.py   # Invocação básica com dicts
├── introduce_langchain_2.py   # Mensagens tipadas (SystemMessage, HumanMessage)
├── introduce_langchain_3.py   # Output parser (StrOutputParser)
├── introduce_langchain_4.py   # LCEL — composição com o operador pipe (|)
├── introduce_langchain_5.py   # Formatação de prompts via .format()
├── introduce_langchain_6.py   # ChatPromptTemplate e variáveis de template
├── introduce_langchain_7.py   # Input do usuário via terminal
├── introduce_langchain_8.py   # Saída estruturada em JSON (manual)
├── introduce_langchain_9.py   # PydanticOutputParser — resposta tipada
├── introduce_langchain_10.py  # Loop de conversação contínuo
├── introduce_langchain_11.py  # Memória de histórico com MessagesPlaceholder
├── introduce_langchain_12.py  # Tool manual (calculadora via Pydantic)
├── introduce_langchain_13.py  # Re-invocação após uso de tool
├── introduce_langchain_14.py  # Loop de tool com condição `use_tool`
├── introduce_langchain_15.py  # Tool com decorator @tool do LangChain
├── introduce_langchain_16.py  # llm.bind_tools + ToolMessage nativo
├── introduce_langchain_17.py  # Múltiplas tools com despacho por dicionário
├── introduce_langchain_18.py  # Multi-agente: Router + Bio + General (monolítico)
│
├── introduce_langchain_19/   # Refatoração 1 — separação por chains
│   ├── orchestrator.py
│   ├── llm/
│   └── chains/
│       ├── router_chain.py
│       ├── bio_chain.py
│       └── general_chain.py
│
└── introduce_langchain_20/   # Refatoração 2 — separação por agentes
    ├── orchestrator.py
    ├── llm/
    │   └── llm.py
    └── agents/
        ├── bio_agent/
        │   ├── bio_agent_chain.py
        │   ├── bio_agent_parser.py
        │   ├── bio_agent_response_format.py
        │   ├── bio_agent_system_prompt.py
        │   └── bio_agent_template.py
        ├── general_agent/   # mesma estrutura do bio_agent
        └── router_agent/    # mesma estrutura do bio_agent
```

---

## Progressão dos Exemplos

### Bloco 1 — Fundamentos (arquivos 1–4)

| Arquivo | Conceito introduzido |
|---|---|
| `_1` | Chamada direta ao LLM com `list[dict]` |
| `_2` | Tipos de mensagem (`SystemMessage`, `HumanMessage`, `AIMessage`) |
| `_3` | `StrOutputParser` para extrair o conteúdo textual da resposta |
| `_4` | **LCEL** — composição de componentes com o operador `\|` (`chain = llm \| parser`) |

### Bloco 2 — Prompts Dinâmicos (arquivos 5–7)

| Arquivo | Conceito introduzido |
|---|---|
| `_5` | Interpolação de variáveis com `.format()` |
| `_6` | `ChatPromptTemplate` + `SystemMessagePromptTemplate` + `HumanMessagePromptTemplate` |
| `_7` | Leitura de input do usuário no terminal |

### Bloco 3 — Saídas Estruturadas (arquivos 8–11)

| Arquivo | Conceito introduzido |
|---|---|
| `_8` | Instrução de saída JSON manual + `json.loads` |
| `_9` | `PydanticOutputParser` com modelo Pydantic (`BaseModel`, `Field`) |
| `_10` | Loop infinito de conversação |
| `_11` | **Memória** — `MessagesPlaceholder` + lista `history` acumulando `HumanMessage` e `AIMessage` |

### Bloco 4 — Tools / Ferramentas (arquivos 12–17)

| Arquivo | Conceito introduzido |
|---|---|
| `_12` | Tool manual (`calculator_tool`) detectada via campo Pydantic `use_tool` |
| `_13` | Re-invocação da chain após execução da tool |
| `_14` | Loop de agência: continua invocando enquanto `use_tool` for `True` |
| `_15` | Decorator `@tool` do LangChain para registrar ferramentas |
| `_16` | `llm.bind_tools()` + `ToolMessage` nativos do LangChain |
| `_17` | Múltiplas tools despacho por dicionário (`tools: dict`) |

### Bloco 5 — Multi-Agentes (arquivo 18 + organizações)

| Artefato | Descrição |
|---|---|
| `_18.py` | Sistema completo em um único arquivo: **Router** → **Bio Agent** ou **General Agent**, com histórico compartilhado |
| `_19/` | Primeira refatoração: chains extraídas para módulos separados (`chains/`) com um `orchestrator.py` central |
| `_20/` | Segunda refatoração: cada agente vira um pacote próprio com chain, parser, template, system prompt e response format isolados |

---

## Como Executar

Execute qualquer arquivo diretamente pela raiz do projeto (para que as importações relativas funcionem):

```bash
# Arquivo simples
python -m part_langchain.introduce_langchain_1

# Versão multi-agente monolítica
python -m part_langchain.introduce_langchain_18

# Versão multi-agente refatorada (organização 2)
python -m part_langchain.introduce_langchain_20.orchestrator
```

> Os arquivos 7 em diante pedem input pelo terminal. Digite sua mensagem e pressione Enter.

---

## Modelo Utilizado

Todos os exemplos usam o modelo `gpt-4.1-mini` da OpenAI via `ChatOpenAI`.
