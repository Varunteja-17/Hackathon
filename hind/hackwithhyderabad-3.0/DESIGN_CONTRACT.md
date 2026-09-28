# DESIGN_CONTRACT.md — StoreSage build (locked 2026-09-28)

Every worker: read this file first and follow it exactly. Non-overlapping
ownership below — do not touch another worker's files.

## Product identity (locked by SB)

- **Name:** StoreSage — "the shopkeeper that never forgets"
- **One-liner:** A WhatsApp-style assistant for small retailers that remembers
  every customer.
- **Demo persona:** Lakshmi, who runs a provisions store.
- **Seeded story (do not rename these facts):** monthly 5kg atta order,
  home-delivery preference, mixer grinder asked about when out of stock
  (Day 15) and back in stock by Day 30.
- **Demo question:** "Hi, do you have atta?"
  - Memory OFF → generic answer, zero memories recalled.
  - Memory ON → "Your usual 5kg bag? … the mixer grinder you asked about is
    back in stock." Side panel lists exactly which memories were recalled.

## Hard rules

1. **Never commit secrets.** No API keys in files or git history. `.env.example`
   only; `.env` is gitignored.
2. **The H-word ban:** everything in `content/` (article, posts, video script)
   must NOT contain the word "hackathon" anywhere — title, body, hashtags.
   Repo docs may name the event "Hack With Hyderabad 3.0".
3. **`src/` is frozen.** Nobody edits `src/` without Ruby's explicit approval.
4. Demo bank id default stays `storesage-demo`.
5. LLM defaults to the transparent stub (no key, no signup). Groq via env vars
   only when the key arrives. Never hardcode endpoints or keys.

## File ownership

| Worker | Owns | Must not touch |
|---|---|---|
| A — runtime | `scripts/` (env fixes only), all infra under `/home/hwh` | `storesage_app.py`, `README.md`, `IDEAS.md`, `content/`, `src/` |
| B — product | `storesage_app.py`, `README.md`, `IDEAS.md` | `src/`, `scripts/`, `content/` |
| C — content | `content/` (new dir) | everything else |

## Definition of done

- **A:** `hwh` user + `/home/hwh` runtime recreated; memory retain/recall
  cross-process OK; `seed_storesage.py` OK (12 memories); `storesage_demo_check.py` OFF/ON
  contrast OK; Gradio app builds as `hwh`. Report PASS/FAIL per step.
- **B:** `storesage_app.py` shows StoreSage branding + Lakshmi story; toggle and
  "What the agent remembered" panel intact; `README.md` leads with StoreSage;
  `IDEAS.md` marks StoreSage ⭐ LOCKED, others "not pursued".
- **C:** `content/storesage-article.md`, `content/storesage-social-posts.md`,
  `content/storesage-video-script.md` — all H-word-free (verify with grep); article has
  real code + before/after + exactly one honest limitation; video script has
  shots + voiceover + opening line "Meet Lakshmi…".
