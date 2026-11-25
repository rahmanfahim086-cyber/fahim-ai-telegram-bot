"""Main Telegram bot application for FAHIM AI - All-in-One Telegram Bot."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from typing import Any

from dotenv import load_dotenv
from telegram import BotCommand, Message, Update
from telegram.constants import ChatAction
from telegram.error import BadRequest, NetworkError, RetryAfter, TelegramError
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from handlers.finance import cmd_crypto, cmd_currency, run_crypto, run_currency
from handlers.fun import (
    cmd_advice,
    cmd_anime,
    cmd_cat,
    cmd_demo,
    cmd_dog,
    cmd_fact,
    cmd_joke,
    cmd_manga,
    cmd_pokemon,
    cmd_quote,
    run_advice,
    run_anime,
    run_cat,
    run_demo_user,
    run_dog,
    run_fact,
    run_joke,
    run_manga,
    run_pokemon,
    run_quote,
)
from handlers.study import cmd_define, cmd_wiki, cmd_wikien, run_define, run_wiki
from handlers.tools import (
    cmd_b64,
    cmd_bin,
    cmd_calc,
    cmd_md5,
    cmd_password,
    cmd_qr,
    cmd_sha256,
    cmd_sha512,
    cmd_unb64,
    cmd_unbin,
    cmd_urldecode,
    cmd_urlencode,
    cmd_uuid,
    run_local_tool,
    run_qr,
)
from handlers.translate import cmd_tr, cmd_trbn, run_translate
from handlers.web import (
    cmd_dns,
    cmd_github,
    cmd_http,
    cmd_ip,
    cmd_ipinfo,
    cmd_json,
    cmd_repo,
    cmd_short,
    cmd_ssl,
    run_dns,
    run_github_repo,
    run_github_user,
    run_http_test,
    run_ip_info,
    run_json_test,
    run_my_ip,
    run_short_url,
    run_ssl,
)
from handlers.weather import cmd_time, cmd_weather, run_bangladesh_time, run_weather
from utils.api import send_safe_html
from utils.buttons import (
    FEATURE_SUBMENU_MAP,
    SUBMENU_KEYBOARD_MAP,
    bot_info_keyboard,
    main_menu_keyboard,
    prompt_cancel_keyboard,
    result_navigation_keyboard,
)
from utils.messages import (
    ABOUT_MESSAGE,
    CANCEL_MESSAGE,
    FEATURE_INPUT_PROMPTS,
    HELP_MESSAGE,
    LOADING_MESSAGE,
    MAIN_MENU_MESSAGE,
    SUBMENU_MESSAGES,
    WELCOME_MESSAGE,
    build_status_message,
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
# Prevent httpx from logging full Telegram Bot API URLs that contain BOT_TOKEN
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

logger = logging.getLogger("fahim_ai.bot")

PENDING_TTL_SECONDS = 600  # 10 minutes
BOT_START_TIME = time.monotonic()

BOT_COMMANDS: list[BotCommand] = [
    BotCommand("start", "বট শুরু করুন ও মূল মেনু দেখুন"),
    BotCommand("help", "ব্যবহার নির্দেশিকা দেখুন"),
    BotCommand("menu", "প্রধান মেনু খুলুন"),
    BotCommand("about", "বট সম্পর্কে জানুন"),
    BotCommand("status", "বটের বর্তমান অবস্থা দেখুন"),
    BotCommand("tr", "ইংরেজি থেকে বাংলা অনুবাদ"),
    BotCommand("trbn", "বাংলা থেকে ইংরেজি অনুবাদ"),
    BotCommand("define", "ইংরেজি শব্দের অর্থ ও উচ্চারণ"),
    BotCommand("weather", "শহরের বর্তমান আবহাওয়া"),
    BotCommand("currency", "মুদ্রা রূপান্তর (যেমন: 100 USD BDT)"),
    BotCommand("crypto", "Bitcoin ও Ethereum বাজারদর"),
    BotCommand("ip", "সার্ভারের Public IP দেখুন"),
    BotCommand("ipinfo", "পাবলিক IP ঠিকানার তথ্য"),
    BotCommand("dns", "ডোমেইনের DNS রেকর্ড দেখুন"),
    BotCommand("ssl", "SSL সার্টিফিকেট পরীক্ষা"),
    BotCommand("qr", "QR কোড তৈরি করুন"),
    BotCommand("short", "বড় লিংক ছোট করুন"),
    BotCommand("wiki", "বাংলা উইকিপিডিয়া সারাংশ"),
    BotCommand("wikien", "ইংরেজি উইকিপিডিয়া সারাংশ"),
    BotCommand("github", "GitHub ব্যবহারকারীর তথ্য"),
    BotCommand("repo", "GitHub রিপোজিটরির তথ্য"),
    BotCommand("joke", "র‍্যান্ডম জোক"),
    BotCommand("quote", "অনুপ্রেরণামূলক উক্তি"),
    BotCommand("fact", "মজার তথ্য"),
    BotCommand("advice", "আজকের পরামর্শ"),
    BotCommand("cat", "বিড়ালের ছবি"),
    BotCommand("dog", "কুকুরের ছবি"),
    BotCommand("anime", "Anime খুঁজুন"),
    BotCommand("manga", "Manga খুঁজুন"),
    BotCommand("pokemon", "Pokemon তথ্য দেখুন"),
    BotCommand("time", "বাংলাদেশের বর্তমান সময়"),
    BotCommand("demo", "ডেমো ব্যবহারকারীর তথ্য"),
    BotCommand("http", "HTTP স্ট্যাটাস কোড টেস্ট"),
    BotCommand("json", "ডেমো JSON ডাটা দেখুন"),
    BotCommand("bin", "টেক্সট থেকে বাইনারি"),
    BotCommand("unbin", "বাইনারি থেকে টেক্সট"),
    BotCommand("b64", "Base64 এনকোড"),
    BotCommand("unb64", "Base64 ডিকোড"),
    BotCommand("md5", "MD5 হ্যাশ তৈরি"),
    BotCommand("sha256", "SHA256 হ্যাশ তৈরি"),
    BotCommand("sha512", "SHA512 হ্যাশ তৈরি"),
    BotCommand("urlencode", "URL এনকোড"),
    BotCommand("urldecode", "URL ডিকোড"),
    BotCommand("password", "শক্তিশালী পাসওয়ার্ড তৈরি"),
    BotCommand("uuid", "র‍্যান্ডম UUID তৈরি"),
    BotCommand("calc", "নিরাপদ ক্যালকুলেটর"),
]


def _pending_store(context: ContextTypes.DEFAULT_TYPE) -> dict[tuple[int, int], tuple[str, float]]:
    return context.application.bot_data.setdefault("pending_inputs", {})


def _pending_key(update: Update) -> tuple[int, int] | None:
    if update.effective_chat is None or update.effective_user is None:
        return None
    return (update.effective_chat.id, update.effective_user.id)


def _clear_pending(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    key = _pending_key(update)
    if key is None:
        return False
    return _pending_store(context).pop(key, None) is not None


def _format_uptime() -> str:
    elapsed = int(max(0, time.monotonic() - BOT_START_TIME))
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{hours} ঘণ্টা {minutes} মিনিট {seconds} সেকেন্ড"


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _clear_pending(update, context)
    if update.effective_message is None:
        return
    await send_safe_html(
        update.effective_message,
        WELCOME_MESSAGE,
        reply_markup=main_menu_keyboard(),
    )


async def cmd_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _clear_pending(update, context)
    if update.effective_message is None:
        return
    await send_safe_html(
        update.effective_message,
        MAIN_MENU_MESSAGE,
        reply_markup=main_menu_keyboard(),
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _clear_pending(update, context)
    if update.effective_message is None:
        return
    await send_safe_html(
        update.effective_message,
        HELP_MESSAGE,
        reply_markup=result_navigation_keyboard("bot_info"),
    )


async def cmd_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _clear_pending(update, context)
    if update.effective_message is None:
        return
    await send_safe_html(
        update.effective_message,
        ABOUT_MESSAGE,
        reply_markup=result_navigation_keyboard("bot_info"),
    )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _clear_pending(update, context)
    if update.effective_message is None:
        return
    active_count = len(_pending_store(context))
    status_text = build_status_message(_format_uptime(), True, active_count)
    await send_safe_html(
        update.effective_message,
        status_text,
        reply_markup=result_navigation_keyboard("bot_info"),
    )


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _clear_pending(update, context)
    if update.effective_message is None:
        return
    await send_safe_html(
        update.effective_message,
        CANCEL_MESSAGE,
        reply_markup=main_menu_keyboard(),
    )


async def execute_input_feature(feature: str, message: Message, user_input: str) -> None:
    """Shared feature dispatcher invoked by pending-input message handler."""
    if feature == "tr":
        await run_translate(message, user_input, "en|bn")
    elif feature == "trbn":
        await run_translate(message, user_input, "bn|en")
    elif feature == "define":
        await run_define(message, user_input)
    elif feature == "wiki":
        await run_wiki(message, user_input, lang="bn")
    elif feature == "wikien":
        await run_wiki(message, user_input, lang="en")
    elif feature == "weather":
        await run_weather(message, user_input)
    elif feature == "currency":
        await run_currency(message, user_input)
    elif feature == "crypto":
        await run_crypto(message, user_input)
    elif feature == "ipinfo":
        await run_ip_info(message, user_input)
    elif feature == "dns":
        await run_dns(message, user_input)
    elif feature == "ssl":
        await run_ssl(message, user_input)
    elif feature == "short":
        await run_short_url(message, user_input)
    elif feature == "github":
        await run_github_user(message, user_input)
    elif feature == "repo":
        await run_github_repo(message, user_input)
    elif feature == "http":
        await run_http_test(message, user_input)
    elif feature == "qr":
        await run_qr(message, user_input)
    elif feature in {
        "bin",
        "unbin",
        "b64",
        "unb64",
        "md5",
        "sha256",
        "sha512",
        "urlencode",
        "urldecode",
        "password",
        "calc",
    }:
        await run_local_tool(message, feature, user_input)
    elif feature == "anime":
        await run_anime(message, user_input)
    elif feature == "manga":
        await run_manga(message, user_input)
    elif feature == "pokemon":
        await run_pokemon(message, user_input)
    else:
        await send_safe_html(
            message,
            "❌ অজানা ফিচার। /menu থেকে আবার চেষ্টা করুন।",
            reply_markup=main_menu_keyboard(),
        )


async def execute_instant_feature(feature: str, message: Message) -> None:
    """Shared instant-feature dispatcher for buttons that require no text input."""
    if feature == "time":
        await run_bangladesh_time(message)
    elif feature == "fact":
        await run_fact(message)
    elif feature == "advice":
        await run_advice(message)
    elif feature == "demo":
        await run_demo_user(message)
    elif feature == "ip":
        await run_my_ip(message)
    elif feature == "json":
        await run_json_test(message)
    elif feature == "uuid":
        await run_local_tool(message, "uuid", "")
    elif feature == "joke":
        await run_joke(message)
    elif feature == "quote":
        await run_quote(message)
    elif feature == "cat":
        await run_cat(message)
    elif feature == "dog":
        await run_dog(message)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all inline keyboard callbacks cleanly."""
    query = update.callback_query
    if query is None:
        return
    await query.answer()

    data = query.data or ""
    msg = query.message
    if not isinstance(msg, Message):
        return

    if data == "action:cancel":
        _clear_pending(update, context)
        await query.edit_message_text(
            CANCEL_MESSAGE,
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(),
        )
        return

    if data.startswith("menu:"):
        _clear_pending(update, context)
        menu_key = data.split(":", 1)[1]
        if menu_key == "main":
            await query.edit_message_text(
                MAIN_MENU_MESSAGE,
                parse_mode="HTML",
                reply_markup=main_menu_keyboard(),
            )
            return
        keyboard_fn = SUBMENU_KEYBOARD_MAP.get(menu_key)
        menu_text = SUBMENU_MESSAGES.get(menu_key)
        if keyboard_fn and menu_text:
            await query.edit_message_text(
                menu_text,
                parse_mode="HTML",
                reply_markup=keyboard_fn(),
            )
        return

    if data.startswith("info:"):
        _clear_pending(update, context)
        info_key = data.split(":", 1)[1]
        if info_key == "status":
            text = build_status_message(_format_uptime(), True, len(_pending_store(context)))
        elif info_key == "about":
            text = ABOUT_MESSAGE
        else:
            text = HELP_MESSAGE
        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=bot_info_keyboard(),
            disable_web_page_preview=True,
        )
        return

    if data.startswith("prompt:"):
        feature = data.split(":", 1)[1]
        prompt_text = FEATURE_INPUT_PROMPTS.get(feature)
        key = _pending_key(update)
        if prompt_text and key is not None:
            _pending_store(context)[key] = (feature, time.monotonic())
            submenu_key = FEATURE_SUBMENU_MAP.get(feature, "main")
            await query.edit_message_text(
                prompt_text,
                parse_mode="HTML",
                reply_markup=prompt_cancel_keyboard(submenu_key),
            )
        return

    if data.startswith("instant:"):
        _clear_pending(update, context)
        feature = data.split(":", 1)[1]
        try:
            await msg.chat.send_action(ChatAction.TYPING)
        except TelegramError:
            pass
        await execute_instant_feature(feature, msg)


