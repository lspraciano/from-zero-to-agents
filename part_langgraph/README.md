# LangGraph — Do Zero aos Agentes

Esta pasta contém uma sequência progressiva de exemplos em Python que introduzem o **LangGraph** partindo do básico (criar um grafo e invocar nós) até a construção de um sistema multi-agente com LLMs reais, ferramentas e persistência de memória. Cada módulo acrescenta um conceito novo ao anterior, formando uma trilha de aprendizado guiada.

---

## Pré-requisitos

- Conhecimento básico de Python
- Ter percorrido a trilha [`part_langchain`](../part_langchain/README.md) (recomendado)
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
part_langgraph/
├── introduce_langgraph_1.py    # Grafo mínimo com roteamento aleatório
├── introduce_langgraph_2.py    # Roteamento determinístico por input do usuário
├── introduce_langgraph_3.py    # Histórico de mensagens dentro do estado
├── introduce_langgraph_4.py    # Histórico de mensagens fora do grafo
├── introduce_langgraph_5.py    # Schema enxuto — messages[-1] como mensagem atual
├── introduce_langgraph_6.py    # Tipos LangChain (HumanMessage / BaseMessage)
├── introduce_langgraph_7.py    # Resposta do nó via campo graph_response
├── introduce_langgraph_8.py    # Reducer add_messages + AIMessage nos nós
├── introduce_langgraph_9.py    # Persistência com MemorySaver e thread_id
│
├── introduce_langgraph_10/     # Refatoração em pacote modular
│   ├── graph_executor.py
│   ├── states/
│   ├── nodes/
│   ├── edges/
│   ├── graphs/
│   └── checkpointers/
│
└── introduce_langgraph_11/     # LLMs reais, agentes e ferramentas nos nós
    ├── graph_executor.py
    ├── states/
    ├── nodes/
    ├── edges/
    ├── graphs/
    ├── checkpointers/
    ├── llm_models/
    ├── tools/
    │   └── invert_text_tool.py
    └── agents/
        ├── router_agent/
        ├── general_agent/
        └── reverse_text_agent/
```

---

## Progressão dos Exemplos

### Bloco 1 — Fundamentos do Grafo (arquivos 1–2)

| Arquivo | Conceito introduzido |
|---|---|
| `_1` | `StateGraph`, `TypedDict`, nós, arestas, `add_conditional_edges`, `compile`, `invoke` — roteamento **aleatório** |
| `_2` | Roteamento **determinístico** baseado no tamanho da mensagem do usuário |

### Bloco 2 — Gestão de Estado (arquivos 3–5)

| Arquivo | Conceito introduzido |
|---|---|
| `_3` | Histórico de mensagens **dentro** do estado (atualizado pelo nó router) |
| `_4` | Histórico de mensagens **fora** do grafo (passado como input a cada invoke) |
| `_5` | Schema enxuto sem campo duplicado — `messages[-1]` como mensagem atual |

### Bloco 3 — Tipos de Mensagem LangChain (arquivos 6–8)

| Arquivo | Conceito introduzido |
|---|---|
| `_6` | `BaseMessage` / `HumanMessage` no estado em vez de strings puras |
| `_7` | Campo `graph_response` nos nós + append manual de `AIMessage` após `invoke` |
| `_8` | **Reducer `add_messages`** — nós emitem `AIMessage` diretamente no estado; fim do campo auxiliar |

### Bloco 4 — Persistência e Threads (arquivo 9)

| Arquivo | Conceito introduzido |
|---|---|
| `_9` | `MemorySaver`, `thread_id` via `RunnableConfig` — estado multi-turno **persistido via checkpoint** |

### Bloco 5 — Estrutura de Projeto (pasta 10)

| Artefato | Descrição |
|---|---|
| `introduce_langgraph_10/` | Refatora os conceitos do módulo 9 em um **pacote modular** com separação clara entre estado, nós, arestas, grafo, checkpointer e executor. Inclui diagrama **Mermaid** do grafo |

### Bloco 6 — LLMs e Ferramentas Reais (pasta 11)

| Artefato | Descrição |
|---|---|
| `introduce_langgraph_11/` | Primeiro módulo com **chamadas reais a LLMs** dentro dos nós. O roteamento é feito por **intenção** (via LLM) em vez de heurística. Introduz **`@tool`**, **`create_agent`** e **saída estruturada com Pydantic** (`response_format`) |

---

## Como Executar

Execute a partir da raiz do projeto para que as importações relativas funcionem:

```bash
# Arquivos simples (módulos 1–9)
python -m part_langgraph.introduce_langgraph_1

# Versões em pacote (módulos 10 e 11)
python -m part_langgraph.introduce_langgraph_10.graph_executor
python -m part_langgraph.introduce_langgraph_11.graph_executor
```

> Os módulos 2 em diante pedem input pelo terminal. Digite sua mensagem e pressione Enter.

---

## Modelo Utilizado

Os módulos com chamadas a LLM usam o modelo `gpt-4.1-mini` da OpenAI via `ChatOpenAI`.

---

## Próximo Passo

Com os fundamentos do LangGraph consolidados, o próximo módulo evolui para agentes com múltiplas ferramentas externas e fluxos de decisão mais complexos.
