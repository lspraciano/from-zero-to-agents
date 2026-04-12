# OpenAI SDK Ponto de Partida

Esta pasta contém o primeiro contato com a API da OpenAI usando o **SDK oficial do Python**, sem nenhuma abstração de framework. É o ponto de partida da trilha antes de evoluir para o LangChain.

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
part_openai/
└── introduce_openai_1.py   # Chamada direta à API da OpenAI via SDK oficial
```

---

## O que o Exemplo Cobre

### `introduce_openai_1.py`

Demonstra o fluxo mais básico possível para conversar com um modelo da OpenAI:

1. Carrega a chave de API a partir do `.env` com `python-dotenv`
2. Instancia o cliente `OpenAI`
3. Monta a lista de mensagens no formato `list[dict]` com roles `system` e `user`
4. Chama `client.chat.completions.create()` com o modelo `gpt-4.1-mini`
5. Imprime o conteúdo da resposta via `response.choices[0].message.content`

---

## Como Executar

```bash
python -m part_openai.introduce_openai_1
```

---

## Próximo Passo

Depois de entender como o SDK funciona diretamente, a pasta [`part_langchain`](../part_langchain/README.md) mostra como o LangChain abstrai e expande esse mesmo fluxo.
