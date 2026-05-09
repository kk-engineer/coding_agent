from config.llm_cloud import chat_stream

from core.prompts import EDIT_SYSTEM_PROMPT
from utils.file_ops import read_file
from utils.streaming import collect_llm_response


def strip_markdown_code_fence(content: str) -> str:

    """
    Remove a single wrapping Markdown code fence from model output.
    """

    stripped = content.strip()

    if not stripped.startswith("```"):

        return content

    lines = stripped.splitlines()

    if len(lines) < 2:

        return content

    opening = lines[0].strip()
    closing = lines[-1].strip()

    if not opening.startswith("```") or closing != "```":

        return content

    return "\n".join(lines[1:-1]).rstrip() + "\n"


def generate_updated_file(
    user_prompt,
    file_path
):

    content = read_file(file_path)

    messages = [
        {
            "role": "system",
            "content": EDIT_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"""
User Request:
{user_prompt}

Current File:
{content}

Return ONLY the updated file contents.
Do not include Markdown fences, language labels, commentary, or explanations.
"""
        }
    ]

    stream = chat_stream(messages)

    updated_content = collect_llm_response(stream)

    return strip_markdown_code_fence(updated_content)
