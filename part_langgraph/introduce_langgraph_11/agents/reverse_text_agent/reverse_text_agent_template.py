from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)

from part_langgraph.introduce_langgraph_11.agents.reverse_text_agent.reverse_text_agent_system_prompt import (
    reverse_text_agent_system_prompt,
)

reverse_text_agent_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(
            template=reverse_text_agent_system_prompt
        ),
        MessagesPlaceholder(variable_name="history"),
    ]
)
