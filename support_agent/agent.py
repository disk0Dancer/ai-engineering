"""Customer support agent with tools, memory and context assembly."""

from __future__ import annotations

import re

from .context import build_context
from .interfaces import LLM, Memory
from .llm import EchoLLM
from .memory import InMemoryMemory
from .schema import AgentResponse, ToolResult
from .tools import TOOLS

INVOICE_RE = re.compile(r"INV-\d+", re.IGNORECASE)
RISK_WORDS = ("chargeback", "fraud", "stolen", "unauthorized", "dispute")
SUBSCRIPTION_RE = re.compile(r"SUB-\d+", re.IGNORECASE)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


class CustomerSupportAgent:
    def __init__(self, llm: LLM | None = None, memory: Memory | None = None) -> None:
        self.llm = llm or EchoLLM()
        self.memory = memory or InMemoryMemory()

    def chat(self, user_text: str, user_id: str = "demo-user") -> AgentResponse:
        lowered = user_text.lower()
        tool_results: list[ToolResult] = []

        if "remember" in lowered or "запомни" in lowered:
            fact = user_text.split(":", 1)[-1] if ":" in user_text else user_text
            self.memory.remember(user_id, fact)

        email_match = EMAIL_RE.search(user_text)
        if email_match:
            customer = TOOLS["lookup_customer"](email=email_match.group(0))
            tool_results.append(ToolResult("lookup_customer", customer))

        invoice_match = INVOICE_RE.search(user_text)
        risk_case = any(word in lowered for word in RISK_WORDS)

        if invoice_match:
            invoice_id = invoice_match.group(0).upper()
            invoice = TOOLS["get_invoice"](invoice_id=invoice_id)
            tool_results.append(ToolResult("get_invoice", invoice))
            if ("refund" in lowered or "возврат" in lowered) and not risk_case:
                refund = TOOLS["create_refund_request"](invoice_id=invoice_id, reason=user_text)
                tool_results.append(ToolResult("create_refund_request", refund))

        subscription_match = SUBSCRIPTION_RE.search(user_text)
        if subscription_match:
            subscription = TOOLS["get_subscription"](
                subscription_id=subscription_match.group(0).upper()
            )
            tool_results.append(ToolResult("get_subscription", subscription))

        if not tool_results or any(
            word in lowered for word in ["how", "policy", "failed", "help", *RISK_WORDS]
        ):
            faq = TOOLS["search_faq"](query=user_text)
            tool_results.append(ToolResult("search_faq", faq))

        messages = build_context(user_text, self.memory.recall(user_id), tool_results)
        llm_summary = self.llm.complete(messages)
        answer = self._render_answer(llm_summary, tool_results)
        return AgentResponse(answer=answer, tool_calls=tool_results)

    @staticmethod
    def _render_answer(llm_summary: str, tool_results: list[ToolResult]) -> str:
        lines = [llm_summary]
        for result in tool_results:
            if result.name == "lookup_customer" and result.data.get("found"):
                lines.append(
                    f"Customer {result.data['name']} ({result.data['email']}): "
                    f"tier={result.data['tier']}, risk={result.data['risk_level']}."
                )
            if result.name == "get_invoice" and result.data.get("found"):
                lines.append(
                    f"Invoice {result.data['invoice_id']}: {result.data['status']}, "
                    f"{result.data['amount']} {result.data['currency']} for "
                    f"{result.data['game']}; delivery={result.data['delivery_status']}."
                )
            if result.name == "get_subscription" and result.data.get("found"):
                lines.append(
                    f"Subscription {result.data['subscription_id']}: {result.data['status']}, "
                    f"plan={result.data['plan']}, renewal={result.data['renewal_date']}."
                )
            if result.name == "create_refund_request":
                if result.data.get("created"):
                    lines.append(f"Refund review ticket created: {result.data['ticket_id']}.")
                else:
                    lines.append(result.data["message"])
            if result.name == "search_faq" and result.data.get("articles"):
                lines.append(result.data["articles"][0]["answer"])
        return "\n".join(lines)
