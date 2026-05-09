import json

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

import uvicorn

import config.agent_config
# MUST happen BEFORE other project imports
config.agent_config.INTERFACE_MODE = "acp"

from core.orchestrator import (
    plan_changes,
    execute_changes
)

from command.services import (
    get_diff,
    get_help,
    get_status,
    list_files_for_command,
    run_detected_tests,
    run_local_command,
    search_repository
)
from core.chat import answer_chat
from core.explainer import explain_path
from utils.token_usage import get_token_usage, reset_token_usage

app = FastAPI()


@app.websocket("/agent")
async def agent_socket(ws: WebSocket):

    await ws.accept()

    try:

        while True:

            raw_data = await ws.receive_text()
            reset_token_usage()

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

            if mode in {"help", "/help", "/"}:

                result = get_help()

            elif mode in {"chat", "ask"}:

                result = await answer_chat(
                    prompt or data.get("question") or "",
                    websocket=ws
                )

            elif mode == "plan":

                result = await plan_changes(
                    prompt,
                    websocket=ws,
                    include_diffs=True
                )

            elif mode == "edit":

                result = await execute_changes(
                    prompt,
                    websocket=ws
                )

            elif mode == "explain":

                result = await explain_path(
                    data.get("path") or prompt or ".",
                    websocket=ws
                )

            elif mode == "search":

                result = search_repository(
                    data.get("query") or prompt or ""
                )

            elif mode == "test":

                result = run_detected_tests(
                    data.get("command")
                )

            elif mode == "diff":

                result = get_diff()

            elif mode == "files":

                result = list_files_for_command(
                    data.get("path") or "."
                )

            elif mode == "pwd":

                result = get_status()["path"]

            elif mode == "run":

                result = run_local_command(
                    data.get("command") or prompt or ""
                )

            elif mode == "status":

                result = get_status()

            elif mode == "clear":

                result = {
                    "success": True,
                    "message": (
                        "Clear is only meaningful in the interactive CLI."
                    )
                }

            else:

                result = {
                    "type": "error",
                    "content": (
                        f"Unknown mode: {mode}"
                    )
                }

            await ws.send_json({
                "type": "complete",
                "result": result,
                "token_usage": get_token_usage()
            })

    except WebSocketDisconnect:
        pass


def main():

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000
    )


if __name__ == "__main__":

    main()
