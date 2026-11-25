import { ABOUT, HELP, WELCOME } from "./messages.ts";
import { handleDefine, handleWiki } from "./handlers/study.ts";
import { handleTranslate } from "./handlers/translate.ts";
import { handleWeather } from "./handlers/weather.ts";
import { handleLocalTool, handleQr } from "./handlers/tools.ts";
import {
  handleDns,
  handleIpInfo,
  handleMyIp,
  handleShorten,
  handleSslCheck,
} from "./handlers/web.ts";

export interface BotResponse {
  text?: string;
  photo?: Buffer;
  caption?: string;
  parseMode?: "HTML";
  disableWebPagePreview?: boolean;
  replyMarkup?: unknown;
}

const MAIN_MENU_MARKUP = {
  inline_keyboard: [
    [
      { text: "📚 পড়াশোনা", callback_data: "menu_study" },
      { text: "🌐 অনুবাদ", callback_data: "menu_translate" },
    ],
    [
      { text: "⛅ আবহাওয়া", callback_data: "menu_weather" },
      { text: "🛠️ টুলস", callback_data: "menu_tools" },
    ],
    [
      { text: "🌍 ওয়েব ও নেটওয়ার্ক", callback_data: "menu_web" },
      { text: "❓ সাহায্য", callback_data: "menu_help" },
    ],
    [{ text: "🤖 সম্পর্কে", callback_data: "menu_about" }],
  ],
};

const BACK_MARKUP = {
  inline_keyboard: [[{ text: "⬅️ মূল মেনু", callback_data: "menu_home" }]],
};

export async function dispatchCommand(inputText: string): Promise<BotResponse> {
  const trimmed = inputText.trim();
  if (!trimmed.startsWith("/")) {
    return { text: HELP, parseMode: "HTML", replyMarkup: MAIN_MENU_MARKUP };
  }

  const firstSpace = trimmed.search(/\s/);
  const rawCmd = firstSpace === -1 ? trimmed : trimmed.slice(0, firstSpace);
  const argsText = firstSpace === -1 ? "" : trimmed.slice(firstSpace + 1).trim();
  const cmd = rawCmd.split("@")[0].slice(1).toLowerCase();

  switch (cmd) {
    case "start":
    case "menu":
      return {
        text: WELCOME,
        parseMode: "HTML",
        replyMarkup: MAIN_MENU_MARKUP,
      };
    case "help":
      return {
        text: HELP,
        parseMode: "HTML",
        replyMarkup: MAIN_MENU_MARKUP,
      };
    case "about":
      return {
        text: ABOUT,
        parseMode: "HTML",
        replyMarkup: BACK_MARKUP,
      };
    case "define":
      return { text: await handleDefine(argsText), parseMode: "HTML" };
    case "wiki":
      return {
        text: await handleWiki(argsText, "bn"),
        parseMode: "HTML",
        disableWebPagePreview: true,
      };
    case "wikien":
      return {
        text: await handleWiki(argsText, "en"),
        parseMode: "HTML",
        disableWebPagePreview: true,
      };
    case "tr":
      return { text: await handleTranslate(argsText, "en|bn"), parseMode: "HTML" };
    case "trbn":
      return { text: await handleTranslate(argsText, "bn|en"), parseMode: "HTML" };
    case "weather":
      return { text: await handleWeather(argsText), parseMode: "HTML" };
    case "qr": {
      const qrResult = await handleQr(argsText);
      if (qrResult.content) {
        return { photo: qrResult.content, caption: "📱 আপনার QR Code" };
      }
      return { text: qrResult.error || "⚠️ QR তৈরি করা যায়নি।" };
    }
    case "bin":
    case "unbin":
    case "b64":
    case "unb64":
    case "md5":
    case "sha256":
    case "sha512":
    case "urlencode":
    case "urldecode":
    case "password":
    case "uuid":
    case "calc":
      return { text: handleLocalTool(cmd, argsText), parseMode: "HTML" };
    case "myip":
      return { text: await handleMyIp(), parseMode: "HTML" };
    case "ipinfo":
      return { text: await handleIpInfo(argsText), parseMode: "HTML" };
    case "dns":
      return { text: await handleDns(argsText), parseMode: "HTML" };
    case "ssl":
      return { text: await handleSslCheck(argsText), parseMode: "HTML" };
    case "short":
      return {
        text: await handleShorten(argsText),
        disableWebPagePreview: true,
      };
    default:
      return {
        text: "অজানা কমান্ড। /help লিখে সব কমান্ড দেখুন।",
        replyMarkup: MAIN_MENU_MARKUP,
      };
  }
}

