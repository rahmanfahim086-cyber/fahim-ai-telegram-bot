import { escapeHtml, getJson, safeError } from "../utils/api.ts";

interface GeocodingResponse {
  results?: Array<{
    name?: string;
    country?: string;
    latitude: number;
    longitude: number;
  }>;
}

interface ForecastResponse {
  current_weather?: {
    temperature?: number;
    windspeed?: number;
    winddirection?: number;
    time?: string;
  };
}

export async function handleWeather(rawCity: string): Promise<string> {
  const city = rawCity.trim();
  if (!city) {
    return "শহরের নাম দিন। উদাহরণ: /weather Rangpur";
  }
  try {
    const geo = await getJson<GeocodingResponse>(
      "https://geocoding-api.open-meteo.com/v1/search",
      {
        name: city,
        count: 1,
        language: "en",
        format: "json",
      }
    );
    const results = geo.results || [];
    if (results.length === 0) {
      return "এই শহরটি খুঁজে পাওয়া যায়নি।";
    }
    const place = results[0];
    const data = await getJson<ForecastResponse>(
      "https://api.open-meteo.com/v1/forecast",
      {
        latitude: place.latitude,
        longitude: place.longitude,
        current_weather: "true",
      }
    );
    const cw = data.current_weather || {};
    return (
      `⛅ <b>${escapeHtml(place.name || city)}, ${escapeHtml(place.country || "")}</b>\n` +
      `🌡️ তাপমাত্রা: ${cw.temperature ?? "N/A"}°C\n` +
      `💨 বাতাসের গতি: ${cw.windspeed ?? "N/A"} km/h\n` +
      `🧭 বাতাসের দিক: ${cw.winddirection ?? "N/A"}°\n` +
      `🕒 পর্যবেক্ষণের সময়: ${cw.time ?? "N/A"}`
    );
  } catch (err) {
    return "⚠️ " + safeError(err);
  }
}
