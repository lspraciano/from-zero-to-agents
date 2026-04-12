from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from part_langchain.introduce_langchain_20.agents.router_agent.router_agent_system_prompt import (
    router_agent_system_prompt,
)

router_agent_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=router_agent_system_prompt),
        HumanMessagePromptTemplate.from_template(template="{user_message}"),
    ]
)
