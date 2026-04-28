"""Small shared data structures for the course examples."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolResult:
    name: str
    data: dict[str, Any]


@dataclass
class AgentResponse:
    answer: str
    tool_calls: list[ToolResult] = field(default_factory=list)
    handoff: str | None = None
