# 🦞 ClawStack — OpenClaw Cost Optimizer & Deployment Toolkit

> **Cut your OpenClaw costs by 80% in 15 minutes.**
> Production-ready configs, smart model routing, security hardening, and automated setup — for solo developers, teams, and businesses running AI agents on a budget.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw v2026.3.2](https://img.shields.io/badge/OpenClaw-v2026.3.2-green.svg)](https://github.com/openclaw/openclaw)
[![Stars](https://img.shields.io/github/stars/YOUR_USERNAME/clawstack?style=social)](https://github.com/YOUR_USERNAME/clawstack)
[![PinchBench Tested](https://img.shields.io/badge/PinchBench-Tested-blue)](https://pinchbench.com)
[![Security Hardened](https://img.shields.io/badge/Security-Hardened-red)](docs/security.md)

**→ [Quick Start](#-quick-start-15-minutes) · [Cost Calculator](#-cost-calculator) · [Docs](docs/) · [Setup Service](#-professional-setup-service)**

---

## 📊 Why ClawStack?

Most OpenClaw deployments use a single expensive model for everything — heartbeats, simple replies, complex analysis — the same way. That's like driving a Ferrari to buy groceries.

| Setup | Monthly Cost | Performance |
|-------|-------------|-------------|
| Default OpenClaw (Claude Sonnet) | $50–200 | 92.7% |
| **ClawStack (smart routing)** | **$13–34** | **91–93%** |
| Managed services (ClickClaw etc.) | $19–49 | 85–90% |
| Self-hosted, unoptimized | $6–50 | varies |

**ClawStack routes each task to the cheapest capable model automatically.**  
Based on [PinchBench](https://pinchbench.com) — the OpenClaw-specific LLM benchmark (23 real agent tasks, Claude Opus judge).

---

## 🗺️ Architecture

```mermaid
flowchart TD
    U[👤 You<br/>Telegram / WhatsApp / Discord] -->|message| GW

    subgraph CLAWSTACK["🦞 ClawStack"]
        GW[OpenClaw Gateway :18789<br/>loopback only • auth required]
        GW --> R[Smart Router<br/>iblai-router :8402<br/>14-dimension scorer]
        GW --> D[Task Decomposer<br/>DECOMPOSE.md]
        D --> R

        R -->|score < 0| LIGHT
        R -->|score 0–0.35| MID  
        R -->|score > 0.35| HEAVY

        subgraph TIERS["Model Tiers"]
            LIGHT[🟢 LIGHT<br/>:free models<br/>$0.00/run]
            MID[🟡 MEDIUM<br/>gpt-5-nano<br/>$0.03/run ★ 85.8%]
            HEAVY[🔴 HEAVY<br/>claude-haiku<br/>$0.64/run ★ 90.8%]
        end

        subgraph AGENTS["Specialized Agents"]
            A1[🔍 researcher<br/>kimi-k2.5 93.4%<br/>$0.20/run]
            A2[💻 coder<br/>gpt-5-nano 85.8%<br/>$0.03/run]
            A3[✍️ writer<br/>gemini-flash:free<br/>$0.00/run]
            A4[📊 monitor<br/>gpt-oss-120b:free<br/>$0.00/run]
        end

        subgraph SANDBOX["🔒 Docker Sandbox"]
            E[exec • browser<br/>file • shell<br/>non-root • no-net]
        end
    end

    MID --> AGENTS
    HEAVY --> AGENTS
    AGENTS --> SANDBOX
    LIGHT --> SANDBOX
```

---

## 🏗️ Repository Structure

```
clawstack/
├── README.md                    # this file
├── LICENSE                      # MIT
├── CHANGELOG.md                 # version history
│
├── configs/                     # ready-to-use openclaw.json configs
│   ├── openclaw-budget.json     # $13/month setup (recommended)
│   ├── openclaw-free.json       # $0/month (Oracle + :free models)
│   ├── openclaw-team.json       # $34/month multi-agent setup
│   └── openclaw-enterprise.json # $50/month maximum config
│
├── workspace/                   # drop-in workspace files
│   ├── SOUL.md                  # agent personality + cost rules
│   ├── AGENTS.md                # team delegation rules
│   ├── HEARTBEAT.md             # background tasks scheduler
│   ├── COST_RULES.md            # token economy rules
│   ├── DECOMPOSE.md             # task decomposition protocol
│   ├── CONTRADICTION.md         # contra-check module
│   ├── PROJECTS.md              # project tracking template
│   └── USER.md                  # user profile template
│
├── skills/                      # custom skills
│   ├── weekly-intel/            # automated weekly research
│   │   └── SKILL.md
│   ├── cost-monitor/            # spending alerts
│   │   └── SKILL.md
│   ├── self-improving/          # learn from corrections
│   │   └── SKILL.md
│   └── morning-brief/           # daily briefing
│       └── SKILL.md
│
├── docker/                      # sandbox configs
│   ├── docker-compose.yml       # production (Tailscale + gVisor)
│   ├── docker-compose.simple.yml # simple local setup
│   └── Dockerfile               # hardened image
│
├── scripts/                     # automation scripts
│   ├── install.sh               # one-line installer
│   ├── setup-vps.sh             # Hetzner/DigitalOcean setup
│   ├── setup-oracle-free.sh     # Oracle Cloud free tier setup
│   ├── check-costs.sh           # OpenRouter/Anthropic cost check
│   └── security-scan.sh         # audit script
│
├── router/                      # smart model router
│   ├── README.md                # how to use iblai-router
│   └── router-config.json       # routing rules + thresholds
│
├── api/                         # your own API layer
│   ├── main.py                  # FastAPI gateway
│   ├── models.py                # Pydantic models
│   ├── auth.py                  # API key auth
│   ├── billing.py               # Stripe integration
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                    # web dashboard
│   ├── README.md
│   └── (Next.js app — см. docs/frontend.md)
│
├── docs/                        # documentation
│   ├── quick-start.md
│   ├── security.md              # CVE list, hardening guide
│   ├── models.md                # model comparison + PinchBench data
│   ├── budget-calculator.md     # cost breakdown
│   ├── gws-setup.md             # Google Workspace CLI setup
│   ├── docker-sandbox.md        # sandbox hardening
│   ├── api-providers.md         # all free/cheap API providers
│   ├── business-model.md        # monetization guide
│   ├── frontend.md              # frontend setup
│   └── faq.md
│
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── workflows/
        ├── security-scan.yml    # weekly CVE check
        └── cost-report.yml      # monthly cost report
```

---

## ⚡ Quick Start (15 minutes)

### Option A — One-line installer
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/clawstack/main/scripts/install.sh | bash
```

### Option B — Manual
```bash
# 1. Prerequisites
node --version   # need >= 22.12.0
docker --version # need >= 29.0

# 2. Install OpenClaw (official only)
npm install -g openclaw@latest
openclaw --version  # check >= 2026.3.2

# 3. Clone ClawStack
git clone https://github.com/YOUR_USERNAME/clawstack
cd clawstack

# 4. Copy your preferred config
cp configs/openclaw-budget.json ~/.openclaw/openclaw.json

# 5. Set up environment
cp .env.example ~/.openclaw/.env
nano ~/.openclaw/.env  # fill in API keys
chmod 600 ~/.openclaw/.env

# 6. Copy workspace files
cp -r workspace/* ~/.openclaw/workspace/
cp -r skills/*    ~/.openclaw/workspace/skills/

# 7. (Optional) Start smart router
git clone https://github.com/iblai/iblai-openclaw-router
cd iblai-openclaw-router && node server.js &

# 8. Google Workspace CLI
npm install -g @googleworkspace/cli
gws auth setup && gws auth login

# 9. Validate & launch
openclaw config validate --json
openclaw doctor --fix
openclaw onboard --install-daemon
openclaw channels login   # Telegram: create bot via @BotFather

# 10. Test
# Message your bot: "Hello! What's your version?"
```

---

## 💰 Cost Calculator

### PinchBench-calibrated model selection

Based on [PinchBench](https://pinchbench.com) — 23 real OpenClaw tasks, scored by Claude Opus.

| Task Type | Recommended Model | Score | Cost/run | Notes |
|-----------|------------------|-------|----------|-------|
| Greeting, simple Q&A | `gpt-oss-120b:free` | ~75% | $0.00 | :free via OpenRouter |
| Research, web search | `kimi-k2.5` | 93.4% | $0.20 | Best value for research |
| Code generation | `gpt-5-nano` | 85.8% | $0.03 | 20× cheaper than Haiku |
| Tool-calling, agents | `claude-haiku-4-5` | 90.8% | $0.64 | Best for tool chains |
| Complex analysis | `claude-sonnet-4-5` | 92.7% | $3.07 | Use sparingly |
| Heartbeat checks | `gemini-2.5-flash-lite` | 76% | $0.05 | Reliable, cheap |

### ❌ Do NOT use for agents (poor value)
| Model | Score | Cost/run | Problem |
|-------|-------|----------|---------|
| `grok-4.1-fast` | 70.0% | $0.24 | Lowest score / highest ratio cost |
| `qwen3-max-thinking` | 40.9% | $0.00 | 40% success rate is unusable |
| `claude-opus-4.6` | 90.6% | $5.89 | Worse than Sonnet, 2× pricier |
| `deepseek-v3.2` | 82.1% | $0.73 | OK for batch code, bad as agent |

### Monthly budget scenarios

```mermaid
pie title Monthly Budget $34 (optimized)
    "Hetzner VPS" : 4
    "gpt-5-nano 500 tasks" : 15
    "kimi-k2.5 50 research" : 10
    "claude-haiku 30 tool-calls" : 3
    "Heartbeat 1440×" : 1
    "Reserve" : 1
```

| Scenario | Cost/month | Tasks/month | Stack |
|----------|-----------|-------------|-------|
| 🆓 Free tier | $0–3 | ~200/day | Oracle Free + Google AI Studio |
| 💚 Budget | $13–20 | ~300/day | Hetzner $4 + gpt-5-nano + :free |
| ⭐ Recommended | $28–35 | ~500/day | Budget + Kimi research + Haiku tools |
| 🚀 Power | $45–50 | ~1000/day | Recommended + Sonnet reserve |

---

## 🔐 Security

OpenClaw has documented CVEs. ClawStack ships with hardening by default.

```mermaid
flowchart LR
    subgraph THREATS["Known Threats"]
        T1[ClawJacked\nWebSocket hijack]
        T2[OC-13\nRCE via bind mount]
        T3[ClawHavoc\n341 malicious skills]
        T4[Fake installers\nVidar stealer]
        T5[Config leak\ncredentials in terminal]
    end

    subgraph FIXES["ClawStack Fixes"]
        F1[✅ bind: loopback\n+ auth.required: true]
        F2[✅ Docker: no socket\n+ read-only FS]
        F3[✅ sandboxFirstRun\n+ trustedSources only]
        F4[✅ Install only from\ngithub.com/openclaw/openclaw]
        F5[✅ OPENCLAW_SANDBOX=1\n+ secrets in .env]
    end

    T1 --> F1
    T2 --> F2
    T3 --> F3
    T4 --> F4
    T5 --> F5
```

**Minimum safe version: v2026.3.2**  
Full CVE list: [docs/security.md](docs/security.md)

### Security checklist (run after install)
```bash
openclaw doctor --fix
openclaw security audit --deep
openclaw config validate --json
chmod 600 ~/.openclaw/openclaw.json ~/.openclaw/.env
```

---

## 🧠 Multi-Agent Architecture

```mermaid
graph TD
    M[🦞 Main Agent<br/>gpt-5-nano<br/>Coordinator] -->|research task| R
    M -->|code task| C
    M -->|write task| W
    M -->|monitor| MO

    R[🔍 Researcher<br/>kimi-k2.5<br/>93.4% success]
    C[💻 Coder<br/>gpt-5-nano<br/>$0.03/run]
    W[✍️ Writer<br/>gemini-flash:free<br/>$0.00]
    MO[📊 Monitor<br/>gpt-oss-120b:free<br/>$0.00]
    SC[🏗️ Skill Creator<br/>gpt-5-nano<br/>auto-builds skills]

    M -->|new task type| SC
    SC -->|creates| SKILL[(SKILL.md<br/>library)]
    SKILL -->|auto-load| M

    H[⏰ Heartbeat<br/>every 30min<br/>gemini-flash-lite]
    H -->|weekly| WI[📋 Weekly Intel<br/>research 5 topics<br/>deepseek-r1:free]
    WI -->|diff alert| TG[📱 Telegram]

    subgraph MEMORY["Memory System"]
        MEM1[memory/YYYY-MM-DD.md<br/>daily log]
        MEM2[MEMORY.md<br/>long-term facts]
        MEM3[.learnings/<br/>self-improvement]
    end

    M <--> MEMORY
```

---

## 🔌 Integrations

### API Providers (free → paid)

```mermaid
flowchart LR
    subgraph FREE["🆓 Free Forever"]
        G[Google AI Studio<br/>500 req/day<br/>Gemini 2.5 Flash]
        OR[OpenRouter :free<br/>200 req/day<br/>Llama • DeepSeek R1<br/>GPT-OSS-120B]
        GR[Groq<br/>14400 req/day<br/>Llama 3.3 70B]
        CF[Cloudflare Workers AI<br/>10k Neurons/day<br/>Llama 3.1 8B]
    end

    subgraph TRIAL["🎁 Free Credits"]
        TO[Together AI<br/>$100 trial<br/>200+ models]
        XAI[xAI Grok<br/>$25 trial<br/>Dev program]
    end

    subgraph PAID["💳 Cheap Paid"]
        GPT5N[gpt-5-nano<br/>$0.03/run ★ 85.8%]
        KIMI[kimi-k2.5<br/>$0.20/run ★ 93.4%]
        HAIKU[claude-haiku-4-5<br/>$0.64/run ★ 90.8%]
    end

    FREE --> |fallback chain| PAID
    TRIAL --> |extends budget| PAID
```

### Google Workspace CLI (gws) — выпущен 06.03.2026

```bash
npm install -g @googleworkspace/cli
gws auth login -s gmail.readonly,calendar.readonly,drive.readonly
gws mcp --tool-mode compact  # 26 tools, MCP server for OpenClaw
```

Добавить в `openclaw.json`:
```json
"mcp": {
  "servers": [{
    "name": "google-workspace",
    "command": "gws",
    "args": ["mcp", "--tool-mode", "compact"]
  }]
}
```

⚠️ Не официальный продукт Google, но Apache-2.0, активно поддерживается.  
Полный гайд: [docs/gws-setup.md](docs/gws-setup.md)

---

## 🗂️ All Config Files

### configs/openclaw-budget.json (рекомендуемый)
→ [configs/openclaw-budget.json](configs/openclaw-budget.json)  
$13–20/мес · gpt-5-nano основной · kimi research · haiku tool-calling

### configs/openclaw-free.json
→ [configs/openclaw-free.json](configs/openclaw-free.json)  
$0–3/мес · Oracle Cloud Free · Google AI Studio · :free модели

### configs/openclaw-team.json
→ [configs/openclaw-team.json](configs/openclaw-team.json)  
$28–35/мес · 5 специализированных агентов · weekly intel · self-improvement

### configs/openclaw-enterprise.json
→ [configs/openclaw-enterprise.json](configs/openclaw-enterprise.json)  
$45–50/мес · максимальный функционал · secrets management · мониторинг

---

## 🐳 Docker Quick Deploy

```bash
# Simple (local)
docker compose -f docker/docker-compose.simple.yml up -d

# Production (Tailscale VPN, zero exposed ports)
TAILSCALE_AUTHKEY=your_key \
OPENCLAW_GATEWAY_SECRET=$(openssl rand -hex 32) \
docker compose -f docker/docker-compose.yml up -d
```

---

## 📅 Weekly Intel — Auto-Research Module

Каждое воскресенье в 03:00 агент сам исследует:
- Новые CVE и баги OpenClaw
- Новые бесплатные LLM API и модели
- Обновления конфига которые стоит применить
- Топ новых skills на ClawHub

Стоимость: ~$0.05–0.15/неделя (deepseek-r1:free)

```bash
openclaw cron add \
  --name "Weekly Intel" \
  --cron "0 3 * * 0" \
  --session isolated \
  --message "Run skill weekly-intel"
```

→ [skills/weekly-intel/SKILL.md](skills/weekly-intel/SKILL.md)

---

## 🛠️ Professional Setup Service

> **Don't want to configure it yourself? We'll do it for you.**

Managed OpenClaw setup eliminates 2–5 hours/month of maintenance — if your time is worth $50+/hour, even a $299 setup pays for itself in 2 months.

| Tier | Price | Includes | SLA |
|------|-------|----------|-----|
| **Starter** | $99 one-time | Config + workspace files + Telegram setup | 30-day email support |
| **Pro** | $299 one-time | Starter + Docker + VPS setup + 3 custom skills | 60-day support |
| **Business** | $799 one-time | Pro + API layer + dashboard + team setup | 90-day support + 1 call/month |
| **Managed** | $49/month | Everything + monitoring + updates + on-call | 99.9% uptime SLA |

**→ [Book setup](https://YOUR_DOMAIN/setup)** · Questions: setup@YOUR_DOMAIN

---

## 💼 Business Model & Revenue Paths

See full business plan: [docs/business-model.md](docs/business-model.md)

```mermaid
flowchart TD
    GH[GitHub Repo\nSEO Traffic\nDeveloper Trust] --> |organic| PATHS

    subgraph PATHS["Revenue Streams"]
        S1[⚡ Setup Service\n$99–799 one-time\nTarget: 20/month = $6k]
        S2[🔄 Managed Hosting\n$49/month/client\nTarget: 100 clients = $4.9k/mo]
        S3[📦 Premium Skills\n$9–49/skill pack\nTarget: 200 sales = $3k/mo]
        S4[📚 Course/Guide\n$49–99 one-time\nTarget: 100 sales = $5k]
        S5[🔗 Affiliates\nHetzner • OpenRouter\nTogether AI = ~$500/mo]
        S6[🏢 Enterprise\n$5k–75k projects\nTarget: 2/year = $15k]
    end

    PATHS --> TOTAL[💰 ~$100k/year\nat scale]
```

---

## 📡 Platform Distribution

ClawStack можно интегрировать в:

| Платформа | Метод | Монетизация |
|-----------|-------|-------------|
| **WordPress** | REST API plugin + WP block | Freemium plugin ($49/year) |
| **Ghost** | API integration + member tier | Subscriber-only content |
| **Webflow** | Embed + API calls | Lead gen → setup service |
| **Framer** | API component | Dashboard demo |
| **Telegram Mini App** | WebApp + Bot | Direct user acquisition |
| **ProductHunt** | Launch → traffic spike | One-time boost |
| **GitHub Marketplace** | Action для CI/CD | B2B leads |

WordPress plugin MVP:
```php
// Минимальный WP plugin — отправляет POST в ваш API
add_action('rest_api_init', function() {
    register_rest_route('clawstack/v1', '/chat', [
        'methods'  => 'POST',
        'callback' => 'clawstack_chat_handler',
        'permission_callback' => '__return_true'
    ]);
});
```

---

## 🗺️ Roadmap

```mermaid
gantt
    title ClawStack Roadmap 2026
    dateFormat  YYYY-MM
    section Open Source
    Core configs + docs     :done, 2026-03, 1M
    Skills library          :active, 2026-03, 2M
    install.sh script       :2026-04, 1M
    Security scanner CI     :2026-04, 1M
    section Product
    Setup service launch    :2026-04, 1M
    Web dashboard MVP       :2026-05, 2M
    API layer + billing     :2026-05, 2M
    WordPress plugin        :2026-06, 1M
    section Growth
    ProductHunt launch      :milestone, 2026-05, 0M
    1000 GitHub stars       :milestone, 2026-06, 0M
    100 paying clients      :milestone, 2026-08, 0M
```

---

## 📖 Documentation

| Doc | Description |
|-----|-------------|
| [Quick Start](docs/quick-start.md) | 15-minute setup guide |
| [Security Guide](docs/security.md) | CVE list, hardening, checklist |
| [Model Comparison](docs/models.md) | PinchBench data, cost/performance |
| [Budget Calculator](docs/budget-calculator.md) | Real cost scenarios |
| [Google Workspace Setup](docs/gws-setup.md) | gws CLI full guide |
| [Docker Sandbox](docs/docker-sandbox.md) | Isolation, gVisor, Tailscale |
| [API Providers](docs/api-providers.md) | All free/cheap providers |
| [Build Your API](docs/own-api.md) | FastAPI layer + Stripe billing |
| [Frontend](docs/frontend.md) | Next.js dashboard |
| [Business Model](docs/business-model.md) | Revenue paths to $100k/year |
| [FAQ](docs/faq.md) | Common questions |

---

## 🤝 Contributing

```bash
git clone https://github.com/YOUR_USERNAME/clawstack
cd clawstack
# Open an issue for bugs or features
# PRs welcome — especially new skills and provider configs
```

**Wanted contributions:**
- New skill SKILL.md files
- Provider configs (302.ai, Together AI, Groq)
- Security improvements
- Translations (RU, ZH, ES, DE)

---

## ⚖️ Comparison

| Feature | ClawStack | ClickClaw | Emergent | BetterClaw |
|---------|-----------|-----------|----------|------------|
| Open source | ✅ MIT | ❌ | ❌ | ❌ |
| Self-hosted | ✅ | ✅ | ❌ cloud | ✅ |
| Smart routing | ✅ 14-dim | ❌ | ❌ | ❌ |
| PinchBench optimized | ✅ | ❌ | ❌ | ❌ |
| Docker sandbox | ✅ | ✅ | ✅ | ✅ |
| Weekly auto-research | ✅ | ❌ | ❌ | ❌ |
| gws CLI integration | ✅ | ❌ | ❌ | ❌ |
| Cost/month (typical) | **$13–34** | $20+ | $19+ | $19+ |
| Setup time | 15 min | 2 min | 2 min | 5 min |

---

## 🔗 Useful Links

- [OpenClaw Official](https://github.com/openclaw/openclaw) — core project
- [OpenClaw Docs](https://docs.openclaw.ai) — official documentation
- [PinchBench](https://pinchbench.com) — model benchmark for OpenClaw
- [OpenRouter Free Models](https://openrouter.ai/collections/free-models) — free LLMs
- [Google AI Studio](https://aistudio.google.com) — 500 req/day free
- [Groq Console](https://console.groq.com) — 14400 req/day free
- [Together AI](https://api.together.ai) — $100 trial credits
- [gws CLI](https://github.com/googleworkspace/cli) — Google Workspace CLI
- [ClawHub](https://clawhub.ai) — community skills (verify before installing!)
- [iblai Router](https://github.com/iblai/iblai-openclaw-router) — smart router
- [Hetzner Cloud](https://hetzner.cloud/?ref=CLAWSTACK) — best budget VPS

---

## 📄 License

MIT © 2026 ClawStack Contributors

OpenClaw is MIT licensed by openclaw/openclaw.  
This project is not affiliated with OpenClaw, Anthropic, Google, or OpenAI.

---

<div align="center">

**⭐ Star this repo if it saved you money**  
**→ [Setup Service](https://YOUR_DOMAIN/setup) · [Discord](https://discord.gg/YOUR) · [Twitter](https://twitter.com/YOUR)**

</div>
