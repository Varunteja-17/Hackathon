"""Seed a demo bank with a multi-week customer history.

This builds the 'learning curve' the demo shows: the same question asked
against an empty bank (generic answer) vs this seeded bank (personalized).

Usage:
    python scripts/seed_storesage.py [--bank storesage-demo] [--scenario storesage]

Scenarios are just seed data — swap in your own for a different project idea.
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

from src.memory import MemoryBank  # noqa: E402

STORESAGE_CUSTOMER_STORY = [
    # (day label, speaker, text)
    ("Day 1", "customer", "Hi, do you have whole wheat atta? What is the price?"),
    ("Day 1", "assistant", "Yes! We have 5kg bags at Rs. 320. Would you like one?"),
    ("Day 1", "customer", "Yes, I'll take the 5kg bag. My name is Lakshmi."),
    ("Day 8", "customer", "Hi, it's Lakshmi. Can you deliver to my home in Kukatpally?"),
    ("Day 8", "assistant", "Of course, Lakshmi. Home delivery is free above Rs. 500."),
    ("Day 8", "customer", "Great, I prefer home delivery always. I can't carry heavy bags."),
    ("Day 15", "customer", "Do you have a mixer grinder? Mine broke down."),
    ("Day 15", "assistant", "Sorry, we're out of stock right now. New stock next month."),
    ("Day 15", "customer", "Please let me know when it arrives. I need one urgently."),
    ("Day 22", "customer", "Hi, it's Lakshmi. My usual 5kg atta please, home delivery."),
    ("Day 22", "assistant", "Done — your usual 5kg whole wheat atta, home delivery tomorrow."),
    # The mixer grinder is back in stock (shopkeeper's note, not told to customer yet)
    ("Day 29", "shopkeeper-note", "Mixer grinder back in stock today. Lakshmi asked about it on Day 15."),
]

STORESAGE_SCENARIOS = {"storesage": STORESAGE_CUSTOMER_STORY}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", default=os.environ["BANK_ID"])
    ap.add_argument("--scenario", default="storesage", choices=list(STORESAGE_SCENARIOS))
    args = ap.parse_args()

    bank = MemoryBank(bank_id=args.bank)
    history = STORESAGE_SCENARIOS[args.scenario]
    for day, speaker, text in history:
        bank.remember(f"[{day}] {speaker}: {text}")
    print(f"[seed] retained {len(history)} memories into bank '{args.bank}'")
    print("[seed] demo question: 'Hi, do you have atta?'")
    print("[seed]   - memory OFF -> generic answer")
    print("[seed]   - memory ON  -> recalls Lakshmi, her usual 5kg, home delivery,")
    print("[seed]                 and the mixer grinder she asked about on Day 15")


if __name__ == "__main__":
    main()
