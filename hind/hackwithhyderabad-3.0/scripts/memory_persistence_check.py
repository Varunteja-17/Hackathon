"""StoreSage memory round-trip + cross-process persistence check.

Usage:
    python scripts/memory_persistence_check.py retain   # process 1
    python scripts/memory_persistence_check.py recall   # separate process 2

If recall (run 2) finds the fact stored by retain (run 1), memory persists
across sessions via the shared embedded daemon. No API keys needed:
embeddings are local, and the LLM provider defaults to llamacpp (local GGUF).
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
os.environ.setdefault("BANK_ID", "storesage-demo")
os.environ.setdefault("HINDSIGHT_LLM_PROVIDER", "none")

from src.memory import MemoryBank  # noqa: E402

STORESAGE_CHECK_BANK = f"{os.environ['BANK_ID']}-persistence-check"
STORESAGE_CHECK_MARKER = "STORESAGE-PERSISTENCE-CHECK"
STORESAGE_CHECK_FACT = (
    f"{STORESAGE_CHECK_MARKER}: the customer's name is Lakshmi and she always "
    "buys 5kg whole wheat atta on the first Monday of the month."
)
STORESAGE_CHECK_QUERY = f"What does {STORESAGE_CHECK_MARKER} say about the customer's usual order?"


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "retain"
    bank = MemoryBank(bank_id=STORESAGE_CHECK_BANK)

    if mode == "retain":
        bank.remember(STORESAGE_CHECK_FACT)
        print(f"[storesage-check] retained: {STORESAGE_CHECK_FACT[:60]}...")
        print("[storesage-check] now run: python scripts/memory_persistence_check.py recall")
    elif mode == "recall":
        time.sleep(2)  # let async extraction settle
        hits = bank.recall(STORESAGE_CHECK_QUERY)
        print(f"[storesage-check] recall returned {len(hits)} memories:")
        for h in hits:
            print("  -", h[:160])
        ok = any(STORESAGE_CHECK_MARKER in h for h in hits)
        print("[storesage-check] PERSISTENCE:", "OK ✅" if ok else "FAILED ❌")
        sys.exit(0 if ok else 1)
    else:
        print("usage: memory_persistence_check.py [retain|recall]")
        sys.exit(2)


if __name__ == "__main__":
    main()
