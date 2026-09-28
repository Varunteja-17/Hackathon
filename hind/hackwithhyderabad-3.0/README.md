# StoreSage — the shopkeeper that never forgets

A WhatsApp-style assistant for small retailers that **remembers every
customer**, built on **Hindsight** (Vectorize's agent-memory system).
Every interaction is retained; every reply is grounded in recalled memories.
The demo makes the learning curve visible: flip memory OFF and the agent is
generic — flip it ON and the same question gets a personalized answer built
from weeks of history.

**Who it serves:** local retailers, kirana/electronics/apparel shops, and D2C
sellers on WhatsApp — starting with **Lakshmi's provisions store**.

Built for **Hack With Hyderabad 3.0** — *"AI Agents That Learn Using Hindsight"*.
⭐ **LOCKED as our entry — selected 2026-09-28** (see [IDEAS.md](IDEAS.md)).

## The 60-second demo

1. `python scripts/seed_storesage.py` — seeds 30 days of customer history (Lakshmi,
   her monthly atta order, home-delivery preference, a mixer grinder she asked
   about when it was out of stock).
2. `python storesage_app.py` — open the chat UI.
3. Ask **"Hi, do you have atta?"** with **Memory OFF** → generic answer.
4. Ask it again with **Memory ON** → *"Your usual 5kg bag, Lakshmi? Fresh batch
   just arrived — and the mixer grinder you asked about on Day 15 is back in
   stock."*
5. The side panel shows **exactly which memories were recalled** for each turn —
   the memory layer is visible, not a black box.

## Quickstart

### Windows PowerShell

```powershell
Copy-Item .env.example .env
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts\seed_storesage.py
python storesage_app.py
```

Open `http://127.0.0.1:7860`. The first Hindsight run may download local embedding
and reranking models.

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1. Verify retain/recall persistence across processes (no keys needed)
python scripts/memory_persistence_check.py retain
python scripts/memory_persistence_check.py recall   # separate process -> persistence proof

# 2. Seed the demo story
python scripts/seed_storesage.py

# 3. Run the demo UI
python storesage_app.py   # -> http://127.0.0.1:7860
```

Copy `.env.example` to `.env` to configure. **Never commit `.env`.**

### Bring your own LLM (optional)

Without a key, the agent runs on a transparent stub LLM — the full memory
before/after demo works with zero signup. To use a real model, set in `.env`:

```
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_API_KEY=<your key>
LLM_MODEL=qwen/qwen3.8-27b
```

Any OpenAI-compatible endpoint works (Groq, OpenAI, Ollama, LiteLLM...).
With the same key, also upgrade Hindsight's own extraction:

```
HINDSIGHT_LLM_PROVIDER=groq
HINDSIGHT_LLM_API_KEY=<your key>
HINDSIGHT_LLM_MODEL=qwen/qwen3.8-27b
# Groq free tier also needs (see .env.example):
# HINDSIGHT_API_LLM_GROQ_SERVICE_TIER=on_demand
# HINDSIGHT_API_RETAIN_MAX_COMPLETION_TOKENS=16000
```

then restart the daemon so it picks up the provider.

## How it works

```
user message
    │
    ▼
recall() ── Hindsight TEMPR search over the bank ──► relevant memories
    │                    (semantic + keyword + graph + temporal)
    ▼
LLM chat (system prompt + memories + message) ──► reply
    │
    ▼
retain() ── the exchange is stored ──► the NEXT turn is smarter
```

- `src/memory.py` — `MemoryBank`: the only module that talks to Hindsight.
  `remember()` / `recall()` / `reflect()`. Swap backends here, nowhere else.
- `src/agent.py` — idea-agnostic agent loop: recall → chat → retain.
- `src/llm.py` — OpenAI-compatible client; stub when no key is configured.
- `src/config.py` — everything via env vars.
- `scripts/memory_persistence_check.py` — minimal retain/recall + cross-process persistence proof.
- `scripts/seed_storesage.py` — seeds the 30-day learning-curve story.
- `scripts/storesage_demo_check.py` — same question with memory OFF vs ON; asserts the contrast.
- `storesage_app.py` — Gradio demo UI with memory ON/OFF toggle + memory inspector.

### Hindsight, self-hosted, zero signup

The embedded daemon (`HindsightEmbedded`) runs a background Hindsight server
shared by all Python processes — memory persists across runs with no server
to manage. Defaults are fully local:

| Piece | Default | External calls |
|---|---|---|
| Database | embedded pg0 (PostgreSQL) | none |
| Embeddings | local `bge-small-en-v1.5` | none |
| Reranker | local cross-encoder | none |
| LLM (fact extraction) | `none` — recall works, extraction degraded | none |

Set `HINDSIGHT_LLM_PROVIDER=groq` (+ key) for full fact extraction and
`reflect`; `llamacpp` for a fully local LLM (auto-downloads a ~3.5GB GGUF
on first run; needs `llama-cpp-python` installed).

> **Root limitation.** The embedded PostgreSQL refuses to `initdb` as root,
> and this VM runs as root. All runtime scripts must therefore run as the
> non-root user `hwh` (created for this project). Use the wrapper:
>
> ```
> su -m -s /bin/bash hwh -- /home/hwh/bin/run-as-hwh.sh scripts/memory_persistence_check.py retain
> ```
>
> The live runtime copy lives at `/home/hwh/hwh3` (the `hwh` user cannot
> traverse `/home/hatch`, so the repo checkout at `~/workspace/hwh3` is the
> source of truth — sync it over after changes). The daemon stores its data
> under `/home/hwh/.hindsight` and `/home/hwh/.pg0`.
>
> When the Groq key arrives: set `LLM_API_KEY` (agent's LLM) and
> `HINDSIGHT_LLM_PROVIDER=groq` + `HINDSIGHT_LLM_API_KEY` (memory extraction)
> in `.env`, then restart the daemon.

## Project ideas

See [IDEAS.md](IDEAS.md) for the full record.

- ⭐ **StoreSage — LOCKED (selected 2026-09-28):** the shopkeeper that never
  forgets — this build.
- **RepRecall** (sales assistant that remembers every objection) — not pursued.
- **IncidentMind** (on-call copilot with institutional memory) — not pursued.

## Rules of the road

- No API keys or secrets in files or git history. Ever.
- No account signups required to run the demo.
- Scan-only research; no PRs/comments on other people's repos.
