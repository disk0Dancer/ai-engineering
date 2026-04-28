"""Context engineering: build the small prompt the agent actually needs."""

from __future__ import annotations

from .schema import Message, ToolResult

SYSTEM_PROMPT = """You are a concise customer support agent for GamePay.
Use tools for invoice/refund facts. Do not invent transaction status.
If the issue is risky or unclear, explain the next safe support step.
""".strip()


def build_context(
    user_text: str, memories: list[str], tool_results: list[ToolResult]
) -> list[Message]:
    memory_block = "\n".join(f"- {fact}" for fact in memories) or "- no saved facts"
    tool_block = (
        "\n".join(f"- {result.name}: {result.data}" for result in tool_results)
        or "- no tools used yet"
    )
    return [
        Message("system", SYSTEM_PROMPT),
        Message("system", f"Known user memory:\n{memory_block}"),
        Message("system", f"Tool observations:\n{tool_block}"),
        Message("user", user_text),
    ]
