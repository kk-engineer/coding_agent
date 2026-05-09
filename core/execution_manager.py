from config.llm_local import chat

from utils.file_ops import read_file


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

    response = chat(messages)

    updated_content = response.choices[0].message.content

    return strip_markdown_code_fence(updated_content)
