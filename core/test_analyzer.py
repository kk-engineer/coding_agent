from config.llm_cloud import (
    chat_stream
)

from core.prompts import TEST_ANALYZER_SYSTEM_PROMPT
from utils.streaming import collect_llm_response


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

    stream = chat_stream(messages)

    return collect_llm_response(stream)
