"""Web, Network, GitHub, and HTTP/JSON test handlers."""

from __future__ import annotations

import ipaddress
import json
import re
from urllib.parse import quote, urlparse

from telegram import Message, Update
from telegram.ext import ContextTypes

from utils.api import (
    escape_html,
    fetch_json,
    fetch_status_code,
    safe_error_message,
    send_safe_html,
    truncate_text,
)
from utils.buttons import result_navigation_keyboard

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)
GITHUB_USER_RE = re.compile(r"^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,38})$")
GITHUB_REPO_RE = re.compile(r"^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$")


async def run_my_ip(message: Message) -> None:
    """Display public IP information of the bot host via ipapi.co."""
    try:
        d = await fetch_json("https://ipapi.co/json/")
        if not isinstance(d, dict):
            raise ValueError("Invalid response")
        reply = (
            "🌍 <b>সার্ভারের Public IP তথ্য</b>\n\n"
            f"• <b>IP:</b> <code>{escape_html(d.get('ip', 'N/A'))}</code>\n"
            f"• <b>দেশ:</b> {escape_html(d.get('country_name', 'N/A'))}\n"
            f"• <b>শহর:</b> {escape_html(d.get('city', 'N/A'))}\n"
            f"• <b>ISP / Org:</b> {escape_html(d.get('org', 'পাওয়া যায়নি'))}"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("web_network"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("web_network"),
        )


async def run_ip_info(message: Message, raw_ip: str) -> None:
    """Look up public IP details via ipwho.is."""
    ip_text = raw_ip.strip().split()[0] if raw_ip.strip() else ""
    try:
        ip_obj = ipaddress.ip_address(ip_text)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            raise ValueError("Private IP")
    except ValueError:
        await send_safe_html(
            message,
            "❌ সঠিক একটি পাবলিক IP ঠিকানা দিন। উদাহরণ: <code>/ipinfo 8.8.8.8</code>",
            reply_markup=result_navigation_keyboard("web_network"),
        )
        return

    try:
        d = await fetch_json(f"https://ipwho.is/{quote(str(ip_obj), safe='')}")
        if not isinstance(d, dict) or d.get("success") is False:
            await send_safe_html(
                message,
                "❌ এই IP ঠিকানার তথ্য পাওয়া যায়নি।",
                reply_markup=result_navigation_keyboard("web_network"),
            )
            return

        conn = d.get("connection") or {}
        tz = d.get("timezone") or {}
        reply = (
            "🔎 <b>IP Lookup ফলাফল</b>\n\n"
            f"• <b>IP:</b> <code>{escape_html(d.get('ip', ip_text))}</code>\n"
            f"• <b>ধরন:</b> {escape_html(d.get('type', 'N/A'))}\n"
            f"• <b>দেশ:</b> {escape_html(d.get('country', 'N/A'))}\n"
            f"• <b>অঞ্চল:</b> {escape_html(d.get('region', 'N/A'))}\n"
            f"• <b>শহর:</b> {escape_html(d.get('city', 'N/A'))}\n"
            f"• <b>ISP:</b> {escape_html(conn.get('isp', 'পাওয়া যায়নি'))}\n"
            f"• <b>টাইমজোন:</b> {escape_html(tz.get('id', 'N/A'))}"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("web_network"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("web_network"),
        )


async def run_dns(message: Message, raw_domain: str) -> None:
    """Query DNS-over-HTTPS via dns.google for A, AAAA, MX, TXT, NS."""
    domain = raw_domain.strip().lower().split()[0] if raw_domain.strip() else ""
    if not DOMAIN_RE.match(domain):
        await send_safe_html(
            message,
            "❌ সঠিক ডোমেইন নাম দিন। উদাহরণ: <code>/dns example.com</code>",
            reply_markup=result_navigation_keyboard("web_network"),
        )
        return

    try:
        lines = [f"🧭 <b>DNS Lookup: {escape_html(domain)}</b>\n"]
        for record_type in ("A", "AAAA", "MX", "TXT", "NS"):
            data = await fetch_json(
                "https://dns.google/resolve",
                params={"name": domain, "type": record_type},
            )
            answers = data.get("Answer") if isinstance(data, dict) else None
            if answers:
                values = ", ".join(escape_html(a.get("data", "")) for a in answers[:6])
            else:
                values = "রেকর্ড পাওয়া যায়নি"
            lines.append(f"• <b>{record_type}:</b> {values}")

        await send_safe_html(
            message,
            "\n".join(lines),
            reply_markup=result_navigation_keyboard("web_network"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("web_network"),
        )


async def run_ssl(message: Message, raw_domain: str) -> None:
    """Check SSL assessment via SSL Labs API without excessive polling."""
    domain = raw_domain.strip().lower().split()[0] if raw_domain.strip() else ""
    if not DOMAIN_RE.match(domain):
        await send_safe_html(
            message,
            "❌ সঠিক ডোমেইন নাম দিন। উদাহরণ: <code>/ssl example.com</code>",
            reply_markup=result_navigation_keyboard("web_network"),
        )
        return

    try:
        data = await fetch_json(
            "https://api.ssllabs.com/api/v3/analyze",
            params={"host": domain, "publish": "off", "fromCache": "on"},
        )
        if not isinstance(data, dict):
            raise ValueError("Invalid SSL Labs response")

        status = str(data.get("status", "UNKNOWN"))
        endpoints = data.get("endpoints") or []

        if status in ("IN_PROGRESS", "DNS"):
            reply = (
                f"🔐 <b>SSL Checker: {escape_html(domain)}</b>\n\n"
                f"• <b>SSL Assessment Status:</b> <code>{escape_html(status)}</code>\n"
                "⏳ SSL Labs বিশ্লেষণ এখনো চলছে (IN_PROGRESS)। "
                "অনুগ্রহ করে ১-২ মিনিট পরে আবার <code>/ssl</code> কমান্ডটি চালান।"
            )
        elif status == "ERROR":
            reply = (
                f"🔐 <b>SSL Checker: {escape_html(domain)}</b>\n\n"
                f"• <b>Status:</b> <code>ERROR</code>\n"
                f"⚠️ বিস্তারিত: {escape_html(data.get('statusMessage', 'বিশ্লেষণ ব্যর্থ হয়েছে'))}"
            )
        else:
            if endpoints:
                ep_lines = []
                for ep in endpoints[:4]:
                    grade = escape_html(ep.get("grade", "N/A"))
                    ep_status = escape_html(ep.get("statusMessage", "N/A"))
                    ip_addr = escape_html(ep.get("ipAddress", ""))
                    ep_lines.append(f"  - {ip_addr}: Grade <b>{grade}</b> ({ep_status})")
                endpoints_text = "\n".join(ep_lines)
            else:
                endpoints_text = "  - এখনো কোনো গ্রেড পাওয়া যায়নি"

            reply = (
                f"🔐 <b>SSL Checker: {escape_html(domain)}</b>\n\n"
                f"• <b>Assessment Status:</b> <code>{escape_html(status)}</code>\n"
                f"• <b>Host / Endpoints:</b>\n{endpoints_text}"
            )

        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("web_network"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("web_network"),
        )


def _is_valid_public_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False
    host = parsed.hostname or ""
    if host in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
        return False
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        if "." not in host:
            return False
    return True


async def run_short_url(message: Message, raw_url: str) -> None:
    """Shorten a validated HTTP/HTTPS URL using is.gd."""
    url = raw_url.strip()
    if not url or len(url) > 1000 or not _is_valid_public_url(url):
        await send_safe_html(
            message,
            "❌ সঠিক একটি পাবলিক URL দিন (http:// বা https:// সহ)।\n"
            "উদাহরণ: <code>/short https://example.com</code>",
            reply_markup=result_navigation_keyboard("web_network"),
        )
        return

    try:
        data = await fetch_json(
            "https://is.gd/create.php",
            params={"format": "json", "url": url},
        )
        short_url = data.get("shorturl") if isinstance(data, dict) else None
        if not short_url:
            err_msg = data.get("errormessage") if isinstance(data, dict) else None
            await send_safe_html(
                message,
                f"⚠️ লিংক ছোট করা যায়নি: {escape_html(err_msg or 'অবৈধ লিংক')}",
                reply_markup=result_navigation_keyboard("web_network"),
            )
            return

        reply = (
            "🔗 <b>ছোট লিংক তৈরি হয়েছে</b>\n\n"
            f"• <b>মূল লিংক:</b> {escape_html(truncate_text(url, 120))}\n"
            f"• <b>ছোট লিংক:</b> {escape_html(short_url)}"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("web_network"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("web_network"),
        )


async def run_github_user(message: Message, raw_username: str) -> None:
    """Fetch public GitHub user profile."""
    username = raw_username.strip().lstrip("@")
    if not GITHUB_USER_RE.match(username):
        await send_safe_html(
            message,
            "❌ সঠিক GitHub ইউজারনেম দিন। উদাহরণ: <code>/github octocat</code>",
            reply_markup=result_navigation_keyboard("web_network"),
        )
        return

    try:
        d = await fetch_json(f"https://api.github.com/users/{quote(username, safe='')}")
        if not isinstance(d, dict):
            raise ValueError("Invalid GitHub user response")

        reply = (
            "🐙 <b>GitHub ব্যবহারকারীর তথ্য</b>\n\n"
            f"• <b>ইউজারনেম:</b> <code>{escape_html(d.get('login', username))}</code>\n"
            f"• <b>নাম:</b> {escape_html(d.get('name') or 'দেওয়া নেই')}\n"
            f"• <b>বায়ো:</b> {escape_html(d.get('bio') or 'দেওয়া নেই')}\n"
            f"• <b>পাবলিক রিপোজিটরি:</b> {escape_html(d.get('public_repos', 0))}\n"
            f"• <b>ফলোয়ার:</b> {escape_html(d.get('followers', 0))}\n"
            f"• <b>প্রোফাইল:</b> {escape_html(d.get('html_url', ''))}"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("web_network"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("web_network"),
        )


async def run_github_repo(message: Message, raw_repo: str) -> None:
    """Fetch public GitHub repository metadata."""
    repo = raw_repo.strip()
    if not GITHUB_REPO_RE.match(repo):
        await send_safe_html(
            message,
            "❌ সঠিক ফরম্যাটে দিন: <code>/repo owner/repo</code>\n"
            "উদাহরণ: <code>/repo python/cpython</code>",
            reply_markup=result_navigation_keyboard("web_network"),
        )
        return

    owner, name = repo.split("/", 1)
    try:
        d = await fetch_json(
            f"https://api.github.com/repos/{quote(owner, safe='')}/{quote(name, safe='')}"
        )
        if not isinstance(d, dict):
            raise ValueError("Invalid GitHub repo response")

        reply = (
            "📦 <b>GitHub রিপোজিটরি তথ্য</b>\n\n"
            f"• <b>নাম:</b> <code>{escape_html(d.get('full_name', repo))}</code>\n"
            f"• <b>বিবরণ:</b> {escape_html(truncate_text(d.get('description') or 'দেওয়া নেই', 300))}\n"
            f"• <b>Stars:</b> ⭐ {escape_html(d.get('stargazers_count', 0))}\n"
            f"• <b>Forks:</b> 🍴 {escape_html(d.get('forks_count', 0))}\n"
            f"• <b>ভাষা:</b> {escape_html(d.get('language') or 'N/A')}\n"
            f"• <b>লিংক:</b> {escape_html(d.get('html_url', ''))}"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("web_network"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("web_network"),
        )


async def run_http_test(message: Message, raw_code: str) -> None:
    """Safely test an HTTP status code via httpbin.org/status/<code>."""
    code_text = raw_code.strip() or "200"
    if not code_text.isdigit():
        await send_safe_html(
            message,
            "❌ শুধুমাত্র ৩ ডিজিটের HTTP স্ট্যাটাস কোড দিন (100–599)। উদাহরণ: <code>/http 200</code>",
            reply_markup=result_navigation_keyboard("web_network"),
        )
        return

    code = int(code_text)
    if not 100 <= code <= 599:
        await send_safe_html(
            message,
            "❌ স্ট্যাটাস কোড অবশ্যই 100 থেকে 599 এর মধ্যে হতে হবে।",
            reply_markup=result_navigation_keyboard("web_network"),
        )
        return

    try:
        status_code, reason = await fetch_status_code(f"https://httpbin.org/status/{code}")
        reply = (
            "🌐 <b>HTTP Status Test (httpbin.org)</b>\n\n"
            f"• <b>অনুরোধকৃত কোড:</b> <code>{code}</code>\n"
            f"• <b>প্রাপ্ত স্ট্যাটাস:</b> <code>{status_code} {escape_html(reason)}</code>"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("web_network"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("web_network"),
        )


async def run_json_test(message: Message) -> None:
    """Fetch formatted demo JSON from jsonplaceholder."""
    try:
        data = await fetch_json("https://jsonplaceholder.typicode.com/todos/1")
        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        reply = (
            "🧪 <b>JSON Test ফলাফল</b>\n\n"
            f"<pre>{escape_html(formatted)}</pre>"
        )
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("web_network"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("web_network"),
        )


async def cmd_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_my_ip(update.effective_message)


async def cmd_ipinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_ip_info(update.effective_message, " ".join(context.args))


async def cmd_dns(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_dns(update.effective_message, " ".join(context.args))


async def cmd_ssl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_ssl(update.effective_message, " ".join(context.args))


async def cmd_short(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_short_url(update.effective_message, " ".join(context.args))


async def cmd_github(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_github_user(update.effective_message, " ".join(context.args))


async def cmd_repo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_github_repo(update.effective_message, " ".join(context.args))


async def cmd_http(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_http_test(update.effective_message, " ".join(context.args))


async def cmd_json(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_json_test(update.effective_message)
