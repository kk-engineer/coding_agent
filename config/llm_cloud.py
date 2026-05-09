import os

from openai import OpenAI, APIConnectionError
from rich.console import Console

import config.agent_config as config
from utils.token_usage import add_prompt_tokens_from_messages

console = Console()

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.environ.get("nvidia_api_key")
)

completion = client.chat.completions.create(
  model="qwen/qwen2.5-coder-32b-instruct",
  messages=[{"role":"user","content":"Hi"}],
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
  stream=False
)

print(completion.choices[0].message)

def empty_stream():
    yield from []

def chat_stream(
    messages,
    temperature=0.1
):

    try:

        add_prompt_tokens_from_messages(messages)

        return client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",
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

