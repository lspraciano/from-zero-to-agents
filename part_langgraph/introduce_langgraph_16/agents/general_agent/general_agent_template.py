from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)

from part_langgraph.introduce_langgraph_16.agents.general_agent.general_agent_system_prompt import (
    general_agent_system_prompt,
)

general_agent_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=general_agent_system_prompt),
        MessagesPlaceholder(variable_name="history"),
    ]
)
