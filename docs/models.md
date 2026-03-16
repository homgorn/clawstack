# Models

These role recommendations are derived from the local `OPENCLAW_FINAL_SPEC.md` research notes.

## Recommended role mapping

| Role | Suggested model | Why |
| --- | --- | --- |
| Main agent | `openai/gpt-5-nano` | Best cost-to-utility baseline |
| Heartbeat / background checks | `google/gemini-2.5-flash-lite` | Cheap and reliable for routine checks |
| Research agent | `moonshotai/kimi-k2.5` | Stronger research value per run |
| Tool-heavy chains | `anthropic/claude-haiku-4-5` | Better fit for tool calling and agent chains |
| Rare heavy fallback | `anthropic/claude-sonnet-4-5` | Reserve for genuinely hard tasks |
| Free-first fallback | `openrouter/openai/gpt-oss-120b:free` | Good for low-cost or free usage paths |

## Routing rule of thumb

- Default to cheap models first.
- Escalate only when the task clearly requires it.
- Do not use premium models for routine heartbeat, greetings, or drafts.

## Models to avoid as defaults

From the current research notes, poor-value defaults include:

- `x-ai/grok-4.1-fast`
- `qwen/qwen3-max-thinking`
- `anthropic/claude-opus-4.6`

## Important note

These are repo recommendations, not official OpenClaw defaults. Re-check real provider pricing and model availability before production changes.
