"""Finance & Crypto handlers: currency converter and CoinGecko prices."""

from __future__ import annotations

from telegram import Message, Update
from telegram.ext import ContextTypes

from utils.api import escape_html, fetch_json, safe_error_message, send_safe_html
from utils.buttons import result_navigation_keyboard

SUPPORTED_COINS = {
    "btc": "bitcoin",
    "bitcoin": "bitcoin",
    "eth": "ethereum",
    "ethereum": "ethereum",
}


async def run_currency(message: Message, raw_args: str) -> None:
    """Convert currencies using open.er-api.com."""
    parts = raw_args.strip().split()
    if len(parts) != 3:
        await send_safe_html(
            message,
            "❌ সঠিক ফরম্যাটে দিন: <code>/currency পরিমাণ FROM TO</code>\n"
            "উদাহরণ: <code>/currency 100 USD BDT</code>",
            reply_markup=result_navigation_keyboard("finance_crypto"),
        )
        return

    amount_raw, from_curr, to_curr = parts[0], parts[1].upper(), parts[2].upper()
    try:
        amount = float(amount_raw)
        if amount < 0 or amount > 1e12:
            raise ValueError("Out of bounds")
    except ValueError:
        await send_safe_html(
            message,
            "❌ সঠিক সংখ্যার পরিমাণ দিন। উদাহরণ: <code>100 USD BDT</code>",
            reply_markup=result_navigation_keyboard("finance_crypto"),
        )
        return

    if not (from_curr.isalpha() and len(from_curr) == 3 and to_curr.isalpha() and len(to_curr) == 3):
        await send_safe_html(
            message,
            "❌ সঠিক ৩ অক্ষরের মুদ্রা কোড দিন (যেমন: USD, BDT, EUR)।",
            reply_markup=result_navigation_keyboard("finance_crypto"),
        )
        return

    try:
        data = await fetch_json("https://open.er-api.com/v6/latest/USD")
        rates = data.get("rates") if isinstance(data, dict) else None
        if not isinstance(rates, dict):
            raise ValueError("Invalid exchange rate data")

        if from_curr not in rates or to_curr not in rates:
            await send_safe_html(
                message,
                f"❌ দুঃখিত, <b>{escape_html(from_curr)}</b> বা <b>{escape_html(to_curr)}</b> মুদ্রাটি সমর্থিত নয়।",
                reply_markup=result_navigation_keyboard("finance_crypto"),
            )
            return

        usd_amount = amount / float(rates[from_curr])
        converted = usd_amount * float(rates[to_curr])
        unit_rate = float(rates[to_curr]) / float(rates[from_curr])

        reply = (
            "💱 <b>মুদ্রা রূপান্তর (Currency Converter)</b>\n\n"
            f"• <b>পরিমাণ:</b> {amount:,.2f} {escape_html(from_curr)}\n"
            f"• <b>রূপান্তরিত মান:</b> <b>{converted:,.2f} {escape_html(to_curr)}</b>\n"
            f"• <b>রেট:</b> 1 {escape_html(from_curr)} = {unit_rate:,.4f} {escape_html(to_curr)}\n"
            f"• <b>হালনাগাদ:</b> {escape_html(data.get('time_last_update_utc', 'N/A'))}"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("finance_crypto"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("finance_crypto"),
        )


async def run_crypto(message: Message, raw_coin: str) -> None:
    """Fetch Bitcoin and/or Ethereum prices in USD and BDT via CoinGecko."""
    coin_input = raw_coin.strip().lower()
    if coin_input and coin_input not in SUPPORTED_COINS and coin_input != "all":
        await send_safe_html(
            message,
            "❌ বর্তমানে শুধু <code>bitcoin</code> (btc) এবং <code>ethereum</code> (eth) সমর্থিত।\n"
            "উদাহরণ: <code>/crypto bitcoin</code>",
            reply_markup=result_navigation_keyboard("finance_crypto"),
        )
        return

    try:
        data = await fetch_json(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "bitcoin,ethereum", "vs_currencies": "usd,bdt"},
        )
        if not isinstance(data, dict):
            raise ValueError("Invalid CoinGecko data")

        target_ids = (
            [SUPPORTED_COINS[coin_input]]
            if coin_input in SUPPORTED_COINS
            else ["bitcoin", "ethereum"]
        )
        lines = ["🪙 <b>ক্রিপ্টোকারেন্সি বাজারদর</b>\n"]
        for coin_id in target_ids:
            info = data.get(coin_id) or {}
            usd = info.get("usd")
            bdt = info.get("bdt")
            usd_str = f"${usd:,.2f}" if isinstance(usd, (int, float)) else "পাওয়া যায়নি"
            bdt_str = f"৳{bdt:,.2f}" if isinstance(bdt, (int, float)) else "পাওয়া যায়নি"
            lines.append(
                f"<b>{escape_html(coin_id.capitalize())}</b>\n"
                f"• USD: {escape_html(usd_str)}\n"
                f"• BDT: {escape_html(bdt_str)}\n"
            )

        await send_safe_html(
            message,
            "\n".join(lines),
            reply_markup=result_navigation_keyboard("finance_crypto"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("finance_crypto"),
        )


async def cmd_currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_currency(update.effective_message, " ".join(context.args))


async def cmd_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_crypto(update.effective_message, " ".join(context.args))
