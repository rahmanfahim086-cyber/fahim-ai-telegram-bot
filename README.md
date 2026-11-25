# 🤖 FAHIM AI — All-in-One বাংলা Telegram Bot

**ডেভেলপার:** MD FAHIM RAHMAN  
**বটের নাম:** FAHIM AI  
**প্রাইমারি ভাষা:** বাংলা  
**Python সংস্করণ:** Python 3.11 / 3.12  
**ফ্রেমওয়ার্ক:** `python-telegram-bot` v21+, `httpx`, `Flask`, `Gunicorn`  
**হোস্টিং প্ল্যাটফর্ম:** GitHub + Render Web Service  

> **গুরুত্বপূর্ণ:** কোনো অতিরিক্ত বাহ্যিক API Key প্রয়োজন নেই। শুধুমাত্র Telegram `BOT_TOKEN` প্রয়োজন।  
> (No external API key is required. Only Telegram `BOT_TOKEN` is required.)

---

## ১. প্রজেক্ট পরিচিতি

**FAHIM AI** হলো একটি সম্পূর্ণ বাংলা-ভাষী All-in-One Telegram Bot। এতে অনুবাদ, ইংরেজি অভিধান, বাংলা ও ইংরেজি উইকিপিডিয়া, আবহাওয়া, মুদ্রা রূপান্তর, ক্রিপ্টোকারেন্সি দাম, আইপি/ডিএনএস/এসএসএল/ইউআরএল শর্টেনার, গিটহাব তথ্য, লোকাল ইউটিলিটি টুলস (QR, Hash, Base64, Binary, Safe Calculator, Password, UUID) এবং বিনোদনমূলক ফিচার একসাথে রয়েছে।

---

## ২. সকল ফিচারের তালিকা

### 🌐 Translate & Study
- `/tr <text>` — ইংরেজি থেকে বাংলা অনুবাদ (MyMemory API)
- `/trbn <text>` — বাংলা থেকে ইংরেজি অনুবাদ (MyMemory API)
- `/define <word>` — ইংরেজি শব্দের অর্থ, উচ্চারণ ও উদাহরণ (Dictionary API)
- `/wiki <topic>` — বাংলা উইকিপিডিয়া সারাংশ
- `/wikien <topic>` — ইংরেজি উইকিপিডিয়া সারাংশ

### ⛅ Weather & Info
- `/weather <city>` — যেকোনো শহরের বর্তমান আবহাওয়া (Open-Meteo; ডিফল্ট: Rangpur)
- `/time` — বাংলাদেশের বর্তমান তারিখ ও সময় (`Asia/Dhaka`)
- `/fact` — মজার র‍্যান্ডম তথ্য
- `/advice` — র‍্যান্ডম পরামর্শ
- `/demo` — টেস্টিংয়ের জন্য ভুয়া/ডেমো ইউজার ডাটা

### 💱 Finance & Crypto
- `/currency <amount> <from> <to>` — মুদ্রা রূপান্তর (যেমন: `/currency 100 USD BDT`)
- `/crypto <coin>` — Bitcoin ও Ethereum বাজারদর (USD ও BDT)

### 🌍 Web & Network
- `/ip` — সার্ভারের Public IP তথ্য
- `/ipinfo <ip>` — যেকোনো পাবলিক IP-এর তথ্য
- `/dns <domain>` — A, AAAA, MX, TXT, NS DNS রেকর্ড লুকআপ
- `/ssl <domain>` — SSL Labs বিশ্লেষণ
- `/short <url>` — URL ছোট করা (`is.gd`)
- `/github <username>` — GitHub প্রোফাইল তথ্য
- `/repo <owner/repo>` — GitHub রিপোজিটরি তথ্য
- `/http <code>` — HTTP স্ট্যাটাস কোড টেস্ট (`httpbin.org`)
- `/json` — ডেমো JSON রেসপন্স টেস্ট

