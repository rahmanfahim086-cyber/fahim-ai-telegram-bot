import { escapeHtml, getJson, safeError } from "../utils/api.ts";

interface DictionaryEntry {
  word?: string;
  phonetic?: string;
  meanings?: Array<{
    partOfSpeech?: string;
    definitions?: Array<{
      definition?: string;
      example?: string;
    }>;
  }>;
}

interface WikiSummary {
  title?: string;
  extract?: string;
  content_urls?: {
    desktop?: {
      page?: string;
    };
  };
}

export async function handleDefine(rawWord: string): Promise<string> {
  const word = rawWord.trim();
  if (!word) {
    return "শব্দ দিন। উদাহরণ: /define beautiful";
  }
  try {
    const data = await getJson<DictionaryEntry[]>(
      `https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`
    );
    const entry = data[0];
    if (!entry) {
      return "তথ্য খুঁজে পাওয়া যায়নি।";
    }
    const phon = entry.phonetic || "পাওয়া যায়নি";
    const lines: string[] = [
      `📖 <b>${escapeHtml(entry.word || word)}</b>`,
      `উচ্চারণ: ${escapeHtml(phon)}`,
    ];
    for (const meaning of (entry.meanings || []).slice(0, 3)) {
      lines.push(`\n<b>${escapeHtml(meaning.partOfSpeech || "")}</b>`);
      for (const def of (meaning.definitions || []).slice(0, 2)) {
        lines.push(`• ${escapeHtml(def.definition || "")}`);
        if (def.example) {
          lines.push(`উদাহরণ: ${escapeHtml(def.example)}`);
        }
      }
    }
    return lines.join("\n").slice(0, 4000);
  } catch (err) {
    return "⚠️ " + safeError(err);
  }
}

export async function handleWiki(
  rawTopic: string,
  lang: "bn" | "en" = "bn"
): Promise<string> {
  const topic = rawTopic.trim();
  if (!topic) {
    return "বিষয় লিখুন।";
  }
  try {
    const slug = encodeURIComponent(topic.replace(/ /g, "_"));
    const data = await getJson<WikiSummary>(
      `https://${lang}.wikipedia.org/api/rest_v1/page/summary/${slug}`
    );
    let text = `📚 <b>${escapeHtml(data.title || topic)}</b>\n\n${escapeHtml(
      data.extract || "তথ্য পাওয়া যায়নি"
    )}`;
    const pageUrl = data.content_urls?.desktop?.page;
    if (pageUrl) {
      text += `\n\n${pageUrl}`;
    }
    return text.slice(0, 4000);
  } catch (err) {
    return "⚠️ " + safeError(err);
  }
}
