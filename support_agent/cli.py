"""CLI entry point for the course support agent."""

from __future__ import annotations

import argparse

from .multi_agent import SupportRouter


def main() -> None:
    parser = argparse.ArgumentParser(description="Intro AI Agents support demo")
    parser.add_argument(
        "message", nargs="*", default=["refund INV-1001 please"], help="Message to send"
    )
    args = parser.parse_args()

    router = SupportRouter()
    response = router.route(" ".join(args.message))
    print(response.answer)


if __name__ == "__main__":
    main()
