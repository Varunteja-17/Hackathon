"""Idea-agnostic agent loop.

Each turn:
  1. recall()  — pull relevant memories (skipped when memory is disabled)
  2. LLM chat  — answer grounded in those memories
  3. retain()  — store the exchange so the NEXT turn is smarter

That retain/recall loop is the whole learning curve the demo shows.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .llm import get_llm
from .memory import MemoryBank

DEFAULT_SYSTEM = (
    "You are a helpful business assistant. You remember past interactions "
    "with each customer and use those memories to personalize every reply. "
    "Be warm, concise, and specific — never generic when you have memories "
    "to draw on."
)


@dataclass
class TurnResult:
    reply: str
    memories_used: list[str] = field(default_factory=list)
    memory_enabled: bool = True


class Agent:
    def __init__(
        self,
        bank_id: str | None = None,
        system_prompt: str = DEFAULT_SYSTEM,
        memory_enabled: bool = True,
    ):
        self.memory = MemoryBank(bank_id=bank_id, enabled=memory_enabled)
        self.system_prompt = system_prompt
        self.memory_enabled = memory_enabled
        self.llm = get_llm()

    def respond(self, user_text: str, speaker: str = "customer") -> TurnResult:
        memories = self.memory.recall(user_text) if self.memory_enabled else []
        reply = self.llm.chat(self.system_prompt, memories, user_text)
        if self.memory_enabled:
            self.memory.remember(f"{speaker}: {user_text}")
            self.memory.remember(f"assistant: {reply}")
        return TurnResult(
            reply=reply, memories_used=memories, memory_enabled=self.memory_enabled
        )

    def set_memory_enabled(self, enabled: bool) -> None:
        self.memory_enabled = enabled
        self.memory.enabled = enabled
