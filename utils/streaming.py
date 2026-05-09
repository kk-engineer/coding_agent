import time

from utils.console import console


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

            delta = (
                chunk.choices[0]
                .delta
                .content
            )

            if not delta:
                continue

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

    console.print()

    return full_response