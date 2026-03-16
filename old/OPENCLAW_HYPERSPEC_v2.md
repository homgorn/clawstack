# 🦞 OPENCLAW HYPERSPEC — ДОПОЛНЕНИЕ v2.0
> Март 2026 | gws CLI (выпущен 06.03.2026) | Авто-ресёрч агент | Weekly Update Module

---

## ⚖️ ИСПРАВЛЕНИЯ К СПЕКУ v1.0

1. `"bind": "loopback"` **недостаточно** без `auth.secret` — внутри хоста любой процесс может подключиться
2. `iblai-router` — нет публичного changelog, статус поддержки неизвестен. Используй как эксперимент, не как production backbone
3. `proactive-research` skill существует на ClawHub — не нужно писать с нуля, но кастомная версия даёт больше контроля
4. `self-improving-agent` skill (openclaw/skills) — уже готовый, не надо изобретать

---

## 1. GOOGLE WORKSPACE CLI (gws) — ГОРЯЧАЯ НОВОСТЬ

Google выпустил `gws` — единый CLI для Drive, Gmail, Calendar, Sheets, Docs и всех Workspace API. Написан на Rust, распространяется через npm. Работает для людей в терминале и для AI-агентов которым нужен структурированный вывод.

`gws` не имеет статического списка команд. Он читает Google Discovery Service в runtime и динамически строит всю командную поверхность. Когда Google добавляет новый API endpoint, `gws` подхватывает его автоматически.

### ⚠️ Важная оговорка
Проект живёт под организацией Google на GitHub, что даёт доверие — но README явно предупреждает: это не официально поддерживаемый Google продукт. Используй, но не строй критическую инфраструктуру без fallback.

### Установка
```bash
# npm (рекомендовано)
npm install -g @googleworkspace/cli

# Проверить
gws --version  # должно быть >= 0.6.3 (от 06.03.2026)

# Аутентификация
gws auth setup   # создаёт Google Cloud Project, включает API
gws auth login   # OAuth flow (нужен браузер один раз)
gws auth login -s drive,gmail,calendar  # только нужные scope
```

### Ключевые команды для агента
```bash
# Gmail
gws gmail messages list --params '{"maxResults":10,"q":"is:unread"}'
gws gmail messages get --id MESSAGE_ID
gws gmail messages send --params '{"to":"...","subject":"...","body":"..."}'

# Drive
gws drive files list --params '{"pageSize":5,"q":"modifiedTime > \"2026-03-01\""}'
gws drive files get --id FILE_ID
gws drive files --page-all  # авто-пагинация → NDJSON stream

# Calendar
gws calendar events list --params '{"calendarId":"primary","maxResults":10}'
gws calendar events insert --params '{"summary":"...","start":{"dateTime":"..."}}'

# Sheets
gws sheets spreadsheets values get --spreadsheet-id ID --range Sheet1!A1:Z100

# Dry-run (показывает HTTP запрос перед выполнением)
gws drive files list --dry-run
```

### MCP режим — интеграция с OpenClaw

Встроен `gws mcp` — MCP сервер, который превращает CLI в live endpoint для AI агентов. Compact mode expose всего ~26 инструментов вместо 200-400, экономя context window.

```bash
# Запустить MCP сервер (stdio mode для OpenClaw)
gws mcp --tool-mode compact  # 26 инструментов
gws mcp --tool-mode full     # 200+ инструментов (осторожно с токенами)
```

Добавить в `openclaw.json`:
```json
{
  "mcp": {
    "servers": [
      {
        "name": "google-workspace",
        "command": "gws",
        "args": ["mcp", "--tool-mode", "compact"],
        "env": {
          "GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE": "/home/user/.config/gws/credentials.json"
        }
      }
    ]
  }
}
```

### Защита от prompt injection

`--sanitize` флаг интегрируется с Google Cloud Model Armor для сканирования Workspace ответов на prompt injection до того как они попадут к агенту.

```bash
# Всегда использовать для email и документов
gws gmail messages get --id ID --sanitize | openclaw send
```

### Безопасность gws

Credentials хранятся как AES-256-GCM зашифрованные файлы в `~/.config/gws/`, ключ — в OS keyring. Мульти-аккаунт поддерживается из коробки.

```bash
# Минимальные scope (принцип наименьших привилегий)
gws auth login -s gmail.readonly,calendar.readonly  # только чтение
# НЕ давать: chat.admin.*, classroom.* (опасные scopes из blocklist)

# Переменная окружения для CI/server (без interactive login)
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/secrets/gws-service-account.json
```

