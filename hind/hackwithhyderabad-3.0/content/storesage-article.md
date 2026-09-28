# StoreSage: The Shopkeeper That Never Forgets

Small retailers run their businesses on WhatsApp. The same questions arrive
every day — "do you have atta?", "what time do you close?" — and every
conversation starts from zero. The shopkeeper doesn't remember what you bought
last month, which brand you prefer, or that you asked about an out-of-stock
item three weeks ago. Repeat customers get treated like strangers, and
follow-ups simply never happen.

StoreSage is our answer: a WhatsApp-style assistant for small retailers that
remembers every customer. Not a FAQ bot with a greeting — an assistant whose
entire product is memory.

## How the memory works

StoreSage is built on [Hindsight](https://hindsight.vectorize.io/) by
Vectorize, an agent-memory system. Every exchange with a customer is retained;
every reply is grounded in recalled memories. The integration lives in one
module — `src/memory.py`, a `MemoryBank` class that is the only code that
talks to Hindsight. Everything else stays idea-agnostic.

Hindsight runs fully self-hosted here: an embedded daemon (`HindsightEmbedded`)
shared by all Python processes, backed by an embedded PostgreSQL database, with
local embeddings (`bge-small-en-v1.5`) and a local reranker. No account, no
signup, no external calls — the demo runs on a laptop. Recall uses Hindsight's
TEMPR search (semantic + keyword + graph + temporal), so "my usual atta" finds
Lakshmi's order from Day 22 even though the wording differs.

The agent loop itself is deliberately small — this is the whole learning
curve:

```python
def respond(self, user_text: str, speaker: str = "customer") -> TurnResult:
    memories = self.memory.recall(user_text) if self.memory_enabled else []
    reply = self.llm.chat(self.system_prompt, memories, user_text)
    if self.memory_enabled:
        self.memory.remember(f"{speaker}: {user_text}")
        self.memory.remember(f"assistant: {reply}")
    return TurnResult(
        reply=reply, memories_used=memories, memory_enabled=self.memory_enabled
    )
```

Three steps per turn: **recall** relevant memories, **chat** grounded in them,
**retain** the exchange so the next turn is smarter. Flip memory off and the
first line is skipped — the same code path produces a generic stranger.

## Before and after: "Hi, do you have atta?"

We seeded 30 days of one customer's history: Lakshmi buys a 5kg bag of whole
wheat atta every month, always prefers home delivery to Kukatpally, and asked
about a mixer grinder on Day 15 when it was out of stock (it's back by Day 30).

**Memory OFF** — the agent knows nothing:

> *Yes! We have 5kg bags at Rs. 320. Would you like one?*
> Memories recalled: 0.

**Memory ON** — the same question, answered by 30 days of history:

> *Your usual 5kg bag, Lakshmi? A fresh batch just arrived — and the mixer
> grinder you asked about on Day 15 is back in stock. Want me to set one
> aside with home delivery?*
> Memories recalled: 5 — her name, her monthly 5kg order, her home-delivery
> preference, the Day 15 grinder request, the Day 29 restock note.

Same question, same code, completely different answer. That gap *is* the
product.

## Screenshots

> **[Screenshot 1 — placeholder]** Gradio chat UI with the memory toggle set
> to OFF. Caption: *"Memory OFF: 'Hi, do you have atta?' gets a generic price
> quote. Zero memories recalled."*

> **[Screenshot 2 — placeholder]** Same UI, toggle set to ON, same question.
> Caption: *"Memory ON: the same question returns Lakshmi's usual 5kg bag,
> her delivery preference, and the grinder follow-up."*

> **[Screenshot 3 — placeholder]** The "What the agent remembered" side panel.
> Caption: *"The memory layer is visible: every reply lists exactly which
> memories were recalled for that turn — no black box."*

> **[Screenshot 4 — placeholder]** Terminal output of `python
> scripts/seed_storesage.py`. Caption: *"Seeding 30 days of customer history: 12
> memories retained into the demo bank."*

### Screenshot plan (capture from the running demo)

1. `storesage_app.py` running → memory **OFF** → ask "Hi, do you have atta?" → capture
   the generic reply.
2. Toggle memory **ON** → ask the same question → capture the personalized
   reply.
3. Capture the **"What the agent remembered"** panel for the ON turn, showing
   the recalled memories list.
4. Terminal: `python scripts/seed_storesage.py` output showing "retained 12
   memories into bank 'storesage-demo'".
5. (Optional) Terminal: `python scripts/memory_persistence_check.py retain` then, in a *separate*
   process, `python scripts/memory_persistence_check.py recall` — the cross-process persistence
   proof.

## One honest limitation

Our demo shows a learning curve, but the 30 days of history are **pre-seeded**,
not learned live: the "before" is an empty bank and the "after" is a bank we
loaded with Lakshmi's story in advance. The agent didn't live through those 30
days in front of you. We chose this because a real month of conversations can't
fit on stage — but it means the demo proves recall, not live learning. The fix
is one live turn: ask a new question, let the agent retain it, and watch the
*next* reply use it. That's the turn we run when anyone asks, "but does it
actually learn?"

## Why this matters

Without memory, every assistant is a stranger that happens to know prices.
With memory, it's the shopkeeper with ten years of customer relationships —
the one who sets aside your usual bag before you ask. That transformation took
three lines of agent logic and a memory system doing the heavy lifting. The
code is public; the demo runs with zero signup. Memory isn't a feature of this
assistant. It *is* the assistant.

---

### Personalizing per member (names TBD)

This is the flagship article — one shared spine every team member adapts:

- **Member A — the builder's angle:** lead with the code (the
  recall → chat → retain loop, the `MemoryBank` module), your own debugging
  anecdote, and what the embedded self-hosted setup taught you.
- **Member B — the shopkeeper's angle:** lead with Lakshmi's story, the
  business case for small retailers, and a real shop from your own
  neighborhood as the imagined first customer.
- **Member C — the customer's angle:** lead with the feeling of being
  remembered, the before/after contrast as a user experience story, and one
  personal anecdote of a shop that knew (or forgot) you.
