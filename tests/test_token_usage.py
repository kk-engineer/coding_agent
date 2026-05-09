from utils.token_usage import (
    add_completion_tokens_from_text,
    add_prompt_tokens_from_messages,
    get_token_usage,
    reset_token_usage
)

import asyncio


def test_token_usage_tracks_prompt_completion_and_total():

    reset_token_usage()
    add_prompt_tokens_from_messages([
        {
            "role": "user",
            "content": "hello world"
        }
    ])
    add_completion_tokens_from_text("done")

    usage = get_token_usage()

    assert usage["prompt_tokens"] > 0
    assert usage["completion_tokens"] > 0
    assert usage["total_tokens"] == (
        usage["prompt_tokens"]
        + usage["completion_tokens"]
    )


def test_token_usage_reset():

    reset_token_usage()
    add_completion_tokens_from_text("done")
    reset_token_usage()

    assert get_token_usage() == {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0
    }


def test_token_usage_survives_asyncio_run():

    async def add_tokens_async():

        add_prompt_tokens_from_messages([
            {
                "role": "user",
                "content": "explain app.py"
            }
        ])
        add_completion_tokens_from_text("explanation")

    reset_token_usage()
    asyncio.run(add_tokens_async())

    usage = get_token_usage()

    assert usage["prompt_tokens"] > 0
    assert usage["completion_tokens"] > 0
    assert usage["total_tokens"] > 0
