Самокритика:

В спеках v1 и v2 я рекомендовал Grok 4.1 как "дешёвый и сильный" — на PinchBench он 70%, это провал для агентных задач. Исправляю.
DeepSeek V3.2 на агентных задачах — 82.1%, не 90%+ как я подразумевал. Хорош для кода, слабее для tool-calling.
Gemini 2.5 Flash (старый) — всего 76.6%. Heartbeat на нём — нормально, но не для агентных задач.
Gemini 3 Flash — 95.1% при вероятно низкой цене. Это меняет приоритеты.

По формату — моё мнение: не третий спек. Это короткий калибровочный лист — 1 таблица + diff к прошлым конфигам. Спек ради спека — балласт, ты потом не найдёшь главное.

🎯 MODEL CALIBRATION — PinchBench (OpenClaw-specific)
Источник: pinchbench.com | 23 задачи | Судья: Claude Opus + авто-скрипты
МодельScoreНаш tierВердиктopenai-codex/gpt-5.397.8%HEAVYЛучший, дорогойgoogle/gemini-3-flash95.1%MID→TOP🔥 Переводим в основной агентminimax/minimax-m2.193.6%MIDХорош, малоизвестенmoonshotai/kimi-k2.593.4%MID✅ researcher — подтверждёнclaude-sonnet (latest)92.7%HEAVY✅ резерв — подтверждёнclaude-haiku-490.8%MID✅ главный агент — подтверждёнclaude-opus-4.690.6%HEAVYДороже Sonnet, не лучшеopenai/gpt-5-nano85.8%CHEAPАльтернатива Haikuqwen/qwen3-coder-next85.4%CHEAPДля кода, бесплатный?google/gemini-2.5-flash83.2%CHEAPHeartbeat — окdeepseek/deepseek-v3.282.1%CHEAP⚠️ Только код, не агентx-ai/grok-4.1-fast70.0%—❌ Убираем из рекомендацийqwen3-max-thinking40.9%—❌ Катастрофа на агентныхopenrouter/aurora-alpha40.1%—❌ Не использовать

Diff к конфигам v1/v2
Что менять в openclaw.json:
json// БЫЛО (v1/v2):
"primary": "anthropic/claude-haiku-4-5",
"fallbacks": [
  "openrouter/google/gemini-2.5-flash-lite",
  "openrouter/deepseek/deepseek-chat-v3-2",
  ...
]

// СТАЛО (с учётом PinchBench):
"primary": "google/gemini-3-flash",          // 95.1%, вероятно дешевле Haiku
"fallbacks": [
  "anthropic/claude-haiku-4-5",              // 90.8%, надёжный
  "moonshotai/kimi-k2.5",                    // 93.4%, для researcher
  "openrouter/deepseek/deepseek-chat-v3-2"   // 82.1%, только для кода
]

// УБРАТЬ ВЕЗДЕ:
// "x-ai/grok-4.1-fast"    → 70%, плохо для агентных задач
// "qwen3-max-thinking"     → 40.9%, полная непригодность
Агент coder — DeepSeek V3.2 (82.1%) остаётся, но только для генерации кода, не для tool-calling. Для tool-use в коде → Haiku или Gemini 3 Flash.
Агент researcher — Kimi K2.5 (93.4%) подтверждён как лучший выбор в бюджетном диапазоне.
Heartbeat — Gemini 2.5 Flash-Lite (76.6% на агентных) для простых проверок достаточно. Не эскалировать на него сложные задачи.

Единственное что нужно проверить — цена gemini-3-flash. Если он дешевле или сопоставим с Haiku — он становится главным агентом. Зайди на openrouter.ai/google/gemini-3-flash и сравни с $1/$5 (Haiku). Если подтвердится — один sed в конфиге и 5% прироста качества бесплатно.