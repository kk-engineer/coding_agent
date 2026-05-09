from openai import OpenAI, APIConnectionError
from rich.console import Console

import config.agent_config as config
from utils.token_usage import add_prompt_tokens_from_messages

console = Console()
BASE_URL="http://localhost:8000/v1"


def empty_stream():
    yield from []


client = OpenAI(
    base_url=BASE_URL,
    api_key="not-needed"
)


def chat_stream(
    messages,
    temperature=0.1
):

    try:

        add_prompt_tokens_from_messages(messages)

        return client.chat.completions.create(
            model="qwen2.5-7b",
            messages=messages,
            temperature=temperature,
            stream=True
        )

    except APIConnectionError:

        error_msg = (
            "LLM server connection failed.\n"
            "Possible reasons:\n"
            "1. Local LLM server is not running\n"
            "2. Wrong base_url/port\n"
            "3. Model server crashed\n"
            "4. Network/socket issue"
        )

        if config.INTERFACE_MODE == "cli":

            console.print(
                f"\n[bold red]{error_msg}[/bold red]"
            )

        return empty_stream()

    except Exception as e:

        error_msg = (
            f"LLM request failed: {str(e)}"
        )

        if config.INTERFACE_MODE == "cli":

            console.print(
                f"\n[bold red]{error_msg}[/bold red]"
            )

        return empty_stream()
