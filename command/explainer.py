from utils.file_ops import (
    read_file
)

from config.llm_local import (
    chat
)


def explain_file(path: str):

    content = read_file(path)

    prompt = f"""
Explain this code in detail.

File:
{path}

Code:
{content}

Explain:
- purpose
- architecture
- important logic
- dependencies
- risks
"""

    return chat(prompt)