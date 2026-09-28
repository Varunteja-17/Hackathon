"""Gradio demo UI — StoreSage, the shopkeeper that never forgets.

The whole pitch in one screen:
  - chat with the agent
  - MEMORY ON/OFF toggle -> the before/after contrast judges score
  - "What the agent remembered" panel -> makes the memory layer VISIBLE

Run:
    python storesage_app.py
Then open the printed URL. Use scripts/seed_storesage.py first for the full story.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))
os.environ.setdefault("BANK_ID", "storesage-demo")
os.environ.setdefault("HINDSIGHT_LLM_PROVIDER", "none")

import src.config  # noqa: F401 — must come first: sanitizes proxy env for httpx
import gradio as gr  # noqa: E402

from src.agent import Agent  # noqa: E402
from src.memory import MemoryBank  # noqa: E402  (imported for side-effect: env sanitizing)

STORESAGE_BANK_ID = os.environ["BANK_ID"]


def create_storesage_agent(memory_on: bool) -> Agent:
    return Agent(bank_id=STORESAGE_BANK_ID, memory_enabled=memory_on)


storesage_memory_agent = create_storesage_agent(True)
storesage_baseline_agent = create_storesage_agent(False)


def storesage_chat_handler(message: str, chat_history: list, memory_on: bool):
    selected_agent = storesage_memory_agent if memory_on else storesage_baseline_agent
    turn_result = selected_agent.respond(message)
    chat_history = chat_history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": turn_result.reply},
    ]
    if turn_result.memories_used:
        memory_markdown = "\n".join(f"- {memory}" for memory in turn_result.memories_used)
    else:
        memory_markdown = "_No memories recalled (memory off or bank empty)._"
    status_text = (
        f"Memory: **{'ON' if turn_result.memory_enabled else 'OFF'}** · "
        f"recalled **{len(turn_result.memories_used)}** memories · "
        f"LLM: `{selected_agent.llm.name}`"
    )
    return chat_history, memory_markdown, status_text


def reset_storesage_bank():
    # Fresh bank id each reset keeps the demo reproducible.
    global storesage_memory_agent, storesage_baseline_agent
    import time

    new_bank = f"{STORESAGE_BANK_ID}-reset-{int(time.time())}"
    os.environ["BANK_ID"] = new_bank
    storesage_memory_agent = Agent(bank_id=new_bank, memory_enabled=True)
    storesage_baseline_agent = Agent(bank_id=new_bank, memory_enabled=False)
    return [], "_Bank reset. Seed it again with scripts/seed_storesage.py._", ""


with gr.Blocks(title="StoreSage — the shopkeeper that never forgets") as storesage_ui:
    gr.Markdown(
        """# StoreSage — the shopkeeper that never forgets 🛒
        Meet **Lakshmi**: her provisions store runs on WhatsApp. On Day 1 the
        assistant is polite but generic — by Day 30 it remembers her usual 5kg
        atta, her home-delivery preference, and the mixer grinder she asked
        about when it was out of stock. Flip the **Memory** switch and ask the
        *same* question: OFF gets you a stranger, ON gets you a regular."""
    )
    with gr.Row():
        storesage_memory_toggle = gr.Checkbox(label="Memory ON", value=True)
        storesage_reset_button = gr.Button("Reset bank", variant="secondary")
    storesage_status_panel = gr.Markdown("")
    with gr.Row():
        storesage_chat_panel = gr.Chatbot(label="Chat", height=420)
        storesage_memory_inspector = gr.Markdown(label="What the agent remembered")
    storesage_message_input = gr.Textbox(label="Your message", placeholder="Hi, do you have atta?")

    def submit_storesage_message(message, chat_history, memory_on):
        chat_history, memory_markdown, status_text = storesage_chat_handler(
            message, chat_history, memory_on
        )
        return chat_history, memory_markdown, status_text, ""

    storesage_message_input.submit(
        submit_storesage_message,
        [storesage_message_input, storesage_chat_panel, storesage_memory_toggle],
        [storesage_chat_panel, storesage_memory_inspector, storesage_status_panel, storesage_message_input],
    )
    storesage_reset_button.click(
        reset_storesage_bank,
        None,
        [storesage_chat_panel, storesage_memory_inspector, storesage_status_panel],
    )

if __name__ == "__main__":
    storesage_ui.launch(server_name="127.0.0.1", server_port=7860)
