from config.llm_local import chat_stream
from core.prompts import PLAN_SYSTEM_PROMPT
from repo_utils.repo_scanner import scan_repo
from repo_utils.file_selector import find_related_files
from utils.streaming import stream_llm_response
from utils.spinner import AgentSpinner
from utils.console import console
import config.agent_config as config


async def create_plan(
    user_prompt,
    websocket=None
):

    # Spinner ONLY in CLI mode
    if config.INTERFACE_MODE == "cli":

        with AgentSpinner(
            "Scanning repository...",
            "dots"
        ):

            repo_files = scan_repo()

    else:

        repo_files = scan_repo()

    # Spinner ONLY in CLI mode
    if config.INTERFACE_MODE == "cli":

        with AgentSpinner(
            "Finding related files...",
            "line"
        ):

            related_files = find_related_files(
                user_prompt
            )

    else:

        related_files = find_related_files(
            user_prompt
        )

    context = f"""
Repository Files:
{repo_files[:100]}

Related Files:
{related_files[:20]}
"""

    messages = [
        {
            "role": "system",
            "content": PLAN_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"""
You are in planning mode.
This is a dry run. Do not apply changes or ask for approval.

User Request:
{user_prompt}

Repository Context:
{context}

Generate:
1. Files to modify
2. Why
3. Risks
4. Step-by-step plan
5. Execution order
6. Tests or checks to run

Do not include full code blocks. Suggested diffs are generated separately.
Respect the detected languages/frameworks, including frontend assets and static-site templates.
"""
        }
    ]

    stream = chat_stream(messages)

    response = await stream_llm_response(
        stream,
        websocket=websocket,
        prefix="Generating execution plan..."
    )

    # CLI newline only
    if config.INTERFACE_MODE == "cli":

        console.print()

    return response
