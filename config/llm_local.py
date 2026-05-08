from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)


def chat(messages, stream=False):

    return client.chat.completions.create(
        model="qwen2.5-7b",
        messages=messages,
        temperature=0.1,
        stream=stream
    )

def chat_stream(
    messages,
    temperature=0.1
):

    return client.chat.completions.create(
        model="qwen2.5-7b",
        messages=messages,
        temperature=temperature,
        stream=True
    )