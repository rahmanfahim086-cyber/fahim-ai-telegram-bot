"""Reusable Bengali message templates for FAHIM AI Telegram Bot."""

WELCOME_MESSAGE = (
    "স্বাগতম <b>FAHIM AI</b>-তে! 🤖\n\n"
    "এটি একটি All-in-One বাংলা Telegram Bot।\n"
    "নিচের মেনু থেকে আপনার প্রয়োজনীয় বিভাগ ও ফিচার নির্বাচন করুন অথবা সরাসরি Command ব্যবহার করুন।\n\n"
    "👨‍💻 ডেভেলপার: <b>MD FAHIM RAHMAN</b>"
)

MAIN_MENU_MESSAGE = (
    "🏠 <b>FAHIM AI — মূল মেনু</b>\n\n"
    "নিচের যেকোনো একটি বিভাগ বেছে নিন:"
)

HELP_MESSAGE = (
    "❓ <b>ব্যবহার নির্দেশিকা (Help)</b>\n\n"
    "১. /menu বা /start লিখে ইনলাইন মেনু খুলুন।\n"
    "২. যেকোনো বাটনে চাপ দিলে বট জানাবে কী ইনপুট দিতে হবে।\n"
    "৩. ইনপুট বাতিল করতে /cancel লিখুন বা <b>বাতিল</b> বাটনে চাপ দিন।\n"
    "৪. চাইলে সরাসরি Command ও Argument দিয়েও কাজ করতে পারবেন।\n\n"
    "<b>উদাহরণ:</b>\n"
    "• <code>/tr Hello world</code> — ইংরেজি থেকে বাংলা অনুবাদ\n"
    "• <code>/trbn আমি ভালো আছি</code> — বাংলা থেকে ইংরেজি অনুবাদ\n"
    "• <code>/define beautiful</code> — ইংরেজি শব্দের অর্থ\n"
    "• <code>/weather Dhaka</code> — শহরের আবহাওয়া\n"
    "• <code>/currency 100 USD BDT</code> — মুদ্রা রূপান্তর\n"
    "• <code>/crypto bitcoin</code> — ক্রিপ্টো দাম\n"
    "• <code>/dns google.com</code> — DNS লুকআপ\n"
    "• <code>/qr https://example.com</code> — QR কোড তৈরি\n"
    "• <code>/calc 12 * (5 + 3)</code> — নিরাপদ ক্যালকুলেটর\n\n"
    "ℹ️ এই বটে কোনো অতিরিক্ত API Key প্রয়োজন নেই—সব ফিচার Public Keyless API ও লোকাল টুলের মাধ্যমে চলে।"
)

ABOUT_MESSAGE = (
    "🤖 <b>FAHIM AI — All-in-One Telegram Bot</b>\n\n"
    "👨‍💻 <b>Developer:</b> MD FAHIM RAHMAN\n"
    "🗣️ <b>ভাষা:</b> বাংলা\n"
    "🐍 <b>Python:</b> 3.11 / 3.12\n"
    "⚙️ <b>Framework:</b> python-telegram-bot v21+\n"
    "🌐 <b>Web Health Server:</b> Flask + Gunicorn\n"
    "☁️ <b>Deployment:</b> GitHub + Render Web Service\n\n"
    "📌 এই বটে অনুবাদ, অভিধান, উইকিপিডিয়া, আবহাওয়া, মুদ্রা, ক্রিপ্টো, নেটওয়ার্ক টুলস, "
    "লোকাল এনক্রিপশন/হ্যাশ টুলস এবং বিনোদন ফিচার রয়েছে।"
)

LOADING_MESSAGE = "🔄 তথ্য সংগ্রহ করা হচ্ছে..."
SUCCESS_MESSAGE = "✅ কাজ সম্পন্ন হয়েছে।"
API_ERROR_MESSAGE = "⚠️ দুঃখিত, API থেকে তথ্য পাওয়া যায়নি। একটু পরে আবার চেষ্টা করুন।"
INVALID_INPUT_MESSAGE = "❌ সঠিক ইনপুট দিন।"
CANCEL_MESSAGE = "🚫 চলমান কাজটি বাতিল করা হয়েছে। /menu লিখে আবার শুরু করতে পারেন।"

