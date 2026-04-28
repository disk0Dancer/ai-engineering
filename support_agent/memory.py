"""Memory examples: short-term and user-scoped facts kept in-process."""

from __future__ import annotations

from collections import defaultdict


class InMemoryMemory:
    """Tiny memory store used to demonstrate the concept without databases."""

    def __init__(self) -> None:
        self._facts: dict[str, list[str]] = defaultdict(list)

    def remember(self, user_id: str, fact: str) -> None:
        fact = fact.strip()
        if fact and fact not in self._facts[user_id]:
            self._facts[user_id].append(fact)

    def recall(self, user_id: str) -> list[str]:
        return list(self._facts.get(user_id, []))
