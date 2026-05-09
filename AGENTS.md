# AGENTS.md — coding-agent

## Quick start

```bash
pip install -e ".[dev]"  # or: uv sync
pytest                   # all tests
pytest tests/test_command_router.py -x  # single file
```

No lint or typecheck commands configured (no ruff, mypy, etc. in pyproject.toml deps).

## CLI commands

All commands are slash-prefixed. Plain text is **read-only chat** — editing never inferred from freeform input.

| Command | Aliases | Action |
|---|---|---|
| `/chat` | `/ask` | Read-only Q&A |
| `/edit` | `/do`, `/change` | Plan, confirm, apply changes |
| `/plan` | — | Generate plan without modifying files |
| `/explain` | `/why` | Explain a file or directory |
| `/search` | `/find` | Repo code search (uses `rg`) |
| `/test` | `/tests` | Run detected test suite |
| `/diff` | — | Show git diff |
| `/files` | — | List files under path |
| `/run` | `!` | Run a local shell command |
| `/status` | `/st` | Workspace + git status |
| `/exit` | `/quit`, `/q` | Quit |

Freeform intents: "explain/describe/summarize/what is/how does" → Explain. "plan/design/approach/how should/what would it take" → Plan. Everything else → Chat.

## Architecture

- `app.py` → `command/cli.py` (REPL loop), `interfaces/acp_server.py` (WebSocket on `:9000`), `interfaces/mcp_server.py` (MCP stdio)
- `INTERFACE_MODE` in `config/agent_config.py` must be set **before** other project imports (see `acp_server.py:11`, `mcp_server.py:5`)
- Core edit flow: `orchestrator.execute_changes()` → `find_related_files()` → for each file: read → LLM generates update → `rollback_manager.backup_file()` → write → `run_tests()` → if fail → `test_analyzer.analyze_test_failure()` → retry (max `MAX_FIX_ATTEMPTS=3`)
- `generate_suggested_diffs()` is dry-run (no writes, no backups) — used by `/plan`
- Backups go to `.agent_backups/`; rollback via `rollback_executor.rollback_all()`

## LLM config

- `config/llm_local.py`: hardcoded `BASE_URL=http://localhost:8000/v1`, default model `QWEN_MODEL="qwen2.5-7b"`
- No offline mock mode — returns empty stream if server unreachable
- Tests monkeypatch `core.execution_manager.chat_stream` / `core.test_analyzer.chat_stream`

## Key dependencies & quirks

- **`rg` (ripgrep) required** — used by `search_code()`, `repo_search()`, `find_related_files()`
- Code search and `find_related_files()` split user prompt into keywords and search each via ripgrep
- `libcst` for Python AST transforms, `jedi` for navigation/definitions, `networkx` for dependency/call graphs
- `fastapi` + `uvicorn` for ACP WebSocket server; `mcp` for MCP stdio server
- File listing in `file_ops.list_directory()` ignores `.git`, `__pycache__`, `.venv`, `node_modules`
- `file_selector.filter_code_files()` also skips binary/lock/generated files

## Interface modes

- **CLI** (default): `INTERFACE_MODE="cli"` — spinner + inline streaming output
- **ACP**: `python -m interfaces.acp_server` — FastAPI WebSocket `ws://0.0.0.0:9000/agent`
- **MCP**: `uv run python -m interfaces.mcp_server` — exposes Chat/Plan/Edit/Search/etc as MCP tools

## Test conventions

- Tests use `monkeypatch` extensively to mock LLM calls, file I/O, and handlers
- `tmp_path` fixture used for filesystem tests (no real test repo needed)
- `test_mcp.py` is a manual integration script, not a pytest test (no `test_` prefix)
- `test_repo/` is a tiny fixture repo used by MCP test script (not needed by pytest suite)

## Code style note

The codebase uses a non-standard formatting style with blank lines after every `:` before the indented block body, and double blank lines between top-level definitions. Preserve this style when editing.
