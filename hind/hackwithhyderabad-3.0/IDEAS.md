# Project Ideas — Hack With Hyderabad 3.0

> **Status:** ⭐ **StoreSage — LOCKED (selected 2026-09-28).**
> RepRecall and IncidentMind are **not pursued**. All three descriptions are
> kept below for the record.

Theme: **"AI Agents That Learn Using Hindsight"** — every team must build with
Hindsight (persistent agent memory). Memory is 25% of the judging: the demo must
SHOW the agent visibly improving via memory (interaction 1 generic → interaction
5 personalized). No student ideas (tutors, quiz bots). Real business workflows only.

---

## ⭐ LOCKED (selected 2026-09-28): StoreSage — the shopkeeper that never forgets

**The real business problem.** Small retailers run their business on WhatsApp.
The same questions arrive daily ("do you have X?", "what time do you close?"),
and every customer interaction starts from zero: the shopkeeper (or their
helper) doesn't remember what you bought last month, your size, your brand
preference, or that you asked about an out-of-stock item two weeks ago.
Repeat customers get treated like strangers. Follow-ups don't happen.

**Who would pay for it.** Local retailers, kirana/electronics/apparel shops,
D2C sellers on WhatsApp — ₹2,000–4,000/month ($25–50) for a WhatsApp assistant
that answers repeat questions and remembers customers. This is also directly
sellable to the prospects on our own outreach call sheet.

**How memory is the star (not a side feature).** The entire product IS memory:
- Day 1: customer asks "do you have whole wheat atta?" → generic answer with price.
- Day 30: same customer asks again → "Your usual 5kg bag? The brand you bought
  last month just got a fresh batch — want me to set one aside?"
- The agent recalls past purchases, brand/size preferences, pending requests
  ("you asked about the mixer grinder when it was out of stock — it's back"),
  and builds per-customer observations over time (budget-conscious, prefers
  home delivery, buys monthly).
- Without Hindsight it is a FAQ bot. With Hindsight it is a shopkeeper with
  10 years of customer relationships.

**The 60-second demo story.** "Meet Lakshmi, who runs a provisions store. Watch
her WhatsApp assistant on Day 1: polite, generic. Now watch Day 30 with the same
customer — it remembers her last order, her brand, and the item she asked about
three weeks ago. Same question, completely different answer. That's not a
chatbot. That's memory."

---

## Idea 2: RepRecall — the sales assistant that remembers every objection *(not pursued)*

**The real business problem.** Sales reps lose deals because context dies between
touches. Objections raised on call 1 ("budget frozen till Q2", "we use
competitor X") live in scattered notes or nowhere. Follow-ups go out generic,
prospects feel unheard, deals stall.

**Who would pay for it.** SMB sales teams, agencies, founders doing sales —
$50/user/month is the standard seat price for sales tooling.

**How memory is the star.** Every call/email summary is retained per prospect.
Before the next touch, the agent recalls: objections raised, competitor mentions,
personal details, what messaging worked on *similar* prospects. Draft 1 (no
memory): "Just bumping this up!" Draft 5 (with memory): references the Q2 budget
unfreeze, counters the competitor-X objection with the angle that won a similar
deal last month. Observations consolidate: "this prospect responds to ROI
framing, not feature lists."

**The 60-second demo story.** "Priya said on call 1 she's worried about price.
It's now call 3. Watch the agent brief the rep BEFORE the call — and draft the
follow-up AFTER — using everything Priya ever said. Generic CRM notes could
never do this."

---

## Idea 3: IncidentMind — on-call copilot with institutional memory *(not pursued)*

**The real business problem.** On-call engineers re-solve the same incidents.
Runbooks go stale, postmortems rot in docs nobody reads, and the engineer who
fixed it last time is asleep. Tribal knowledge evaporates with attrition.

**Who would pay for it.** Startups and SMBs with small ops teams who can't afford
a dedicated SRE function — priced per incident volume or per seat.

**How memory is the star.** Every incident (symptoms, diagnosis, fix, resolver)
is retained. When a new alert fires, the agent recalls similar past incidents
and proposes the fix that worked last time — with evidence quotes. Incident 1:
generic troubleshooting checklist. Incident 10: "This matches the Redis memory
spike from March 12 — same error signature, same 3 AM pattern. Here's the exact
fix that resolved it in 11 minutes." Observations consolidate into living
runbooks: "database failovers on this cluster usually need the connection pool
drain first."

**The 60-second demo story.** "2 AM. Pager fires: elevated 500s on checkout.
Watch the copilot skip the generic checklist and go straight to the fix —
because it remembers the last three times this happened."

---

## Why StoreSage is recommended

1. **Most visceral demo.** Judges FEEL memory when an agent remembers a
   customer's last order. Incident timelines and sales objections are strong but
   abstract; a shopkeeper remembering you is instant.
2. **Clearest payer.** Every judge knows a shop that would buy this.
3. **Real continuity.** It doubles as a product SB can sell to the Hyderabad
   businesses already on his call sheet — the hackathon project becomes
   pipeline, not a weekend toy.
4. **Fits the scaffold.** The idea-agnostic core (memory abstraction + chat UI +
   before/after seed script) maps 1:1 onto StoreSage with zero rework.
