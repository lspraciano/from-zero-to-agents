# Agentes com LangChain e LangGraph

Do zero ao agente real — uma progressão incremental onde cada módulo resolve um problema que o anterior ainda tinha.

---

## Por que esse curso é diferente

A maioria dos tutoriais começa pelo resultado final. Aqui a ordem é inversa: você implementa cada mecanismo na mão antes de ver o framework fazer por você. Quando o `AgentExecutor` encapsula o loop de tools no módulo 12, você já sabe exatamente o que está acontecendo lá dentro — porque você mesmo escreveu isso no módulo 11.

---

## Estrutura

```
.
├── 01/   # Chamada direta à API OpenAI
├── 02/   # Introdução ao LangChain
├── 03/   # Templates de prompt dinâmicos
├── 04/   # Histórico de conversa manual
├── 05/   # Histórico gerenciado pelo framework
├── 06/   # Saída estruturada com Pydantic Parser
├── 07/   # Saída estruturada nativa do LLM
├── 08/   # Router pattern entre chains
├── 09/   # Function calling manual via JSON
├── 10/   # Tool calling nativo
├── 11/   # Loop de tool calling
├── 12/   # AgentExecutor
├── 13/   # Introdução ao LangGraph
├── 14/   # Grafo com LLM router
├── 15/   # Histórico de conversa no grafo
├── 16/   # Persistência com MemorySaver
└── 17/   # Agente multi-nó completo
```

---

## Pré-requisitos

- Python 3.11+
- Uma chave de API da OpenAI
- Familiaridade básica com Python (funções, classes, tipos)

```bash
pip install langchain langchain-openai langchain-community langgraph pydantic python-dotenv
```

Crie um arquivo `.env` na raiz:

```env
OPENAI_API_KEY=sk-...
```

---

## Módulos

### Fase 1 — Fundamentos de LLM

> Antes do framework, o mecanismo.

**`01` · Primeira chamada a um LLM**

SDK da OpenAI direto, sem abstrações. Você entende o que é `messages`, o que é `role`, o que é `system prompt` e como ler a resposta antes de qualquer framework entrar em cena.

**`02` · Introdução ao LangChain**

Mesmo resultado, nova camada: `ChatOpenAI`, tipos de mensagem (`SystemMessage`, `HumanMessage`, `AIMessage`), `StrOutputParser` e o operador `|` que conecta tudo numa chain.

---

### Fase 2 — Chains e Memória

> Cada módulo aqui resolve algo que o anterior ainda deixava na mão do dev.

**`03` · Templates de prompt dinâmicos**

`ChatPromptTemplate` com variáveis — o sistema prompt deixa de ser texto fixo e passa a receber parâmetros em tempo de execução.

**`04` · Histórico de conversa manual**

`MessagesPlaceholder` + uma lista que você mesmo mantém. O modelo passa a ter contexto das mensagens anteriores. A memória existe, mas é responsabilidade sua.

**`05` · Histórico gerenciado pelo framework**

`RunnableWithMessageHistory` + `session_id`. O framework cuida do histórico. Você passa a focar no que importa.

**`06` · Saída estruturada com Pydantic Parser**

`PydanticOutputParser` força o modelo a responder num schema definido via `BaseModel`. Funciona — mas exige `format_instructions` no prompt.

**`07` · Saída estruturada nativa do LLM**

`llm.with_structured_output(schema=...)` — sem instruções de formato no prompt, sem parsing frágil. O modelo usa function calling internamente para garantir o schema.

---

### Fase 3 — Roteamento, Tools e Agentes

> A progressão mais importante do curso. Não pule o módulo 09.

**`08` · Router pattern entre chains**

Um LLM classifica a pergunta e despacha para chains especializadas. Primeiro contato com a ideia de que diferentes perguntas merecem diferentes contextos.

**`09` · Function calling manual via JSON**

O modelo retorna um JSON com nome de função e argumentos. Você parseia, executa e injeta o resultado. Feio, mas essencial — é exatamente o que o framework faz nos módulos seguintes.

**`10` · Tool calling nativo**

`@tool`, `llm.bind_tools()`, `ToolMessage`. O ciclo completo numa chamada: LLM decide a tool → você executa → resultado volta ao LLM → resposta final.

**`11` · Loop de tool calling**

Múltiplas tools, múltiplas chamadas. Um `while` que continua enquanto o modelo quiser chamar ferramentas. Esse loop é o núcleo de qualquer agente.

**`12` · AgentExecutor**

`create_tool_calling_agent` + `AgentExecutor` encapsulam o loop do módulo 11. `verbose=True` deixa o raciocínio visível. O agente está pronto — mas ainda sem controle fino do fluxo.

---

### Fase 4 — LangGraph

> Quando o AgentExecutor não é suficiente, você desenha o grafo.

**`13` · Introdução ao LangGraph**

`StateGraph`, `TypedDict`, nós, arestas e `add_conditional_edges`. O grafo mais simples possível: um roteador que decide entre três nós com `random.choice`.

**`14` · Grafo com LLM router inteligente**

O roteador aleatório vira um LLM com `with_structured_output`. Nós especializados por domínio. Chat interativo em loop com o grafo compilado.

**`15` · Histórico de conversa no grafo**

`Annotated[list[BaseMessage], add_messages]` no estado. As mensagens se acumulam automaticamente a cada invocação — sem append manual, sem lógica extra.

**`16` · Persistência com MemorySaver**

`MemorySaver` como checkpointer. O estado é salvo entre chamadas e isolado por `thread_id`. Memória real, zero código adicional.

**`17` · Agente multi-nó completo**

O projeto integrador. Um assistente de saúde com:

- Router de intenção (coleta vs agendamento)
- Nó de coleta com schema `DadosUsuario` e controle de completude
- Nó de agendamento com tool call (`agendar_consulta`) e loop interno
- `MemorySaver` mantendo o estado entre turnos da conversa

Tudo junto, num caso de uso real.

---

## Como usar este repositório

Cada pasta é independente. Para rodar qualquer módulo:

```bash
cd 07
python langchain_main.py
```

A recomendação é seguir a ordem. Especialmente a transição 09 → 10 — entender o function calling manual torna tudo o que vem depois muito mais claro.

---

## Stack

| Biblioteca | Uso |
|---|---|
| `langchain-openai` | Interface com modelos da OpenAI |
| `langchain-core` | Tipos, prompts, parsers, runnables |
| `langchain-community` | ChatMessageHistory e utilitários |
| `langgraph` | Grafos de agentes com estado |
| `pydantic` | Schemas de entrada e saída |
| `python-dotenv` | Gerenciamento de variáveis de ambiente |

---

> Módulos 01–17 · LangChain + LangGraph · Python 3.11+
