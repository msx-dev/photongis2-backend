from llm.provider import client
from llm.prompts import SYSTEM_PROMPT


def chat(user_message: str) -> str:

    response = client.responses.create(
        model="google/gemma-4-26b-a4b-it:free",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )

    return response.output_text