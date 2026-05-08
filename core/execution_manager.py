from config.llm_local import chat

from utils.file_ops import read_file


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

Return ONLY updated file.
"""
        }
    ]

    response = chat(messages)

    return response.choices[0].message.content