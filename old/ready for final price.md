 Самокритика
В спеках я рекомендовал Gemini 3 Flash как "вероятно дешёвый" — он $0.72/запуск, дороже Claude Haiku ($0.64). Ошибся. GPT-5-nano я вообще не выделял — а он феноменален. Исправляю.

Value Matrix — Success Rate / Cost
МодельScoreCost/runRatioЗонаgpt-5-nano85.8%$0.032860🏆 Абсолютный чемпионgemini-2.5-flash-lite~76%$0.051520🔥 Heartbeat/фонkimi-k2.593.4%$0.20467✅ Лучший платныйgemini-2.5-flash76.6%$0.20383⚠️ Хуже flash-litegrok-4.1-fast70.0%$0.24292❌ Плохой ratioclaude-haiku-4.590.8%$0.64142✅ Tool-callinggemini-3-flash95.1%$0.72132⚠️ Дороже Haikudeepseek-v3.282.1%$0.73112⚠️ Переоценёнclaude-sonnet-4.592.7%$3.0730💸 Только при необходимостиclaude-opus-4.690.6%$5.8915❌ Хуже Sonnet, дороже
$0.00 модели — либо truly free, либо настолько дешёвые что округляется. claude-sonnet-4 (не 4.5) за $0.00 — похоже кэш/промо от Anthropic на момент замера, не надёжно.

Финальный конфиг по данным PinchBench
json"agents": {
  "defaults": {
    "model": {
      "primary":   "openai/gpt-5-nano",          // 85.8% за $0.03 — основной агент
      "fallbacks": [
        "anthropic/claude-haiku-4-5",            // 90.8% tool-calling
        "moonshotai/kimi-k2.5",                  // 93.4% сложные задачи
        "openrouter/meta-llama/llama-3.3-70b-instruct:free"  // бесплатный fallback
      ]
    },
    "heartbeat": {
      "model": "google/gemini-2.5-flash-lite"    // $0.05, достаточно для проверок
    }
  },
  "list": [
    { "id": "coder",      "model": { "primary": "openai/gpt-5-nano" } },   // пересмотр — лучше DeepSeek по ratio
    { "id": "researcher", "model": { "primary": "moonshotai/kimi-k2.5" } }, // 93.4% — лучший для research
    { "id": "heavy",      "model": { "primary": "anthropic/claude-haiku-4-5" } } // tool-calling, агенты
  ]
}

Главные выводы для бюджета $50
Убрать из всех конфигов: grok-4.1-fast (70% за $0.24 — худший ratio), deepseek-v3.2 как агент (82.1% за $0.73 — дорого для такого score; оставить только для batch-генерации кода офлайн), claude-opus-4.6 (хуже Sonnet и дороже).
Добавить: gpt-5-nano как основной рабочий агент. За $0.03/задачу при 85.8% — это до 1600 агентных задач в месяц за $50. kimi-k2.5 для research и сложных задач ($0.20, 93.4%).
Пересчёт бюджета с новыми данными:
СтатьяСтарый конфигНовый конфигХостинг$4$4~500 агентных задач/мес (основная модель)$320 (Haiku)$15 (gpt-5-nano)~50 сложных задач (researcher)$10 (Kimi)$10 (Kimi, без изменений)Heartbeat 1440/мес$0.15$0.07Итого$334~$29
Haiku как основной агент при 500 задачах — это $320/мес. GPT-5-nano при том же объёме — $15. Разница в 20 раз.