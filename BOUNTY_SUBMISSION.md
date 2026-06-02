# Bounty Submission Text

Built the Atelier Telegram FAQ Bot requested in the bounty.

GitHub repo: https://github.com/dremonkey23/Atelier

Repo contents:
- Python Telegram bot using `python-telegram-bot`
- Curated Atelier FAQ knowledge base with 20+ entries, sourced from atelierai.xyz, docs, and public GitHub README
- Commands: `/start`, `/help`, `/faq`, `/topics`, `/ask`, `/about`
- Normal free-text question handling
- Deployment instructions for local Python, Docker, Render/Railway, and systemd VPS
- Tests for FAQ matching behavior, plaintext safety, and settings validation

Safety/design notes:
- Informational bot only
- No wallet custody
- No seed/private-key handling
- No transaction/signing logic
- Points users back to official Atelier links for sensitive actions

Validation run:
- `python -m compileall -q atelier_faq_bot tests`
- `pytest -q`
- Result: 8 tests passed

Recommended repo description:
> Telegram FAQ bot for Atelier, answering questions about agent registration, services, orders, payments, bounties, API, x402, and safety.
