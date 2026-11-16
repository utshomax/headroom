"""ChatGPT Codex backend endpoint formulas.

``CHATGPT_TARGET_API_URL`` points Codex's ChatGPT-subscription traffic at another backend, such as a gateway that
passes it on to chatgpt.com (like ``OPENAI_TARGET_API_URL`` does for API-key traffic). Its ``/backend-api/...``
paths are kept, and the WebSocket URL follows the same host (``https`` → ``wss``, ``http`` → ``ws``).
"""

from __future__ import annotations

import os


def _ws(base: str) -> str:
    if base.startswith("https://"):
        return "wss://" + base[len("https://") :]
    if base.startswith("http://"):
        return "ws://" + base[len("http://") :]
    return base


CHATGPT_BACKEND_API_URL = (
    (os.environ.get("CHATGPT_TARGET_API_URL") or "https://chatgpt.com").strip().rstrip("/")
)
CHATGPT_BACKEND_WS_URL = _ws(CHATGPT_BACKEND_API_URL)
CODEX_BACKEND_PREFIX = "/backend-api/codex"


def chatgpt_backend_url(path: str, query: str = "") -> str:
    """Return a ChatGPT HTTPS backend URL for an absolute backend path."""
    url = f"{CHATGPT_BACKEND_API_URL}{path}"
    if query:
        return f"{url}?{query}"
    return url


def codex_backend_url(path: str, query: str = "") -> str:
    """Return a ChatGPT HTTPS backend URL under `/backend-api/codex`."""
    path_suffix = path if path.startswith("/") else f"/{path}"
    return chatgpt_backend_url(f"{CODEX_BACKEND_PREFIX}{path_suffix}", query)


def codex_backend_ws_url(path: str = "") -> str:
    """Return a ChatGPT WebSocket backend URL under `/backend-api/codex`."""
    path_suffix = path if not path or path.startswith("/") else f"/{path}"
    return f"{CHATGPT_BACKEND_WS_URL}{CODEX_BACKEND_PREFIX}{path_suffix}"
