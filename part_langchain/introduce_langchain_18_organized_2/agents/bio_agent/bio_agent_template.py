from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from part_langchain.introduce_langchain_18_organized_2.agents.bio_agent.bio_agent_system_prompt import (
    bio_agent_system_prompt,
)

bio_agent_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=bio_agent_system_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template(template="{user_message}"),
    ]
)
