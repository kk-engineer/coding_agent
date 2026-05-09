from openai import OpenAI, APIConnectionError
from rich.console import Console

console = Console()
BASE_URL="http://localhost:8000/v1"


def empty_stream():
    yield from []


client = OpenAI(
    base_url=BASE_URL,
    api_key="not-needed"
)


def chat(messages, stream=False):
    # TODO exception handling
    return client.chat.completions.create(
        model="qwen2.5-7b",
        messages=messages,
        temperature=0.1,
        stream=stream
    )

def chat_stream(
    messages,
    temperature=0.1
):

    try:

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

        console.print(
            f"\n[bold red]{error_msg}[/bold red]"
        )

        return empty_stream()

    except Exception as e:

        error_msg = (
            f"LLM request failed: {str(e)}"
        )

        console.print(
            f"\n[bold red]{error_msg}[/bold red]"
        )

        return empty_stream()