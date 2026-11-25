"""QR code and local Python utility tools (no eval, uses secrets and AST)."""

from __future__ import annotations

import ast
import base64
import hashlib
import math
import operator
import secrets
import string
import uuid
from urllib.parse import quote, unquote

from telegram import Message, Update
from telegram.ext import ContextTypes

from utils.api import escape_html, fetch_bytes, safe_error_message, send_safe_html
from utils.buttons import result_navigation_keyboard

MAX_TEXT_INPUT = 2000

_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_calculate(expression: str) -> float | int:
    """Safely evaluate arithmetic expressions using AST without eval()."""
    expr = expression.strip()
    if not expr or len(expr) > 100:
        raise ValueError("Expression must be 1 to 100 characters.")

    def _eval_node(node: ast.AST) -> float | int:
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
            return _UNARY_OPS[type(node.op)](_eval_node(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            if isinstance(node.op, ast.Pow):
                if abs(right) > 10 or abs(left) > 10000:
                    raise ValueError("Exponent or base too large.")
            if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
                raise ValueError("Division by zero.")
            return _BINARY_OPS[type(node.op)](left, right)
        raise ValueError("Unsupported syntax or operator.")

    tree = ast.parse(expr, mode="eval")
    result = _eval_node(tree)
    if not math.isfinite(result) or abs(result) > 1e100:
        raise ValueError("Result out of bounds.")
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def generate_secure_password(length_text: str) -> str:
    """Generate a cryptographically strong password using secrets."""
    raw = length_text.strip() or "16"
    if not raw.isdigit():
        raise ValueError("Length must be an integer.")
    length = int(raw)
    if not 8 <= length <= 128:
        raise ValueError("Length must be between 8 and 128.")

    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    # Ensure at least one character from each class
    required = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()-_=+"),
    ]
    rest = [secrets.choice(alphabet) for _ in range(length - len(required))]
    combined = required + rest
    secrets.SystemRandom().shuffle(combined)
    return "".join(combined)


async def run_qr(message: Message, raw_text: str) -> None:
    """Generate a QR code image via api.qrserver.com."""
    text = raw_text.strip()
    if not text or len(text) > 1000:
        await send_safe_html(
            message,
            "❌ QR কোডের জন্য লেখা বা লিংক দিন (সর্বোচ্চ ১০০০ অক্ষর)।\n"
            "উদাহরণ: <code>/qr https://example.com</code>",
            reply_markup=result_navigation_keyboard("tools_security"),
        )
        return

    try:
        content, _ = await fetch_bytes(
            "https://api.qrserver.com/v1/create-qr-code/",
            params={"size": "500x500", "data": text},
            expected_content_prefix="image",
        )
        await message.reply_photo(
            photo=content,
            caption="📱 আপনার QR Code তৈরি হয়েছে ✅",
            reply_markup=result_navigation_keyboard("tools_security"),
        )
    except Exception as exc:
        await send_safe_html(
            message,
            safe_error_message(exc),
            reply_markup=result_navigation_keyboard("tools_security"),
        )


async def run_local_tool(message: Message, cmd: str, raw_input: str) -> None:
    """Execute local Python text/crypto/math utility tools."""
    raw = raw_input.strip()
    if cmd != "uuid" and cmd != "password" and not raw:
        await send_safe_html(
            message,
            f"❌ দয়া করে <code>/{cmd}</code> কমান্ডের সাথে ইনপুট দিন।",
            reply_markup=result_navigation_keyboard("tools_security"),
        )
        return

    if len(raw) > MAX_TEXT_INPUT:
        await send_safe_html(
            message,
            f"❌ ইনপুট সর্বোচ্চ {MAX_TEXT_INPUT} অক্ষরের মধ্যে হতে হবে।",
            reply_markup=result_navigation_keyboard("tools_security"),
        )
        return

    extra_note = ""
    try:
        if cmd == "bin":
            result = " ".join(format(b, "08b") for b in raw.encode("utf-8"))
        elif cmd == "unbin":
            bits = raw.split()
            compact = raw.replace(" ", "")
            if len(bits) == 1 and len(compact) % 8 == 0:
                bits = [compact[i : i + 8] for i in range(0, len(compact), 8)]
            if not bits or any(not set(b).issubset({"0", "1"}) for b in bits):
                raise ValueError("Invalid binary")
            result = bytes(int(b, 2) for b in bits).decode("utf-8")
        elif cmd == "b64":
            result = base64.b64encode(raw.encode("utf-8")).decode("ascii")
        elif cmd == "unb64":
            result = base64.b64decode(raw.encode("ascii"), validate=True).decode("utf-8")
        elif cmd == "md5":
            result = hashlib.md5(raw.encode("utf-8")).hexdigest()
            extra_note = (
                "\n\n⚠️ <b>সতর্কতা:</b> MD5 পাসওয়ার্ড নিরাপত্তার জন্য উপযুক্ত নয়; "
                "এটি শুধু সাধারণ ফাইল চেকসাম বা টেস্টিংয়ের জন্য ব্যবহার করুন।"
            )
        elif cmd == "sha256":
            result = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        elif cmd == "sha512":
            result = hashlib.sha512(raw.encode("utf-8")).hexdigest()
        elif cmd == "urlencode":
            result = quote(raw, safe="")
        elif cmd == "urldecode":
            result = unquote(raw)
        elif cmd == "password":
            result = generate_secure_password(raw)
            extra_note = "\n\n🔒 Python <code>secrets</code> মডিউল দিয়ে নিরাপদভাবে তৈরি।"
        elif cmd == "uuid":
            result = str(uuid.uuid4())
        elif cmd == "calc":
            result = str(safe_calculate(raw))
        else:
            await send_safe_html(
                message,
                "❌ অজানা টুল।",
                reply_markup=result_navigation_keyboard("tools_security"),
            )
            return

        reply = f"✅ <b>ফলাফল ({escape_html(cmd.upper())})</b>\n\n<code>{escape_html(result)}</code>{extra_note}"
        await send_safe_html(
            message,
            reply,
            reply_markup=result_navigation_keyboard("tools_security"),
        )
    except Exception:
        await send_safe_html(
            message,
            "❌ সঠিক ইনপুট দিন। উদাহরণ দেখতে /help লিখুন।",
            reply_markup=result_navigation_keyboard("tools_security"),
        )


async def cmd_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_qr(update.effective_message, " ".join(context.args))


async def _make_local_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE, cmd: str) -> None:
    if update.effective_message is None:
        return
    raw = update.effective_message.text.partition(" ")[2] if update.effective_message.text else ""
    await run_local_tool(update.effective_message, cmd, raw)


async def cmd_bin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "bin")


async def cmd_unbin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "unbin")


async def cmd_b64(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "b64")


async def cmd_unb64(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "unb64")


async def cmd_md5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "md5")


async def cmd_sha256(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "sha256")


async def cmd_sha512(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "sha512")


async def cmd_urlencode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "urlencode")


async def cmd_urldecode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "urldecode")


async def cmd_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "password")


async def cmd_uuid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return
    await run_local_tool(update.effective_message, "uuid", "")


async def cmd_calc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _make_local_cmd(update, context, "calc")
