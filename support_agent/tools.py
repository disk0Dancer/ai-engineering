"""Tools for the GamePay customer support agent.

The functions intentionally look like MCP tools: name, description, JSON input,
JSON output. In real MCP they would be exposed by a server; here they are plain
Python functions backed by small JSON datasets for demos and exercises.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

DATA_DIR = Path(__file__).with_name("data")


@dataclass(frozen=True)
class FunctionTool:
    name: str
    description: str
    fn: Callable[..., dict[str, Any]]

    def __call__(self, **kwargs: Any) -> dict[str, Any]:
        return self.fn(**kwargs)


@lru_cache(maxsize=None)
def _load_table(name: str) -> list[dict[str, Any]]:
    with (DATA_DIR / name).open(encoding="utf-8") as file:
        return json.load(file)


def _index_by(table_name: str, field: str) -> dict[str, dict[str, Any]]:
    return {str(row[field]).lower(): row for row in _load_table(table_name)}


def get_invoice(invoice_id: str) -> dict[str, Any]:
    invoice = _index_by("invoices.json", "invoice_id").get(invoice_id.lower())
    if invoice is None:
        return {"found": False, "message": "Invoice not found"}
    return {"found": True, **invoice}


def lookup_customer(email: str) -> dict[str, Any]:
    customer = _index_by("customers.json", "email").get(email.lower())
    if customer is None:
        return {"found": False, "message": "Customer not found"}
    return {"found": True, **customer}


def get_subscription(subscription_id: str) -> dict[str, Any]:
    subscription = _index_by("subscriptions.json", "subscription_id").get(subscription_id.lower())
    if subscription is None:
        return {"found": False, "message": "Subscription not found"}
    return {"found": True, **subscription}


def cancel_subscription(subscription_id: str, reason: str) -> dict[str, Any]:
    """TODO: implement subscription cancellation for the student exercise.

    Expected behaviour:
    - find subscription by `subscription_id`;
    - reject unknown IDs with a structured message;
    - return a cancellation ticket for active/past_due subscriptions;
    - keep output JSON-serializable.
    """
    return {
        "cancelled": False,
        "subscription_id": subscription_id.upper(),
        "message": "TODO: implement cancel_subscription",
        "reason": reason,
    }


def search_faq(query: str) -> dict[str, Any]:
    query_lower = query.lower()
    query_words = set(query_lower.replace("?", "").split())
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in _load_table("faq.json"):
        haystack = f"{item['topic']} {item['title']} {item['answer']}".lower()
        score = sum(1 for word in query_words if word in haystack)
        if item["topic"] in query_lower:
            score += 3
        if score:
            scored.append((score, item))

    scored.sort(key=lambda item: item[0], reverse=True)
    articles = [item for _, item in scored[:2]] or _load_table("faq.json")[:1]
    return {"found": bool(articles), "articles": articles}


def create_refund_request(invoice_id: str, reason: str) -> dict[str, Any]:
    invoice = get_invoice(invoice_id)
    if not invoice.get("found"):
        return {"created": False, "message": "Cannot create refund: invoice not found"}
    if invoice["status"] == "refunded":
        return {"created": False, "message": "Invoice is already refunded"}
    if invoice["status"] == "failed":
        return {
            "created": False,
            "message": "Payment failed, so there is no successful invoice to refund yet",
        }
    return {
        "created": True,
        "ticket_id": f"RF-{invoice_id.upper()}",
        "status": "needs_review",
        "reason": reason,
    }


TOOLS: dict[str, FunctionTool] = {
    "get_invoice": FunctionTool("get_invoice", "Look up invoice by invoice_id", get_invoice),
    "lookup_customer": FunctionTool("lookup_customer", "Find customer by email", lookup_customer),
    "get_subscription": FunctionTool(
        "get_subscription", "Look up subscription by subscription_id", get_subscription
    ),
    "cancel_subscription": FunctionTool(
        "cancel_subscription", "Cancel an active support subscription", cancel_subscription
    ),
    "search_faq": FunctionTool("search_faq", "Search support FAQ by text query", search_faq),
    "create_refund_request": FunctionTool(
        "create_refund_request", "Open a refund review ticket", create_refund_request
    ),
}
