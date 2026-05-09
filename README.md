# Coding Agent

An interactive CLI tool that assists with software engineering tasks including code explanation, planning, editing, testing, and more.

## Features

- **Interactive REPL**: Chat-based interface for coding assistance
- **Command System**: Slash-prefixed commands for specific actions
- **Multiple Interface Modes**: 
  - CLI (default): Terminal-based interaction
  - ACP: WebSocket server (`ws://0.0.0.0:9000/agent`)
  - MCP: Standard I/O server exposing tools
- **Code Understanding**: Explain, summarize, and walk through codebases
- **Planning & Editing**: Generate plans and apply changes with safety mechanisms
- **Search & Navigation**: Ripgrep-based code search and file operations
- **Testing Integration**: Run tests and analyze failures
- **LLM Integration**: Connects to local or cloud LLM providers
- **Backup & Rollback**: Automatic backups before changes with rollback capability

## Installation

```bash
# Clone the repository
git clone https://github.com/kk-engineer/coding_agent
cd coding_agent

# Install in development mode
pip install -e ".[dev]"
# or with uv
uv sync

# Run tests to verify installation
pytest
```

## Quick Start

```bash
# Start the coding agent
python -m app

# In the interactive shell:
# Ask questions naturally
How does the authentication system work?

# Use slash commands for specific actions
/edit Add error handling to the login function
/plan Design a caching layer for the API
/search Find all usages of the validate_user function
/test Run the test suite
/status Check git status and workspace
/files List files in the src directory
/explain Explain the database connection module
/diff Show pending changes
```

## Architecture

```
app.py
├── command/cli.py          # REPL loop and command dispatch
│   ├── command_router.py   # Command parsing and intent inference
│   ├── commands.py         # Command definitions
│   ├── handlers.py         # Command implementation
│   └── help_text.py        # Help documentation
├── interfaces/
│   ├── acp_server.py       # WebSocket server (ACP mode)
│   └── mcp_server.py       # MCP stdio server
├── config/
│   ├── agent_config.py     # Configuration including INTERFACE_MODE
│   └── llm_local.py        # LLM provider configuration
├── core/                   # Core orchestration logic
├── repo_utils/             # Repository scanning and analysis
├── utils/                  # Utility functions (console, streaming, etc.)
└── ast_utils/              # AST transformation utilities
```

### Key Components

1. **Command Processing**: 
   - Natural language input is routed to appropriate commands via intent recognition
   - Slash commands bypass inference for explicit actions

2. **Edit Flow** (for `/edit` and `/do`):
   ```
   orchestrator.execute_changes()
   → find_related_files()
   → For each file:
        read → LLM generates update → backup_file() → write → run_tests()
        → If test fails: analyze_failure() → retry (max 3 attempts)
   ```

3. **Interface Modes** (set in `config/agent_config.py`):
   - `CLI` (default): Terminal with spinner and inline streaming
   - `ACP`: FastAPI WebSocket server on port 9000
   - `MCP`: Standard I/O server exposing MCP tools

## Configuration

### LLM Provider

Edit `config/llm_local.py` to switch between local and cloud LLM providers:

```python
# Local LLM (default)
BASE_URL = "http://localhost:8000/v1"

# Cloud LLM (example)
BASE_URL = "https://api.cloud-llm-provider.com/v1"
```

### Interface Mode

Set `INTERFACE_MODE` in `config/agent_config.py`:
```python
# Options: "cli", "acp", "mcp"
INTERFACE_MODE = "cli"
```

## Command Reference

| Command | Aliases | Description |
|---------|---------|-------------|
| `/chat` | `/ask` | Read-only Q&A (natural language) |
| `/edit` | `/do`, `/change` | Plan, confirm, and apply code changes |
| `/plan` | — | Generate plan without modifying files |
| `/explain` | `/why` | Explain a file or directory |
| `/search` | `/find` | Repository code search (uses ripgrep) |
| `/test` | `/tests` | Run detected test suite |
| `/diff` | — | Show git diff of pending changes |
| `/files` | — | List files under a path |
| `/run` | `!` | Execute a local shell command |
| `/status` | `/st` | Show workspace and git status |
| `/exit` | `/quit`, `/q` | Quit the application |

### Freeform Interpretation

Plain text input is interpreted as:
- **Explain** (`/explain`): Starts with "explain", "describe", "summarize", etc.
- **Plan** (`/plan`): Starts with "plan", "design", "approach", etc.
- **Chat** (`/chat`): Everything else

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_command_router.py -x

# Run tests with verbose output
pytest -v
```

### Code Style

The codebase uses a non-standard formatting style:
- Blank lines after every `:` before indented blocks
- Double blank lines between top-level definitions
- Preserve this style when editing

### Dependencies

Core dependencies include:
- `fastapi` + `uvicorn` (ACP server)
- `mcp` (MCP server)
- `openai` (LLM client)
- `rich` (terminal formatting)
- `libcst` (Python AST transforms)
- `jedi` (navigation/definitions)
- `networkx` (dependency/call graphs)
- `ripgrep` (required for code search)

Development dependencies:
- `pytest` (testing)

## Safety Features

1. **Change Preview**: `/plan` shows suggested diffs without applying changes
2. **Automatic Backups**: Files are backed up to `.agent_backups/` before modification
3. **Test Verification**: Changes are validated by running tests
4. **Retry Mechanism**: Failed changes are analyzed and retried (up to 3 times)
5. **Rollback Capability**: All changes can be rolled back via `rollback_executor.rollback_all()`

## Extending the Agent

To add new commands:
1. Add command definition in `command/commands.py`
2. Implement handler in `command/handlers.py`
3. Register handler in `command/cli.py` dispatch function
4. Add help text in `command/help_text.py`

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for terminal formatting
- Uses [FastAPI](https://fastapi.tiangolo.com/) for ACP WebSocket server
- Leverages [MCP](https://modelcontextprotocol.io/) for standard I/O integration
- Powered by local or cloud LLM providers

---

For more detailed information, refer to `AGENTS.md` which contains in-depth documentation about the architecture, interfaces, and internal workings of the coding agent.