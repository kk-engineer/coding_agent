_TOKEN_USAGE = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
}


def reset_token_usage():

    _TOKEN_USAGE["prompt_tokens"] = 0
    _TOKEN_USAGE["completion_tokens"] = 0
    _TOKEN_USAGE["total_tokens"] = 0


def get_token_usage():

    return dict(_TOKEN_USAGE)


def add_prompt_tokens_from_messages(messages):

    add_token_usage(
        prompt_tokens=estimate_tokens(str(messages))
    )


def add_completion_tokens_from_text(text: str):

    add_token_usage(
        completion_tokens=estimate_tokens(text)
    )


def add_token_usage(
    prompt_tokens: int = 0,
    completion_tokens: int = 0
):

    _TOKEN_USAGE["prompt_tokens"] += prompt_tokens
    _TOKEN_USAGE["completion_tokens"] += completion_tokens
    _TOKEN_USAGE["total_tokens"] = (
        _TOKEN_USAGE["prompt_tokens"]
        + _TOKEN_USAGE["completion_tokens"]
    )


def set_token_usage(
    prompt_tokens: int,
    completion_tokens: int
):

    _TOKEN_USAGE["prompt_tokens"] = prompt_tokens
    _TOKEN_USAGE["completion_tokens"] = completion_tokens
    _TOKEN_USAGE["total_tokens"] = prompt_tokens + completion_tokens


def estimate_tokens(text: str):

    if not text:

        return 0

    return max(1, len(text) // 4)
