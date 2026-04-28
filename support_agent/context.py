"""Context engineering: build the small prompt the agent actually needs."""

from __future__ import annotations

from .schema import Message, ToolResult

MAX_OBSERVATION_CHARS = 240

SYSTEM_PROMPT = """You are a concise customer support agent for GamePay.
Use tools for invoice/refund facts. Do not invent transaction status.
If the issue is risky or unclear, explain the next safe support step.
""".strip()


def trim_tool_observation(value: object, max_chars: int = MAX_OBSERVATION_CHARS) -> str:
    """TODO: keep tool observations within a context budget.

    The implementation should preserve the start and end of long observations and
    include an explicit marker that content was truncated.
    """
    return str(value)


def build_context(
    user_text: str, memories: list[str], tool_results: list[ToolResult]
) -> list[Message]:
    memory_block = "\n".join(f"- {fact}" for fact in memories) or "- no saved facts"
    tool_block = (
        "\n".join(
            f"- {result.name}: {trim_tool_observation(result.data)}" for result in tool_results
        )
        or "- no tools used yet"
    )
    return [
        Message("system", SYSTEM_PROMPT),
        Message("system", f"Known user memory:\n{memory_block}"),
        Message("system", f"Tool observations:\n{tool_block}"),
        Message("user", user_text),
    ]