SUBMENU_MESSAGES = {
    "translate_study": (
        "🌐 <b>অনুবাদ ও পড়াশোনা (Translate &amp; Study)</b>\n\n"
        "নিচের যেকোনো একটি ফিচার নির্বাচন করুন:"
    ),
    "weather_info": (
        "⛅ <b>আবহাওয়া ও তথ্য (Weather &amp; Info)</b>\n\n"
        "নিচের যেকোনো একটি ফিচার নির্বাচন করুন:"
    ),
    "finance_crypto": (
        "💱 <b>অর্থ ও ক্রিপ্টো (Finance &amp; Crypto)</b>\n\n"
        "নিচের যেকোনো একটি ফিচার নির্বাচন করুন:"
    ),
    "web_network": (
        "🌍 <b>ওয়েব ও নেটওয়ার্ক (Web &amp; Network)</b>\n\n"
        "নিচের যেকোনো একটি ফিচার নির্বাচন করুন:"
    ),
    "tools_security": (
        "📱 <b>টুলস ও সিকিউরিটি (Tools &amp; Security)</b>\n\n"
        "নিচের যেকোনো একটি ফিচার নির্বাচন করুন:"
    ),
    "entertainment": (
        "🎬 <b>বিনোদন (Entertainment)</b>\n\n"
        "নিচের যেকোনো একটি ফিচার নির্বাচন করুন:"
    ),
    "bot_info": (
        "⚙️ <b>বট তথ্য (Bot Info)</b>\n\n"
        "বটের অবস্থা, পরিচিতি ও নির্দেশিকা দেখুন:"
    ),
}

