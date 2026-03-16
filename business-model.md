# ClawStack Business Model — Path to $100k/year

> Март 2026. Рынок: <$200/мес тратят большинство OpenClaw пользователей без оптимизации.
> Managed сервисы берут $19–49/мес. Найм разработчика — $5k–75k за проект.
> ClawStack закрывает всё между "бесплатный DIY" и "дорогой managed".

---

## Validated Pain Points (из исследований)

1. **Setup friction**: 30-60 минут конфигурации для нетехнических пользователей
2. **Cost surprise**: пользователи тратят $47–200/мес без оптимизации
3. **Security**: CVE-2026-25253 + ClawHavoc атака — люди боятся настраивать сами
4. **Maintenance**: 2-5 часов/мес на обновления, OAuth токены, debugging

---

## Revenue Streams

### 1. Setup Service — главный продукт (быстрые деньги)
| Tier | Price | Time | Margin |
|------|-------|------|--------|
| Starter — базовый конфиг + TG | $99 | 1 час | 99% |
| Pro — VPS + Docker + 3 skills | $299 | 3 часа | 90% |
| Business — API + dashboard + team | $799 | 8 часов | 85% |
| Enterprise — полный проект | $5,000–15,000 | 40-80ч | 70% |

**Target**: 20 Starter/мес + 5 Pro/мес = $99×20 + $299×5 = $3,475/мес

### 2. Managed Hosting — рекуррентный доход
$49/мес за клиента: мониторинг + обновления + on-call
**Target**: 50 клиентов = $2,450/мес

### 3. Premium Skills Marketplace
$9–49 за skill pack (5–10 skills)
- Email automation pack: $19
- Business workflow pack: $29  
- Developer tools pack: $39
**Target**: 200 продаж/мес = ~$3,000/мес

### 4. Course / Setup Guide
PDF/Video: "Complete OpenClaw Setup from Zero to $13/month"
$49 — базовый · $99 — с видео · $199 — с коллом
**Target**: 50 продаж/мес = ~$3,500/мес

### 5. Affiliate Commissions
| Партнёр | Комиссия | Конверсия |
|---------|---------|-----------|
| Hetzner | €30/клиент | ~10% от ссылок |
| DigitalOcean | $25/клиент | ~8% |
| OpenRouter | 10% первый мес | ~15% |
| Together AI | % от spend | ~12% |
**Target**: 200 referrals/мес = ~$1,000/мес

### 6. Enterprise Consulting
$150–300/час · проекты $5k–75k
**Target**: 1 проект/квартал = ~$2,000/мес в среднем

---

## Итоговые цифры

| Stream | Year 1 Target | Year 2 Target |
|--------|--------------|--------------|
| Setup service | $30k | $60k |
| Managed hosting | $15k | $35k |
| Skills + Course | $20k | $40k |
| Affiliates | $5k | $10k |
| Enterprise | $10k | $25k |
| **TOTAL** | **$80k** | **$170k** |

Year 1 реалистичен при: активном SEO контенте (2-4 статьи/мес) + ProductHunt launch + Reddit/HN посевы.

---

## GTM (Go-to-Market)

### Фаза 1 — Traffic (мес 1-3)
- GitHub repo с README как SEO-лендинг
- 8-10 статей на dev.to / hashnode / medium (ключевые: "openclaw cost", "openclaw setup 2026")
- Reddit r/selfhosted, r/artificial — органические посты с ценностью, не реклама
- HackerNews Show HN

### Фаза 2 — Conversion (мес 2-4)
- Лендинг с калькулятором экономии (React, embedded на GitHub Pages)
- Setup service оплата через Stripe (Telegram бот или форма)
- Email рассылка через ConvertKit (бесплатно до 1000 подписчиков)

### Фаза 3 — Scale (мес 4-12)
- ProductHunt launch
- YouTube канал (2-3 видео/мес, SEO через тайтлы)
- Partnership с OpenClaw community Discord
- WordPress plugin (freemium, 10k+ сайтов)

---

## Tech Stack для Сервиса

### Минимальный (запустить за неделю)
- **Лендинг**: GitHub Pages + README как главная + Carrd.co ($19/год)
- **Оплата**: Stripe Payment Links (без кода)
- **Delivery**: email + Telegram с конфигами
- **Support**: Telegram group + email

### MVP продукта (1-2 месяца)
- **Backend**: FastAPI (Python) или Hono (TypeScript)
- **Frontend**: Next.js 15 + Tailwind
- **DB**: Supabase (бесплатный tier)
- **Payments**: Stripe Subscriptions
- **Hosting**: Vercel (frontend) + Hetzner VPS (API)
- **Analytics**: Plausible ($9/мес) или Umami (self-hosted)

### Dashboard функции
- Cost calculator (калькулятор по моделям)
- Config generator (выбираешь параметры → получаешь openclaw.json)
- Security checker (вставляешь конфиг → показывает уязвимости)
- Model selector (по задаче → рекомендует модель из PinchBench)
- Usage tracker (подключаешь OpenRouter API → видишь расходы)

---

## WordPress Plugin Concept

**Название**: "ClawConnect — OpenClaw for WordPress"
**Функция**: chat widget + OpenClaw API интеграция
**Монетизация**: $49/год или $9/мес (Freemium — базовый виджет бесплатно)

Сценарии использования:
- Поддержка/FAQ бот на сайте
- Лид-генерация чат
- Customer service автоответчик
- Документация по запросу

```php
// wp-content/plugins/clawconnect/clawconnect.php
/**
 * Plugin Name: ClawConnect
 * Description: OpenClaw AI Agent for WordPress
 * Version: 1.0.0
 * License: GPL v2
 */

class ClawConnect {
    public function __construct() {
        add_action('wp_footer', [$this, 'render_widget']);
        add_action('rest_api_init', [$this, 'register_routes']);
    }
    
    public function render_widget() {
        $api_url = get_option('clawconnect_api_url');
        // Render chat widget
    }
    
    public function register_routes() {
        register_rest_route('clawconnect/v1', '/chat', [
            'methods'  => 'POST',
            'callback' => [$this, 'handle_chat'],
            'permission_callback' => '__return_true'
        ]);
    }
}
new ClawConnect();
```

---

## Конкуренты и Позиционирование

| Конкурент | Цена | Проблема | Наше преимущество |
|-----------|------|---------|-------------------|
| ClickClaw | $20+/мес | Нет routing, bundled AI credits | Open source, 80% дешевле |
| Emergent (YC) | ~$19+/мес | Managed = меньше контроля | Self-hosted, приватность |
| BetterClaw | $19/мес | Proprietary | MIT license, полный контроль |
| vibeopenclaw.com | $$$ | Setup услуга без toolkit | Мы даём и toolkit И сервис |
| DIY | $5-200 | Часы настройки, CVE | Готово за 15 минут |

**Незанятая ниша**: "OpenClaw + cost optimization + open source toolkit + optional paid service"  
Это то, что ClawStack занимает.

---

## Ключевые метрики для отслеживания

- GitHub stars (цель: 1000 за 3 мес)
- Unique visitors/мес (цель: 5000 за 3 мес из поиска)
- Setup service conversions (цель: 5% от посетителей)
- MRR (monthly recurring revenue)
- CAC (cost to acquire customer) — должен быть < $10 при SEO стратегии
- LTV (lifetime value) — цель > $150 на клиента