### Service Account (для headless/Docker)
```bash
# В Docker контейнере — нет браузера, нужен Service Account
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/run/secrets/service-account.json
# Impersonation для Domain-Wide Delegation
export GOOGLE_WORKSPACE_CLI_IMPERSONATED_USER=user@yourdomain.com
gws drive files list  # работает без login
```

---

## 2. АВТО-РЕСЁРЧ МОДУЛЬ — ЕЖЕНЕДЕЛЬНОЕ ОБНОВЛЕНИЕ

### Архитектура
```
Каждое воскресенье 03:00
    │
    ▼
research-coordinator (Haiku)
    ├── spawn: agent:web-researcher-1  → "openclaw новые фичи этой недели"
    ├── spawn: agent:web-researcher-2  → "openclaw CVE баги март 2026"
    ├── spawn: agent:web-researcher-3  → "новые бесплатные LLM API март 2026"
    ├── spawn: agent:web-researcher-4  → "openclaw skills clawhub топ новые"
    └── spawn: agent:web-researcher-5  → "ai agent routing cost optimization 2026"
    │
    ▼ (все завершились)
synthesizer (DeepSeek R1:free)  →  WEEKLY_INTEL.md
    │
    ▼
diff-checker (Haiku)  →  сравнить с прошлой неделей
    │
    ▼
report → Telegram: только если есть изменения
```

### HEARTBEAT.md — добавить секцию
```markdown
## Weekly Research Update (воскресенье 03:00)
Модель: deepseek-r1:free для synthesis, haiku для координации

### Темы для исследования (менять по необходимости)
RESEARCH_TOPICS:
  - "openclaw новые фичи changelog"
  - "openclaw CVE security vulnerability"
  - "openrouter new free models"
  - "best cheap LLM API 2026 alternative"
  - "openclaw community forks improvements"
  - "google workspace cli gws updates"
  - "groq new models free tier"

### Алгоритм
1. Запустить 5 параллельных researcher субагентов по темам
2. Каждый пишет результат в ~/.openclaw/research/YYYY-MM-DD/[тема].md
3. Synthesizer читает все файлы и пишет WEEKLY_INTEL.md
4. Diff-checker сравнивает с прошлой неделей
5. Если diff > 20% → отправить сводку в Telegram
6. Если нашли CVE или critical bug → отправить НЕМЕДЛЕННО (не ждать воскресенья)

### Формат итогового отчёта
WEEKLY_INTEL.md:
  - Новые фичи openclaw (если есть)
  - Баги/CVE (если есть) — всегда первым
  - Новые бесплатные модели
  - Интересные skills появились
  - Рекомендация: что обновить в конфиге
```

### Skill для weekly research — SKILL.md
Создать `~/.openclaw/workspace/skills/weekly-intel/SKILL.md`:
```markdown
---
name: weekly-intel
description: "Запускай каждое воскресенье: исследует обновления openclaw, LLM API, CVE, новые skills. Пишет WEEKLY_INTEL.md и отправляет diff в Telegram. Триггерные слова: 'обнови знания', 'weekly research', 'что нового за неделю'."
version: 1.0.0
models:
  coordinator: anthropic/claude-haiku-4-5
  researcher: openrouter/deepseek/deepseek-r1:free
  synthesizer: openrouter/deepseek/deepseek-r1:free
permissions:
  fs.write: ["~/.openclaw/research/"]
  web: true
  sessions.spawn: true
---

# Weekly Intel Skill

## Шаг 1: Подготовка
Создать директорию: `~/.openclaw/research/$(date +%Y-%m-%d)/`
Прочитать прошлый отчёт: `~/.openclaw/research/LATEST/WEEKLY_INTEL.md`

## Шаг 2: Параллельные исследования
Spawni 5 субагентов (sessions_spawn), каждый исследует одну тему:
- Делает 3-5 web_search запросов
- Пишет результат в research/[дата]/[тема].md
- Формат: bullets, только факты, без воды

## Шаг 3: Синтез
Прочитать все файлы из research/[дата]/
Написать WEEKLY_INTEL.md структурированно:
```
# Weekly Intel [дата]

## 🚨 CVE / Баги (если есть)
...

## 🆕 Новые фичи OpenClaw
...

## 🆓 Новые бесплатные API / модели
...

## 🔧 Рекомендации по конфигу
...

## 📊 Score изменений
Масштаб изменений: [low/medium/high]
Рекомендация: [update_config / update_openclaw / nothing_critical]
```

## Шаг 4: Diff и уведомление
Сравнить с прошлым отчётом.
Если score = high → отправить полный отчёт в Telegram
Если score = medium → отправить краткую сводку (3 bullet)
Если score = low → только обновить файл, не беспокоить
Если CVE найден → уведомить немедленно с [URGENT] префиксом

## Стоимость на вызов
~$0.05-0.15 (5 агентов × deepseek-r1:free = бесплатно + haiku синтез ~$0.05)
```

