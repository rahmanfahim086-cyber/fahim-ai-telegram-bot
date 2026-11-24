import base64, hashlib, math, operator, random, string, uuid, ast
from urllib.parse import quote, unquote
from telegram import Update
from telegram.ext import ContextTypes
from utils.api import get_bytes, get_json, safe_error

async def qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text: await update.effective_message.reply_text("ব্যবহার: /qr আপনার লেখা বা লিংক"); return
    try:
        content, ctype = await get_bytes("https://api.qrserver.com/v1/create-qr-code/", {"size":"500x500","data":text})
        if "image" not in ctype: raise ValueError()
        await update.effective_message.reply_photo(content, caption="📱 আপনার QR Code")
    except Exception as exc: await update.effective_message.reply_text("⚠️ " + safe_error(exc))

async def local_tool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.effective_message.text.split()[0].split("@")[0].lstrip("/").lower()
    raw = update.effective_message.text.partition(" ")[2].strip()
    try:
        if cmd == "bin": result = " ".join(format(ord(c), "08b") for c in raw)
        elif cmd == "unbin":
            bits = raw.split()
            if len(bits) == 1 and len(raw.replace(" ","")) % 8 == 0: bits = [raw[i:i+8] for i in range(0,len(raw),8)]
            result = "".join(chr(int(b,2)) for b in bits)
        elif cmd == "b64": result = base64.b64encode(raw.encode()).decode()
        elif cmd == "unb64": result = base64.b64decode(raw, validate=True).decode()
        elif cmd in ("md5","sha256","sha512"):
            if not raw: raise ValueError()
            result = hashlib.new(cmd, raw.encode()).hexdigest()
        elif cmd == "urlencode": result = quote(raw, safe="")
        elif cmd == "urldecode": result = unquote(raw)
        elif cmd == "password":
            n = int(raw or "16")
            if not 8 <= n <= 128: raise ValueError()
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
            result = "".join(random.SystemRandom().choice(alphabet) for _ in range(n))
        elif cmd == "uuid": result = str(uuid.uuid4())
        elif cmd == "calc": result = str(safe_calculate(raw))
        else: result = "অজানা টুল।"
        await update.effective_message.reply_text(f"✅ <b>ফলাফল</b>\n<code>{result}</code>", parse_mode="HTML")
    except Exception:
        await update.effective_message.reply_text("⚠️ ইনপুট সঠিক নয়। /help দেখে সঠিক ব্যবহার লিখুন।")

def safe_calculate(expression):
    if not expression or len(expression) > 100: raise ValueError()
    allowed = {ast.Add:operator.add, ast.Sub:operator.sub, ast.Mult:operator.mul, ast.Div:operator.truediv,
               ast.FloorDiv:operator.floordiv, ast.Mod:operator.mod, ast.Pow:operator.pow,
               ast.USub:operator.neg, ast.UAdd:operator.pos}
    def walk(node):
        if isinstance(node, ast.Expression): return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value,(int,float)): return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in allowed:
            if isinstance(node.op, ast.Pow) and abs(node.right.value if isinstance(node.right, ast.Constant) else 999) > 10: raise ValueError()
            return allowed[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed: return allowed[type(node.op)](walk(node.operand))
        raise ValueError()
    value = walk(ast.parse(expression, mode="eval"))
    if not math.isfinite(value) or abs(value) > 1e100: raise ValueError()
    return value
