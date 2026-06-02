# Atelier Telegram FAQ Bot

A lightweight Telegram FAQ bot for [Atelier](https://atelierai.xyz), the AI-agent marketplace on Solana. Built for the Atelier bounty: answer common questions about Atelier, registration, payments, services, orders, bounties, and API usage.

## What it does

- Answers common Atelier questions from a curated FAQ knowledge base with 20+ entries.
- Supports `/start`, `/help`, `/faq`, `/ask`, `/topics`, and `/about`.
- Uses deterministic keyword matching first, so it can run cheaply without an LLM.
- Includes source links back to Atelier website/docs/GitHub.
- Can be deployed on any VPS, Render, Railway, Fly.io, or Docker host.
- Avoids custody, private keys, wallet signing, or transaction handling.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set TELEGRAM_BOT_TOKEN
python -m atelier_faq_bot
```

## Telegram setup

1. Open Telegram and message `@BotFather`.
2. Run `/newbot`.
3. Choose a bot name and username.
4. Copy the bot token.
5. Put it in `.env` as:

```env
TELEGRAM_BOT_TOKEN=123456:example_token_from_botfather
LOG_LEVEL=INFO
```

## Commands

| Command | Description |
|---|---|
| `/start` | Welcome message and usage examples |
| `/help` | Command list |
| `/faq` | Top FAQs |
| `/topics` | Supported topics |
| `/ask <question>` | Ask a question |
| `/about` | Atelier summary + source links |

Users can also send normal messages without `/ask`.

## Example questions

- What is Atelier?
- How do I register an agent?
- How do payments work?
- How do I list a service?
- What are bounties?
- What is x402?
- What chains does Atelier support?
- How do I get an API key?

## Deployment options

### Docker

```bash
docker build -t atelier-faq-bot .
docker run --env-file .env atelier-faq-bot
```

### Render / Railway

- Build command: `pip install -r requirements.txt`
- Start command: `python -m atelier_faq_bot`
- Environment variable: `TELEGRAM_BOT_TOKEN`

### Systemd VPS

```ini
[Unit]
Description=Atelier Telegram FAQ Bot
After=network.target

[Service]
WorkingDirectory=/opt/atelier-telegram-faq-bot
EnvironmentFile=/opt/atelier-telegram-faq-bot/.env
ExecStart=/opt/atelier-telegram-faq-bot/.venv/bin/python -m atelier_faq_bot
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Project structure

```text
atelier_faq_bot/
  __init__.py
  __main__.py
  bot.py
  faq.py
  matcher.py
  settings.py
tests/
  test_matcher.py
.env.example
Dockerfile
README.md
requirements.txt
```

## Sources used

- Website: https://atelierai.xyz
- Docs/API reference: https://atelierai.xyz/docs
- GitHub: https://github.com/remp0x/atelier
- X: https://x.com/useAtelier
- Telegram: https://t.me/atelierai

## Bounty deliverable

GitHub repo link containing full source code and deployment instructions: https://github.com/dremonkey23/Atelier
