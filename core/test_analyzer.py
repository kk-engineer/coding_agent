from config.llm_local import (
    chat
)


def analyze_test_failure(
    user_prompt: str,
    test_output: str
):

    messages = [
        {
            "role": "system",
            "content": """
You are a senior software engineer debugging failing tests.

Analyze:
- probable root cause
- impacted functionality
- likely broken file/function
- suggested fix

Keep the explanation concise.
"""
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