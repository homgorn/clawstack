# API Providers

Use a mix of free, trial, and low-cost providers instead of assuming a single premium stack.

## Free or mostly free paths

| Provider | Notes |
| --- | --- |
| Google AI Studio | Useful free quota for Gemini models |
| OpenRouter `:free` models | Good fallback path for low-cost setups |
| Groq | Strong free usage for some open models |
| Cloudflare Workers AI | Lightweight provider option for smaller workloads |

## Trial-credit paths

| Provider | Notes |
| --- | --- |
| Together AI | Often useful for early testing credits |
| xAI programs | Can extend experimentation budget |
| AI21 Labs | Limited but useful for testing |

## Paid but cost-aware paths

| Provider | Best use |
| --- | --- |
| OpenAI | Cheap main-agent role if using `gpt-5-nano` |
| Anthropic | Tool-heavy and premium fallback paths |
| Moonshot | Research-focused routing |

## Guidance

- Start with at least one free fallback.
- Add one cheap reliable paid default.
- Add one higher-quality reserve model only when needed.
