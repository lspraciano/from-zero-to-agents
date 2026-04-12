from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from langchain_core.tools import BaseTool

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    # Roteamento
    router_response: RouterResponse = router_chain.invoke(
        input={
            "user_message": user_message,
            "format_instructions": router_parse.get_format_instructions(),
        }
    )

    print(f"[Router] → {router_response.agent}")

    if router_response.agent == "math":
        response: AIMessage = math_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": math_parse.get_format_instructions(),
                "history": history,
            }
        )

        while response.tool_calls:
            history.append(response)

            for tool_call in response.tool_calls:
                selected_tool: BaseTool = tools[tool_call["name"]]
                tool_result = selected_tool.invoke(input=tool_call["args"])

                print(f"[Tool] {tool_call['name']}({tool_call['args']}) = {tool_result}")

                tool_message: ToolMessage = ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                )

                history.append(tool_message)

            response = math_chain.invoke(
                input={
                    "user_message": user_message,
                    "format_instructions": math_parse.get_format_instructions(),
                    "history": history,
                }
            )

        parsed_response: MathResponse = math_parse.invoke(input=response)

    else:
        parsed_response: GeneralResponse = general_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": general_parse.get_format_instructions(),
                "history": history,
            }
        )

    human_message: HumanMessage = HumanMessage(content=user_message)

    ai_message: AIMessage = AIMessage(content=parsed_response.response)

    history.append(human_message)

    history.append(ai_message)

    print(f"AI response: {parsed_response.response}")
