from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)

from part_langgraph.introduce_langgraph_13.agents.pokemon_agent.pokemon_agent_system_prompt import \
    pokemon_agent_system_prompt

pokemon_agent_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(
            template=pokemon_agent_system_prompt
        ),
        MessagesPlaceholder(variable_name="history"),
    ]
)