FEATURE_INPUT_PROMPTS = {
    "tr": "🌐 অনুবাদের জন্য ইংরেজি লেখা পাঠান।\nউদাহরণ: <code>Hello, how are you?</code>",
    "trbn": "🌐 ইংরেজিতে অনুবাদের জন্য বাংলা লেখা পাঠান।\nউদাহরণ: <code>বাংলাদেশ একটি সুন্দর দেশ।</code>",
    "define": "📖 অর্থ জানার জন্য একটি ইংরেজি শব্দ পাঠান।\nউদাহরণ: <code>resilient</code>",
    "wiki": "📚 বাংলা উইকিপিডিয়ায় খুঁজতে বিষয় লিখুন।\nউদাহরণ: <code>বাংলাদেশ</code>",
    "wikien": "🌐 ইংরেজি উইকিপিডিয়ায় খুঁজতে বিষয় লিখুন।\nউদাহরণ: <code>Python programming</code>",
    "weather": "⛅ আবহাওয়া জানতে শহরের নাম পাঠান (ডিফল্ট: Rangpur লিখতে পারেন)।\nউদাহরণ: <code>Dhaka</code> বা <code>Rangpur</code>",
    "currency": "💱 পরিমাণ এবং দুইটি মুদ্রার কোড পাঠান।\nউদাহরণ: <code>100 USD BDT</code>",
    "crypto": "🪙 ক্রিপ্টো কয়েনের নাম পাঠান (<code>bitcoin</code> বা <code>ethereum</code>)।",
    "ipinfo": "🔎 তথ্য জানার জন্য একটি পাবলিক IP ঠিকানা পাঠান।\nউদাহরণ: <code>8.8.8.8</code>",
    "dns": "🧭 DNS রেকর্ড দেখার জন্য ডোমেইন নাম পাঠান।\nউদাহরণ: <code>example.com</code>",
    "ssl": "🔐 SSL পরীক্ষা করার জন্য ডোমেইন নাম পাঠান।\nউদাহরণ: <code>example.com</code>",
    "short": "🔗 ছোট করার জন্য পূর্ণ লিংক (http:// বা https://) পাঠান।\nউদাহরণ: <code>https://example.com</code>",
    "github": "🐙 GitHub ইউজারনেম পাঠান।\nউদাহরণ: <code>torvalds</code>",
    "repo": "📦 GitHub রিপোজিটরি পাঠান (<code>owner/repo</code> ফরম্যাটে)।\nউদাহরণ: <code>python/cpython</code>",
    "http": "🌐 HTTP স্ট্যাটাস টেস্টের জন্য ৩ ডিজিটের স্ট্যাটাস কোড পাঠান (100–599)।\nউদাহরণ: <code>200</code> বা <code>404</code>",
    "qr": "📱 QR কোড তৈরি করার জন্য লেখা বা লিংক পাঠান।\nউদাহরণ: <code>https://t.me</code>",
    "bin": "🔢 বাইনারিতে রূপান্তরের জন্য লেখা পাঠান।\nউদাহরণ: <code>FAHIM</code>",
    "unbin": "🔤 টেক্সটে রূপান্তরের জন্য বাইনারি কোড পাঠান।\nউদাহরণ: <code>01001000 01101001</code>",
    "b64": "🧬 Base64 এনকোড করার জন্য লেখা পাঠান।\nউদাহরণ: <code>Hello Fahim</code>",
    "unb64": "🧬 Base64 ডিকোড করার জন্য এনকোডেড লেখা পাঠান।\nউদাহরণ: <code>SGVsbG8=</code>",
    "md5": "🔐 MD5 হ্যাশ তৈরি করার জন্য লেখা পাঠান (শুধু চেকসাম/টেস্টিংয়ের জন্য)।",
    "sha256": "🔐 SHA256 হ্যাশ তৈরি করার জন্য লেখা পাঠান।",
    "sha512": "🔐 SHA512 হ্যাশ তৈরি করার জন্য লেখা পাঠান।",
    "urlencode": "🔗 URL এনকোড করার জন্য লেখা পাঠান।",
    "urldecode": "🔗 URL ডিকোড করার জন্য এনকোডেড লেখা পাঠান।",
    "password": "🔑 কত অক্ষরের শক্তিশালী পাসওয়ার্ড চান তা লিখুন (৮ থেকে ১২৮ এর মধ্যে)।\nউদাহরণ: <code>16</code>",
    "calc": "🧮 হিসাব করার জন্য গাণিতিক এক্সপ্রেশন পাঠান।\nউদাহরণ: <code>(25 + 15) * 2 / 5</code>",
    "anime": "🎌 খুঁজতে চাওয়া Anime-এর নাম পাঠান।\nউদাহরণ: <code>Naruto</code>",
    "manga": "📖 খুঁজতে চাওয়া Manga-এর নাম পাঠান।\nউদাহরণ: <code>One Piece</code>",
    "pokemon": "⚡ Pokemon-এর নাম বা আইডি পাঠান।\nউদাহরণ: <code>pikachu</code>",
}


def build_status_message(uptime_text: str, bot_healthy: bool, active_pending: int) -> str:
    """Build a Bengali status summary without exposing secrets."""
    health_label = "সচল ✅" if bot_healthy else "সমস্যা ⚠️"
    return (
        "📊 <b>FAHIM AI — বটের অবস্থা</b>\n\n"
        f"• <b>বট স্ট্যাটাস:</b> {health_label}\n"
        f"• <b>আপটাইম:</b> {uptime_text}\n"
        f"• <b>সক্রিয় ইনপুট সেশন:</b> {active_pending}\n"
        "• <b>ডাটাবেজ:</b> ইন-মেমোরি স্টেট (রিস্টার্ট হলে পেন্ডিং স্টেট মুছে যায়)\n"
        "• <b>API নীতি:</b> শুধু Keyless Public API ব্যবহৃত হচ্ছে"
    )
