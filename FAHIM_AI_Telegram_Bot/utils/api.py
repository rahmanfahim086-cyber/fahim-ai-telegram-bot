"""Shared asynchronous HTTP client and Telegram message safety helpers."""

from __future__ import annotations

import html
import logging
from typing import Any

import httpx
from telegram import InlineKeyboardMarkup, Message
from telegram.error import BadRequest, RetryAfter, TelegramError

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=10.0)
DEFAULT_HEADERS = {
    "User-Agent": "FAHIM-AI-Telegram-Bot/1.0 (+https://github.com/rahmanfahim086-cyber)",
    "Accept": "application/json",
}
MAX_TELEGRAM_TEXT_LENGTH = 4000


class ApiRequestError(Exception):
    """Raised when an external API fails or returns invalid data."""

    def __init__(self, user_message: str, detail: str = "") -> None:
        super().__init__(detail or user_message)
        self.user_message = user_message


def escape_html(value: Any) -> str:
    """Safely escape any dynamic or API-provided value for Telegram HTML."""
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def truncate_text(text: str, limit: int = 350) -> str:
    """Truncate long text cleanly with ellipsis."""
    cleaned = " ".join(text.split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: max(0, limit - 1)].rstrip() + "…"


async def fetch_json(
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 30.0,
) -> Any:
    """Perform an async GET request and return validated JSON."""
    req_headers = dict(DEFAULT_HEADERS)
    if headers:
        req_headers.update(headers)

    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(timeout, connect=10.0),
            follow_redirects=True,
        ) as client:
            response = await client.get(url, params=params, headers=req_headers)
    except httpx.TimeoutException as exc:
        logger.warning("HTTP timeout for %s: %s", url, exc)
        raise ApiRequestError(
            "⚠️ সার্ভার থেকে উত্তর আসতে বেশি সময় লাগছে। একটু পরে আবার চেষ্টা করুন।"
        ) from exc
    except httpx.RequestError as exc:
        logger.warning("HTTP request error for %s: %s", url, exc.__class__.__name__)
        raise ApiRequestError(
            "⚠️ নেটওয়ার্ক সমস্যার কারণে API-এর সাথে সংযোগ করা যায়নি।"
        ) from exc

    if response.status_code == 429:
        raise ApiRequestError(
            "⚠️ API-এর লিমিট (Rate Limit) অতিক্রম হয়েছে। অনুগ্রহ করে কিছুক্ষণ পরে চেষ্টা করুন।"
        )
    if response.status_code == 404:
        raise ApiRequestError("❌ দুঃখিত, আপনার অনুরোধকৃত তথ্যটি খুঁজে পাওয়া যায়নি।")
    if response.status_code >= 400:
        raise ApiRequestError(
            f"⚠️ API থেকে ত্রুটি পাওয়া গেছে (HTTP {response.status_code})। পরে আবার চেষ্টা করুন।"
        )

    try:
        return response.json()
    except ValueError as exc:
        logger.warning("Invalid JSON returned from %s", url)
        raise ApiRequestError(
            "⚠️ API থেকে সঠিক ফরম্যাটে তথ্য পাওয়া যায়নি।"
        ) from exc


async def fetch_bytes(
    url: str,
    params: dict[str, Any] | None = None,
    expected_content_prefix: str | None = None,
    timeout: float = 30.0,
) -> tuple[bytes, str]:
    """Perform an async GET request and return raw bytes plus content-type."""
    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(timeout, connect=10.0),
            follow_redirects=True,
        ) as client:
            response = await client.get(url, params=params, headers=DEFAULT_HEADERS)
    except httpx.TimeoutException as exc:
        raise ApiRequestError(
            "⚠️ ফাইল বা ছবি ডাউনলোড করতে বেশি সময় লাগছে। পরে আবার চেষ্টা করুন।"
        ) from exc
    except httpx.RequestError as exc:
        raise ApiRequestError(
            "⚠️ নেটওয়ার্ক সমস্যার কারণে ডাটা আনা যায়নি।"
        ) from exc

    if response.status_code == 429:
        raise ApiRequestError("⚠️ API Rate Limit পূর্ণ হয়েছে। কিছুক্ষণ পরে চেষ্টা করুন।")
    if response.status_code >= 400:
        raise ApiRequestError(
            f"⚠️ সার্ভার থেকে ফাইল আনা যায়নি (HTTP {response.status_code})।"
        )

    content_type = response.headers.get("content-type", "")
    if expected_content_prefix and expected_content_prefix not in content_type.lower():
        raise ApiRequestError("⚠️ সার্ভার থেকে প্রত্যাশিত ফরম্যাটের ফাইল পাওয়া যায়নি।")

    return response.content, content_type


async def fetch_status_code(url: str, timeout: float = 30.0) -> tuple[int, str]:
    """Perform a safe GET request strictly for httpbin status testing."""
    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(timeout, connect=10.0),
            follow_redirects=False,
        ) as client:
            response = await client.get(url, headers=DEFAULT_HEADERS)
            return response.status_code, response.reason_phrase or ""
    except httpx.TimeoutException as exc:
        raise ApiRequestError(
            "⚠️ HTTP টেস্টে টাইমআউট হয়েছে। পরে আবার চেষ্টা করুন।"
        ) from exc
    except httpx.RequestError as exc:
        raise ApiRequestError(
            "⚠️ HTTP টেস্ট সার্ভারের সাথে সংযোগ করা যায়নি।"
        ) from exc


def safe_error_message(exc: Exception) -> str:
    """Return a clean Bengali error message for any exception."""
    if isinstance(exc, ApiRequestError):
        return exc.user_message
    return "⚠️ দুঃখিত, API থেকে তথ্য পাওয়া যায়নি। একটু পরে আবার চেষ্টা করুন।"


def split_telegram_message(text: str, max_len: int = MAX_TELEGRAM_TEXT_LENGTH) -> list[str]:
    """Split long text into Telegram-safe chunks."""
    if len(text) <= max_len:
        return [text]
    chunks: list[str] = []
    remaining = text
    while len(remaining) > max_len:
        split_at = remaining.rfind("\n", 0, max_len)
        if split_at <= 0:
            split_at = max_len
        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip("\n")
    if remaining:
        chunks.append(remaining)
    return chunks


async def send_safe_html(
    message: Message,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    disable_web_page_preview: bool = True,
) -> None:
    """Send HTML text safely, handling Telegram limits, BadRequest, and RetryAfter."""
    chunks = split_telegram_message(text)
    for idx, chunk in enumerate(chunks):
        markup = reply_markup if idx == len(chunks) - 1 else None
        try:
            await message.reply_text(
                chunk,
                parse_mode="HTML",
                reply_markup=markup,
                disable_web_page_preview=disable_web_page_preview,
            )
        except RetryAfter as exc:
            logger.warning("Telegram rate limit hit: retry after %s", exc.retry_after)
            raise ApiRequestError(
                "⚠️ টেলিগ্রামের মেসেজ সীমা অতিক্রম হয়েছে। কয়েক সেকেন্ড পরে চেষ্টা করুন।"
            ) from exc
        except BadRequest as exc:
            logger.warning("Telegram BadRequest on HTML send: %s", exc)
            plain = html.unescape(chunk)
            await message.reply_text(
                plain[:MAX_TELEGRAM_TEXT_LENGTH],
                reply_markup=markup,
                disable_web_page_preview=disable_web_page_preview,
            )
        except TelegramError as exc:
            logger.warning("TelegramError on send: %s", exc)
            raise
