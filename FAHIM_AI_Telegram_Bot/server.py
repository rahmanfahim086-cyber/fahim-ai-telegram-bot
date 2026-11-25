"""Flask web health server plus single-instance background Telegram polling bot."""

from __future__ import annotations

import asyncio
import logging
import os
import threading
from typing import Any

from dotenv import load_dotenv
from flask import Flask, jsonify

from bot import run_bot_in_background

load_dotenv()

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("fahim_ai.server")

app = Flask(__name__)

_bot_lock = threading.Lock()
_bot_thread: threading.Thread | None = None
_bot_state: dict[str, Any] = {
    "running": False,
    "error": None,
}


def _bot_worker() -> None:
    """Dedicated thread entrypoint creating an isolated asyncio event loop."""
    try:
        asyncio.run(run_bot_in_background(_bot_state))
    except Exception as exc:
        _bot_state["running"] = False
        # Store only exception class/safe message, never secrets
        _bot_state["error"] = str(exc)
        logger.error("Telegram bot background thread stopped: %s", exc)


def ensure_bot_started() -> None:
    """Start the Telegram bot background thread at most once."""
    global _bot_thread
    with _bot_lock:
        if _bot_thread is not None and _bot_thread.is_alive():
            return
        _bot_state["error"] = None
        _bot_thread = threading.Thread(
            target=_bot_worker,
            name="fahim-ai-telegram-bot",
            daemon=True,
        )
        _bot_thread.start()


def is_bot_healthy() -> bool:
    """True only if the background thread is alive and polling without crash."""
    return (
        _bot_thread is not None
        and _bot_thread.is_alive()
        and bool(_bot_state.get("running"))
        and _bot_state.get("error") is None
    )


@app.get("/")
def index():
    """Root route required by Render health check."""
    return "FAHIM AI Bot is running", 200


@app.get("/healthz")
def healthz():
    """Accurate health check reflecting real Telegram bot thread state."""
    if is_bot_healthy():
        return jsonify({"status": "healthy", "bot_running": True}), 200
    return (
        jsonify(
            {
                "status": "unhealthy",
                "bot_running": False,
                "error": _bot_state.get("error") or "Bot polling is not active",
            }
        ),
        503,
    )


ensure_bot_started()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
