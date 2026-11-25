"""Inline keyboard builders for FAHIM AI Telegram Bot."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Return the main category menu keyboard."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🌐 Translate & Study", callback_data="menu:translate_study"),
                InlineKeyboardButton("⛅ Weather & Info", callback_data="menu:weather_info"),
            ],
            [
                InlineKeyboardButton("💱 Finance & Crypto", callback_data="menu:finance_crypto"),
                InlineKeyboardButton("🌍 Web & Network", callback_data="menu:web_network"),
            ],
            [
                InlineKeyboardButton("📱 Tools & Security", callback_data="menu:tools_security"),
                InlineKeyboardButton("🎬 Entertainment", callback_data="menu:entertainment"),
            ],
            [
                InlineKeyboardButton("⚙️ Bot Info", callback_data="menu:bot_info"),
            ],
        ]
    )


def _with_navigation(rows: list[list[InlineKeyboardButton]], back_target: str = "menu:main") -> InlineKeyboardMarkup:
    """Append Back and Main Menu buttons to every submenu."""
    nav_row = [
        InlineKeyboardButton("🔙 পেছনে যান", callback_data=back_target),
        InlineKeyboardButton("🏠 মূল মেনু", callback_data="menu:main"),
    ]
    return InlineKeyboardMarkup([*rows, nav_row])


def translate_study_keyboard() -> InlineKeyboardMarkup:
    return _with_navigation(
        [
            [
                InlineKeyboardButton("🌐 Translate", callback_data="prompt:tr"),
                InlineKeyboardButton("🌐 Translate BN→EN", callback_data="prompt:trbn"),
            ],
            [
                InlineKeyboardButton("📖 Dictionary", callback_data="prompt:define"),
                InlineKeyboardButton("📚 Wikipedia", callback_data="prompt:wiki"),
            ],
            [
                InlineKeyboardButton("🌐 English Wiki", callback_data="prompt:wikien"),
            ],
        ]
    )


def weather_info_keyboard() -> InlineKeyboardMarkup:
    return _with_navigation(
        [
            [
                InlineKeyboardButton("⛅ Weather", callback_data="prompt:weather"),
                InlineKeyboardButton("🕒 Bangladesh Time", callback_data="instant:time"),
            ],
            [
                InlineKeyboardButton("🧠 Fact", callback_data="instant:fact"),
                InlineKeyboardButton("🧭 Advice", callback_data="instant:advice"),
            ],
            [
                InlineKeyboardButton("👤 Demo User", callback_data="instant:demo"),
            ],
        ]
    )


def finance_crypto_keyboard() -> InlineKeyboardMarkup:
    return _with_navigation(
        [
            [
                InlineKeyboardButton("💱 Currency", callback_data="prompt:currency"),
                InlineKeyboardButton("🪙 Crypto", callback_data="prompt:crypto"),
            ],
        ]
    )


def web_network_keyboard() -> InlineKeyboardMarkup:
    return _with_navigation(
        [
            [
                InlineKeyboardButton("🌍 My IP", callback_data="instant:ip"),
                InlineKeyboardButton("🔎 IP Lookup", callback_data="prompt:ipinfo"),
            ],
            [
                InlineKeyboardButton("🧭 DNS Lookup", callback_data="prompt:dns"),
                InlineKeyboardButton("🔐 SSL Checker", callback_data="prompt:ssl"),
            ],
            [
                InlineKeyboardButton("🔗 Short URL", callback_data="prompt:short"),
                InlineKeyboardButton("🐙 GitHub User", callback_data="prompt:github"),
            ],
            [
                InlineKeyboardButton("📦 GitHub Repo", callback_data="prompt:repo"),
                InlineKeyboardButton("🌐 HTTP Test", callback_data="prompt:http"),
            ],
            [
                InlineKeyboardButton("🧪 JSON Test", callback_data="instant:json"),
            ],
        ]
    )


def tools_security_keyboard() -> InlineKeyboardMarkup:
    return _with_navigation(
        [
            [
                InlineKeyboardButton("📱 QR Code", callback_data="prompt:qr"),
                InlineKeyboardButton("🧮 Calculator", callback_data="prompt:calc"),
            ],
            [
                InlineKeyboardButton("🔢 Binary Encode", callback_data="prompt:bin"),
                InlineKeyboardButton("🔤 Binary Decode", callback_data="prompt:unbin"),
            ],
            [
                InlineKeyboardButton("🧬 Base64 Encode", callback_data="prompt:b64"),
                InlineKeyboardButton("🧬 Base64 Decode", callback_data="prompt:unb64"),
            ],
            [
                InlineKeyboardButton("🔐 MD5", callback_data="prompt:md5"),
                InlineKeyboardButton("🔐 SHA256", callback_data="prompt:sha256"),
            ],
            [
                InlineKeyboardButton("🔐 SHA512", callback_data="prompt:sha512"),
                InlineKeyboardButton("🔑 Password", callback_data="prompt:password"),
            ],
            [
                InlineKeyboardButton("🔗 URL Encode", callback_data="prompt:urlencode"),
                InlineKeyboardButton("🔗 URL Decode", callback_data="prompt:urldecode"),
            ],
            [
                InlineKeyboardButton("🆔 UUID", callback_data="instant:uuid"),
            ],
        ]
    )


def entertainment_keyboard() -> InlineKeyboardMarkup:
    return _with_navigation(
        [
            [
                InlineKeyboardButton("😂 Joke", callback_data="instant:joke"),
                InlineKeyboardButton("💡 Quote", callback_data="instant:quote"),
            ],
            [
                InlineKeyboardButton("🐱 Cat", callback_data="instant:cat"),
                InlineKeyboardButton("🐶 Dog", callback_data="instant:dog"),
            ],
            [
                InlineKeyboardButton("🎌 Anime", callback_data="prompt:anime"),
                InlineKeyboardButton("📖 Manga", callback_data="prompt:manga"),
            ],
            [
                InlineKeyboardButton("⚡ Pokemon", callback_data="prompt:pokemon"),
            ],
        ]
    )


def bot_info_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📊 Bot Status", callback_data="info:status"),
                InlineKeyboardButton("ℹ️ About", callback_data="info:about"),
            ],
            [
                InlineKeyboardButton("❓ Help", callback_data="info:help"),
                InlineKeyboardButton("🔙 মূল মেনু", callback_data="menu:main"),
            ],
        ]
    )


def prompt_cancel_keyboard(submenu_key: str) -> InlineKeyboardMarkup:
    """Keyboard shown while waiting for user input."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❌ বাতিল করুন", callback_data="action:cancel"),
                InlineKeyboardButton("🔙 পেছনে যান", callback_data=f"menu:{submenu_key}"),
            ],
            [
                InlineKeyboardButton("🏠 মূল মেনু", callback_data="menu:main"),
            ],
        ]
    )


