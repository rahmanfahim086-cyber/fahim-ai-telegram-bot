from telegram import Update
from telegram.ext import ContextTypes
from utils.api import get_json, safe_error

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args).strip()
    if not city:
        await update.effective_message.reply_text("শহরের নাম দিন। উদাহরণ: /weather Rangpur"); return
    try:
        geo = await get_json("https://geocoding-api.open-meteo.com/v1/search", {"name": city, "count": 1, "language": "en", "format": "json"})
        results = geo.get("results", [])
        if not results:
            await update.effective_message.reply_text("এই শহরটি খুঁজে পাওয়া যায়নি।"); return
        place = results[0]
        data = await get_json("https://api.open-meteo.com/v1/forecast", {
            "latitude": place["latitude"], "longitude": place["longitude"], "current_weather": "true"
        })
        cw = data.get("current_weather", {})
        await update.effective_message.reply_text(
            f"⛅ <b>{place.get('name')}, {place.get('country','')}</b>\n"
            f"🌡️ তাপমাত্রা: {cw.get('temperature','N/A')}°C\n"
            f"💨 বাতাসের গতি: {cw.get('windspeed','N/A')} km/h\n"
            f"🧭 বাতাসের দিক: {cw.get('winddirection','N/A')}°\n"
            f"🕒 পর্যবেক্ষণের সময়: {cw.get('time','N/A')}", parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))
