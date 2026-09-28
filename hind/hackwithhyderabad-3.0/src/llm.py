"""Agent's own LLM — OpenAI-compatible endpoint, configured via env vars.

When no LLM_API_KEY is set, a transparent StubLLM answers instead so the
whole demo (including the memory before/after contrast) runs with zero keys.
The stub is honest about what it is: it weaves recalled memories into a
templated reply, which is exactly what the demo needs to prove.
"""

from __future__ import annotations

from . import config


class StubLLM:
    """Key-less stand-in. Echoes the query, grounded in recalled memories."""

    name = "stub (no API key configured)"

    def chat(self, system: str, memories: list[str], user_text: str) -> str:
        if memories:
            joined = "\n".join(f"- {m}" for m in memories[:4])
            return (
                f"Thanks for asking: \"{user_text}\"\n\n"
                f"Here's what I remember that's relevant:\n{joined}\n\n"
                f"Based on that, my suggestion: this looks like a repeat of "
                f"your usual pattern — want me to go ahead as last time?"
            )
        return (
            f"Thanks for asking: \"{user_text}\"\n\n"
            "I don't have any past context on this yet, so here's a general "
            "answer: I'd need more details to give you a specific "
            "recommendation. (Memory is OFF or this bank is empty.)"
        )


class OpenAILLM:
    """Real LLM via any OpenAI-compatible endpoint (Groq, OpenAI, Ollama...)."""

    def __init__(self):
        from openai import OpenAI

        self._client = OpenAI(
            base_url=config.LLM_BASE_URL,
            api_key=config.LLM_API_KEY,
        )
        self.name = f"{config.LLM_MODEL} @ {config.LLM_BASE_URL}"

    def chat(self, system: str, memories: list[str], user_text: str) -> str:
        mem_block = ""
        if memories:
            mem_block = (
                "\n\nRelevant memories about this user (use them to "
                "personalize your reply):\n" + "\n".join(f"- {m}" for m in memories)
            )
        resp = self._client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[
                {"role": "system", "content": system + mem_block},
                {"role": "user", "content": user_text},
            ],
            temperature=0.7,
        )
        return resp.choices[0].message.content or ""


def get_llm():
    """Real LLM when a key is configured, stub otherwise."""
    if config.LLM_API_KEY:
        return OpenAILLM()
    return StubLLM()
