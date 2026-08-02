from sqlalchemy.orm import Session
from models import User

from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
)

from llm.provider import client
from llm.prompts import SYSTEM_PROMPT
from llm.tools import TOOLS
from llm.tools.registry import TOOL_FUNCTIONS


def chat(
    user_message: str,
    user: User,
    db: Session,
):

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]


    # First LLM call
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )


    assistant_message = response.choices[0].message


    # Check if LLM wants to call a tool
    if assistant_message.tool_calls:

        tool_call = assistant_message.tool_calls[0]


        if tool_call.type != "function":
            raise ValueError("Unsupported tool type")


        function_name = tool_call.function.name


        tool_function = TOOL_FUNCTIONS.get(function_name)

        if tool_function is None:
            raise ValueError(
                f"Unknown tool requested: {function_name}"
            )


        # Execute tool
        result = tool_function(
            user=user,
            db=db,
        )


        # Convert assistant response into request format
        assistant_tool_message: ChatCompletionAssistantMessageParam = {
            "role": "assistant",
            "content": assistant_message.content or "",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
            ],
        }

        messages.append(assistant_tool_message)


        # Add tool result
        tool_result_message: ChatCompletionToolMessageParam = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result),
        }

        messages.append(tool_result_message)


        # Second LLM call with tool data
        final_response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=messages,
        )


        return final_response.choices[0].message.content


    # Normal LLM response
    return assistant_message.content