"""Memory-layer abstraction over Hindsight.

The rest of the app only talks to MemoryBank — never to Hindsight directly —
so the memory backend can be swapped without touching agent logic.
"""

from __future__ import annotations

from typing import Any

from . import config


class MemoryBank:
    """A named, persistent memory bank backed by Hindsight.

    retain()  — store what happened (conversation turns, facts, events)
    recall()  — retrieve relevant memories for a query (TEMPR search)
    reflect() — disposition-aware reasoning over the bank (uses bank mission)
    """

    def __init__(self, bank_id: str | None = None, enabled: bool = True):
        self.bank_id = bank_id or config.BANK_ID
        self.enabled = enabled
        self._client = self._connect()

    # -- connection -----------------------------------------------------
    def _connect(self):
        if config.HINDSIGHT_MODE == "server":
            from hindsight_client import Hindsight

            return Hindsight(base_url=config.HINDSIGHT_URL)
        # Embedded daemon: one background process shared by ALL python
        # processes on this machine, so memory persists across runs.
        from hindsight import HindsightEmbedded

        kwargs: dict[str, Any] = {"llm_provider": config.HINDSIGHT_LLM_PROVIDER}
        if config.HINDSIGHT_LLM_MODEL:
            kwargs["llm_model"] = config.HINDSIGHT_LLM_MODEL
        if config.HINDSIGHT_LLM_API_KEY:
            kwargs["llm_api_key"] = config.HINDSIGHT_LLM_API_KEY
        return HindsightEmbedded(**kwargs)

    # -- operations -----------------------------------------------------
    def remember(self, content: str) -> None:
        """Store a piece of content (a turn, a fact, an event) in the bank."""
        self._client.retain(bank_id=self.bank_id, content=content)

    def recall(self, query: str, top_k: int = 5) -> list[str]:
        """Return the most relevant memories for a query (empty when disabled)."""
        if not self.enabled:
            return []
        results = self._client.recall(bank_id=self.bank_id, query=query)
        return [self._text(r) for r in self._as_list(results)[:top_k]]

    def reflect(self, query: str) -> str:
        """Agentic reasoning over the bank, shaped by its mission/directives."""
        if not self.enabled:
            return ""
        result = self._client.reflect(bank_id=self.bank_id, query=query)
        return self._text(result)

    # -- helpers --------------------------------------------------------
    @staticmethod
    def _as_list(results: Any) -> list:
        if results is None:
            return []
        if isinstance(results, list):
            return results
        for attr in ("memories", "results", "items", "data"):
            if hasattr(results, attr):
                return list(getattr(results, attr) or [])
        if isinstance(results, dict):
            for key in ("memories", "results", "items", "data"):
                if key in results:
                    return list(results[key] or [])
        return [results]

    @staticmethod
    def _text(item: Any) -> str:
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            for key in ("content", "text", "memory", "fact", "observation"):
                if item.get(key):
                    return str(item[key])
            return str(item)
        for attr in ("content", "text", "memory", "fact"):
            if hasattr(item, attr):
                val = getattr(item, attr)
                if val:
                    return str(val)
        return str(item)