### 📱 Tools & Security (লোকাল টুলস + QR)
- `/qr <text>` — QR কোড তৈরি ও ছবি পাঠানো
- `/bin <text>` / `/unbin <binary>` — বাইনারি এনকোড ও ডিকোড
- `/b64 <text>` / `/unb64 <encoded>` — Base64 এনকোড ও ডিকোড
- `/md5 <text>` — MD5 হ্যাশ (সতর্কতা: পাসওয়ার্ড সংরক্ষণের জন্য উপযুক্ত নয়)
- `/sha256 <text>` / `/sha512 <text>` — SHA256 ও SHA512 হ্যাশ
- `/urlencode <text>` / `/urldecode <text>` — URL এনকোড ও ডিকোড
- `/password <length>` — Python `secrets` ব্যবহার করে শক্তিশালী পাসওয়ার্ড (৮–১২৮ অক্ষর)
- `/uuid` — র‍্যান্ডম UUID তৈরি
- `/calc <expression>` — AST-ভিত্তিক নিরাপদ ক্যালকুলেটর (`eval()` ব্যবহার করা হয়নি)

### 🎬 Entertainment
- `/joke` — র‍্যান্ডম জোক
- `/quote` — অনুপ্রেরণামূলক উক্তি
- `/cat` — বিড়ালের ছবি
- `/dog` — কুকুরের ছবি
- `/anime <name>` — Anime তথ্য (Jikan API)
- `/manga <name>` — Manga তথ্য (Jikan API)
- `/pokemon <name>` — Pokemon তথ্য (PokeAPI)

### ⚙️ Bot Info
- `/start` ও `/menu` — ইনলাইন মূল মেনু
- `/status` — বটের বর্তমান অবস্থা
- `/about` — বট পরিচিতি
- `/help` — ব্যবহার নির্দেশিকা
- `/cancel` — চলমান ইনপুট বাতিল

---

## ৩. ফোল্ডার স্ট্রাকচার

```text
FAHIM_AI_Telegram_Bot/
├── bot.py
├── server.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── render.yaml
├── Procfile
├── runtime.txt
├── utils/
│   ├── __init__.py
│   ├── api.py
│   ├── buttons.py
│   └── messages.py
└── handlers/
    ├── __init__.py
    ├── translate.py
    ├── study.py
    ├── weather.py
    ├── finance.py
    ├── web.py
    ├── tools.py
    └── fun.py
```

---

## ৪. প্রয়োজনীয় টোকেন (BOT_TOKEN) ও BotFather গাইড

এই বট চালাতে শুধুমাত্র টেলিগ্রামের **BOT_TOKEN** প্রয়োজন।

