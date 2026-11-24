# FAHIM AI — All-in-One Telegram Bot

**Developer:** MD FAHIM RAHMAN  
**Language:** বাংলা  
**Python:** 3.11+  
**Framework:** python-telegram-bot v21+  
**Hosting:** Render Web Service

## বৈশিষ্ট্য
- Translation, Dictionary, Wikipedia
- Weather, Bangladesh Time, Currency, Crypto
- IP, DNS, SSL, URL shortener, GitHub lookup
- QR, Binary, Base64, Hash, URL tools, Password, UUID, Calculator
- Joke, Quote, Fact, Advice, Cat/Dog, Anime, Manga, Pokemon
- বাংলা Inline menu ও Telegram command

## API Key
এই প্রজেক্টে তালিকাভুক্ত public no-key API ব্যবহার করা হয়েছে। **কোনো external API key বা API account প্রয়োজন নেই।** শুধু Telegram BotFather-এর `BOT_TOKEN` প্রয়োজন।

> Public API তৃতীয় পক্ষের; availability, rate limit, response format বা policy পরিবর্তিত হতে পারে। API key-free মানেই unlimited বা guaranteed uptime নয়।

## 1. GitHub-এ ফাইল আপলোড
1. GitHub-এ নতুন repository তৈরি করুন, যেমন `fahim-ai-telegram-bot`।
2. ZIP extract করে ভেতরের সব ফাইল ও folder repository root-এ আপলোড করুন।
3. `bot.py`, `server.py`, `requirements.txt`, `render.yaml`, `Procfile`, `.env.example`, `README.md`, `.gitignore` root-এ থাকবে।
4. `handlers/` এবং `utils/` folder-সহ তাদের Python ফাইলগুলোও আপলোড করুন।
5. `.env` বা Bot Token কখনো GitHub-এ আপলোড করবেন না।

## 2. BotFather থেকে BOT_TOKEN
1. Telegram-এ `@BotFather` খুলুন।
2. `/newbot` পাঠান।
3. Bot name ও username দিন।
4. BotFather যে token দেবে সেটি গোপন রাখুন। কাউকে পাঠাবেন না।

## 3. Render Web Service
1. Render-এ লগইন করুন।
2. **New + → Web Service** নির্বাচন করুন।
3. GitHub repository connect করুন।
4. Runtime: Python
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn server:app --workers 1 --threads 4 --timeout 120`
7. Health Check Path: `/`
8. Environment Variables-এ যোগ করুন:
   - Key: `BOT_TOKEN`
   - Value: BotFather থেকে পাওয়া token
9. Deploy করুন।

`render.yaml` ব্যবহার করলে Render service configuration স্বয়ংক্রিয়ভাবে প্রস্তাব করতে পারে। Environment Variable অবশ্যই Render Dashboard-এ যোগ করতে হবে।

## 4. Telegram-এ পরীক্ষা
Deploy সফল হলে Telegram-এ আপনার bot খুলে `/start` পাঠান। Menu button ও command ব্যবহার করে পরীক্ষা করুন। `/help`-এ নির্দেশিকা আছে।

## 5. কোনো API কাজ না করলে
- API provider সাময়িকভাবে down বা rate-limited হতে পারে।
- Command-এর input format পরীক্ষা করুন।
- Render → Logs-এ error দেখুন।
- কয়েক মিনিট পরে আবার চেষ্টা করুন।
- Render-এর Environment Variable-এ BOT_TOKEN আছে কি না যাচাই করুন।
- API response format বদলে গেলে সংশ্লিষ্ট handler update করতে হবে।

## 6. গুরুত্বপূর্ণ সীমাবদ্ধতা
- Render Free Web Service inactivity-তে sleep করতে পারে; সবসময় instant response নিশ্চিত নয়।
- এই সংস্করণে database নেই; pending button input process memory-তে থাকে।
- SSL Labs প্রথম request-এ `IN_PROGRESS` দিতে পারে; পরে আবার `/ssl domain` চালাতে হতে পারে।
- Weather city lookup-এর জন্য Open-Meteo Geocoding public endpoint অতিরিক্তভাবে ব্যবহৃত হয়।
- HTTP command status code argument গ্রহণ করে; এই demo কেবল status input দেখায়, arbitrary status response test করে না।
- `/demo` fake/test data তৈরি করে; বাস্তব ব্যক্তির তথ্য নয়।
- Calculator সীমিত arithmetic expression গ্রহণ করে; Python `eval()` ব্যবহার করে না।
- API provider-এর Terms, rate limits ও privacy policy মেনে ব্যবহার করুন।

## Local run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .env ফাইলে BOT_TOKEN দিন
python bot.py
```
