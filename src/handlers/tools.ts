import crypto from "node:crypto";
import { escapeHtml, getBytes, safeError } from "../utils/api.ts";

export async function handleQr(
  rawText: string
): Promise<{ content?: Buffer; contentType?: string; error?: string }> {
  const text = rawText.trim();
  if (!text) {
    return { error: "ব্যবহার: /qr আপনার লেখা বা লিংক" };
  }
  try {
    const { content, contentType } = await getBytes(
      "https://api.qrserver.com/v1/create-qr-code/",
      { size: "500x500", data: text }
    );
    if (!contentType.includes("image")) {
      throw new Error("Invalid image response");
    }
    return { content, contentType };
  } catch (err) {
    return { error: "⚠️ " + safeError(err) };
  }
}

export function safeCalculate(expression: string): number {
  if (!expression || expression.length > 100) {
    throw new Error("Invalid expression");
  }

  let pos = 0;
  const src = expression;

  function skipWhitespace() {
    while (pos < src.length && /\s/.test(src[pos])) pos++;
  }

  function parseExpression(): number {
    let left = parseTerm();
    while (true) {
      skipWhitespace();
      const ch = src[pos];
      if (ch === "+" || ch === "-") {
        pos++;
        const right = parseTerm();
        left = ch === "+" ? left + right : left - right;
      } else {
        break;
      }
    }
    return left;
  }

  function parseTerm(): number {
    let left = parsePower();
    while (true) {
      skipWhitespace();
      if (src.startsWith("//", pos)) {
        pos += 2;
        const right = parsePower();
        if (right === 0) throw new Error("Division by zero");
        left = Math.floor(left / right);
      } else if (src[pos] === "*" && src[pos + 1] !== "*") {
        pos++;
        left = left * parsePower();
      } else if (src[pos] === "/") {
        pos++;
        const right = parsePower();
        if (right === 0) throw new Error("Division by zero");
        left = left / right;
      } else if (src[pos] === "%") {
        pos++;
        const right = parsePower();
        if (right === 0) throw new Error("Modulo by zero");
        left = ((left % right) + right) % right;
      } else {
        break;
      }
    }
    return left;
  }

  function parsePower(): number {
    const base = parseUnary();
    skipWhitespace();
    if (src.startsWith("**", pos)) {
      pos += 2;
      const exponent = parsePower();
      if (Math.abs(exponent) > 10) {
        throw new Error("Exponent too large");
      }
      return Math.pow(base, exponent);
    }
    return base;
  }

  function parseUnary(): number {
    skipWhitespace();
    if (src[pos] === "+") {
      pos++;
      return parseUnary();
    }
    if (src[pos] === "-") {
      pos++;
      return -parseUnary();
    }
    return parsePrimary();
  }

  function parsePrimary(): number {
    skipWhitespace();
    if (src[pos] === "(") {
      pos++;
      const val = parseExpression();
      skipWhitespace();
      if (src[pos] !== ")") {
        throw new Error("Mismatched parentheses");
      }
      pos++;
      return val;
    }
    const match = src.slice(pos).match(/^(?:\d+\.?\d*|\.\d+)/);
    if (!match) {
      throw new Error("Expected number");
    }
    pos += match[0].length;
    const num = Number(match[0]);
    if (!Number.isFinite(num)) {
      throw new Error("Invalid number");
    }
    return num;
  }

  const value = parseExpression();
  skipWhitespace();
  if (pos !== src.length) {
    throw new Error("Unexpected trailing characters");
  }
  if (!Number.isFinite(value) || Math.abs(value) > 1e100) {
    throw new Error("Result out of bounds");
  }
  return value;
}

export function handleLocalTool(cmd: string, rawInput: string): string {
  const command = cmd.toLowerCase();
  const raw = rawInput.trim();
  try {
    let result: string;
    if (command === "bin") {
      result = Array.from(Buffer.from(raw, "utf8"))
        .map((b) => b.toString(2).padStart(8, "0"))
        .join(" ");
    } else if (command === "unbin") {
      let bits = raw.split(/\s+/).filter(Boolean);
      const compact = raw.replace(/\s+/g, "");
      if (bits.length <= 1 && compact.length > 0 && compact.length % 8 === 0) {
        bits = compact.match(/.{8}/g) || [];
      }
      if (bits.length === 0) throw new Error("Empty binary input");
      const bytes = bits.map((b) => {
        if (!/^[01]+$/.test(b)) throw new Error("Invalid binary");
        return parseInt(b, 2);
      });
      result = Buffer.from(bytes).toString("utf8");
    } else if (command === "b64") {
      result = Buffer.from(raw, "utf8").toString("base64");
    } else if (command === "unb64") {
      const cleaned = raw.replace(/\s+/g, "");
      if (!/^[A-Za-z0-9+/]*={0,2}$/.test(cleaned) || cleaned.length % 4 !== 0) {
        throw new Error("Invalid base64");
      }
      result = Buffer.from(cleaned, "base64").toString("utf8");
    } else if (command === "md5" || command === "sha256" || command === "sha512") {
      if (!raw) throw new Error("Empty input");
      result = crypto.createHash(command).update(raw, "utf8").digest("hex");
    } else if (command === "urlencode") {
      result = encodeURIComponent(raw);
    } else if (command === "urldecode") {
      result = decodeURIComponent(raw);
    } else if (command === "password") {
      const n = Number.parseInt(raw || "16", 10);
      if (!Number.isInteger(n) || n < 8 || n > 128 || (raw && !/^\d+$/.test(raw))) {
        throw new Error("Invalid length");
      }
      const alphabet =
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+";
      let out = "";
      for (let i = 0; i < n; i++) {
        out += alphabet[crypto.randomInt(0, alphabet.length)];
      }
      result = out;
    } else if (command === "uuid") {
      result = crypto.randomUUID();
    } else if (command === "calc") {
      result = String(safeCalculate(raw));
    } else {
      return "অজানা টুল।";
    }
    return `✅ <b>ফলাফল</b>\n<code>${escapeHtml(result)}</code>`;
  } catch {
    return "⚠️ ইনপুট সঠিক নয়। /help দেখে সঠিক ব্যবহার লিখুন।";
  }
}
