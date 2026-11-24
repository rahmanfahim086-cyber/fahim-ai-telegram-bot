import logging, os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from utils.buttons import main_menu, submenu, back_menu
from utils.messages import WELCOME, HELP, ABOUT
from handlers.translate import translate, translate_bn
from handlers.study import define, wiki, wikien
from handlers.weather import weather
from handlers.finance import currency, crypto
from handlers.web import my_ip, ip_info, dns, ssl_check, shorten
from handlers.tools import qr, local_tool
from handlers.fun import random_content, animal, anime_manga, pokemon, github

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("fahim-ai")
PENDING = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(WELCOME, parse_mode="HTML", reply_markup=main_menu())
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("📋 <b>প্রধান মেনু</b>\nএকটি বিভাগ নির্বাচন করুন:", parse_mode="HTML", reply_markup=main_menu())
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(HELP, parse_mode="HTML", reply_markup=back_menu())
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(ABOUT, parse_mode="HTML", reply_markup=back_menu())
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("📊 <b>FAHIM AI Status</b>\nBot process: সচল\nAPI mode: Public no-key APIs\nHosting: Render Web Service", parse_mode="HTML", reply_markup=back_menu())

ASK_COMMANDS = {
    "tr": ("ইংরেজি লেখা পাঠান।", translate), "trbn": ("বাংলা লেখা পাঠান।", translate_bn),
    "define": ("ইংরেজি শব্দ পাঠান।", define), "weather": ("শহরের নাম পাঠান।", weather),
    "currency": ("পরিমাণ ও মুদ্রা লিখুন। উদাহরণ: 100 USD BDT", currency),
    "crypto": ("bitcoin অথবা ethereum লিখুন।", crypto), "ipinfo": ("IP address পাঠান।", ip_info),
    "dns": ("Domain লিখুন।", dns), "ssl": ("Domain লিখুন।", ssl_check),
    "short": ("সম্পূর্ণ URL পাঠান।", shorten), "qr": ("QR বানানোর লেখা/লিংক পাঠান।", qr),
    "wiki": ("বাংলা উইকিপিডিয়ার বিষয় লিখুন।", wiki), "wikien": ("ইংরেজি বিষয় লিখুন।", wikien),
    "bin": ("যে লেখা Binary করতে চান পাঠান।", local_tool), "unbin": ("Binary পাঠান।", local_tool),
    "b64": ("যে লেখা Base64 করতে চান পাঠান।", local_tool), "unb64": ("Base64 পাঠান।", local_tool),
    "md5": ("Hash করার লেখা পাঠান।", local_tool), "sha256": ("Hash করার লেখা পাঠান।", local_tool),
    "sha512": ("Hash করার লেখা পাঠান।", local_tool), "urlencode": ("Encode করার লেখা পাঠান।", local_tool),
    "urldecode": ("Decode করার লেখা পাঠান।", local_tool), "password": ("Password length (8-128) দিন।", local_tool),
    "calc": ("গাণিতিক expression পাঠান।", local_tool), "anime": ("Anime-এর নাম পাঠান।", anime_manga),
    "manga": ("Manga-এর নাম পাঠান।", anime_manga), "pokemon": ("Pokemon-এর নাম পাঠান।", pokemon),
    "github": ("GitHub username পাঠান।", github), "repo": ("owner/repo লিখুন।", github),
    "http": ("HTTP status code দিন (100-599)।", random_content),
}
RUN_COMMANDS = {
    "ip": my_ip, "time": random_content, "joke": random_content, "quote": random_content,
    "fact": random_content, "advice": random_content, "cat": animal, "dog": animal,
    "uuid": local_tool, "demo": random_content, "json": random_content, "http": random_content,
}
async def ask_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data.split(":",1)[1]
    prompt, _ = ASK_COMMANDS[action]
    PENDING[query.from_user.id] = action
    await query.message.reply_text(f"✍️ {prompt}\n\nবাতিল করতে /menu লিখুন।", reply_markup=back_menu())
async def run_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query; await query.answer()
    action=query.data.split(":",1)[1]
    if action=="about": await about(update,context)
    elif action=="help": await help_cmd(update,context)
    elif action=="status": await status(update,context)
    else:
        handler=RUN_COMMANDS[action]
        class FakeMessage:
            text="/"+action
            async def reply_text(self,*a,**kw): return await query.message.reply_text(*a,**kw)
            async def reply_photo(self,*a,**kw): return await query.message.reply_photo(*a,**kw)
        class FakeUpdate:
            effective_message=FakeMessage()
            effective_user=query.from_user
        await handler(FakeUpdate(), context)
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    if q.data=="home":
        await q.answer()
        await q.message.reply_text("📋 প্রধান মেনু:", reply_markup=main_menu())
    elif q.data.startswith("cat:"):
        await q.answer()
        cat=q.data.split(":",1)[1]
        names={"study":"Translate & Study","weather":"Weather & Info","finance":"Finance & Crypto","web":"Web & Network","tools":"Tools & Security","fun":"Entertainment","info":"Bot Info"}
        await q.message.reply_text(f"📂 <b>{names.get(cat,'Menu')}</b>",parse_mode="HTML",reply_markup=submenu(cat))
    elif q.data.startswith("ask:"): await ask_callback(update,context)
    elif q.data.startswith("run:"): await run_callback(update,context)

