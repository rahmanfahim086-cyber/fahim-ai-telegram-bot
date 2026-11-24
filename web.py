import socket, ssl, asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.api import get_json, safe_error

async def my_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        d = await get_json("https://ipapi.co/json/")
        await update.effective_message.reply_text(
            f"🌍 <b>আপনার Public IP</b>\nIP: {d.get('ip','N/A')}\nদেশ: {d.get('country_name','N/A')}\nশহর: {d.get('city','N/A')}\nISP: {d.get('org','N/A')}", parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def ip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ip = context.args[0] if context.args else ""
    if not ip: await update.effective_message.reply_text("ব্যবহার: /ipinfo 8.8.8.8"); return
    try:
        d = await get_json(f"https://ipwho.is/{ip}")
        if not d.get("success", True): raise ValueError()
        await update.effective_message.reply_text(f"🔎 <b>IP তথ্য</b>\nIP: {d.get('ip')}\nদেশ: {d.get('country')}\nশহর: {d.get('city')}\nঅঞ্চল: {d.get('region')}\nISP: {d.get('connection',{}).get('isp','N/A')}", parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def dns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    domain = context.args[0].strip() if context.args else ""
    if not domain: await update.effective_message.reply_text("ব্যবহার: /dns example.com"); return
    try:
        chunks = []
        for typ in ("A","AAAA","MX","TXT","NS"):
            data = await get_json("https://dns.google/resolve", {"name":domain,"type":typ})
            answers = data.get("Answer", [])
            chunks.append(f"<b>{typ}</b>: " + (", ".join(a.get("data","") for a in answers[:8]) if answers else "রেকর্ড পাওয়া যায়নি"))
        await update.effective_message.reply_text("🧭 <b>DNS Lookup: "+domain+"</b>\n\n"+"\n".join(chunks), parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def ssl_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    domain = context.args[0].strip() if context.args else ""
    if not domain: await update.effective_message.reply_text("ব্যবহার: /ssl example.com"); return
    try:
        d = await get_json("https://api.ssllabs.com/api/v3/analyze", {"host":domain,"publish":"off","all":"done"})
        endpoints = d.get("endpoints", [])
        grades = ", ".join(f"{e.get('grade','N/A')} ({e.get('statusMessage','')})" for e in endpoints) or "পরীক্ষা চলছে বা ফলাফল এখনো পাওয়া যায়নি"
        await update.effective_message.reply_text(f"🔐 <b>SSL Labs: {domain}</b>\nStatus: {d.get('status','N/A')}\nফলাফল: {grades}\n\nSSL Labs-এর বিশ্লেষণে কয়েক মিনিট লাগতে পারে।", parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def shorten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = " ".join(context.args).strip()
    if not url: await update.effective_message.reply_text("ব্যবহার: /short https://example.com"); return
    try:
        d = await get_json("https://is.gd/create.php", {"format":"json","url":url})
        if "shorturl" not in d: raise ValueError()
        await update.effective_message.reply_text("🔗 ছোট লিংক:\n"+d["shorturl"], disable_web_page_preview=True)
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))
