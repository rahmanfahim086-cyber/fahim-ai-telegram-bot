"""Flask health endpoint plus Telegram polling bot in a background thread."""
import os
import threading
import logging
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
_bot_thread = None

@app.get("/")
def health():
    return jsonify({"status":"ok","service":"FAHIM AI Bot is running"}), 200

@app.get("/healthz")
def healthz():
    return jsonify({"status":"healthy"}), 200

def start_bot():
    # Python 3.11 does not automatically create an event loop in a new thread.
    import asyncio
    from dotenv import load_dotenv
    load_dotenv()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    from bot import main
    try:
        main()
    finally:
        if not loop.is_closed():
            loop.close()

def ensure_bot_started():
    global _bot_thread
    if _bot_thread is None or not _bot_thread.is_alive():
        _bot_thread = threading.Thread(target=start_bot, name="telegram-bot", daemon=True)
        _bot_thread.start()

ensure_bot_started()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