async def handle_pending_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle plain text messages when a user has an active pending feature."""
    if update.effective_message is None or not update.effective_message.text:
        return

    key = _pending_key(update)
    if key is None:
        return

    store = _pending_store(context)
    pending = store.get(key)
    if pending is None:
        await send_safe_html(
            update.effective_message,
            "ℹ️ মেনু থেকে একটি ফিচার বেছে নিন অথবা /help লিখে কমান্ডগুলো দেখুন।",
            reply_markup=main_menu_keyboard(),
        )
        return

    feature, created_at = pending
    if time.monotonic() - created_at > PENDING_TTL_SECONDS:
        store.pop(key, None)
        await send_safe_html(
            update.effective_message,
            "⌛ ইনপুটের সময়সীমা শেষ হয়ে গেছে। অনুগ্রহ করে /menu থেকে আবার ফিচারটি নির্বাচন করুন।",
            reply_markup=main_menu_keyboard(),
        )
        return

    user_input = update.effective_message.text.strip()
    if not user_input:
        await send_safe_html(
            update.effective_message,
            "❌ খালি ইনপুট দেওয়া যাবে না। সঠিক তথ্য পাঠান অথবা /cancel লিখুন।",
        )
        return

    store.pop(key, None)
    status_msg = await update.effective_message.reply_text(LOADING_MESSAGE)
    try:
        await execute_input_feature(feature, update.effective_message, user_input)
    finally:
        try:
            await status_msg.delete()
        except TelegramError:
            pass


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler logging cleanly without leaking BOT_TOKEN."""
    err = context.error
    if isinstance(err, RetryAfter):
        logger.warning("Telegram RetryAfter: %s seconds", err.retry_after)
        return
    if isinstance(err, (NetworkError, BadRequest)):
        logger.warning("Telegram API error: %s", err)
        return
    logger.error("Unhandled bot exception: %s", err, exc_info=err)

    if isinstance(update, Update) and update.effective_message is not None:
        try:
            await update.effective_message.reply_text(
                "⚠️ একটি অপ্রত্যাশিত সমস্যা হয়েছে। একটু পরে আবার চেষ্টা করুন।"
            )
        except TelegramError:
            pass