function getCallbackResponse(data: string): BotResponse {
  switch (data) {
    case "menu_home":
      return { text: WELCOME, parseMode: "HTML", replyMarkup: MAIN_MENU_MARKUP };
    case "menu_study":
      return {
        text:
          "📚 <b>পড়াশোনা বিভাগ</b>\n\n" +
          "<code>/define beautiful</code> — ইংরেজি শব্দের অর্থ\n" +
          "<code>/wiki বাংলাদেশ</code> — বাংলা উইকিপিডিয়া\n" +
          "<code>/wikien Python</code> — ইংরেজি উইকিপিডিয়া",
        parseMode: "HTML",
        replyMarkup: BACK_MARKUP,
      };
    case "menu_translate":
      return {
        text:
          "🌐 <b>অনুবাদ বিভাগ</b>\n\n" +
          "<code>/tr Hello world</code> — ইংরেজি থেকে বাংলা\n" +
          "<code>/trbn কেমন আছেন</code> — বাংলা থেকে ইংরেজি",
        parseMode: "HTML",
        replyMarkup: BACK_MARKUP,
      };
    case "menu_weather":
      return {
        text:
          "⛅ <b>আবহাওয়া বিভাগ</b>\n\n" +
          "<code>/weather Rangpur</code> — যেকোনো শহরের বর্তমান আবহাওয়া",
        parseMode: "HTML",
        replyMarkup: BACK_MARKUP,
      };
    case "menu_tools":
      return {
        text:
          "🛠️ <b>টুলস বিভাগ</b>\n\n" +
          "<code>/qr https://example.com</code> — QR Code\n" +
          "<code>/calc 12 * (5 + 3)</code> — ক্যালকুলেটর\n" +
          "<code>/password 16</code> — পাসওয়ার্ড জেনারেটর\n" +
          "<code>/uuid</code> — UUID\n" +
          "<code>/b64 text</code> / <code>/unb64 ...</code>\n" +
          "<code>/bin text</code> / <code>/unbin ...</code>\n" +
          "<code>/md5</code> / <code>/sha256</code> / <code>/sha512</code>\n" +
          "<code>/urlencode</code> / <code>/urldecode</code>",
        parseMode: "HTML",
        replyMarkup: BACK_MARKUP,
      };
    case "menu_web":
      return {
        text:
          "🌍 <b>ওয়েব ও নেটওয়ার্ক বিভাগ</b>\n\n" +
          "<code>/myip</code> — সার্ভার Public IP\n" +
          "<code>/ipinfo 8.8.8.8</code> — IP তথ্য\n" +
          "<code>/dns example.com</code> — DNS Lookup\n" +
          "<code>/ssl example.com</code> — SSL Labs পরীক্ষা\n" +
          "<code>/short https://example.com</code> — লিংক শর্টেনার",
        parseMode: "HTML",
        replyMarkup: BACK_MARKUP,
      };
    case "menu_help":
      return { text: HELP, parseMode: "HTML", replyMarkup: BACK_MARKUP };
    case "menu_about":
      return { text: ABOUT, parseMode: "HTML", replyMarkup: BACK_MARKUP };
    default:
      return { text: WELCOME, parseMode: "HTML", replyMarkup: MAIN_MENU_MARKUP };
  }
}

async function callTelegram(
  token: string,
  method: string,
  payload: Record<string, unknown>
): Promise<unknown> {
  const res = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(35000),
  });
  return res.json();
}

async function sendBotResponse(
  token: string,
  chatId: number,
  response: BotResponse
): Promise<void> {
  if (response.photo) {
    const form = new FormData();
    form.append("chat_id", String(chatId));
    form.append(
      "photo",
      new Blob([new Uint8Array(response.photo)], { type: "image/png" }),
      "qrcode.png"
    );
    if (response.caption) {
      form.append("caption", response.caption);
    }
    await fetch(`https://api.telegram.org/bot${token}/sendPhoto`, {
      method: "POST",
      body: form,
      signal: AbortSignal.timeout(20000),
    });
    return;
  }

  if (response.text) {
    await callTelegram(token, "sendMessage", {
      chat_id: chatId,
      text: response.text,
      parse_mode: response.parseMode,
      disable_web_page_preview: response.disableWebPagePreview,
      reply_markup: response.replyMarkup,
    });
  }
}

interface TelegramUpdate {
  update_id: number;
  message?: {
    chat: { id: number };
    text?: string;
  };
  callback_query?: {
    id: string;
    data?: string;
    message?: {
      chat: { id: number };
      message_id: number;
    };
  };
}

let pollingActive = false;

export function startTelegramBot(): void {
  const token = process.env.BOT_TOKEN?.trim();
  if (!token) {
    console.warn(
      "[FAHIM AI] BOT_TOKEN not configured — Telegram polling skipped; HTTP API active on port 3000"
    );
    return;
  }
  if (pollingActive) return;
  pollingActive = true;

  void (async () => {
    let offset = 0;
    console.log("[FAHIM AI] Telegram polling started");
    while (pollingActive) {
      try {
        const res = (await callTelegram(token, "getUpdates", {
          offset,
          timeout: 25,
          allowed_updates: ["message", "callback_query"],
        })) as { ok?: boolean; result?: TelegramUpdate[] };

        if (!res.ok || !Array.isArray(res.result)) {
          await new Promise((r) => setTimeout(r, 3000));
          continue;
        }

        for (const update of res.result) {
          offset = update.update_id + 1;
          if (update.message?.text) {
            const resp = await dispatchCommand(update.message.text);
            await sendBotResponse(token, update.message.chat.id, resp);
          } else if (update.callback_query) {
            const cq = update.callback_query;
            await callTelegram(token, "answerCallbackQuery", {
              callback_query_id: cq.id,
            });
            if (cq.message && cq.data) {
              const resp = getCallbackResponse(cq.data);
              await callTelegram(token, "editMessageText", {
                chat_id: cq.message.chat.id,
                message_id: cq.message.message_id,
                text: resp.text,
                parse_mode: resp.parseMode,
                reply_markup: resp.replyMarkup,
              });
            }
          }
        }
      } catch (err) {
        console.warn("[FAHIM AI] Telegram polling error:", err);
        await new Promise((r) => setTimeout(r, 5000));
      }
    }
  })();
}
