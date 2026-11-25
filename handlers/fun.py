"""Entertainment and miscellaneous public info handlers."""

from __future__ import annotations

from urllib.parse import quote

from telegram import Message, Update
from telegram.ext import ContextTypes

from utils.api import (
    escape_html,
    fetch_bytes,
    fetch_json,
    safe_error_message,
    send_safe_html,
    truncate_text,
)
from utils.buttons import result_navigation_keyboard


async def run_joke(message: Message) -> None:
    """Fetch a random joke from official-joke-api."""
    try:
        d = await fetch_json("https://official-joke-api.appspot.com/random_joke")
        if not isinstance(d, dict):
            raise ValueError("Invalid joke response")
        reply = (
            "😂 <b>র‍্যান্ডম জোক</b>\n\n"
            f"❓ {escape_html(d.get('setup', ''))}\n\n"
            f"👉 <b>{escape_html(d.get('punchline', ''))}</b>"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("entertainment"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("entertainment"),
        )


async def run_quote(message: Message) -> None:
    """Fetch a motivational quote from zenquotes.io."""
    try:
        data = await fetch_json("https://zenquotes.io/api/random")
        item = data[0] if isinstance(data, list) and data else {}
        quote_text = item.get("q") or "Stay focused and keep learning."
        author = item.get("a") or "Unknown"
        reply = (
            "💡 <b>অনুপ্রেরণামূলক উক্তি</b>\n\n"
            f"“{escape_html(quote_text)}”\n\n"
            f"— <i>{escape_html(author)}</i>"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("entertainment"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("entertainment"),
        )


async def run_fact(message: Message) -> None:
    """Fetch a random interesting fact from uselessfacts.jsph.pl."""
    try:
        d = await fetch_json("https://uselessfacts.jsph.pl/api/v2/facts/random")
        if not isinstance(d, dict) or not d.get("text"):
            raise ValueError("Invalid fact response")
        reply = (
            "🧠 <b>মজার তথ্য (Random Fact)</b>\n\n"
            f"{escape_html(d['text'])}"
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


async def run_advice(message: Message) -> None:
    """Fetch random advice from api.adviceslip.com."""
    try:
        d = await fetch_json("https://api.adviceslip.com/advice")
        slip = d.get("slip") if isinstance(d, dict) else None
        advice = slip.get("advice") if isinstance(slip, dict) else None
        if not advice:
            raise ValueError("Missing advice")
        reply = f"🧭 <b>আজকের পরামর্শ</b>\n\n“{escape_html(advice)}”"
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


async def run_cat(message: Message) -> None:
    """Fetch and send a random cat image from TheCatAPI."""
    try:
        data = await fetch_json("https://api.thecatapi.com/v1/images/search")
        img_url = data[0].get("url") if isinstance(data, list) and data else None
        if not img_url:
            raise ValueError("Missing cat image URL")
        content, _ = await fetch_bytes(img_url, expected_content_prefix="image")
        await message.reply_photo(
            photo=content,
            caption="🐱 কিউট বিড়ালের ছবি!",
            reply_markup=result_navigation_keyboard("entertainment"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("entertainment"),
        )


async def run_dog(message: Message) -> None:
    """Fetch and send a random dog image from dog.ceo."""
    try:
        data = await fetch_json("https://dog.ceo/api/breeds/image/random")
        img_url = data.get("message") if isinstance(data, dict) else None
        if not img_url:
            raise ValueError("Missing dog image URL")
        content, _ = await fetch_bytes(img_url, expected_content_prefix="image")
        await message.reply_photo(
            photo=content,
            caption="🐶 কিউট কুকুরের ছবি!",
            reply_markup=result_navigation_keyboard("entertainment"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("entertainment"),
        )


async def run_anime(message: Message, raw_name: str) -> None:
    """Search anime information via Jikan API."""
    name = raw_name.strip()
    if not name or len(name) > 120:
        await send_safe_html(
            message,
            "❌ Anime-এর নাম লিখুন। উদাহরণ: <code>/anime Naruto</code>",
            reply_markup=result_navigation_keyboard("entertainment"),
        )
        return

    try:
        res = await fetch_json("https://api.jikan.moe/v4/anime", params={"q": name, "limit": 1})
        items = res.get("data") if isinstance(res, dict) else None
        if not items:
            await send_safe_html(
                message,
                "❌ এই নামে কোনো Anime খুঁজে পাওয়া যায়নি।",
                reply_markup=result_navigation_keyboard("entertainment"),
            )
            return

        anime = items[0]
        title = anime.get("title", name)
        score = anime.get("score", "N/A")
        episodes = anime.get("episodes", "N/A")
        synopsis = truncate_text(anime.get("synopsis") or "বিবরণ পাওয়া যায়নি।", 500)
        url = anime.get("url", "")
        img_url = (anime.get("images") or {}).get("jpg", {}).get("image_url")

        caption = (
            f"🎌 <b>{escape_html(title)}</b>\n\n"
            f"• <b>স্কোর:</b> ⭐ {escape_html(score)}\n"
            f"• <b>পর্ব (Episodes):</b> {escape_html(episodes)}\n"
            f"• <b>সংক্ষেপ:</b> {escape_html(synopsis)}"
        )
        if url:
            caption += f"\n• <b>তথ্য লিংক:</b> {escape_html(url)}"

        if img_url:
            try:
                content, _ = await fetch_bytes(img_url, expected_content_prefix="image")
                await message.reply_photo(
                    photo=content,
                    caption=caption[:1000],
                    parse_mode="HTML",
                    reply_markup=result_navigation_keyboard("entertainment"),
                )
                return
            except Exception:
                pass

        await send_safe_html(
            message,
            caption,
            reply_markup=result_navigation_keyboard("entertainment"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("entertainment"),
        )


async def run_manga(message: Message, raw_name: str) -> None:
    """Search manga information via Jikan API."""
    name = raw_name.strip()
    if not name or len(name) > 120:
        await send_safe_html(
            message,
            "❌ Manga-এর নাম লিখুন। উদাহরণ: <code>/manga One Piece</code>",
            reply_markup=result_navigation_keyboard("entertainment"),
        )
        return

    try:
        res = await fetch_json("https://api.jikan.moe/v4/manga", params={"q": name, "limit": 1})
        items = res.get("data") if isinstance(res, dict) else None
        if not items:
            await send_safe_html(
                message,
                "❌ এই নামে কোনো Manga খুঁজে পাওয়া যায়নি।",
                reply_markup=result_navigation_keyboard("entertainment"),
            )
            return

        manga = items[0]
        title = manga.get("title", name)
        score = manga.get("score", "N/A")
        chapters = manga.get("chapters", "চলমান / N/A")
        status = manga.get("status", "N/A")
        synopsis = truncate_text(manga.get("synopsis") or "বিবরণ পাওয়া যায়নি।", 500)
        url = manga.get("url", "")

        reply = (
            f"📖 <b>{escape_html(title)}</b>\n\n"
            f"• <b>স্কোর:</b> ⭐ {escape_html(score)}\n"
            f"• <b>চ্যাপ্টার:</b> {escape_html(chapters)}\n"
            f"• <b>অবস্থা:</b> {escape_html(status)}\n"
            f"• <b>সংক্ষেপ:</b> {escape_html(synopsis)}"
        )
        if url:
            reply += f"\n• <b>তথ্য লিংক:</b> {escape_html(url)}"

        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("entertainment"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("entertainment"),
        )


async def run_pokemon(message: Message, raw_name: str) -> None:
    """Fetch Pokemon details via PokeAPI."""
    name = raw_name.strip().lower()
    if not name or len(name) > 60:
        await send_safe_html(
            message,
            "❌ Pokemon-এর নাম দিন। উদাহরণ: <code>/pokemon pikachu</code>",
            reply_markup=result_navigation_keyboard("entertainment"),
        )
        return

    try:
        d = await fetch_json(f"https://pokeapi.co/api/v2/pokemon/{quote(name, safe='')}")
        if not isinstance(d, dict):
            raise ValueError("Invalid PokeAPI response")

        types = ", ".join(t["type"]["name"] for t in (d.get("types") or [])) or "N/A"
        stats_lines = [
            f"{s['stat']['name']}: {s['base_stat']}"
            for s in (d.get("stats") or [])[:6]
        ]
        img_url = (
            (d.get("sprites") or {})
            .get("other", {})
            .get("official-artwork", {})
            .get("front_default")
            or (d.get("sprites") or {}).get("front_default")
        )
        caption = (
            f"⚡ <b>Pokemon: {escape_html(str(d.get('name', name)).capitalize())}</b>\n\n"
            f"• <b>ধরন (Type):</b> {escape_html(types)}\n"
            f"• <b>উচ্চতা:</b> {escape_html(d.get('height', 'N/A'))}\n"
            f"• <b>ওজন:</b> {escape_html(d.get('weight', 'N/A'))}\n"
            f"• <b>স্ট্যাটস:</b> {escape_html(', '.join(stats_lines))}"
        )

        if img_url:
            try:
                content, _ = await fetch_bytes(img_url, expected_content_prefix="image")
                await message.reply_photo(
                    photo=content,
                    caption=caption[:1000],
                    parse_mode="HTML",
                    reply_markup=result_navigation_keyboard("entertainment"),
                )
                return
            except Exception:
                pass

        await send_safe_html(
            message,
            caption,
            reply_markup=result_navigation_keyboard("entertainment"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("entertainment"),
        )


async def run_demo_user(message: Message) -> None:
    """Fetch a fake demo user profile from randomuser.me for testing only."""
    try:
        res = await fetch_json("https://randomuser.me/api/")
        results = res.get("results") if isinstance(res, dict) else None
        if not results:
            raise ValueError("Missing demo user")

        u = results[0]
        name = u.get("name") or {}
        loc = u.get("location") or {}
        full_name = f"{name.get('first', '')} {name.get('last', '')}".strip()

        reply = (
            "👤 <b>ডেমো ব্যবহারকারীর তথ্য (শুধুমাত্র টেস্টিংয়ের জন্য ভুয়া/ডামি ডাটা)</b>\n\n"
            f"• <b>নাম:</b> {escape_html(full_name or 'N/A')}\n"
            f"• <b>লিঙ্গ:</b> {escape_html(u.get('gender', 'N/A'))}\n"
            f"• <b>ইমেইল (Demo):</b> <code>{escape_html(u.get('email', 'N/A'))}</code>\n"
            f"• <b>দেশ:</b> {escape_html(loc.get('country', 'N/A'))}\n"
            f"• <b>শহর:</b> {escape_html(loc.get('city', 'N/A'))}\n\n"
            "ℹ️ এটি একটি কাল্পনিক/ডেমো প্রোফাইল (Fake Test Data)।"
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


async def cmd_joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_joke(update.effective_message)


async def cmd_quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_quote(update.effective_message)


async def cmd_fact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_fact(update.effective_message)


async def cmd_advice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_advice(update.effective_message)


async def cmd_cat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_cat(update.effective_message)


async def cmd_dog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_dog(update.effective_message)


async def cmd_anime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_anime(update.effective_message, " ".join(context.args))


async def cmd_manga(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_manga(update.effective_message, " ".join(context.args))


async def cmd_pokemon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_pokemon(update.effective_message, " ".join(context.args))


async def cmd_demo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_demo_user(update.effective_message)
