from urllib.parse import quote
from telegram import Update
from telegram.ext import ContextTypes
from utils.api import get_json, safe_error

async def random_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.effective_message.text.split()[0].split("@")[0].lstrip("/").lower()
    endpoints = {
        "joke":"https://official-joke-api.appspot.com/random_joke",
        "quote":"https://zenquotes.io/api/random",
        "fact":"https://uselessfacts.jsph.pl/api/v2/facts/random?language=en",
        "advice":"https://api.adviceslip.com/advice",
        "time":"https://worldtimeapi.org/api/timezone/Asia/Dhaka",
        "demo":"https://randomuser.me/api/",
        "json":"https://jsonplaceholder.typicode.com/todos/1",
        "http":"https://httpbin.org/status/200",
    }
    try:
        if cmd == "http":
            import httpx
            code = int(context.args[0]) if context.args else 200
            if not 100 <= code <= 599: raise ValueError()
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                response = await client.get(f"https://httpbin.org/status/{code}")
            await update.effective_message.reply_text(
                f"🌐 HTTP Test\nচাওয়া Status: {code}\nপ্রাপ্ত Status: {response.status_code}\nফলাফল: {'সফল' if response.status_code == code else 'ভিন্ন Status'}")
            return
        d = await get_json(endpoints[cmd])
        if cmd == "joke": text = "😂 <b>জোক</b>\n\n"+d.get("setup","")+"\n"+d.get("punchline","")
        elif cmd == "quote": text = "💡 <b>উক্তি</b>\n\n"+d[0].get("q","")+"\n— "+d[0].get("a","")
        elif cmd == "fact": text = "🧠 <b>আজকের তথ্য</b>\n\n"+d.get("text","")
        elif cmd == "advice": text = "🧭 <b>পরামর্শ</b>\n\n"+d.get("slip",{}).get("advice","")
        elif cmd == "time": text = "🕒 <b>বাংলাদেশের সময়</b>\n\n"+d.get("datetime","")+"\nটাইমজোন: "+d.get("timezone","Asia/Dhaka")
        elif cmd == "demo":
            u=d["results"][0]; text=f"👤 <b>Demo User (নকল তথ্য)</b>\nনাম: {u['name']['first']} {u['name']['last']}\nদেশ: {u['location']['country']}\nইমেইল: {u['email']}"
        else: text = "🧪 <b>JSON Demo</b>\n<code>"+str(d)[:3000]+"</code>"
        await update.effective_message.reply_text(text[:3900], parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def animal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.effective_message.text.split()[0].split("@")[0].lstrip("/").lower()
    try:
        if cmd == "cat": d = await get_json("https://api.thecatapi.com/v1/images/search")
        else: d = await get_json("https://dog.ceo/api/breeds/image/random")
        url = d[0]["url"] if cmd == "cat" else d["message"]
        await update.effective_message.reply_photo(url, caption="🐱 বিড়াল" if cmd=="cat" else "🐶 কুকুর")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def anime_manga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.effective_message.text.split()[0].split("@")[0].lstrip("/").lower()
    name = " ".join(context.args).strip()
    if not name: await update.effective_message.reply_text(f"নাম লিখুন। উদাহরণ: /{cmd} Naruto"); return
    try:
        d = await get_json(f"https://api.jikan.moe/v4/{cmd}", {"q":name,"limit":3})
        items=d.get("data",[])
        if not items: await update.effective_message.reply_text("কোনো ফলাফল পাওয়া যায়নি।"); return
        lines=[]
        for x in items:
            lines.append(f"🎌 <b>{x.get('title','N/A')}</b>\nস্কোর: {x.get('score','N/A')} | পর্ব/অধ্যায়: {x.get('episodes',x.get('chapters','N/A'))}\n{x.get('synopsis','')[:500]}")
        await update.effective_message.reply_text("\n\n".join(lines)[:3900], parse_mode="HTML")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def pokemon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = " ".join(context.args).strip().lower()
    if not name: await update.effective_message.reply_text("ব্যবহার: /pokemon pikachu"); return
    try:
        d=await get_json(f"https://pokeapi.co/api/v2/pokemon/{quote(name)}")
        types=", ".join(x["type"]["name"] for x in d["types"])
        stats=", ".join(f"{x['stat']['name']}: {x['base_stat']}" for x in d["stats"])
        await update.effective_message.reply_photo(d["sprites"]["front_default"], caption=f"⚡ {d['name'].title()}\nType: {types}\n{stats}")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def github(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.effective_message.text.split()[0].split("@")[0].lstrip("/").lower()
    arg = " ".join(context.args).strip()
    if not arg: await update.effective_message.reply_text("Username অথবা owner/repo লিখুন।"); return
    try:
        if cmd == "github":
            d=await get_json(f"https://api.github.com/users/{quote(arg)}")
            msg=f"🐙 <b>{d.get('login')}</b>\nনাম: {d.get('name') or 'N/A'}\nBio: {d.get('bio') or 'N/A'}\nPublic Repos: {d.get('public_repos')}\nFollowers: {d.get('followers')}\nProfile: {d.get('html_url')}"
        else:
            if "/" not in arg: raise ValueError()
            d=await get_json(f"https://api.github.com/repos/{arg}")
            msg=f"📦 <b>{d.get('full_name')}</b>\n⭐ Stars: {d.get('stargazers_count')}\n🍴 Forks: {d.get('forks_count')}\nLanguage: {d.get('language') or 'N/A'}\nবিবরণ: {d.get('description') or 'N/A'}\n{d.get('html_url')}"
        await update.effective_message.reply_text(msg[:3900], parse_mode="HTML", disable_web_page_preview=True)
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))
