"""End-to-end check: same question with memory OFF vs ON.

Proves the demo's core contrast without a browser:
  - memory OFF -> generic answer, no memories recalled
  - memory ON  -> personalized answer grounded in recalled memories

Usage: python scripts/storesage_demo_check.py [--bank storesage-demo]
Requires the bank to be seeded (see scripts/seed_storesage.py).
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
os.environ.setdefault("BANK_ID", "storesage-demo")
os.environ.setdefault("HINDSIGHT_LLM_PROVIDER", "none")

from src.agent import Agent  # noqa: E402

STORESAGE_DEMO_QUESTION = "Hi, do you have atta?"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", default=os.environ["BANK_ID"])
    args = ap.parse_args()

    baseline_result = Agent(bank_id=args.bank, memory_enabled=False).respond(STORESAGE_DEMO_QUESTION)
    memory_result = Agent(bank_id=args.bank, memory_enabled=True).respond(STORESAGE_DEMO_QUESTION)

    print("=== MEMORY OFF ===")
    print(baseline_result.reply)
    print()
    print("=== MEMORY ON (recalled %d) ===" % len(memory_result.memories_used))
    for recalled_memory in memory_result.memories_used:
        print("  [memory]", recalled_memory[:110])
    print()
    print(memory_result.reply)

    assert not baseline_result.memories_used, "memory OFF should recall nothing"
    assert memory_result.memories_used, "memory ON should recall seeded memories"
    print()
    print("E2E: OK ✅")


if __name__ == "__main__":
    main()