def result_navigation_keyboard(submenu_key: str) -> InlineKeyboardMarkup:
    """Quick navigation keyboard shown after completing a feature."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔙 বিভাগে ফিরুন", callback_data=f"menu:{submenu_key}"),
                InlineKeyboardButton("🏠 মূল মেনু", callback_data="menu:main"),
            ]
        ]
    )


SUBMENU_KEYBOARD_MAP = {
    "translate_study": translate_study_keyboard,
    "weather_info": weather_info_keyboard,
    "finance_crypto": finance_crypto_keyboard,
    "web_network": web_network_keyboard,
    "tools_security": tools_security_keyboard,
    "entertainment": entertainment_keyboard,
    "bot_info": bot_info_keyboard,
}

FEATURE_SUBMENU_MAP = {
    "tr": "translate_study",
    "trbn": "translate_study",
    "define": "translate_study",
    "wiki": "translate_study",
    "wikien": "translate_study",
    "weather": "weather_info",
    "time": "weather_info",
    "fact": "weather_info",
    "advice": "weather_info",
    "demo": "weather_info",
    "currency": "finance_crypto",
    "crypto": "finance_crypto",
    "ip": "web_network",
    "ipinfo": "web_network",
    "dns": "web_network",
    "ssl": "web_network",
    "short": "web_network",
    "github": "web_network",
    "repo": "web_network",
    "http": "web_network",
    "json": "web_network",
    "qr": "tools_security",
    "bin": "tools_security",
    "unbin": "tools_security",
    "b64": "tools_security",
    "unb64": "tools_security",
    "md5": "tools_security",
    "sha256": "tools_security",
    "sha512": "tools_security",
    "urlencode": "tools_security",
    "urldecode": "tools_security",
    "password": "tools_security",
    "uuid": "tools_security",
    "calc": "tools_security",
    "joke": "entertainment",
    "quote": "entertainment",
    "cat": "entertainment",
    "dog": "entertainment",
    "anime": "entertainment",
    "manga": "entertainment",
    "pokemon": "entertainment",
}
