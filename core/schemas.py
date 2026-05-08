from pydantic import BaseModel
from typing import List, Optional


class AgentStep(BaseModel):

    type: str

    content: str


class DiffEntry(BaseModel):

    file: str

    diff: str


class RollbackEntry(BaseModel):

    file: str

    rollback_id: str

    backup_path: str


class TestResult(BaseModel):

    success: bool

    stdout: str

    stderr: str

    returncode: int


class PlanResponse(BaseModel):

    steps: List[AgentStep]

    related_files: List[str]

    plan: str


class ExecuteResponse(BaseModel):

    steps: List[AgentStep]

    diffs: List[DiffEntry]

    rollbacks: List[RollbackEntry]

    tests: Optional[TestResult] = None