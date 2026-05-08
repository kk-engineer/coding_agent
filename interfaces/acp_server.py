import json

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

import uvicorn

from core.orchestrator import (
    plan_changes,
    execute_changes
)

from utils.console import console

app = FastAPI()


@app.websocket("/agent")
async def agent_socket(ws: WebSocket):

    await ws.accept()

    console.print(
        "[green]Client connected[/green]"
    )

    try:

        while True:

            raw_data = await ws.receive_text()

            console.print(
                f"[cyan]Received:[/cyan] "
                f"{raw_data}"
            )

            try:

                data = json.loads(raw_data)

            except json.JSONDecodeError as e:

                await ws.send_json({
                    "type": "error",
                    "content": str(e)
                })

                continue

            mode = data.get("mode")

            prompt = data.get("prompt")

            if mode == "plan":

                result = await plan_changes(
                    prompt,
                    websocket=ws
                )

            elif mode == "edit":

                result = await execute_changes(
                    prompt,
                    websocket=ws
                )

            else:

                result = {
                    "type": "error",
                    "content": (
                        f"Unknown mode: {mode}"
                    )
                }

            await ws.send_json({
                "type": "complete",
                "result": result
            })

    except WebSocketDisconnect:

        console.print(
            "[red]Client disconnected[/red]"
        )


def main():

    console.print(
        "[bold green]ACP Server Ready[/bold green]"
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000
    )


if __name__ == "__main__":

    main()