### Cron регистрация
```bash
# Зарегистрировать в OpenClaw scheduler
openclaw cron add \
  --name "Weekly Intel" \
  --cron "0 3 * * 0" \
  --tz "Europe/Moscow" \
  --session isolated \
  --wake now \
  --message "Запусти weekly-intel skill. Исследуй обновления openclaw, LLM API, CVE за последнюю неделю. Напиши отчёт."

# Проверить что cron добавлен
openclaw cron list
```

---

## 3. SELF-IMPROVING AGENT SKILL — ГОТОВЫЙ

Официальный `self-improving-agent` skill от openclaw/skills. Захватывает ошибки и исправления в `.learnings/LEARNINGS.md`. Когда паттерн встречается >= 3 раз за 30 дней → автоматически промоутит правило в `SOUL.md` / `AGENTS.md`.

```bash
# Установка
npx playbooks add skill openclaw/skills --skill self-improving-agent

# Или вручную — скопировать из
# playbooks.com/skills/openclaw/skills/self-improving-agent
```

Добавить в `SOUL.md`:
```markdown
# Self-Improvement
При любой ошибке или исправлении пользователя:
→ записать в .learnings/LEARNINGS.md
→ если pattern повторился 3+ раз → промоутить в SOUL.md
```

---

## 4. ГОТОВЫЕ SKILLS ИЗ CLAWHUB (ПРОВЕРЕННЫЕ)

ClawHub содержит 13,729 community skills (февраль 2026). Есть VirusTotal partnership — каждый skill сканируется.

Установка:
```bash
# Через ClawHub CLI
clawhub install [skill-name]

# Или через chat (агент сам установит)
# Напиши: "Установи skill из https://github.com/openclaw/skills/tree/main/[name]"
```

### Топ skills для твоего сетапа

| Skill | Команда | Стоимость | Что делает |
|-------|---------|-----------|------------|
| `proactive-research` | `clawhub install proactive-research` | free | Мониторинг тем + алерты + weekly digest |
| `self-improving-agent` | `npx playbooks add skill openclaw/skills --skill self-improving-agent` | free | Авто-улучшение из ошибок |
| `auto-updater` | `clawhub install auto-updater` | free | Ежедневные updates openclaw + skills |
| `agent-team-orchestration` | `clawhub install agent-team-orchestration` | haiku | Task lifecycle + handoff protocols |
| `agent-commons` | `clawhub install agent-commons` | free | Консультация + reasoning chains |
| `manus-planning` | `clawhub install manus-planning` | free | task_plan.md + findings.md для сложных задач |
| `complexity-router` | `clawhub install complexity-router` | free | Авто-detect Haiku vs Sonnet |
| `cron-backup` | `clawhub install cron-backup` | free | Ежедневный backup конфига |

⚠️ Важно: инцидент февраля 2026 — агент Summer Yue удалил весь email из-за compaction. Для email skills ВСЕГДА настраивать `requireApproval: true` для delete/send/move.

### Безопасная установка skill (чеклист)
```bash
# 1. Проверить VirusTotal отчёт на clawhub.ai/skills/[name]
# 2. Прочитать SKILL.md вручную
grep -i "permissions" SKILL.md  # смотреть что запрашивает

# 3. Красные флаги — ОТКАЗАТЬ если skill просит:
#    shell.execute + нет safeBins
#    fs.read_root или fs.write_root
#    network.unrestricted
#    env.read (читает переменные окружения!)

# 4. Установить в sandbox-режиме первые 3 запуска
```

---

## 5. ПОЛНЫЙ СТЕК ПЕРЕМЕННЫХ ОКРУЖЕНИЯ

Создать `~/.openclaw/.env` (никогда не коммитить!):
```bash
# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# OpenRouter
OPENROUTER_API_KEY=sk-or-...

# Google AI Studio
GOOGLE_AI_STUDIO_KEY=AIza...

# Google Workspace CLI
GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/home/user/.config/gws/credentials.json
# Для Docker/headless:
# GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/run/secrets/gws-sa.json

# Groq (бесплатный)
GROQ_API_KEY=gsk_...

# Together AI ($100 trial)
TOGETHER_API_KEY=...

# Telegram Bot
TELEGRAM_BOT_TOKEN=...

# OpenClaw Gateway Secret (ГЕНЕРИРОВАТЬ: openssl rand -hex 32)
OPENCLAW_GATEWAY_SECRET=...

# 302.ai (если используешь)
AI302_API_KEY=...
```

