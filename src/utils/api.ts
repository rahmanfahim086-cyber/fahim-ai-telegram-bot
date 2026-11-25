export async function getJson<T = unknown>(
  url: string,
  params?: Record<string, string | number>
): Promise<T> {
  const target = new URL(url);
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      target.searchParams.set(k, String(v));
    }
  }
  const response = await fetch(target.toString(), {
    headers: {
      "User-Agent": "FAHIM-AI-Bot/1.0",
      Accept: "application/json",
    },
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return (await response.json()) as T;
}

export async function getBytes(
  url: string,
  params?: Record<string, string | number>
): Promise<{ content: Buffer; contentType: string }> {
  const target = new URL(url);
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      target.searchParams.set(k, String(v));
    }
  }
  const response = await fetch(target.toString(), {
    headers: {
      "User-Agent": "FAHIM-AI-Bot/1.0",
    },
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const arrayBuffer = await response.arrayBuffer();
  return {
    content: Buffer.from(arrayBuffer),
    contentType: response.headers.get("content-type") ?? "",
  };
}

export function safeError(err: unknown): string {
  if (err instanceof Error) {
    if (err.name === "TimeoutError" || err.name === "AbortError") {
      return "সার্ভার থেকে উত্তর আসতে বেশি সময় লাগছে। পরে আবার চেষ্টা করুন।";
    }
    if (err.message.startsWith("HTTP 404")) {
      return "তথ্য খুঁজে পাওয়া যায়নি।";
    }
    if (err.message.startsWith("HTTP ")) {
      return `তথ্য আনতে সমস্যা হয়েছে (${err.message})।`;
    }
  }
  return "একটি সমস্যা হয়েছে। অনুগ্রহ করে পরে আবার চেষ্টা করুন।";
}

export function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
