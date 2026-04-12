from langchain_core.messages import AIMessage, HumanMessage, BaseMessage

from part_langchain.introduce_langchain_18_organized_1.chains.bio_chain import (
    bio_chain,
    BioResponse,
    bio_parser,
)
from part_langchain.introduce_langchain_18_organized_1.chains.general_chain import (
    general_chain,
    general_parser,
    GeneralResponse,
)
from part_langchain.introduce_langchain_18_organized_1.chains.router_chain import (
    router_chain,
    router_parser,
    RouterResponse,
)

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    human_message: HumanMessage = HumanMessage(content=user_message)

    history.append(human_message)

    router_response: RouterResponse = router_chain.invoke(
        input={
            "user_message": user_message,
            "format_instructions": router_parser.get_format_instructions(),
        }
    )

    print(f"[Router] → {router_response}")

    if router_response.agent == "bio":
        bio_response: BioResponse = bio_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": bio_parser.get_format_instructions(),
                "history": history,
            }
        )

        ai_message: AIMessage = AIMessage(content=bio_response.response)

        print(f"[Bio Agent] → {bio_response}")

    else:
        general_response: GeneralResponse = general_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": general_parser.get_format_instructions(),
                "history": history,
            }
        )

        ai_message: AIMessage = AIMessage(content=general_response.response)

        print(f"[General Agent] → {general_response}")

    history.append(ai_message)

    print(f"AI response: {ai_message}")