Права доступа:
```bash
chmod 600 ~/.openclaw/.env
chmod 700 ~/.openclaw/
```

---

## 6. МОДУЛЬ ПРОТИВОРЕЧИЙ — ИСПРАВЛЕННАЯ ВЕРСИЯ

(В v1.0 был только как файл. Теперь — с конкретным триггером в HEARTBEAT.)

Добавить в `SOUL.md`:
```markdown
# Contradiction Check (обязательно при каждом ответе с утверждением)
Перед финальным ответом если он содержит рекомендацию или утверждение:
  → применить CONTRADICTION.md протокол
  → если найдено сильное противоречие → скорректировать ответ
  → всегда показывать пользователю: ⚖️ CONTRA: [найденные противоречия]
```

Добавить в `HEARTBEAT.md` секцию проверки:
```markdown
## Еженедельный противоречие-аудит (воскресенье 04:00, после weekly-intel)
Прочитать WEEKLY_INTEL.md
Для каждой рекомендации найти 2 contra-факта
Если рекомендация в текущем конфиге противоречит новым данным → уведомить
```

---

## 7. ИСПРАВЛЕННЫЙ openclaw.json — КРИТИЧЕСКИЕ ДОПОЛНЕНИЯ

Секции которые были упущены в v1.0:

```json
{
  "gateway": {
    "bind": "loopback",
    "port": 18789,
    "maxConcurrent": 4,
    "auth": {
      "secret": "${OPENCLAW_GATEWAY_SECRET}",
      "required": true
    },
    "hooks": {
      "tokenAuth": "header",
      "warnQueryParamTokens": true
    }
  },

  "env": {
    "file": "~/.openclaw/.env"
  },

  "mcp": {
    "servers": [
      {
        "name": "google-workspace",
        "command": "gws",
        "args": ["mcp", "--tool-mode", "compact"],
        "env": {
          "GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE": "${GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE}"
        }
      }
    ]
  },

  "tools": {
    "exec": {
      "enabled": true,
      "safeBins": ["git", "npm", "python3", "curl", "ls", "cat", "echo", "jq", "node", "gws"],
      "requireApproval": {
        "delete": true,
        "write_outside_workspace": true
      }
    },
    "email": {
      "requireApproval": ["send", "delete", "move"]
    }
  },

  "skills": {
    "autoLoad": true,
    "directory": "~/.openclaw/workspace/skills/",
    "sandboxFirstRun": true,
    "trustedSources": [
      "github.com/openclaw/skills",
      "clawhub.ai/verified"
    ]
  }
}
```

---

## 8. БЮДЖЕТ С gws (ОБНОВЛЁННЫЙ)

| Статья | Было | Стало |
|--------|------|-------|
| Хостинг Hetzner | $4 | $4 |
| Google Workspace CLI (gws) | нет | $0 (Apache-2.0, бесплатно) |
| Google AI Studio free tier | $0 | $0 (500 req/day) |
| Heartbeat + weekly research | $0.15 | $0.20 (5 доп агентов/нед) |
| DeepSeek (код) | $0.81 | $0.81 |
| Claude Haiku (координация) | $2.00 | $2.00 |
| Claude Sonnet (редко) | $3.00 | $3.00 |
| gws MCP токены (compact mode) | — | ~$0.50 (меньше чем полный) |
| **Итого** | **~$10** | **~$10.50** |

gws compact mode (~26 инструментов) экономит токены по сравнению с Gog плагином (~50+ tools).

---

## 9. ИСТОЧНИКИ ДОПОЛНЕНИЯ

- github.com/googleworkspace/cli — официальный репозиторий gws
- github.com/googleworkspace/cli/releases — v0.6.3 от 06.03.2026
- marktechpost.com/2026/03/05/google-ai-releases-a-cli-tool-gws — детальный разбор
- venturebeat.com/orchestration/google-workspace-cli — enterprise оценка
- winbuzzer.com/2026/03/06/google-workspace-cli-mcp-server — MCP + security детали
- windowsforum.com/threads/google-workspace-cli-gws — community обсуждение
- github.com/VoltAgent/awesome-openclaw-skills — 5494 curated skills
- playbooks.com/skills/openclaw/skills/self-improving-agent — self-improvement skill
- lobehub.com/skills/openclaw-skills-updater — auto-updater skill
- agentskillshub.dev/openclaw/top-100 — топ 100 skills март 2026
- digitalocean.com/resources/articles/what-are-openclaw-skills — что такое skills
- pcbuildadvisor.com/best-openclaw-skills-plugins-and-automations — топ skills гайд
