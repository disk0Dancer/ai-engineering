"""Multi-agent pattern: route a task to a specialized small agent."""

from __future__ import annotations

from dataclasses import dataclass

from .agent import CustomerSupportAgent
from .schema import AgentResponse


@dataclass(frozen=True)
class RoutedAgent:
    name: str
    keywords: tuple[str, ...]
    instruction: str


SPECIALISTS = [
    RoutedAgent(
        "risk-agent",
        ("chargeback", "fraud", "stolen", "unauthorized", "dispute"),
        "Handles payment risk and ownership-sensitive cases.",
    ),
    RoutedAgent("refund-agent", ("refund", "возврат"), "Handles refunds and policy checks."),
    RoutedAgent(
        "billing-agent", ("invoice", "payment", "оплат"), "Handles invoices and payment status."
    ),
    RoutedAgent("tech-agent", ("error", "bug", "ошибка"), "Handles technical troubleshooting."),
]


class SupportRouter:
    def __init__(self, base_agent: CustomerSupportAgent | None = None) -> None:
        self.base_agent = base_agent or CustomerSupportAgent()

    def route(self, user_text: str, user_id: str = "demo-user") -> AgentResponse:
        lowered = user_text.lower()
        default_specialist = next(agent for agent in SPECIALISTS if agent.name == "billing-agent")
        specialist = next(
            (agent for agent in SPECIALISTS if any(k in lowered for k in agent.keywords)),
            default_specialist,
        )
        response = self.base_agent.chat(user_text, user_id=user_id)
        response.handoff = specialist.name
        response.answer = f"[{specialist.name}] {response.answer}"
        return response
