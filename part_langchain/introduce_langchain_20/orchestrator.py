from langchain_core.messages import AIMessage, HumanMessage, BaseMessage

from part_langchain.introduce_langchain_20.agents.bio_agent.bio_agent_chain import (
    bio_agent_chain,
)
from part_langchain.introduce_langchain_20.agents.bio_agent.bio_agent_parser import (
    bio_agent_parser,
)
from part_langchain.introduce_langchain_20.agents.bio_agent.bio_agent_response_format import (
    BioAgentResponseFormat,
)
from part_langchain.introduce_langchain_20.agents.general_agent.general_agent_chain import (
    general_agent_chain,
)
from part_langchain.introduce_langchain_20.agents.general_agent.general_agent_parser import (
    general_agent_parser,
)
from part_langchain.introduce_langchain_20.agents.general_agent.general_agent_response_format import (
    GeneralAgentResponseFormat,
)
from part_langchain.introduce_langchain_20.agents.router_agent.router_agent_chain import (
    router_agent_chain,
)
from part_langchain.introduce_langchain_20.agents.router_agent.router_agent_parser import (
    router_agent_parser,
)
from part_langchain.introduce_langchain_20.agents.router_agent.router_agent_response_format import (
    RouterAgentResponseFormat,
)

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    human_message: HumanMessage = HumanMessage(content=user_message)

    history.append(human_message)

    router_response: RouterAgentResponseFormat = router_agent_chain.invoke(
        input={
            "user_message": user_message,
            "format_instructions": router_agent_parser.get_format_instructions(),
        }
    )

    print(f"[Router] → {router_response}")

    if router_response.agent == "bio":
        bio_response: BioAgentResponseFormat = bio_agent_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": bio_agent_parser.get_format_instructions(),
                "history": history,
            }
        )

        ai_message: AIMessage = AIMessage(content=bio_response.response)

        print(f"[Bio Agent] → {bio_response}")

    else:
        general_response: GeneralAgentResponseFormat = general_agent_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": general_agent_parser.get_format_instructions(),
                "history": history,
            }
        )

        ai_message: AIMessage = AIMessage(content=general_response.response)

        print(f"[General Agent] → {general_response}")

    history.append(ai_message)

    print(f"AI response: {ai_message}")
