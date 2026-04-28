"""LLM adapters. The default one is deterministic for offline learning/tests."""

from __future__ import annotations

from .schema import Message


class EchoLLM:
    """Deterministic LLM adapter used before wiring OpenAI/Anthropic/Ollama/etc."""

    def complete(self, messages: list[Message]) -> str:
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        observations = [
            m.content for m in messages if m.role == "system" and "Tool observations" in m.content
        ]
        if observations and "found': True" in observations[-1]:
            return "I checked the available support data and summarized the safe next step below."
        return f"I can help with that. You said: {user}"
