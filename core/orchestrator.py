from core.reasoning import StepLogger

from core.planner import (
    create_plan
)

from core.execution_manager import (
    generate_updated_file
)

from core.rollback_manager import (
    backup_file
)

from core.test_analyzer import (
    analyze_test_failure
)

from repo_utils.file_selector import (
    find_related_files
)

from repo_utils.project_detector import (
    detect_test_command
)

from utils.file_ops import (
    read_file
)

from utils.file_ops import (
    write_file
)

from utils.diff_generator import (
    generate_diff
)

from utils.test_runner import (
    run_tests
)

from utils.console import (
    console
)

from utils.spinner import (
    AgentSpinner
)

import config.agent_config as config

from config.agent_config import (
    MAX_FIX_ATTEMPTS
)


async def emit_step(
    logger,
    step_type,
    content,
    websocket=None
):

    """
    Emit step to:
    - reasoning logger
    - CLI console (cli mode only)
    - websocket client (ACP only)
    """

    logger.add(
        step_type,
        content
    )

    # CLI rendering ONLY
    if config.INTERFACE_MODE == "cli":

        console.print(
            f"[bold cyan][{step_type}][/bold cyan] "
            f"{content}"
        )

    # ACP websocket streaming
    if websocket:

        await websocket.send_json({
            "type": "step",
            "stage": step_type,
            "content": content
        })


async def plan_changes(
    user_prompt: str,
    websocket=None
):

    logger = StepLogger()

    await emit_step(
        logger,
        "planning",
        "Analyzing repository structure...",
        websocket
    )

    # Spinner ONLY in CLI mode
    if config.INTERFACE_MODE == "cli":

        with AgentSpinner(
            "Finding related files...",
            "dots"
        ):

            related_files = find_related_files(
                user_prompt
            )

    else:

        related_files = find_related_files(
            user_prompt
        )

    related_files = list(set(related_files))

    await emit_step(
        logger,
        "planning",
        (
            f"Identified "
            f"{len(related_files)} "
            f"related files"
        ),
        websocket
    )

    plan = await create_plan(
        user_prompt,
        websocket=websocket
    )

    await emit_step(
        logger,
        "planning",
        "Generated execution plan",
        websocket
    )

    return {
        "steps": logger.get_steps(),
        "related_files": related_files,
        "plan": plan
    }


async def execute_changes(
    user_prompt: str,
    websocket=None
):

    logger = StepLogger()

    await emit_step(
        logger,
        "execution",
        "Finding related files...",
        websocket
    )

    # Spinner ONLY in CLI mode
    if config.INTERFACE_MODE == "cli":

        with AgentSpinner(
            "Scanning repository...",
            "dots"
        ):

            files = find_related_files(
                user_prompt
            )

    else:

        files = find_related_files(
            user_prompt
        )

    files = list(set(files))

    await emit_step(
        logger,
        "execution",
        f"Selected {len(files)} files",
        websocket
    )

    all_diffs = []

    all_rollbacks = []

    for file_path in files:

        try:

            await emit_step(
                logger,
                "execution",
                f"Reading file: {file_path}",
                websocket
            )

            old_content = read_file(
                file_path
            )

            await emit_step(
                logger,
                "execution",
                (
                    f"Generating update "
                    f"for {file_path}"
                ),
                websocket
            )

            new_content = generate_updated_file(
                user_prompt=user_prompt,
                file_path=file_path
            )

            await emit_step(
                logger,
                "execution",
                (
                    f"Creating rollback "
                    f"backup for {file_path}"
                ),
                websocket
            )

            rollback_id, backup_path = backup_file(
                file_path
            )

            await emit_step(
                logger,
                "execution",
                (
                    f"Writing updated file: "
                    f"{file_path}"
                ),
                websocket
            )

            write_file(
                file_path,
                new_content
            )

            diff = generate_diff(
                old_content,
                new_content,
                file_path
            )

            all_diffs.append({
                "file": file_path,
                "diff": diff
            })

            all_rollbacks.append({
                "file": file_path,
                "rollback_id": rollback_id,
                "backup_path": backup_path
            })

            await emit_step(
                logger,
                "diff",
                (
                    f"Generated diff for "
                    f"{file_path}"
                ),
                websocket
            )

            if websocket:

                await websocket.send_json({
                    "type": "diff",
                    "file": file_path,
                    "content": diff
                })

        except Exception as e:

            await emit_step(
                logger,
                "error",
                f"{file_path}: {str(e)}",
                websocket
            )

    await emit_step(
        logger,
        "testing",
        (
            "Detecting project "
            "test framework..."
        ),
        websocket
    )

    test_command = detect_test_command()

    await emit_step(
        logger,
        "testing",
        f"Using test command: {test_command}",
        websocket
    )

    attempt = 0

    final_test_result = None

    while attempt < MAX_FIX_ATTEMPTS:

        await emit_step(
            logger,
            "testing",
            (
                f"Running tests "
                f"(attempt {attempt + 1})..."
            ),
            websocket
        )

        # Spinner ONLY in CLI mode
        if config.INTERFACE_MODE == "cli":

            with AgentSpinner(
                "Running tests...",
                "material"
            ):

                test_result = run_tests(
                    test_command
                )

        else:

            test_result = run_tests(
                test_command
            )

        final_test_result = test_result

        if websocket:

            await websocket.send_json({
                "type": "test",
                "success": test_result["success"],
                "stdout": test_result["stdout"],
                "stderr": test_result["stderr"]
            })

        if test_result["success"]:

            await emit_step(
                logger,
                "testing",
                "All tests passed",
                websocket
            )

            break

        await emit_step(
            logger,
            "testing",
            "Tests failed",
            websocket
        )

        analysis = analyze_test_failure(
            user_prompt=user_prompt,
            test_output=test_result["stdout"]
        )

        await emit_step(
            logger,
            "analysis",
            analysis,
            websocket
        )

        attempt += 1

    final_result = {
        "steps": logger.get_steps(),
        "diffs": all_diffs,
        "rollbacks": all_rollbacks,
        "tests": final_test_result
    }

    if websocket:

        await websocket.send_json({
            "type": "complete",
            "result": final_result
        })

    return final_result