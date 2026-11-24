"""Shared async HTTP helpers for public, no-key APIs."""
import httpx

TIMEOUT = httpx.Timeout(30.0, connect=10.0)
HEADERS = {"User-Agent": "FAHIM-AI-Telegram-Bot/1.0 (public API client)"}

async def get_json(url: str, params=None):
    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS, follow_redirects=True) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

async def get_text(url: str, params=None):
    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS, follow_redirects=True) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.text

async def get_bytes(url: str, params=None):
    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS, follow_redirects=True) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.content, response.headers.get("content-type", "")

def safe_error(exc: Exception) -> str:
    if isinstance(exc, httpx.TimeoutException):
        return "অনুরোধের সময় শেষ হয়েছে। কিছুক্ষণ পরে আবার চেষ্টা করুন।"
    if isinstance(exc, httpx.HTTPStatusError):
        return f"সার্ভার HTTP {exc.response.status_code} ত্রুটি দিয়েছে। পরে আবার চেষ্টা করুন।"
    if isinstance(exc, httpx.RequestError):
        return "API সার্ভারের সঙ্গে সংযোগ করা যায়নি। API সাময়িকভাবে বন্ধ থাকতে পারে।"
    if isinstance(exc, (ValueError, KeyError)):
        return "API থেকে পাওয়া তথ্য সঠিক ফরম্যাটে নেই।"
    return "দুঃখিত, অনুরোধটি সম্পন্ন করা যায়নি। ইনপুট পরীক্ষা করে আবার চেষ্টা করুন।"
