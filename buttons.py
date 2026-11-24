from telegram import InlineKeyboardButton, InlineKeyboardMarkup

MAIN_CATEGORIES = [
    ("🌐 Translate & Study", "cat:study"),
    ("⛅ Weather & Info", "cat:weather"),
    ("💱 Finance & Crypto", "cat:finance"),
    ("🌍 Web & Network", "cat:web"),
    ("📱 Tools & Security", "cat:tools"),
    ("🎬 Entertainment", "cat:fun"),
    ("⚙️ Bot Info", "cat:info"),
]
SUBMENUS = {
    "study": [
        ("🌐 Translate", "ask:tr"), ("🌐 Translate BN→EN", "ask:trbn"),
        ("📖 Dictionary", "ask:define"), ("📚 Wikipedia", "ask:wiki"),
        ("🌐 English Wiki", "ask:wikien"),
    ],
    "weather": [
        ("⛅ Weather", "ask:weather"), ("🕒 Bangladesh Time", "run:time"),
        ("🧠 Fact", "run:fact"), ("🧭 Advice", "run:advice"),
    ],
    "finance": [("💱 Currency", "ask:currency"), ("🪙 Crypto", "ask:crypto")],
    "web": [
        ("🌍 My IP", "run:ip"), ("🔎 IP Lookup", "ask:ipinfo"),
        ("🧭 DNS Lookup", "ask:dns"), ("🔐 SSL Checker", "ask:ssl"),
        ("🔗 Short URL", "ask:short"), ("🐙 GitHub User", "ask:github"),
        ("📦 GitHub Repo", "ask:repo"),
    ],
    "tools": [
        ("📱 QR Code", "ask:qr"), ("🔢 Binary Encode", "ask:bin"),
        ("🔤 Binary Decode", "ask:unbin"), ("🧬 Base64 Encode", "ask:b64"),
        ("🧬 Base64 Decode", "ask:unb64"), ("🔐 MD5", "ask:md5"),
        ("🔐 SHA256", "ask:sha256"), ("🔐 SHA512", "ask:sha512"),
        ("🔗 URL Encode", "ask:urlencode"), ("🔗 URL Decode", "ask:urldecode"),
        ("🔑 Password", "ask:password"), ("🆔 UUID", "run:uuid"),
        ("🧮 Calculator", "ask:calc"), ("🌐 HTTP Test", "ask:http"),
        ("🧪 JSON Test", "run:json"), ("👤 Demo User", "run:demo"),
    ],
    "fun": [
        ("😂 Joke", "run:joke"), ("💡 Quote", "run:quote"),
        ("🐱 Cat", "run:cat"), ("🐶 Dog", "run:dog"),
        ("🎌 Anime", "ask:anime"), ("📖 Manga", "ask:manga"),
        ("⚡ Pokemon", "ask:pokemon"),
    ],
    "info": [("📊 Bot Status", "run:status"), ("ℹ️ About", "run:about"), ("❓ Help", "run:help")],
}
def main_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton(t, callback_data=d)] for t,d in MAIN_CATEGORIES])
def submenu(category):
    items = SUBMENUS.get(category, [])
    rows = [[InlineKeyboardButton(t, callback_data=d)] for t,d in items]
    rows.append([InlineKeyboardButton("🔙 মূল মেনু", callback_data="home")])
    return InlineKeyboardMarkup(rows)
def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 মূল মেনু", callback_data="home")]])
