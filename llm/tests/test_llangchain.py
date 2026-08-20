from llm.provider import model


# Send a very simple message to the model.
#
# This is NOT the agent yet.
# We're only testing that:
#
# FastAPI/Python
#       ↓
# LangChain
#       ↓
# OpenRouter
#       ↓
# GPT-OSS
#
# works correctly.
response = model.invoke(
    "Say hello in one short sentence."
)


print(response.content)