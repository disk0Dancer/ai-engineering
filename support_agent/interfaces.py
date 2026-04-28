"""Protocols: the stable boundaries between LLMs, tools, memory and agents."""

from __future__ import annotations

from typing import Any, Protocol

from .schema import Message


class LLM(Protocol):
    def complete(self, messages: list[Message]) -> str:
        """Return the next assistant message for a list of chat messages."""


class Memory(Protocol):
    def remember(self, user_id: str, fact: str) -> None:
        """Persist a small fact about the user/session."""

    def recall(self, user_id: str) -> list[str]:
        """Return known facts for the user/session."""


class Tool(Protocol):
    name: str
    description: str

    def __call__(self, **kwargs: Any) -> dict[str, Any]:
        """Run the tool and return JSON-serializable data."""
