import os

from dotenv import load_dotenv
from pydantic import SecretStr
from langchain_openai import ChatOpenAI


# Load variables from the .env file.
load_dotenv()


# Read the OpenRouter API key.
api_key = os.getenv("OPENROUTER_API_KEY")


# Give a clear error if the key is missing.
if not api_key:
    raise RuntimeError(
        "OPENROUTER_API_KEY environment variable is not set."
    )


# LangChain's ChatOpenAI integration can communicate
# with OpenAI-compatible APIs such as OpenRouter.
model = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    api_key=SecretStr(api_key),
    base_url="https://openrouter.ai/api/v1",
)