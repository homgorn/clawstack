FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE index.html styles.css app.js favicon.svg og-card.svg robots.txt sitemap.xml llms.txt site.webmanifest ./
COPY docs ./docs
COPY configs ./configs
COPY workspace ./workspace
COPY skills ./skills
COPY backend ./backend

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "clawstack_backend.app:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8000"]
