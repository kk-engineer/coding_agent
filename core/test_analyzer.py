from config.llm_local import (
    chat
)

from core.prompts import TEST_ANALYZER_SYSTEM_PROMPT


def analyze_test_failure(
    user_prompt: str,
    test_output: str
):

    messages = [
        {
            "role": "system",
            "content": TEST_ANALYZER_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"""
User Request:
{user_prompt}

Test Output:
{test_output}
"""
        }
    ]

    response = chat(messages)

    return response.choices[0].message.content
