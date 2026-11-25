import { escapeHtml, getJson, safeError } from "../utils/api.ts";

interface MyMemoryResponse {
  responseData?: {
    translatedText?: string;
  };
}

export async function handleTranslate(
  rawText: string,
  pair: "en|bn" | "bn|en" = "en|bn"
): Promise<string> {
  const text = rawText.trim();
  if (!text) {
    return "অনুবাদের লেখা দিন। উদাহরণ: /tr Hello";
  }
  try {
    const data = await getJson<MyMemoryResponse>(
      "https://api.mymemory.translated.net/get",
      { q: text, langpair: pair }
    );
    const result = data.responseData?.translatedText;
    if (!result) {
      throw new Error("empty translation");
    }
    return `🌐 <b>অনুবাদ</b>\n\n${escapeHtml(result)}`;
  } catch (err) {
    return "⚠️ " + safeError(err);
  }
}
