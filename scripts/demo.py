import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from support_agent.multi_agent import SupportRouter

SCENARIOS = [
    "How do refunds work?",
    "Please refund INV-1001 for alex@example.com",
    "Payment failed for INV-2001, what should I tell maria@example.com?",
    "My item from INV-3001 is still missing",
    "Can you check subscription SUB-7001?",
    "I see a chargeback on INV-1001, is it safe to refund?",
]

router = SupportRouter()
for message in SCENARIOS:
    print(f"\n> {message}")
    print(router.route(message).answer)
