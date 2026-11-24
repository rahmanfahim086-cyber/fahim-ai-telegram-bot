from urllib.parse import quote
from telegram import Update
from telegram.ext import ContextTypes
from utils.api import get_json, safe_error

async def define(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = " ".join(context.args).strip()
    if not word:
        await update.effective_message.reply_text("শব্দ দিন। উদাহরণ: /define beautiful"); return
    try:
        data = await get_json(f"https://api.dictionaryapi.dev/api/v2/entries/en/{quote(word)}")
        entry = data[0]
        phon = entry.get("phonetic", "পাওয়া যায়নি")
        lines = [f"📖 <b>{entry.get('word', word)}</b>", f"উচ্চারণ: {phon}"]
        for meaning in entry.get("meanings", [])[:3]:
            lines.append(f"\n<b>{meaning.get('partOfSpeech','')}</b>")
            for d in meaning.get("definitions", [])[:2]:
                lines.append("• " + d.get("definition", ""))
                if d.get("example"): lines.append("উদাহরণ: " + d["example"])
        await update.effective_message.reply_text("\n".join(lines)[:4000], parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _wiki(update, context, "bn")
async def wikien(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _wiki(update, context, "en")
async def _wiki(update, context, lang):
    topic = " ".join(context.args).strip()
    if not topic:
        await update.effective_message.reply_text("বিষয় লিখুন।"); return
    try:
        data = await get_json(f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(topic.replace(' ','_'))}")
        text = f"📚 <b>{data.get('title', topic)}</b>\n\n{data.get('extract','তথ্য পাওয়া যায়নি')}"
        if data.get("content_urls", {}).get("desktop", {}).get("page"):
            text += "\n\n" + data["content_urls"]["desktop"]["page"]
        await update.effective_message.reply_text(text[:4000], parse_mode="HTML", disable_web_page_preview=True)
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))
