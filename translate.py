from telegram import Update
from telegram.ext import ContextTypes
from utils.api import get_json, safe_error

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _translate(update, context, "en|bn")
async def translate_bn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _translate(update, context, "bn|en")
async def _translate(update, context, pair):
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("অনুবাদের লেখা দিন। উদাহরণ: /tr Hello")
        return
    try:
        data = await get_json("https://api.mymemory.translated.net/get", {"q": text, "langpair": pair})
        result = data.get("responseData", {}).get("translatedText")
        if not result:
            raise ValueError("empty translation")
        await update.effective_message.reply_text(f"🌐 <b>অনুবাদ</b>\n\n{result}", parse_mode="HTML")
    except Exception as exc:
        await update.effective_message.reply_text("⚠️ " + safe_error(exc))
