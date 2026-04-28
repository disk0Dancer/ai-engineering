from support_agent.agent import CustomerSupportAgent
from support_agent.memory import InMemoryMemory
from support_agent.multi_agent import SupportRouter
from support_agent.tools import get_invoice, get_subscription, lookup_customer, search_faq


def test_invoice_tool_finds_known_invoice():
    invoice = get_invoice("INV-1001")
    assert invoice["found"] is True
    assert invoice["status"] == "paid"
    assert invoice["currency"] == "USD"


def test_customer_tool_finds_customer_by_email():
    customer = lookup_customer("alex@example.com")
    assert customer["found"] is True
    assert customer["customer_id"] == "cus_alex"


def test_subscription_tool_finds_known_subscription():
    subscription = get_subscription("SUB-7001")
    assert subscription["found"] is True
    assert subscription["status"] == "active"


def test_faq_tool_returns_refund_article():
    result = search_faq("refund")
    assert result["found"] is True
    assert "Refunds" in result["articles"][0]["answer"]


def test_memory_deduplicates_facts():
    memory = InMemoryMemory()
    memory.remember("u1", "prefers Russian")
    memory.remember("u1", "prefers Russian")
    assert memory.recall("u1") == ["prefers Russian"]


def test_agent_uses_customer_invoice_and_refund_tools():
    response = CustomerSupportAgent().chat("refund INV-1001 for alex@example.com")
    assert "Customer Alex Chen" in response.answer
    assert "Invoice INV-1001" in response.answer
    assert "Refund review ticket created" in response.answer
    assert [call.name for call in response.tool_calls[:3]] == [
        "lookup_customer",
        "get_invoice",
        "create_refund_request",
    ]


def test_agent_handles_subscription_lookup():
    response = CustomerSupportAgent().chat("check SUB-7001")
    assert "Subscription SUB-7001" in response.answer
    assert response.tool_calls[0].name == "get_subscription"


def test_router_marks_specialist_handoff():
    response = SupportRouter().route("refund INV-1001")
    assert response.handoff == "refund-agent"
    assert response.answer.startswith("[refund-agent]")


def test_risk_message_routes_without_creating_refund():
    response = SupportRouter().route("chargeback on INV-1001, should we refund?")
    assert response.handoff == "risk-agent"
    assert "Chargeback" in response.answer
    assert "Refund review ticket created" not in response.answer
    assert [call.name for call in response.tool_calls] == ["get_invoice", "search_faq"]
