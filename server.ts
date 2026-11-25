import "dotenv/config";
import path from "node:path";
import express from "express";
import { ABOUT, HELP, WELCOME } from "./src/messages.ts";
import { dispatchCommand, startTelegramBot } from "./src/bot.ts";
import { handleDefine, handleWiki } from "./src/handlers/study.ts";
import { handleTranslate } from "./src/handlers/translate.ts";
import { handleWeather } from "./src/handlers/weather.ts";
import { handleLocalTool, handleQr } from "./src/handlers/tools.ts";
import {
  handleDns,
  handleIpInfo,
  handleMyIp,
  handleShorten,
  handleSslCheck,
} from "./src/handlers/web.ts";

const app = express();
app.use(express.json());

const ZIP_FILE_PATH = path.resolve(
  process.cwd(),
  "public",
  "FAHIM_AI_Telegram_Bot.zip"
);

app.get("/download/FAHIM_AI_Telegram_Bot.zip", (_req, res) => {
  res.download(ZIP_FILE_PATH, "FAHIM_AI_Telegram_Bot.zip");
});

app.get("/FAHIM_AI_Telegram_Bot.zip", (_req, res) => {
  res.download(ZIP_FILE_PATH, "FAHIM_AI_Telegram_Bot.zip");
});

app.get("/", (_req, res) => {
  res.status(200).type("html").send(`<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FAHIM AI Telegram Bot — Project ZIP</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; background: #0f1115; color: #e6edf3; margin: 0; padding: 20px; line-height: 1.6; }
    .card { max-width: 720px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 14px; padding: 24px; }
    h1 { margin-top: 0; font-size: 1.5rem; color: #ffffff; }
    .btn { display: inline-block; background: #238636; color: #ffffff; text-decoration: none; font-weight: 600; padding: 14px 20px; border-radius: 10px; margin: 12px 0 20px; }
    .btn:hover { background: #2ea043; }
    pre { background: #0d1117; border: 1px solid #30363d; border-radius: 10px; padding: 14px; overflow-x: auto; font-size: 0.88rem; color: #c9d1d9; }
    .note { background: #1c2128; border-left: 4px solid #58a6ff; padding: 12px 14px; border-radius: 6px; font-size: 0.92rem; }
  </style>
</head>
<body>
  <div class="card">
    <h1>🤖 FAHIM AI — All-in-One Telegram Bot</h1>
    <p>ডেভেলপার: <strong>MD FAHIM RAHMAN</strong> • Python 3.12 • python-telegram-bot v21+ • Flask + Gunicorn</p>
    <a class="btn" href="/download/FAHIM_AI_Telegram_Bot.zip" download>⬇️ FAHIM_AI_Telegram_Bot.zip ডাউনলোড করুন (২১টি ফাইল)</a>
    <div class="note">
      <strong>গুরুত্বপূর্ণ:</strong> কোনো অতিরিক্ত বাহ্যিক API Key প্রয়োজন নেই। শুধুমাত্র Telegram <code>BOT_TOKEN</code> Render Environment Variables-এ দিলেই বট চলবে।
    </div>
    <h3>📁 প্রজেক্ট ফোল্ডার স্ট্রাকচার</h3>
    <pre>FAHIM_AI_Telegram_Bot/
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
    └── fun.py</pre>
  </div>
</body>
</html>`);
});

app.get("/healthz", (_req, res) => {
  res.status(200).json({ status: "healthy" });
});

app.get("/api/messages", (_req, res) => {
  res.json({ welcome: WELCOME, help: HELP, about: ABOUT });
});

app.post("/api/command", async (req, res) => {
  const command =
    typeof req.body?.command === "string" ? req.body.command : "";
  if (!command.trim()) {
    res.status(400).json({ error: "Missing command string" });
    return;
  }
  const result = await dispatchCommand(command);
  if (result.photo) {
    res.json({
      caption: result.caption,
      photoBase64: result.photo.toString("base64"),
      mimeType: "image/png",
    });
    return;
  }
  res.json({ text: result.text ?? "", parseMode: result.parseMode });
});

app.get("/api/define", async (req, res) => {
  const word = typeof req.query.word === "string" ? req.query.word : "";
  res.json({ result: await handleDefine(word) });
});

app.get("/api/wiki", async (req, res) => {
  const topic = typeof req.query.topic === "string" ? req.query.topic : "";
  const lang = req.query.lang === "en" ? "en" : "bn";
  res.json({ result: await handleWiki(topic, lang) });
});

app.get("/api/tr", async (req, res) => {
  const text = typeof req.query.text === "string" ? req.query.text : "";
  const pair = req.query.pair === "bn|en" ? "bn|en" : "en|bn";
  res.json({ result: await handleTranslate(text, pair) });
});

app.get("/api/weather", async (req, res) => {
  const city = typeof req.query.city === "string" ? req.query.city : "";
  res.json({ result: await handleWeather(city) });
});

app.get("/api/tools/qr", async (req, res) => {
  const text = typeof req.query.text === "string" ? req.query.text : "";
  const qr = await handleQr(text);
  if (qr.content) {
    res.setHeader("Content-Type", qr.contentType || "image/png");
    res.send(qr.content);
    return;
  }
  res.status(400).json({ error: qr.error || "Failed to generate QR code" });
});

app.get("/api/tools/:cmd", (req, res) => {
  const input = typeof req.query.input === "string" ? req.query.input : "";
  res.json({ result: handleLocalTool(req.params.cmd, input) });
});

app.post("/api/tools/:cmd", (req, res) => {
  const input = typeof req.body?.input === "string" ? req.body.input : "";
  res.json({ result: handleLocalTool(req.params.cmd, input) });
});

app.get("/api/web/myip", async (_req, res) => {
  res.json({ result: await handleMyIp() });
});

app.get("/api/web/ipinfo", async (req, res) => {
  const ip = typeof req.query.ip === "string" ? req.query.ip : "";
  res.json({ result: await handleIpInfo(ip) });
});

app.get("/api/web/dns", async (req, res) => {
  const domain = typeof req.query.domain === "string" ? req.query.domain : "";
  res.json({ result: await handleDns(domain) });
});

app.get("/api/web/ssl", async (req, res) => {
  const domain = typeof req.query.domain === "string" ? req.query.domain : "";
  res.json({ result: await handleSslCheck(domain) });
});

app.get("/api/web/short", async (req, res) => {
  const url = typeof req.query.url === "string" ? req.query.url : "";
  res.json({ result: await handleShorten(url) });
});

const port = Number(process.env.PORT) || 3000;
app.listen(port, "0.0.0.0", () => {
  console.log(`[FAHIM AI] Server listening on http://0.0.0.0:${port}`);
  startTelegramBot();
});
