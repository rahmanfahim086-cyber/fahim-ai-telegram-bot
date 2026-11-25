import { escapeHtml, getJson, safeError } from "../utils/api.ts";

interface IpApiResponse {
  ip?: string;
  country_name?: string;
  city?: string;
  org?: string;
}

interface IpWhoResponse {
  success?: boolean;
  ip?: string;
  country?: string;
  city?: string;
  region?: string;
  connection?: {
    isp?: string;
  };
}

interface DnsResponse {
  Answer?: Array<{
    data?: string;
  }>;
}

interface SslLabsResponse {
  status?: string;
  endpoints?: Array<{
    grade?: string;
    statusMessage?: string;
  }>;
}

interface IsGdResponse {
  shorturl?: string;
}

export async function handleMyIp(): Promise<string> {
  try {
    const d = await getJson<IpApiResponse>("https://ipapi.co/json/");
    return (
      `🌍 <b>আপনার Public IP</b>\n` +
      `IP: ${escapeHtml(d.ip || "N/A")}\n` +
      `দেশ: ${escapeHtml(d.country_name || "N/A")}\n` +
      `শহর: ${escapeHtml(d.city || "N/A")}\n` +
      `ISP: ${escapeHtml(d.org || "N/A")}`
    );
  } catch (err) {
    return "⚠️ " + safeError(err);
  }
}

export async function handleIpInfo(rawIp: string): Promise<string> {
  const ip = rawIp.trim().split(/\s+/)[0] || "";
  if (!ip) {
    return "ব্যবহার: /ipinfo 8.8.8.8";
  }
  try {
    const d = await getJson<IpWhoResponse>(
      `https://ipwho.is/${encodeURIComponent(ip)}`
    );
    if (d.success === false) {
      throw new Error("IP lookup failed");
    }
    return (
      `🔎 <b>IP তথ্য</b>\n` +
      `IP: ${escapeHtml(d.ip || "N/A")}\n` +
      `দেশ: ${escapeHtml(d.country || "N/A")}\n` +
      `শহর: ${escapeHtml(d.city || "N/A")}\n` +
      `অঞ্চল: ${escapeHtml(d.region || "N/A")}\n` +
      `ISP: ${escapeHtml(d.connection?.isp || "N/A")}`
    );
  } catch (err) {
    return "⚠️ " + safeError(err);
  }
}

export async function handleDns(rawDomain: string): Promise<string> {
  const domain = rawDomain.trim().split(/\s+/)[0] || "";
  if (!domain) {
    return "ব্যবহার: /dns example.com";
  }
  try {
    const chunks: string[] = [];
    for (const typ of ["A", "AAAA", "MX", "TXT", "NS"]) {
      const data = await getJson<DnsResponse>("https://dns.google/resolve", {
        name: domain,
        type: typ,
      });
      const answers = data.Answer || [];
      chunks.push(
        `<b>${typ}</b>: ` +
          (answers.length > 0
            ? answers
                .slice(0, 8)
                .map((a) => escapeHtml(a.data || ""))
                .join(", ")
            : "রেকর্ড পাওয়া যায়নি")
      );
    }
    return `🧭 <b>DNS Lookup: ${escapeHtml(domain)}</b>\n\n${chunks.join("\n")}`;
  } catch (err) {
    return "⚠️ " + safeError(err);
  }
}

export async function handleSslCheck(rawDomain: string): Promise<string> {
  const domain = rawDomain.trim().split(/\s+/)[0] || "";
  if (!domain) {
    return "ব্যবহার: /ssl example.com";
  }
  try {
    const d = await getJson<SslLabsResponse>(
      "https://api.ssllabs.com/api/v3/analyze",
      { host: domain, publish: "off", all: "done" }
    );
    const endpoints = d.endpoints || [];
    const grades =
      endpoints
        .map(
          (e) =>
            `${escapeHtml(e.grade || "N/A")} (${escapeHtml(e.statusMessage || "")})`
        )
        .join(", ") || "পরীক্ষা চলছে বা ফলাফল এখনো পাওয়া যায়নি";
    return (
      `🔐 <b>SSL Labs: ${escapeHtml(domain)}</b>\n` +
      `Status: ${escapeHtml(d.status || "N/A")}\n` +
      `ফলাফল: ${grades}\n\n` +
      `SSL Labs-এর বিশ্লেষণে কয়েক মিনিট লাগতে পারে।`
    );
  } catch (err) {
    return "⚠️ " + safeError(err);
  }
}

export async function handleShorten(rawUrl: string): Promise<string> {
  const url = rawUrl.trim();
  if (!url) {
    return "ব্যবহার: /short https://example.com";
  }
  try {
    const d = await getJson<IsGdResponse>("https://is.gd/create.php", {
      format: "json",
      url,
    });
    if (!d.shorturl) {
      throw new Error("No shorturl returned");
    }
    return `🔗 ছোট লিংক:\n${d.shorturl}`;
  } catch (err) {
    return "⚠️ " + safeError(err);
  }
}