async def post_init(application: Application) -> None:
    """Register Telegram bot commands via setMyCommands on startup."""
    try:
        await application.bot.set_my_commands(BOT_COMMANDS)
        logger.info("Registered %d bot commands via setMyCommands", len(BOT_COMMANDS))
    except TelegramError as exc:
        logger.warning("Failed to set_my_commands: %s", exc)


def load_bot_token() -> str:
    """Read and validate BOT_TOKEN from environment without exposing it."""
    load_dotenv()
    token = os.environ.get("BOT_TOKEN", "").strip()
    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN" or ":" not in token:
        raise RuntimeError(
            "BOT_TOKEN পরিবেশ ভ্যারিয়েবল সেট করা নেই বা সঠিক নয়।"
        )
    return token


def build_application(token: str) -> Application:
    """Build and configure the python-telegram-bot v21+ Application."""
    application = Application.builder().token(token).post_init(post_init).build()

    command_handlers: list[tuple[str, Any]] = [
        ("start", cmd_start),
        ("menu", cmd_menu),
        ("help", cmd_help),
        ("about", cmd_about),
        ("status", cmd_status),
        ("cancel", cmd_cancel),
        ("tr", cmd_tr),
        ("trbn", cmd_trbn),
        ("define", cmd_define),
        ("wiki", cmd_wiki),
        ("wikien", cmd_wikien),
        ("weather", cmd_weather),
        ("time", cmd_time),
        ("currency", cmd_currency),
        ("crypto", cmd_crypto),
        ("ip", cmd_ip),
        ("ipinfo", cmd_ipinfo),
        ("dns", cmd_dns),
        ("ssl", cmd_ssl),
        ("short", cmd_short),
        ("github", cmd_github),
        ("repo", cmd_repo),
        ("http", cmd_http),
        ("json", cmd_json),
        ("qr", cmd_qr),
        ("bin", cmd_bin),
        ("unbin", cmd_unbin),
        ("b64", cmd_b64),
        ("unb64", cmd_unb64),
        ("md5", cmd_md5),
        ("sha256", cmd_sha256),
        ("sha512", cmd_sha512),
        ("urlencode", cmd_urlencode),
        ("urldecode", cmd_urldecode),
        ("password", cmd_password),
        ("uuid", cmd_uuid),
        ("calc", cmd_calc),
        ("joke", cmd_joke),
        ("quote", cmd_quote),
        ("fact", cmd_fact),
        ("advice", cmd_advice),
        ("cat", cmd_cat),
        ("dog", cmd_dog),
        ("anime", cmd_anime),
        ("manga", cmd_manga),
        ("pokemon", cmd_pokemon),
        ("demo", cmd_demo),
    ]

    for cmd_name, callback in command_handlers:
        application.add_handler(CommandHandler(cmd_name, callback))

    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_pending_input)
    )
    application.add_error_handler(handle_error)
    return application


async def run_bot_in_background(
    bot_state: dict[str, Any],
    stop_event: asyncio.Event | None = None,
) -> None:
    """Async lifecycle safe for running inside a background thread."""
    token = load_bot_token()
    application = build_application(token)
    async with application:
        await post_init(application)
        await application.start()
        if application.updater is None:
            raise RuntimeError("Updater unavailable on Application")
        await application.updater.start_polling(drop_pending_updates=True)
        bot_state["running"] = True
        bot_state["error"] = None
        logger.info("FAHIM AI Telegram Bot polling started successfully.")

        waiter = stop_event or asyncio.Event()
        try:
            await waiter.wait()
        finally:
            bot_state["running"] = False
            await application.updater.stop()
            await application.stop()


def main() -> None:
    """Standalone CLI entrypoint (python bot.py)."""
    token = load_bot_token()
    application = build_application(token)
    logger.info("Starting FAHIM AI Telegram Bot in standalone polling mode...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
