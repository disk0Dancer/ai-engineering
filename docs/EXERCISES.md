# Exercises

Use these tasks to extend the agent while preserving the current architecture boundaries.

## 1. Add a new tool

Implement `cancel_subscription(subscription_id: str)` in `support_agent/tools.py`.

Acceptance criteria:

- the tool returns structured data;
- the tool is registered in `TOOLS`;
- a test proves known and unknown subscription IDs are handled.

## 2. Swap the LLM adapter

Create a new class that implements `LLM.complete(messages)`.

Ideas:

- OpenAI-compatible endpoint;
- Anthropic;
- Ollama running locally;
- any hosted model provider.

Acceptance criteria:

- `CustomerSupportAgent(llm=YourLLM(...))` works without changing `agent.py`;
- failures are surfaced as readable errors.

## 3. Improve memory

Replace append-only facts with a compact user profile.

Acceptance criteria:

- repeated facts are deduplicated;
- outdated facts can be overwritten;
- tests cover at least two users.

## 4. Add a risk specialist

Extend `SPECIALISTS` with `risk-agent` for messages about fraud, chargebacks, suspicious activity, stolen cards or account takeover.

Acceptance criteria:

- risk messages route to `risk-agent`;
- regular refund and billing messages keep existing routing.

## 5. Improve context engineering

Update `build_context()` so long tool observations are shortened before they reach the LLM.

Acceptance criteria:

- context stays readable;
- important invoice/refund fields are preserved;
- tests cover long observations.

## 6. Describe an MCP migration

Write a short design note explaining how `support_agent/tools.py` could become an MCP server.

Cover:

- tool names and schemas;
- where authentication would live;
- what should stay in the agent process;
- what should move to the MCP server.
