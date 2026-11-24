from telegram import Update
from telegram.ext import ContextTypes
from utils.api import get_json, safe_error

async def currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.effective_message.reply_text("ব্যবহার: /currency 100 USD BDT"); return
    try:
        amount, source, target = float(context.args[0]), context.args[1].upper(), context.args[2].upper()
        if amount < 0: raise ValueError()
        data = await get_json("https://open.er-api.com/v6/latest/USD")
        rates = data.get("rates", {})
        if source not in rates or target not in rates: raise ValueError()
        result = amount / rates[source] * rates[target]
        await update.effective_message.reply_text(f"💱 {amount:g} {source} = <b>{result:,.4f} {target}</b>\nরেটের তারিখ: {data.get('time_last_update_utc','N/A')}", parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ মুদ্রার কোড/পরিমাণ পরীক্ষা করুন। " + safe_error(exc))

async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = (context.args[0].lower() if context.args else "bitcoin")
    aliases = {"btc":"bitcoin", "eth":"ethereum"}
    coin = aliases.get(coin, coin)
    if coin not in ("bitcoin", "ethereum"):
        await update.effective_message.reply_text("এই সংস্করণে bitcoin অথবা ethereum ব্যবহার করুন।"); return
    try:
        data = await get_json("https://api.coingecko.com/api/v3/simple/price", {"ids":"bitcoin,ethereum","vs_currencies":"usd,bdt"})
        item = data[coin]
        await update.effective_message.reply_text(f"🪙 <b>{coin.title()}</b>\nUSD: ${item['usd']:,.2f}\nBDT: ৳{item['bdt']:,.2f}", parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))