async def pending_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    action=PENDING.pop(uid,None)
    if not action: return
    handler=ASK_COMMANDS[action][1]
    # Adapt a typed message to the existing command handlers without mutating Telegram objects.
    class ArgsContext:
        args=update.effective_message.text.split()
    proxy=ArgsContext()
    proxy.args = [update.effective_message.text] if action not in ("currency","repo","http","password") else update.effective_message.text.split()
    if action in ("bin","unbin","b64","unb64","md5","sha256","sha512","urlencode","urldecode","calc"):
        async def fake_text_handler():
            original=update.effective_message.text
            class M:
                text="/"+action+" "+original
                async def reply_text(self,*a,**kw): return await update.effective_message.reply_text(*a,**kw)
            class U: effective_message=M()
            return await handler(U(),context)
        await fake_text_handler()
    else:
        class M:
            text="/"+action+" "+update.effective_message.text
            async def reply_text(self,*a,**kw): return await update.effective_message.reply_text(*a,**kw)
            async def reply_photo(self,*a,**kw): return await update.effective_message.reply_photo(*a,**kw)
        class U: effective_message=M()
        await handler(U(),proxy)

def build_application():
    token=os.getenv("BOT_TOKEN","").strip()
    if not token: raise RuntimeError("BOT_TOKEN পরিবেশ ভেরিয়েবল সেট করা নেই।")
    app=Application.builder().token(token).build()
    commands = {
        "start":start,"help":help_cmd,"menu":menu,"about":about,"status":status,
        "tr":translate,"trbn":translate_bn,"define":define,"weather":weather,
        "currency":currency,"crypto":crypto,"ip":my_ip,"ipinfo":ip_info,"dns":dns,
        "ssl":ssl_check,"qr":qr,"short":shorten,"wiki":wiki,"wikien":wikien,
        "github":github,"repo":github,"joke":random_content,"quote":random_content,
        "fact":random_content,"advice":random_content,"cat":animal,"dog":animal,
        "anime":anime_manga,"manga":anime_manga,"pokemon":pokemon,"time":random_content,
        "demo":random_content,"http":random_content,"json":random_content,
    }
    for name, handler in commands.items(): app.add_handler(CommandHandler(name,handler))
    for name in ("bin","unbin","b64","unb64","md5","sha256","sha512","urlencode","urldecode","password","uuid","calc"):
        app.add_handler(CommandHandler(name,local_tool))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pending_text))
    app.bot_data["registered_commands"] = commands
    return app

def main():
    application=build_application()
    async def post_init(app):
        command_list=[
            ("start","বট চালু করুন"),("help","ব্যবহার নির্দেশিকা"),("menu","প্রধান মেনু"),("about","বট সম্পর্কে"),("status","বটের অবস্থা"),
            ("tr","English থেকে বাংলা অনুবাদ"),("trbn","বাংলা থেকে English অনুবাদ"),("define","ইংরেজি শব্দের অর্থ"),("weather","শহরের আবহাওয়া"),
            ("currency","মুদ্রা রূপান্তর"),("crypto","ক্রিপ্টো মূল্য"),("ip","নিজের Public IP"),("ipinfo","IP তথ্য"),("dns","DNS Lookup"),
            ("ssl","SSL পরীক্ষা"),("qr","QR Code তৈরি"),("short","লিংক ছোট করুন"),("wiki","বাংলা Wikipedia"),("wikien","English Wikipedia"),
            ("github","GitHub User"),("repo","GitHub Repository"),("joke","মজার কৌতুক"),("quote","উক্তি"),("fact","মজার তথ্য"),
            ("advice","পরামর্শ"),("cat","বিড়ালের ছবি"),("dog","কুকুরের ছবি"),("anime","Anime অনুসন্ধান"),("manga","Manga অনুসন্ধান"),
            ("pokemon","Pokemon তথ্য"),("time","বাংলাদেশের সময়"),("demo","নকল Demo User"),("http","HTTP Status Test"),("json","JSON Demo"),
            ("bin","Binary Encode"),("unbin","Binary Decode"),("b64","Base64 Encode"),("unb64","Base64 Decode"),("md5","MD5 Hash"),
            ("sha256","SHA256 Hash"),("sha512","SHA512 Hash"),("urlencode","URL Encode"),("urldecode","URL Decode"),
            ("password","Strong Password"),("uuid","UUID তৈরি"),("calc","Calculator")]
        await app.bot.set_my_commands(command_list)
    application.post_init=post_init
    application.run_polling(drop_pending_updates=True)

if __name__=="__main__":
    main()
