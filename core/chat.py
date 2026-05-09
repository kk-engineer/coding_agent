import config.agent_config as config
from config.llm_local import chat_stream
from core.prompts import CHAT_SYSTEM_PROMPT
from repo_utils.repo_scanner import scan_repo
from utils.console import console
from utils.streaming import stream_llm_response


async def answer_chat(
    user_prompt: str,
    websocket=None
):

    repo_files = scan_repo()

    messages = [
        {
            "role": "system",
            "content": CHAT_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"""
User question:
{user_prompt}

Repository files:
{repo_files[:120]}
"""
        }
    ]

    stream = chat_stream(messages)

    response = await stream_llm_response(
        stream,
        websocket=websocket,
        prefix="Answering question..."
    )

    if config.INTERFACE_MODE == "cli":

        console.print()

    return response
