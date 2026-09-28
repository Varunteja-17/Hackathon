"""Configuration — everything via environment variables (see .env.example)."""

import os


def _sanitize_no_proxy() -> None:
    """Sandbox quirk: NO_PROXY ships bare IPv6 literals (e.g. ``::1``) which
    break httpx's proxy parsing (``httpx.InvalidURL``) on import inside
    gradio/huggingface_hub. Keep only entries httpx can parse; localhost
    bypasses the proxy either way."""
    for var in ("no_proxy", "NO_PROXY"):
        val = os.environ.get(var)
        if not val:
            continue
        keep = [
            p.strip()
            for p in val.split(",")
            if p.strip() and ("." in p or p.strip() == "localhost")
        ]
        os.environ[var] = ",".join(keep) or "localhost,127.0.0.1"


_sanitize_no_proxy()


def get(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


# Agent's own LLM (OpenAI-compatible)
LLM_BASE_URL = get("LLM_BASE_URL", "https://api.groq.com/openai/v1")
LLM_API_KEY = get("LLM_API_KEY", "")
LLM_MODEL = get("LLM_MODEL", "qwen/qwen3-32b")

# Hindsight memory layer
HINDSIGHT_MODE = get("HINDSIGHT_MODE", "embedded")  # embedded | server
HINDSIGHT_URL = get("HINDSIGHT_URL", "http://localhost:8888")
HINDSIGHT_LLM_PROVIDER = get("HINDSIGHT_LLM_PROVIDER", "llamacpp")
HINDSIGHT_LLM_MODEL = get("HINDSIGHT_LLM_MODEL", "")
HINDSIGHT_LLM_API_KEY = get("HINDSIGHT_LLM_API_KEY", "")

BANK_ID = get("BANK_ID", "shopmind-demo")
