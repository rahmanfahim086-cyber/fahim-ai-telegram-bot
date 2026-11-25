"""Study handlers: English dictionary and Bengali/English Wikipedia."""

from __future__ import annotations

from urllib.parse import quote

from telegram import Message, Update
from telegram.ext import ContextTypes

from utils.api import escape_html, fetch_json, safe_error_message, send_safe_html, truncate_text
from utils.buttons import result_navigation_keyboard


async def run_define(message: Message, raw_word: str) -> None:
    """Look up an English word via Free Dictionary API."""
    word = raw_word.strip()
    if not word or len(word) > 80:
        await send_safe_html(
            message,
            "❌ সঠিক একটি ইংরেজি শব্দ দিন। উদাহরণ: <code>/define beautiful</code>",
            reply_markup=result_navigation_keyboard("translate_study"),
        )
        return

    try:
        data = await fetch_json(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{quote(word, safe='')}"
        )
        if not isinstance(data, list) or not data:
            await send_safe_html(
                message,
                "❌ শব্দটির অর্থ পাওয়া যায়নি।",
                reply_markup=result_navigation_keyboard("translate_study"),
            )
            return

        entry = data[0]
        phonetic = entry.get("phonetic")
        if not phonetic:
            for p in entry.get("phonetics", []) or []:
                if isinstance(p, dict) and p.get("text"):
                    phonetic = p["text"]
                    break

        lines = [
            f"📖 <b>{escape_html(entry.get('word', word))}</b>",
            f"🔊 <b>উচ্চারণ:</b> {escape_html(phonetic or 'পাওয়া যায়নি')}",
        ]
        for meaning in (entry.get("meanings") or [])[:3]:
            pos = meaning.get("partOfSpeech", "")
            lines.append(f"\n<b>{escape_html(pos)}</b>")
            for definition in (meaning.get("definitions") or [])[:2]:
                lines.append(f"• {escape_html(definition.get('definition', ''))}")
                example = definition.get("example")
                if example:
                    lines.append(f"  <i>উদাহরণ: {escape_html(example)}</i>")

        await send_safe_html(
            message,
            "\n".join(lines),
            reply_markup=result_navigation_keyboard("translate_study"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("translate_study"),
        )


async def run_wiki(message: Message, raw_topic: str, lang: str = "bn") -> None:
    """Fetch a Wikipedia summary in Bengali or English."""
    topic = raw_topic.strip()
    if not topic or len(topic) > 150:
        cmd_name = "/wiki" if lang == "bn" else "/wikien"
        await send_safe_html(
            message,
            f"❌ অনুসন্ধানের বিষয় লিখুন। উদাহরণ: <code>{cmd_name} বাংলাদেশ</code>",
            reply_markup=result_navigation_keyboard("translate_study"),
        )
        return

    try:
        slug = quote(topic.replace(" ", "_"), safe="")
        data = await fetch_json(
            f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{slug}"
        )
        if not isinstance(data, dict):
            raise ValueError("Invalid Wikipedia response")

        title = escape_html(data.get("title", topic))
        extract = escape_html(truncate_text(data.get("extract") or "তথ্য পাওয়া যায়নি।", 1500))
        page_url = data.get("content_urls", {}).get("desktop", {}).get("page")

        lang_label = "বাংলা উইকিপিডিয়া" if lang == "bn" else "English Wikipedia"
        text = f"📚 <b>{title}</b> ({lang_label})\n\n{extract}"
        if page_url:
            text += f"\n\n🔗 বিস্তারিত: {escape_html(page_url)}"

        await send_safe_html(
            message,
            text,
            reply_markup=result_navigation_keyboard("translate_study"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("translate_study"),
        )


async def cmd_define(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_define(update.effective_message, " ".join(context.args))


async def cmd_wiki(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_wiki(update.effective_message, " ".join(context.args), lang="bn")


async def cmd_wikien(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_wiki(update.effective_message, " ".join(context.args), lang="en")
