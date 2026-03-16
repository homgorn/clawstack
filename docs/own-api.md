# Building Your Own API

You do not need a hosted product on day one. A thin API wrapper is enough for many early use cases.

## When to add this layer

- you want API keys per user;
- you want free vs paid limits;
- you want billing and rate limiting outside the core agent runtime.

## Recommended scope

Keep the first version thin:

- auth;
- rate limits;
- usage counters;
- routing to the local OpenClaw gateway.

## Minimal shape

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}
```

Then add proxying and billing only after the config and routing patterns settle.
