"""Translation handlers (English <-> Bengali) using MyMemory public API."""

from __future__ import annotations

from telegram import Message, Update
from telegram.ext import ContextTypes

from utils.api import escape_html, fetch_json, safe_error_message, send_safe_html
from utils.buttons import result_navigation_keyboard

MAX_TRANSLATE_LENGTH = 500


async def run_translate(message: Message, raw_text: str, pair: str) -> None:
    """Shared translation action used by both commands and inline buttons."""
    text = raw_text.strip()
    if not text:
        example = "/tr Hello" if pair == "en|bn" else "/trbn কেমন আছেন"
        await send_safe_html(
            message,
            f"❌ অনুবাদের জন্য লেখা দিন। উদাহরণ: <code>{example}</code>",
            reply_markup=result_navigation_keyboard("translate_study"),
        )
        return

    if len(text) > MAX_TRANSLATE_LENGTH:
        await send_safe_html(
            message,
            f"❌ অনুবাদের লেখা সর্বোচ্চ {MAX_TRANSLATE_LENGTH} অক্ষরের মধ্যে হতে হবে।",
            reply_markup=result_navigation_keyboard("translate_study"),
        )
        return

    try:
        data = await fetch_json(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": pair},
        )
        response_data = data.get("responseData") if isinstance(data, dict) else None
        translated = response_data.get("translatedText") if isinstance(response_data, dict) else None
        if not translated:
            await send_safe_html(
                message,
                "⚠️ অনুবাদ পাওয়া যায়নি। অন্য লেখা দিয়ে চেষ্টা করুন।",
                reply_markup=result_navigation_keyboard("translate_study"),
            )
            return

        direction_label = "ইংরেজি → বাংলা" if pair == "en|bn" else "বাংলা → ইংরেজি"
        reply = (
            f"🌐 <b>অনুবাদ ({direction_label})</b>\n\n"
            f"<b>মূল লেখা:</b>\n{escape_html(text)}\n\n"
            f"<b>অনুবাদিত ফলাফল:</b>\n{escape_html(translated)}"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("translate_study"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("translate_study"),
        )


async def cmd_tr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_translate(update.effective_message, " ".join(context.args), "en|bn")


async def cmd_trbn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_translate(update.effective_message, " ".join(context.args), "bn|en")