1. টেলিগ্রামে [@BotFather](https://t.me/BotFather) ওপেন করুন।
2. `/newbot` কমান্ড পাঠান।
3. বটের নাম দিন (যেমন: `FAHIM AI`)।
4. ইউজারনেম দিন যার শেষে `bot` থাকবে (যেমন: `fahim_ai_helper_bot`)।
5. BotFather আপনাকে একটি **HTTP API Token** দেবে। সেটি নিরাপদ জায়গায় কপি করে রাখুন। কখনোই টোকেনটি GitHub বা README-তে লিখবেন না।

---

## ৫. Google AI Studio থেকে GitHub-এ আপলোড (Android ফোন থেকে)

1. Google AI Studio ওয়ার্কস্পেসের উপরের **GitHub / Push to GitHub** বাটন ব্যবহার করে সরাসরি আপনার GitHub রিপোজিটরিতে (`fahim-ai-telegram-bot`) ফাইলগুলো Sync/Push করুন।
2. বিকল্প হিসেবে ম্যানুয়ালি আপলোড করতে চাইলে [GitHub](https://github.com)-এ নতুন রিপোজিটরি তৈরি করে **Add file → Upload files** দিয়ে প্রজেক্টের মূল ফোল্ডারের সব ফাইল (`bot.py`, `server.py`, `requirements.txt`, `render.yaml`, `Procfile`, `runtime.txt`, `.env.example`, `.gitignore`, `README.md`, `utils/`, `handlers/`) রিপোজিটরির রুটে আপলোড করে **Commit changes** দিন।
   - লক্ষ্য রাখবেন: `.env` ফাইল বা `BOT_TOKEN` কখনোই GitHub-এ আপলোড করবেন না।
   - নিশ্চিত করুন `utils/` ও `handlers/` ফোল্ডারের ভেতরে `__init__.py` এবং সব মডিউল সঠিকভাবে আছে।

---

## ৬. Render Web Service-এ ডিপ্লয়মেন্ট

1. [Render Dashboard](https://dashboard.render.com/)-এ গিয়ে **New + → Web Service** ক্লিক করুন।
2. আপনার GitHub অ্যাকাউন্ট কানেক্ট করে `fahim-ai-telegram-bot` রিপোজিটরি সিলেক্ট করুন।
3. নিচের কনফিগারেশনগুলো দিন (অথবা `render.yaml` অনুযায়ী Blueprint ব্যবহার করুন):
   - **Runtime:** `Python 3`
   - **Plan:** `Free`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn server:app --workers 1 --threads 4 --timeout 120`
   - **Health Check Path:** `/`
4. **Environment Variables** সেকশনে গিয়ে যোগ করুন:
   - Key: `BOT_TOKEN`
   - Value: আপনার BotFather থেকে পাওয়া টোকেন
5. **Create Web Service** ক্লিক করে ডিপ্লয় শেষ হওয়া পর্যন্ত অপেক্ষা করুন।

> **নোট:** এই বটে পেন্ডিং ইউজার ইনপুট (যেমন বাটন ক্লিকের পর ইনপুট অপেক্ষা) মেমোরিতে সংরক্ষিত থাকে। Render ফ্রি সার্ভার রিস্টার্ট বা স্লিপ হলে চলমান পেন্ডিং স্টেট মুছে যাবে—ব্যবহারকারী আবার `/menu` থেকে শুরু করতে পারবেন।

---

## ৭. লোকাল কম্পিউটার বা ফোনে টেস্ট করা

```bash
cp .env.example .env
# .env ফাইলে আপনার BOT_TOKEN বসান
pip install -r requirements.txt
python server.py
```

---

## ৮. `/start` টেস্ট ও Render লগ দেখা

1. ডিপ্লয় **"Live"** হলে আপনার Render ওয়েবসাইট URL-এ ব্রাউজারে গেলে `FAHIM AI Bot is running` লেখা দেখতে পাবেন এবং `/healthz` এন্ডপয়েন্ট `healthy` দেখাবে।
2. টেলিগ্রামে আপনার বট ওপেন করে `/start` পাঠান। মূল মেনু ও ৭টি ক্যাটাগরি বাটন দেখা যাবে।
3. কোনো সমস্যা হলে Render Dashboard → আপনার সার্ভিস → **Logs** ট্যাবে গিয়ে এরর দেখতে পারবেন।

---

## ৯. সাধারণ সমস্যা ও সমাধান

| সমস্যা | সম্ভাব্য কারণ ও সমাধান |
|---|---|
| `ModuleNotFoundError: No module named 'utils'` | রিপোজিটরিতে ফাইল আপলোডের সময় `utils/` ও `handlers/` ফোল্ডারসহ `__init__.py` সঠিকভাবে আপলোড হয়নি, অথবা একটির ভেতর আরেকটি ফোল্ডার ডাবল নেস্ট হয়েছে। রুট ডিরেক্টরিতেই `bot.py`, `utils/`, `handlers/` থাকতে হবে। |
| `/healthz` `503 unhealthy` দেখাচ্ছে | `BOT_TOKEN` Environment Variable দেওয়া হয়নি বা টোকেন ভুল। Render → Environment-এ `BOT_TOKEN` ঠিক করে Manual Deploy করুন। |
| বট একই মেসেজে ২ বার উত্তর দিচ্ছে | Gunicorn-এ `--workers 1` এর বেশি দেওয়া হয়েছে অথবা একই টোকেনে অন্য কোথাও বট চলছে। সর্বদা `--workers 1` ব্যবহার করুন। |
| `RuntimeError: This event loop is already running` | এই প্রজেক্টের `server.py` ও `bot.py` আলাদা থ্রেড ও ডেডিকেটেড ইভেন্ট লুপ ব্যবহার করে, তাই এই সমস্যা হবে না। |

---

## ১০. Public API সীমাবদ্ধতা ও Rate Limit

- এই বটের সব বাহ্যিক API ফ্রি ও Keyless থার্ড-পার্টি Public Endpoint।
- অনেক বেশি রিকোয়েস্ট পাঠালে (`HTTP 429` Rate Limit) কিছু সময়ের জন্য রেসপন্স বন্ধ থাকতে পারে।
- `api.ssllabs.com` বিশ্লেষণে ১-২ মিনিট সময় নিতে পারে (`IN_PROGRESS`)।
- কোনো API সাময়িকভাবে ডাউন থাকলে বট ক্র্যাশ করবে না; বরং ব্যবহারকারীকে পরিষ্কার বাংলায় ত্রুটি বার্তা দেখাবে এবং কিছুক্ষণ পর আবার চেষ্টা করতে বলবে।
