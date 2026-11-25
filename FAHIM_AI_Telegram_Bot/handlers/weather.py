"""Weather and Bangladesh time handlers."""

from __future__ import annotations

from datetime import datetime

from telegram import Message, Update
from telegram.ext import ContextTypes

from utils.api import escape_html, fetch_json, safe_error_message, send_safe_html
from utils.buttons import result_navigation_keyboard

DEFAULT_CITY = "Rangpur"
DEFAULT_LAT = 25.75
DEFAULT_LON = 89.25

WMO_WEATHER_CODES = {
    0: "পরিষ্কার আকাশ ☀️",
    1: "প্রায় পরিষ্কার আকাশ 🌤️",
    2: "আংশিক মেঘলা ⛅",
    3: "মেঘলা আকাশ ☁️",
    45: "কুয়াশা 🌫️",
    48: "ঘন কুয়াশা 🌫️",
    51: "হালকা গুঁড়ি গুঁড়ি বৃষ্টি 🌦️",
    53: "মাঝারি গুঁড়ি গুঁড়ি বৃষ্টি 🌦️",
    55: "ঘন গুঁড়ি গুঁড়ি বৃষ্টি 🌧️",
    61: "হালকা বৃষ্টি 🌦️",
    63: "মাঝারি বৃষ্টি 🌧️",
    65: "ভারী বৃষ্টি 🌧️",
    71: "হালকা তুষারপাত ❄️",
    73: "মাঝারি তুষারপাত ❄️",
    75: "ভারী তুষারপাত ❄️",
    80: "হালকা বৃষ্টির ঝাপটা 🌦️",
    81: "মাঝারি বৃষ্টির ঝাপটা 🌧️",
    82: "প্রবল বৃষ্টিপাত ⛈️",
    95: "বজ্রসহ বৃষ্টি ⛈️",
    96: "বজ্রপাত ও শিলাবৃষ্টি ⛈️",
    99: "তীব্র বজ্রসহ শিলাবৃষ্টি ⛈️",
}


async def run_weather(message: Message, raw_city: str) -> None:
    """Fetch current weather using Open-Meteo geocoding + forecast APIs."""
    city = raw_city.strip()
    if len(city) > 100:
        await send_safe_html(
            message,
            "❌ শহরের নাম খুব বেশি বড়। সঠিক শহরের নাম দিন।",
            reply_markup=result_navigation_keyboard("weather_info"),
        )
        return

    try:
        if not city or city.lower() in ("default", "rangpur"):
            place_name = DEFAULT_CITY
            country = "Bangladesh"
            lat = DEFAULT_LAT
            lon = DEFAULT_LON
            used_default = not city
        else:
            geo = await fetch_json(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1, "language": "en", "format": "json"},
            )
            results = geo.get("results") if isinstance(geo, dict) else None
            if not results:
                await send_safe_html(
                    message,
                    "❌ এই শহরটি খুঁজে পাওয়া যায়নি। সঠিক শহরের ইংরেজি নাম লিখুন।",
                    reply_markup=result_navigation_keyboard("weather_info"),
                )
                return
            place = results[0]
            place_name = place.get("name") or city
            country = place.get("country") or ""
            lat = place["latitude"]
            lon = place["longitude"]
            used_default = False

        forecast = await fetch_json(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
                "timezone": "auto",
            },
        )
        cw = forecast.get("current_weather") if isinstance(forecast, dict) else None
        if not isinstance(cw, dict):
            raise ValueError("Missing current_weather")

        weather_code = cw.get("weathercode")
        condition = WMO_WEATHER_CODES.get(weather_code, "তথ্য পাওয়া গেছে 🌤️")
        day_night = "দিন ☀️" if cw.get("is_day") == 1 else "রাত 🌙"

        location_title = f"{place_name}, {country}".strip(", ")
        reply = (
            f"⛅ <b>আবহাওয়ার তথ্য: {escape_html(location_title)}</b>\n\n"
            f"• <b>অবস্থা:</b> {escape_html(condition)} ({day_night})\n"
            f"• <b>তাপমাত্রা:</b> {escape_html(cw.get('temperature', 'N/A'))}°C\n"
            f"• <b>বাতাসের গতি:</b> {escape_html(cw.get('windspeed', 'N/A'))} km/h\n"
            f"• <b>বাতাসের দিক:</b> {escape_html(cw.get('winddirection', 'N/A'))}°\n"
            f"• <b>স্থানাঙ্ক:</b> {escape_html(lat)}, {escape_html(lon)}\n"
            f"• <b>সময়:</b> {escape_html(cw.get('time', 'N/A'))}"
        )
        if used_default:
            reply += "\n\nℹ️ ডিফল্ট অবস্থান (Rangpur) দেখানো হয়েছে। অন্য শহরের জন্য <code>/weather Dhaka</code> লিখুন।"

        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("weather_info"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("weather_info"),
        )


async def run_bangladesh_time(message: Message) -> None:
    """Fetch current Bangladesh time from WorldTimeAPI."""
    try:
        data = await fetch_json("https://worldtimeapi.org/api/timezone/Asia/Dhaka")
        dt_str = data.get("datetime") if isinstance(data, dict) else None
        if not dt_str:
            raise ValueError("Missing datetime")

        parsed = datetime.fromisoformat(dt_str)
        date_text = parsed.strftime("%d %B %Y (%A)")
        time_text = parsed.strftime("%I:%M:%S %p")
        reply = (
            "🕒 <b>বাংলাদেশের বর্তমান সময়</b>\n\n"
            f"📅 <b>তারিখ:</b> {escape_html(date_text)}\n"
            f"⏰ <b>সময়:</b> {escape_html(time_text)}\n"
            f"🌏 <b>টাইমজোন:</b> {escape_html(data.get('timezone', 'Asia/Dhaka'))} "
            f"(UTC{escape_html(data.get('utc_offset', '+06:00'))})"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("weather_info"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("weather_info"),
        )


async def cmd_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_weather(update.effective_message, " ".join(context.args))


async def cmd_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_bangladesh_time(update.effective_message)
