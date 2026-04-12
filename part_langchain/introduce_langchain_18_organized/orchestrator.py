from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from langchain_core.tools import BaseTool

from part_langchain.introduce_langchain_18_organized.chains.general_chain import (
    general_chain, general_parser,
    GeneralResponse
)
from part_langchain.introduce_langchain_18_organized.chains.math_chain import math_chain, math_parser, MathResponse
from part_langchain.introduce_langchain_18_organized.chains.router_chain import router_chain, router_parser, RouterResponse
from tool.calculator_tool import calculator_tool

tools: dict[str, BaseTool] = {
    calculator_tool.name: calculator_tool,
}

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    router_response: RouterResponse = router_chain.invoke(
        input={
            "user_message": user_message,
            "format_instructions": router_parser.get_format_instructions(),
        }
    )

    print(f"[Router] → {router_response.agent}")

    parsed_response: MathResponse | GeneralResponse

    if router_response.agent == "math":
        response: AIMessage = math_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": math_parser.get_format_instructions(),
                "history": history,
            }
        )

        while response.tool_calls:
            history.append(response)

            for tool_call in response.tool_calls:
                current_tool_name: str = tool_call["name"]
                current_tool_args: dict = tool_call["args"]

                current_tool: BaseTool = tools[current_tool_name]

                current_tool_result: Any = current_tool.invoke(input=current_tool_args)

                print(f"[Tool] {current_tool_name}({current_tool_args}) = {current_tool_result}")

                current_tool_message: ToolMessage = ToolMessage(
                    content=str(current_tool_result),
                    tool_call_id=tool_call["id"],
                )

                history.append(current_tool_message)

            response: AIMessage = math_chain.invoke(
                input={
                    "user_message": user_message,
                    "format_instructions": math_parser.get_format_instructions(),
                    "history": history,
                }
            )

        parsed_response: MathResponse = math_parser.invoke(input=response)

    else:
        parsed_response: GeneralResponse = general_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": general_parser.get_format_instructions(),
                "history": history,
            }
        )

    human_message: HumanMessage = HumanMessage(content=user_message)

    ai_message: AIMessage = AIMessage(content=parsed_response.response)

    history.append(human_message)

    history.append(ai_message)

    print(f"AI: {parsed_response.response}")
