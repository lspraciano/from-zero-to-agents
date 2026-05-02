from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)

from part_langgraph.introduce_langgraph_14.agents.knowledge_agent.knowledge_agent_system_prompt import (
    knowledge_agent_system_prompt,
)

knowledge_agent_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(
            template=knowledge_agent_system_prompt
        ),
        MessagesPlaceholder(variable_name="history"),
    ]
)
