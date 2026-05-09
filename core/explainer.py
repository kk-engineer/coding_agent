from pathlib import Path

import config.agent_config as config
from config.llm_local import chat_stream
from core.prompts import EXPLAINER_SYSTEM_PROMPT
from utils.console import console
from utils.file_ops import list_directory, read_file
from utils.streaming import stream_llm_response


async def explain_path(
    path: str,
    websocket=None
):

    path_obj = Path(path)

    if not path_obj.exists():

        return (
            f"Error: '{path}' does not exist."
        )

    try:

        if path_obj.is_file():

            content = read_file(path)

            user_prompt = f"""
Explain this code in detail.

File:
{path}

Code:
{content[:12000]}

Explain:
- purpose
- architecture
- important logic
- dependencies
- risks
"""

        elif path_obj.is_dir():

            files = list_directory(path)

            if not files:

                return (
                    f"Directory '{path}' is empty."
                )

            tree = "\n".join(files[:200])

            user_prompt = f"""
Explain this directory/module.

Directory:
{path}

Files:
{tree}

Explain:
- overall purpose
- architecture
- important modules
- execution flow
- dependencies
- risks
"""

        messages = [
            {
                "role": "system",
                "content": EXPLAINER_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        stream = chat_stream(messages)

        response = await stream_llm_response(
            stream,
            websocket=websocket,
            prefix=f"Explaining {path}..."
        )

        if config.INTERFACE_MODE == "cli":

            console.print()

        return response

    except Exception as e:

        return (
            f"Failed to explain '{path}'\n"
            f"Reason: {str(e)}"
        )


async def explain_file(
    path: str,
    websocket=None
):

    return await explain_path(
        path,
        websocket=websocket
    )
