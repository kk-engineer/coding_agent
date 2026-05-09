import time

import config.agent_config as config
from utils.console import console
from utils.token_usage import (
    add_completion_tokens_from_text,
    set_token_usage
)


async def stream_llm_response(
    stream,
    websocket=None,
    prefix=None
):

    full_response = ""

    token_buffer = ""

    last_flush = time.time()

    FLUSH_INTERVAL = 0.05

    if prefix:

        if config.INTERFACE_MODE == "cli":

            console.print(
                f"\n[bold cyan]{prefix}[/bold cyan]\n"
            )

        if websocket:

            await websocket.send_json({
                "type": "step",
                "content": prefix
            })

    # Handle failed/empty stream
    if not stream:

        error_msg = (
            "No response stream received from LLM.\n"
            "The model server may be offline or unreachable."
        )

        if config.INTERFACE_MODE == "cli":

            console.print(
                f"[bold red]{error_msg}[/bold red]"
            )

        if websocket:

            await websocket.send_json({
                "type": "error",
                "content": error_msg
            })

        return ""

    for chunk in stream:

        try:

            record_provider_usage(chunk)

            delta = (
                chunk.choices[0]
                .delta
                .content
            )

            if not delta:
                continue

            if config.INTERFACE_MODE == "cli":

                console.print(
                    delta,
                    end=""
                )

            full_response += delta

            token_buffer += delta

            now = time.time()

            should_flush = (
                now - last_flush
                > FLUSH_INTERVAL
            )

            newline_flush = (
                "\n" in token_buffer
            )

            if (
                websocket
                and
                (
                    should_flush
                    or newline_flush
                )
            ):

                await websocket.send_json({
                    "type": "token",
                    "content": token_buffer
                })

                token_buffer = ""

                last_flush = now

        except Exception:
            pass

    if websocket and token_buffer:

        await websocket.send_json({
            "type": "token",
            "content": token_buffer
        })

    add_completion_tokens_from_text(full_response)

    if config.INTERFACE_MODE == "cli":

        console.print()

    return full_response


def collect_llm_response(
    stream,
    on_token=None
):

    """
    Collect a streaming LLM response without rendering it to the CLI.
    """

    full_response = ""

    if not stream:

        return full_response

    for chunk in stream:

        try:

            record_provider_usage(chunk)

            delta = (
                chunk.choices[0]
                .delta
                .content
            )

            if not delta:

                continue

            full_response += delta

            if on_token:

                on_token(delta)

        except Exception:

            pass

    add_completion_tokens_from_text(full_response)

    return full_response


def record_provider_usage(chunk):

    usage = getattr(chunk, "usage", None)

    if not usage:

        return

    prompt_tokens = getattr(usage, "prompt_tokens", None)
    completion_tokens = getattr(usage, "completion_tokens", None)

    if prompt_tokens is None or completion_tokens is None:

        return

    set_token_usage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens
    )
