import pytest

from support_agent.context import trim_tool_observation
from support_agent.tools import TOOLS, cancel_subscription


@pytest.mark.todo
def test_todo_cancel_subscription_creates_ticket_for_active_subscription():
    result = cancel_subscription("SUB-7001", reason="customer requested cancellation")

    assert result["cancelled"] is True
    assert result["subscription_id"] == "SUB-7001"
    assert result["ticket_id"].startswith("CS-SUB-7001")
    assert result["status"] == "cancellation_requested"


@pytest.mark.todo
def test_todo_cancel_subscription_is_registered_as_tool():
    result = TOOLS["cancel_subscription"](
        subscription_id="SUB-7001",
        reason="customer requested cancellation",
    )

    assert result["cancelled"] is True


@pytest.mark.todo
def test_todo_long_tool_observations_are_trimmed_for_context_budget():
    observation = {"content": "A" * 500 + " important ending"}

    trimmed = trim_tool_observation(observation, max_chars=120)

    assert len(trimmed) <= 120
    assert "...truncated..." in trimmed
    assert "important ending" in trimmed
