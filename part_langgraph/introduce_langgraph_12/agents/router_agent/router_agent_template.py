from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)

from part_langgraph.introduce_langgraph_12.agents.router_agent.router_agent_system_prompt import (
    router_agent_system_prompt,
)

router_agent_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=router_agent_system_prompt),
        MessagesPlaceholder(variable_name="history"),
    ]
)
